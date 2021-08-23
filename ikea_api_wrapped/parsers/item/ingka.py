from __future__ import annotations

import re
from typing import Any, Callable, TypedDict

from box import Box

from ikea_api_wrapped.parsers import get_box
from ikea_api_wrapped.parsers.item import ChildItemDict


def parse_ingka_item(dictionary: dict[str, Any]):
    return IngkaItem(dictionary)()


class IngkaItemDict(TypedDict):
    is_combination: bool
    item_code: str
    name: str
    image_url: str | None
    weight: float
    child_items: list[ChildItemDict]


class IngkaItem:
    def __init__(self, dictionary: dict[str, Any]):
        self.d = get_box(dictionary)
        self._local_chunk = self.get_local_chunk()

    def __call__(self):
        return IngkaItemDict(
            is_combination=self.get_is_combination(),
            item_code=self.get_item_code(),
            name=self.get_name(),
            image_url=self.get_image_url(),
            weight=self.get_weight(),
            child_items=self.get_child_items(),
        )

    def get_local_chunk(self) -> Box:
        for communication in self.d.localisedCommunications:
            if communication.languageCode == "ru":
                return communication
        raise RuntimeError("Cannot find localized chunk")

    def get_weight(self) -> float:
        measurements: list[Box] = self._local_chunk.packageMeasurements
        if measurements:
            for package in measurements:
                if package.type == "WEIGHT":
                    return round(float(package.valueMetric), 2)
        return 0.0

    def get_child_items(self) -> list[ChildItemDict]:
        return [
            {
                "item_code": str(child.itemKey.itemNo),
                "item_name": None,
                "weight": 0.0,
                "qty": child.quantity,
            }
            for child in self.d.childItems or []
        ]

    def get_is_combination(self) -> bool:
        return self.d.itemKey.itemType == "SPR"

    def get_item_code(self) -> str:
        return self.d.itemKey.itemNo

    def get_name(self):
        item_name: str = self._local_chunk.productName
        type_of_item: str | None = self._local_chunk.productType.name
        design_text: str = self._local_chunk.validDesign.text
        measurements: list[Any] = self._local_chunk.measurements.referenceMeasurements

        match: Callable[[Any, str], int] = (
            lambda regex, text: len(re.findall(regex, text)) > 0
        )
        if match(r"[А-яЁё ]+", item_name):  # Russian text found
            name_changed = False
            if match(r"\d+", item_name):  # Numbers found
                if matches := re.findall(
                    r"^[^А-яЁё]+?([А-яЁё].*)", item_name
                ):  # Any text before Russian found
                    item_name = matches[0]
                    name_changed = True
            else:
                if match(r"[^А-яЁё /+]+", item_name):  # In some cases this regex works
                    item_name = re.sub(r"[^А-яЁё /+]+", "", item_name)
                    name_changed = True

            if name_changed:  # Substitute spaces where they shouldn't be
                item_name = re.sub(r"\s+", " ", item_name)
                item_name = re.sub(r"^ | $", "", item_name)

        measurement_text: str | None = measurements[0].metric if measurements else None
        type_of_item = type_of_item.capitalize() if type_of_item else None

        return ", ".join(
            part
            for part in (item_name, type_of_item, design_text, measurement_text)
            if part
        )

    def get_image_url(self) -> str | None:
        images: list[Any] = self._local_chunk.media
        image_url = None
        for image in images:
            if image.typeName == "MAIN_PRODUCT_IMAGE":
                for v in image.variants:
                    if v.quality == "S5":
                        image_url = v.href
                        break
                    image_url = image.variants[0].href
                break
            image_url = images[0].variants[0].href
        return image_url
