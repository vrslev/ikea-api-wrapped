from __future__ import annotations

import asyncio
import re

import aiohttp


def _fetch_location_headers(urls: list[str]):
    async def main():
        async def fetch(session: aiohttp.ClientSession, url: str):
            async with session.get(url, allow_redirects=False) as r:
                return r.headers.get("Location")

        async def fetch_all(session: aiohttp.ClientSession):
            tasks = (asyncio.create_task(fetch(session, url)) for url in urls)
            return await asyncio.gather(*tasks)

        async with aiohttp.ClientSession() as session:
            return await fetch_all(session)

    return asyncio.run(main())


def _unshorten_ingka_pagelinks(message: str):
    postfixes = re.findall("ingka.page.link/([0-9A-z]+)", message)
    if not postfixes:
        return (message,)

    base_url = "https://ingka.page.link/"
    shorten_urls = [base_url + p for p in postfixes]

    return (url for url in _fetch_location_headers(shorten_urls) if url)


def _get_item_codes_from_string(message: str) -> list[str]:
    raw_item_codes = re.findall(r"\d{3}[, .-]{0,2}\d{3}[, .-]{0,2}\d{2}", message)
    regex = re.compile(r"[^0-9]")
    try:
        clean_item_codes = [regex.sub("", i) for i in raw_item_codes]
        return list(set(clean_item_codes))
    except TypeError:
        return []


def parse_item_codes(message: str | int | list[str | int]) -> list[str]:
    message = str(message)
    return _get_item_codes_from_string(
        " ".join(_unshorten_ingka_pagelinks(message)) + " " + message
    )


def format_item_code(item_code: str) -> str | None:
    if matches := _get_item_codes_from_string(item_code):
        item_code = matches[0]
        return item_code[0:3] + "." + item_code[3:6] + "." + item_code[6:8]
