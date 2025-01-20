# Simple AQW Bot using Python Scripts

Arrange your commands, and the bot will execute them in sequence. See an example in `bot_tes.py`.

## Requirements

- Python version 3.9+

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/letsssgoo/aqw-python.git
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

Run commands using `bot_tes.py`:

```bash
python -m examples.bot_tes
```

### Scriptable Mode

Run the bot in scriptable mode using `single_acc_without_env.py`:

```bash
python single_acc_without_env.py
```

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
