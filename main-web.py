import os
from dotenv import load_dotenv
import importlib
import builtins
from core.bot import Bot
import asyncio
import sys
import threading
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__, template_folder='ui-template')
socketio = SocketIO(app)

log_storage = {}

# Thread-safe logging
log_lock = threading.Lock()

def custom_print(*args, **kwargs):
    kwargs['flush'] = True
    log_message = " ".join(map(str, args))
    
    # Log to console
    sys.stdout.write(log_message + "\n")
    sys.stdout.flush()
    
    with log_lock:
        account = kwargs.get('account', 'combined')
        if account not in log_storage:
            log_storage[account] = []
        log_storage[account].append(log_message)

        socketio.emit('log_update', {'account': account, 'message': log_message}, room=account)

builtins.print = custom_print

@app.route('/')
def index():
    accounts = list(log_storage.keys())
    return render_template('index.html', accounts=accounts)

# WebSocket event to join a room (account-based)
@socketio.on('join')
def on_join(data):
    account = data['account']
    join_room(account)  # Correct usage of join_room

    with log_lock:
        past_logs = log_storage.get(account, [])
        emit('log_update', {'message': '<br>'.join(past_logs), 'clear': True}, room=request.sid)

    emit('log_update', {'message': f'Joined room for {account}'}, room=account)

load_dotenv()

def parse_env_variable(variable):
    return variable.strip("[]").split(",") if variable else []

usernames = parse_env_variable(os.getenv("USERNAME_AQW"))
passwords = parse_env_variable(os.getenv("PASSWORD_AQW"))
servers = parse_env_variable(os.getenv("SERVER"))
bot_paths = parse_env_variable(os.getenv("BOT_PATH"))
classes_name = parse_env_variable(os.getenv("CLASS_TO_USE"))

if len(usernames) != len(passwords) or len(usernames) != len(servers) or len(usernames) != len(bot_paths):
    print("Error: The number of usernames, passwords, servers, and bot paths must be equal!")
    exit(1)

items_white_list = [
    "Astral Ephemerite Essence",
    "Belrot the Fiend Essence",
    "Black Knight Essence",
    "Tiger Leech Essence",
    "Carnax Essence",
    "Chaos Vordred Essence",
    "Dai Tengu Essence",
    "Unending Avatar Essence",
    "Void Dragon Essence",
    "Creature Creation Essence",
    "Void Aura"
]

def create_bot(username, password, server, room_number, class_name):
    bot = Bot(
        roomNumber=room_number,
        itemsDropWhiteList=items_white_list,
        showLog=True,
        showDebug=False,
        showChat=True,
        isScriptable=True,
        farmClass=class_name
    )
    bot.set_login_info(username, password, server)
    return bot

async def run_bot(bot_class_path, bot_instance, account):
    try:
        bot_class = importlib.import_module(bot_class_path)
        print(f"Starting bot: {bot_class_path.split('.')[-1]}", account=account)
        await bot_instance.start_bot(bot_class.main)
    except ModuleNotFoundError as e:
        print(f"Error: {e}", account=account)


async def main():
    tasks = [
        run_bot(bot_paths[i], create_bot(usernames[i], passwords[i], servers[i], room_number=91923, class_name=classes_name[i]), usernames[i])
        for i in range(len(usernames))
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Start Flask-SocketIO app in a separate thread
    flask_thread = threading.Thread(target=lambda: socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False,allow_unsafe_werkzeug=True))
    flask_thread.start()

    print(f"Total bots: {len(usernames)}")
    asyncio.run(main())
