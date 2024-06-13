# -*- coding: utf-8 -*-
import asyncio

import aiosqlite
from aiogram import Bot, Dispatcher, Router
from aiogram.types import BotCommand
from loguru import logger

from api_handlers import get_crypto_price
from handlers import router as handlers_router
from settings import Settings, get_settings

cfg: Settings = get_settings()

# bot instance
bot = Bot(token=cfg.bot_token)
dp = Dispatcher()

# routers
telegram_router = Router(name="telegram")
telegram_router.include_router(handlers_router)
dp.include_router(telegram_router)


async def init_db():
    async with aiosqlite.connect(cfg.database) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS thresholds (
                            user_id INTEGER,
                            symbol TEXT,
                            threshold_down REAL,
                            threshold_up REAL,
                            last_val REAL DEFAULT 0.0,
                            PRIMARY KEY (user_id, symbol)
                          )"""
        )
        await db.commit()


async def set_bot_commands_menu(my_bot: Bot) -> None:
    # register commands for Telegram bot (menu)
    commands = [
        BotCommand(command="/start", description="▶️ Start menu"),
        BotCommand(command="/id", description="👋 Get my ID"),
    ]
    try:
        await my_bot.set_my_commands(commands)
    except Exception as e:
        logger.error(f"Can't set commands - {e}")


async def check_prices(bot):
    while True:
        async with aiosqlite.connect(cfg.database) as db:
            async with db.execute(
                "SELECT user_id, symbol, threshold_down, threshold_up, last_val FROM thresholds"
            ) as cursor:
                async for row in cursor:
                    user_id, symbol, threshold_down, threshold_up, last_val = row
                    try:
                        price = await get_crypto_price(symbol)
                        if price < threshold_down and last_val > threshold_down:
                            await bot.send_message(
                                user_id,
                                f"Price {symbol} fallen below {threshold_down} USD. Current price: {price} USD.",
                            )
                        elif price > threshold_up > last_val > 0.0:
                            await bot.send_message(
                                user_id,
                                f"Price {symbol} exceeded {threshold_up} USD. Current price: {price} USD.",
                            )
                        await db.execute(
                            "UPDATE thresholds SET last_val = ? WHERE user_id = ? AND symbol = ?",
                            (price, user_id, symbol),
                        )
                        await db.commit()
                    except Exception as e:
                        print(f"Error checking price for {symbol}: {e}")
        await asyncio.sleep(cfg.check_interval)


async def on_startup(dp):
    await init_db()
    asyncio.create_task(check_prices(bot))


async def main():
    # start bot
    await bot.delete_webhook(drop_pending_updates=True)
    await set_bot_commands_menu(bot)
    await on_startup(bot)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
