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
    category_name: str | None
    category_url: str | None


class PipItem:
    def __init__(self, dictionary: dict[str, Any]):
        self.d = get_box(dictionary)

    def _get_item_code(self) -> str:
        return re.sub("[^0-9]+", "", self.d.id)

    def _get_price(self) -> int:
        return self.d.priceNumeral

    def _get_url(self) -> str:
        return self.d.pipUrl

    def _get_category_name_and_url(self) -> tuple[str | None, str | None]:
        for _, ref in self.d.catalogRefs.items():
            if ref.elements[0].name and ref.elements[0].url:
                return ref.elements[0].name, ref.elements[0].url
        return None, None

    def __call__(self):
        category_name, category_url = self._get_category_name_and_url()
        return PipItemDict(
            item_code=self._get_item_code(),
            price=self._get_price(),
            url=self._get_url(),
            category_name=category_name,
            category_url=category_url,
        )
