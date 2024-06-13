# -*- coding: utf-8 -*-
import aiosqlite
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from settings import Settings, get_settings

cfg: Settings = get_settings()

router = Router(name=__name__)


# just for test
@router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    await message.answer(f"🆔 Your ID: {message.from_user.id}")


@router.message(Command("setthreshold"))
async def set_thrshld(message: Message) -> None:
    try:
        symbol, threshold_down, threshold_up = message.text.split()[1:]
        threshold_down = float(threshold_down)
        threshold_up = float(threshold_up)

        user_id = message.from_user.id
        async with aiosqlite.connect(cfg.database) as db:
            await db.execute(
                "REPLACE INTO thresholds (user_id, symbol, threshold_down, threshold_up) VALUES (?, ?, ?, ?)",
                (user_id, symbol, threshold_down, threshold_up),
            )
            await db.commit()

        await message.reply(
            f"Looking after {symbol} set up. Min: {threshold_down} USD, Max: {threshold_up} USD."
        )
    except ValueError:
        await message.reply(
            "Incorrect request. Use: /setthreshold <token> <low> <high>"
        )
