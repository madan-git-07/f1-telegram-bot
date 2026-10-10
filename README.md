# F1 Telegram Bot

Sends a daily Formula 1 brief to Telegram: next race weekend in IST, driver and constructor standings, top 5 headlines.

Data: [Jolpica F1 API](https://github.com/jolpica/jolpica-f1) (schedule + standings) and the official F1 RSS feed.

## Run locally

```bash
pip install -r requirements.txt
echo "BOT_TOKEN=..." > .env
echo "CHAT_ID=..." >> .env
python main.py --dry   # print the message, send nothing
python main.py         # send it
```

## Run on GitHub Actions

Add `BOT_TOKEN` and `CHAT_ID` under Settings → Secrets and variables → Actions. The workflow runs daily at 09:00 IST and can be triggered manually.

Note: GitHub disables scheduled workflows on repos with no activity for 60 days. If the messages stop, re-enable it in the Actions tab.
