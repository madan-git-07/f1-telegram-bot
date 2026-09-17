# F1 Telegram Bot

A Python bot that sends a daily Formula 1 briefing to a Telegram chat. It collects the next race weekend schedule in IST, current driver and constructor standings, and the latest F1 headlines, then posts everything as a single Telegram message.

This project is designed to run locally or automatically via GitHub Actions with no dedicated server required.

## Features

- Next race weekend schedule
  - Pulls the upcoming Grand Prix weekend from FastF1
  - Converts all session times to IST (Asia/Kolkata)
- Driver standings
  - Displays the current championship table from a Jolpica-F1 / Ergast-compatible API
- Constructor standings
  - Shows the latest constructor rankings
- Latest F1 news
  - Fetches top headlines from the official Formula 1 RSS feed
- Telegram delivery
  - Combines all details into a Markdown-formatted message and sends it via Telegram Bot API
- Scheduled automation
  - Runs automatically via GitHub Actions on a cron schedule

## Project Structure

- `main.py` — entry point for the bot
- `schedule.py` — fetches and formats upcoming race session times
- `standings.py` — gets driver and constructor standings
- `news.py` — fetches latest F1 headlines
- `telegram_bot.py` — sends the final message to Telegram
- `config.py` — loads environment variables
- `requirements.txt` — Python dependencies
- `.github/workflows/daily.yml` — scheduled GitHub Action

## Download and Clone

Public download links:

- Download ZIP: https://github.com/madan-git-07/f1-telegram-bot/archive/refs/heads/main.zip
- Download TAR.GZ: https://github.com/madan-git-07/f1-telegram-bot/archive/refs/heads/main.tar.gz
- Clone repository: `git clone https://github.com/madan-git-07/f1-telegram-bot.git`

## Prerequisites

- Python 3.9+
- A Telegram bot token from @BotFather
- A Telegram chat ID where the message should be posted
- Internet access for fetching F1 data and news

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/madan-git-07/f1-telegram-bot.git
   cd f1-telegram-bot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a Telegram bot:

   - Open Telegram and message @BotFather
   - Run `/newbot`
   - Follow the instructions to create your bot
   - Save the bot token you receive
   - Add the bot to the target chat/group/channel
   - Get the chat ID for that chat

4. Configure environment variables:

   Create a `.env` file in the project root with:

   ```env
   BOT_TOKEN=your_telegram_bot_token
   CHAT_ID=your_chat_id
   ```

   Example:

   ```env
   BOT_TOKEN=123456:ABCDEF...
   CHAT_ID=-1001234567890
   ```

5. Run the bot locally:

   ```bash
   python main.py
   ```

   The script fetches race information, standings, and news, then sends the combined briefing to your Telegram chat.

## GitHub Actions Automation

The repository includes a workflow that runs automatically on a schedule and can also be triggered manually.

Workflow details:

- Runs at approximately 09:00 IST and 18:00 IST
- Uses repository secrets for `BOT_TOKEN` and `CHAT_ID`
- Can be started manually from the GitHub Actions tab

To enable it in your fork:

1. Go to your GitHub repository
2. Open Settings → Secrets and variables → Actions
3. Add:
   - `BOT_TOKEN`
   - `CHAT_ID`
4. Enable the workflow if needed

## Notes

- The standings currently display the top 11 entries by default.
- Session times are converted to IST by default in `schedule.py`.
- FastF1 caches data locally in a `cache/` directory, which is ignored by git.

## License

This project is provided as-is for educational and personal use.

## Contributing

Pull requests and suggestions are welcome. If you improve the formatting, add new features, or fix bugs, feel free to contribute.

## Support

If you are running this bot and need help with setup, Telegram chat IDs, or workflow configuration, open an issue in this repository.
