from schedule import get_schedule
from standings import get_driver_standings, get_constructor_standings
from news import get_news
from telegram_bot import send_message

message = f"""
🏎 *F1 Daily Brief*

{get_schedule()}

{get_driver_standings()}

{get_constructor_standings()}

{get_news()}
"""

send_message(message)
print("Daily brief sent!")