import asyncio
import re

import aiohttp

from ikea_api_wrapped.wrappers import (
    add_items_to_cart,
    get_delivery_services,
    get_items,
    get_purchase_history,
    get_purchase_info,
)

__version__ = "0.2.2"
__all__ = [
    "unshorten_ingka_pagelinks",
    "get_item_codes_from_string",
    "format_item_code",
    "add_items_to_cart",
    "get_delivery_services",
    "get_items",
    "get_purchase_history",
    "get_purchase_info",
]


def _get_location(response: aiohttp.ClientResponse):
    return response.headers.get("Location")


def _fetch_location_headers(urls: list[str]):
    async def main():
        async def fetch(session: aiohttp.ClientSession, url: str):
            async with session.get(url, allow_redirects=False) as r:
                return _get_location(r)

        async def fetch_all(session: aiohttp.ClientSession):
            tasks = (asyncio.create_task(fetch(session, url)) for url in urls)
            return await asyncio.gather(*tasks)

        async with aiohttp.ClientSession() as session:
            return await fetch_all(session)

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(main())


def unshorten_ingka_pagelinks(message: str):
    postfixes = re.findall("ingka.page.link/([0-9A-z]+)", message)
    if not postfixes:
        return message

    base_url = "https://ingka.page.link/"
    shorten_urls = [base_url + p for p in postfixes]

    return _fetch_location_headers(shorten_urls)


def get_item_codes_from_string(message: str) -> list[str]:
    raw_item_codes = re.findall(r"\d{3}[, .-]{0,2}\d{3}[, .-]{0,2}\d{2}", message)
    regex = re.compile(r"[^0-9]")
    try:
        clean_item_codes = [regex.sub("", i) for i in raw_item_codes]
        return list(set(clean_item_codes))
    except TypeError:
        return []


def format_item_code(item_code: str):
    matches = get_item_codes_from_string(item_code)
    if matches:
        item_code = matches[0]
    return item_code[0:3] + "." + item_code[3:6] + "." + item_code[6:8]
