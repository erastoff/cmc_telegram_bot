# -*- coding: utf-8 -*-
import aiohttp

from settings import Settings, get_settings

cfg: Settings = get_settings()


async def get_crypto_price(crypto):
    parameters = {"symbol": crypto, "convert": "USD"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": cfg.cmc_api_key,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(cfg.cmc_url, headers=headers, params=parameters) as response:
            data = await response.json()
            return data["data"][crypto]["quote"]["USD"]["price"]
