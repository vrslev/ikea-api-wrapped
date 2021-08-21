from __future__ import annotations

import re
from typing import Any, TypedDict

from ikea_api_wrapped.parsers import get_box


def parse_pip_item(dictionary: dict[str, Any]):
    return PipItem(dictionary)()


class PipItemDict(TypedDict):
    item_code: str
    price: int
    url: str


class PipItem:
    def __init__(self, dictionary: dict[str, Any]):
        self.d = get_box(dictionary)

    def _get_item_code(self) -> str:
        return re.sub("[^0-9]+", "", self.d.id)

    def _get_price(self) -> int:
        return self.d.priceNumeral

    def _get_url(self) -> str:
        return self.d.pipUrl

    def __call__(self):
        return PipItemDict(
            item_code=self._get_item_code(),
            price=self._get_price(),
            url=self._get_url(),
        )
