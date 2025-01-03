import asyncio

async def server_handler_task(bot: 'Bot'):
    print("Running server handler...")
    while bot.is_client_connected:
        messages = bot.read_batch(bot.client_socket)
        if messages:
            for msg in messages:
                await bot.handle_server_response(msg)
    print("Stopping server handler...")