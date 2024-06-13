# CMC notification bot (Aiogram)

This is a Telegram bot which is created using the [Aiogram](https://github.com/aiogram/aiogram) library in Python. Unlike the webhook approach in MoneyBot, polling method was used here.

## Prerequisites

- Python 3.10+
- Aiogram 3.1.1
- aiosqlite 0.20.0+

#### Description

For set the thresholds for your favorite token use the command below:
- /setthreshold <TOKEN> <LOW> <HIGH>

Example:
- /setthreshold BTC 65000 70000
