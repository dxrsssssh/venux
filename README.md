# Your Awesome Discord Bot

A powerful and customizable Discord bot with moderation, fun, utility, and leveling features, designed for a professional and engaging user experience.

## Features

*   **Hybrid Commands:** All commands are available via both prefix (`!`) and Discord Slash Commands (`/`).
*   **Owner Commands:** Bot owner can use commands without a prefix.
*   **Embed-Only Replies:** Clean, professional, and consistent bot responses using Discord embeds.
*   **Custom Emojis:** Leverages server-specific custom emojis for enhanced visual flair.
*   **MongoDB Integration:** Uses MongoDB for robust and scalable data storage.
*   **Modular Design:** Easy to extend and maintain with cogs (extensions).

## Technologies Used

*   **Python 3.10+**
*   **Pycord:** Asynchronous Discord API wrapper.
*   **Beanie:** Asynchronous ODM for MongoDB.
*   **Motor:** Asynchronous MongoDB driver.
*   **MongoDB Atlas:** Cloud-hosted NoSQL database.
*   **Render:** Cloud platform for hosting.
*   **GitHub:** For version control and code management.

## Setup & Installation

### 1. Discord Bot Application

1.  Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2.  Click "New Application," give it a name, and create it.
3.  Go to the "Bot" tab and click "Add Bot." Confirm.
4.  **Important: Enable Privileged Gateway Intents.** Under the "Bot" tab, scroll down and enable:
    *   `Presence Intent`
    *   `Server Members Intent`
    *   `Message Content Intent`
5.  Copy your bot's token (keep this secure!).
6.  Go to "OAuth2" -> "URL Generator."
    *   Select `bot` and `applications.commands` scopes.
    *   Select the necessary permissions (e.g., `Administrator` for quick testing, or `Manage Roles`, `Kick Members`, `Send Messages`, `Read Message History`, `Use External Emojis`, etc., for production).
    *   Copy the generated URL and invite your bot to a test server.

### 2. MongoDB Atlas Database

1.  Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and create a free tier (M0) cluster.
2.  Create a new Database User (e.g., `botuser`) and remember its password.
3.  Configure Network Access: Add `0.0.0.0/0` to your IP Access List for "Allow Access from Anywhere" (for simplicity with Render, though more restrictive IPs are better for production).
4.  Connect your application: Get your "Connection String" (URI). It will look like `mongodb+srv://<username>:<password>@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority`. **Replace `<password>` with your actual database user's password.**

### 3. Local Development

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-discord-bot.git
    cd your-discord-bot
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment:**
    *   On Windows: `.\venv\Scripts\activate`
    *   On macOS/Linux: `source venv/bin/activate`
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Create a `.env` file** in the root directory (see `.env` section above) and fill in your bot token, owner ID, and MongoDB URI/DB name.
6.  **Run the bot:**
    ```bash
    python bot.py
    ```

### 4. Deployment on Render

1.  Sign up/Log in to [Render.com](https://render.com/).
2.  Create a new "Web Service."
3.  Connect your GitHub repository.
4.  **Build Command:** `pip install -r requirements.txt`
5.  **Start Command:** `python bot.py`
6.  **Environment Variables:** Add the following environment variables (using the values you used in your local `.env` file):
    *   `DISCORD_TOKEN`
    *   `BOT_PREFIX`
    *   `BOT_OWNER_ID`
    *   `MONGO_URI`
    *   `MONGO_DB_NAME`
    *   `PORT` (Render usually sets this automatically, but explicitly adding `PORT=8000` is harmless for the health check workaround)
7.  **Important for Free Tier:** If using Render's free Web Service tier, enable the health check by ensuring your `bot.py` creates a small web server on the provided `PORT` (as shown in the `on_ready` example in `bot.py`).

## Usage

*   **Prefix Commands:** Use `!command` (or your custom prefix) followed by arguments.
*   **Slash Commands:** Type `/` in Discord and select your bot to see available commands.
*   **Owner Commands:** If you are the bot owner, you can use commands without a prefix (e.g., `kick @user`).

## Contributing

Feel free to open issues or submit pull requests.

## License

[MIT License](LICENSE) (or choose your preferred license)
