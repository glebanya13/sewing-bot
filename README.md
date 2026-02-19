# 🧵 Sewing Bot
Sewing Bot is a Python-based project designed to monitor and process messages from specific Telegram chat channels. Its primary function is to identify and filter potential order requests based on predefined keywords and patterns, while ignoring irrelevant messages such as job postings or marketplace advertisements. This bot utilizes the Telegram API through the `telethon` library, allowing it to receive and send messages. The project's core features include message filtering, order request identification, and broadcasting messages to configured chat IDs.

## 🚀 Key Features
- **Message Filtering**: The bot filters messages based on predefined keywords and patterns to identify potential order requests.
- **Order Request Identification**: The bot uses specific logic to determine if a message is an order request, ensuring accurate identification while avoiding false positives.
- **Broadcasting Messages**: The bot can send messages to all configured chat IDs, useful for sending notifications or updates.
- **Customizable Configuration**: The project uses environment variables for configuration, making it flexible and easily deployable across different environments.

## 🛠️ Tech Stack
- **Python**: The primary programming language used for the project.
- **Telethon**: A Python library for interacting with the Telegram API.
- **Requests**: Used for making HTTP requests, specifically for sending messages via the Telegram Bot API.
- **Dotenv**: A library for loading environment variables from a `.env` file.
- **OS**: For interacting with the operating system, particularly for loading environment variables.
- **Threading**: Although not explicitly used in the provided snippet, it's imported, suggesting potential use in handling concurrent tasks or messages.

## 📦 Installation
### Prerequisites
- Python 3.8 or higher
- `telethon` library
- `requests` library
- `dotenv` library
- `os` library
- `threading` library

### Installation Steps
1. Clone the repository using `git clone`.
2. Install the required libraries using `pip install -r requirements.txt`.
3. Create a `.env` file and configure the environment variables (e.g., `API_ID`, `API_HASH`, `BOT_TOKEN`, `CHAT_IDS`, `CHANNEL_IDS`).

### Running Locally
1. Run the bot using `python main.py`.
2. The bot will connect to Telegram and start monitoring messages from the specified chat channels.

## 💻 Usage
- The bot will automatically filter messages based on predefined keywords and patterns.
- The bot will identify potential order requests and broadcast messages to configured chat IDs if necessary.

## 📂 Project Structure
```markdown
.
├── main.py
├── requirements.txt
├── .env
└── README.md
```

## 🤝 Contributing
Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request.

## 📝 License
The project is licensed under the MIT License.

## 📬 Contact
For any questions or concerns, please contact us at [glebanya.com@gmail.com](mailto:glebanya.com@gmail.com).
