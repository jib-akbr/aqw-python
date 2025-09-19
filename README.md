# AQW Python Bot

This toolkit supports two bot workflows depending on how you like to automate:

- **Sequential Execution Mode** - queue commands and let the engine run them in order. Based on **Grimlite** botting commands. 
- **Scriptable Mode** - write Python script to run the commands as you want.

## Requirements

- Python version 3.9+

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/froztt13/aqw-python.git
   cd aqw-python
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Use the `.env.example` file as a template to create your `.env` file in the root directory.

   Update the `.env` file with your actual environment variable values.

## Usage

### Sequential Execution Mode

Scripts under `bot_cmds/` run commands one after another. Example: `bot_cmds/bot_tes.py`.

```bash
python -m bot_cmds.bot_tes
```

### Scriptable Mode

Use the `bot/` package to script complex behaviour. Example: `start.py`.

```bash
python start.py
```

You can also run the scriptable mode in Docker via `start_env.py`, which handles environment setup automatically.

### Docker Setup (Optional)

If you prefer to use Docker to run the bot, follow these steps.

1. Build the Docker image:

   If you haven't built the Docker image yet, run the following command:

   ```bash
   docker-compose up --build -d
   ```

2. Start the bot using Docker Compose:

   To start the bot using Docker, use the following command (this will run in detached mode):

   ```bash
   docker-compose up -d
   ```

3. Stop the bot:

   To stop the running containers:

   ```bash
   docker-compose down
   ```

4. View logs:

   To view the logs of the container:

   ```bash
   docker-compose logs
   ```
