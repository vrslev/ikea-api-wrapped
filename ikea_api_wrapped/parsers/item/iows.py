from __future__ import annotations

import json
import re
from typing import Any

from box import Box
from ikea_api.constants import Constants

from ikea_api_wrapped.parsers import get_box
from ikea_api_wrapped.parsers.item import ChildItemDict, ParsedItem


def parse_iows_item(dictionary: dict[str, Any]):
    return IowsItem(dictionary)()


class IowsItem:
    def __init__(self, dictionary: dict[str, Any]):
        dictionary = get_rid_of_dollars(dictionary)
        self.d = get_box(dictionary)

    def __call__(self):
        self.is_combination = self.get_is_combination()
        self.item_code = self.get_item_code()
        self.category_name, self.category_url = self.get_category_name_and_url()
        return ParsedItem(
            is_combination=self.is_combination,
            item_code=self.item_code,
            name=self.get_name(),
            image_url=self.get_image_url(),
            weight=self.get_weight(),
            child_items=self.get_child_items(),
            price=self.get_price(),
            url=self.get_url(),
            category_name=self.category_name,
            category_url=self.category_url,
        )

    def get_is_combination(self) -> bool:
        return self.d.ItemType == "SPR"

    def get_item_code(self) -> str:
        return str(self.d.ItemNo)

    def get_name(self, item: Box | None = None):
        if not item:
            item = self.d

        first_part: str | None = item.ProductName
        second_part: str | None = item.ProductTypeName.capitalize()
        if second_part:
            second_part = second_part.capitalize()

        measurement_text: str | None = self.d.ItemMeasureReferenceTextMetric
        design_text: str | None = self.d.ValidDesignText

        attrs = (first_part, second_part, measurement_text, design_text)
        return ", ".join(attr for attr in attrs if attr)

    def get_image_url(self) -> str | None:
        images_raw: list[Any] = self.d.RetailItemImageList.RetailItemImage
        re_validate_image_url = re.compile(r"\.(png|jpg)$", re.IGNORECASE)
        all_images: dict[str, str] = {}

        for image in images_raw:
            image_url: Any = image.ImageUrl
            image_type: str = image.ImageType
            if isinstance(image_url, str):
                if re_validate_image_url.findall(image_url):
                    if image.ImageSize == "S5" and image_type != "LINE DRAWING":
                        return Constants.BASE_URL + image_url
                    else:
                        all_images[image_url] = image.ImageSize

        for image, size in all_images.items():
            for acceptable_size in ("S4", "S3", "S2", "S1", "S0"):
                if size == acceptable_size:
                    return Constants.BASE_URL + image

    def get_weight(self, item: Box | None = None) -> float:
        if not item:
            item = self.d

        measurement_list: list[
            Any
        ] = item.RetailItemCommPackageMeasureList.RetailItemCommPackageMeasure
        weight = 0.0

        if measurement_list:
            for measurement in measurement_list:
                if measurement.PackageMeasureType == "WEIGHT":
                    weight += parse_weight(measurement.PackageMeasureTextMetric)

        return round(weight, 2)

    def get_child_items(self) -> list[ChildItemDict]:
        return [
            {
                "item_code": str(child.ItemNo),
                "item_name": self.get_name(child),
                "weight": self.get_weight(child),
                "qty": child.Quantity,
            }
            for child in self.d.RetailItemCommChildList.RetailItemCommChild or []
        ]

    def get_price(self) -> int:
        price_list: list[
            object
        ] | object = self.d.RetailItemCommPriceList.RetailItemCommPrice
        if not price_list:
            return 0
        if isinstance(price_list, list):
            return min(p.Price for p in price_list)
        return price_list.Price

    def get_url(self):
        return f"{Constants.BASE_URL}/ru/ru/p/-{'s' + self.item_code if self.is_combination else self.item_code}"

    def get_category_name_and_url(self) -> tuple[str, str]:
        catalog_list: list[object | list[object]] = self.d.CatalogRefList.CatalogRef
        idx = 0 if len(catalog_list) == 1 else 1
        category: list[object] | object = catalog_list[
            idx
        ].CatalogElementList.CatalogElement
        if isinstance(category, list):
            category = category[0]
        return (
            category.CatalogElementName,
            f"{Constants.BASE_URL}/ru/ru/cat/-{category.CatalogElementId}",
        )


def get_rid_of_dollars(d: dict[Any, Any]):
    d_json = json.dumps(d)
    d_json = re.sub(
        r'{"\$": ([^}]+)}', lambda x: x.group(1) if x.group(1) else "", d_json
    )
    return json.loads(d_json)


def parse_weight(weight: str):
    if res := re.findall(r"[0-9.,]+", weight):
        return float(res[0].replace(",", "."))
    return 0.0
