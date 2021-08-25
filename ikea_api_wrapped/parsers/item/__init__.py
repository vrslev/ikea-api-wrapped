from __future__ import annotations

from typing import TypedDict


class ChildItemDict(TypedDict):
    item_code: str
    item_name: str | None  # TODO: Rename to name
    weight: float
    qty: int


class ParsedItem(TypedDict):
    is_combination: bool
    item_code: str
    name: str
    image_url: str | None
    weight: float
    child_items: list[ChildItemDict]
    price: int
    url: str
    category_name: str | None
    category_url: str | None
