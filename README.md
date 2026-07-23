# F1 Telegram Bot

A Python bot that sends a daily Formula 1 briefing to a Telegram chat — the next race weekend's session schedule (in IST), current driver and constructor standings, and the latest headlines from Formula1.com. It's designed to run automatically via GitHub Actions, twice a day.

## Features:
1. Next race schedule — pulls the upcoming Grand Prix weekend from FastF1's official schedule data and converts every session time to IST.
2. Driver standings — current championship driver standings (top 11), via the Jolpica-F1 Ergast-compatible API.
3.Constructor standings — current constructors' championship table (top 11).
4. Latest news — top 5 headlines from Formula1.com's RSS feed, with links.
5. Telegram delivery — combines everything into one Markdown-formatted message and posts it via the Telegram Bot API.
6. Scheduled automation — a GitHub Actions workflow triggers the bot on a cron schedule, no server required.

## How it works:

main.py is the entry point. It pulls a piece of the briefing from each module and stitches them into a single message:

schedule.py       → next race weekend + session times (IST)
standings.py      → driver standings + constructor standings
news.py           → latest headlines (RSS)
telegram_bot.py   → sends the combined message to Telegram

Project structure
.
├── main.py                       # Entry point — assembles the daily brief and sends it
├── schedule.py                   # Next race weekend session times (FastF1), converted to IST
├── standings.py                  # Driver & constructor standings (Jolpica-F1 / Ergast-compatible API)
├── news.py                       # Latest F1 headlines from the official RSS feed
├── telegram_bot.py                # Sends the final message via the Telegram Bot API
├── config.py                      # Loads BOT_TOKEN / CHAT_ID from environment variables
├── formatter.py                   # Currently empty — reserved for future message-formatting helpers
├── requirements.txt                # Python dependencies
├── .github/workflows/daily.yml     # GitHub Actions workflow that runs the bot on a schedule
└── .gitignore

Setup
1. Clone the repo using the given command and paste it in your terminal


git clone https://github.com/madan-git-07/f1-telegram-bot.git
cd f1-telegram-bot


2. Install dependencies , you can do it manually or also by the given command and paste it in your terminal


pip install -r requirements.txt


3. Create a Telegram bot

Message @BotFather on Telegram and run /newbot, following the prompts.
Copy the bot token BotFather gives you.
Add the bot to the chat, group, or channel you want the briefing posted to, and get the corresponding chat ID (e.g. via @userinfobot or the Bot API's getUpdates endpoint).

4. Configure environment variables

Create a .env file in the project root:

BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_chat_id

5. Run it


python main.py

This fetches the schedule, standings, and news, then sends the combined brief to your configured Telegram chat.

Automating with GitHub Actions

The included workflow (.github/workflows/daily.yml) runs the bot automatically:

🕕 09:00 IST (03:30 UTC)
🕕 18:00 IST (12:30 UTC)
Can also be triggered manually from the Actions tab (workflow_dispatch)

To enable this on your own fork or copy of the repo, add BOT_TOKEN and CHAT_ID as repository secrets under Settings → Secrets and variables → Actions. The workflow installs requirements.txt on a fresh ubuntu-latest runner (Python 3.12) and runs python main.py.

Key dependencies

See requirements.txt for the full pinned list; the main ones are:

Package	Purpose
fastf1	Official/historical F1 session schedules & data
requests	HTTP calls to the Telegram API and standings API
feedparser	Parses the F1 news RSS feed
python-dotenv	Loads .env for local runs
pytz	UTC → IST timezone conversion
pandas, numpy, matplotlib	Pulled in as FastF1 dependencies


Notes:
1. Driver and constructor standings currently display only the top 11 entries. You can change it for any no. of standings upto 22 (as there are 22 drivers in the grid) by changing [:11] from standings.py. But for Constructor Champiaoship don't change it to more than 11 (as there 11 11 teams). 
2. Session times are hardcoded to convert to IST (Asia/Kolkata) in schedule.py — change the timezone there if you want a different local time.
3. FastF1 caches schedule data locally in a cache/ folder, which is git-ignored.
