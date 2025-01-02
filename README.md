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

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Use the `.env.example` file as a template to create your `.env` file in the root directory. Example:
   ```bash
   cp .env.example .env
   ```
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
