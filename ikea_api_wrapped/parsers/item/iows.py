from __future__ import annotations

import json
import re
from typing import Any, TypedDict

from box import Box
from ikea_api.constants import Constants

from ikea_api_wrapped.parsers import get_box


def parse_iows_item(dictionary: dict[str, Any]):
    return IowsItem(dictionary)()


class IowsItemDict(TypedDict):
    is_combination: bool
    item_code: str
    name: str
    image_url: str | None
    weight: float
    child_items: list[dict[str, str | float | int]]
    price: int
    url: str
    category_name: str | None
    category_url: str | None


class IowsItem:
    is_combination: bool
    item_code: str
    name: str
    image_url: str | None = None
    weight: float = 0.0
    child_items: list[dict[str, str | float | int]] = []
    price: int
    url: str
    category_name: str | None = None
    category_url: str | None = None

    def __init__(self, dictionary: dict[str, Any]):
        dictionary = get_rid_of_dollars(dictionary)
        self.d = get_box(dictionary)
        self.get_is_combination()
        self.get_item_code()
        self.name = self.get_name()
        self.get_image_url()
        self.get_weight_and_child_items()
        self.get_price()

        self.get_item_category_name_and_url()
        self.build_url()

        del self.d

    def __call__(self) -> IowsItemDict:
        return self.__dict__

    def get_is_combination(self):
        self.is_combination: bool = self.d.ItemType == "SPR"

    def get_item_code(self):
        self.item_code = str(self.d.ItemNo) if self.d.ItemNo else None

    def get_name(self, item: Any | None = None):
        if not item:
            item = self.d

        first_part: str | None = item.ProductName
        second_part: str | None = item.ProductTypeName

        if first_part and second_part:
            name = first_part + " " + second_part.capitalize()
        elif first_part:
            name = first_part
        elif second_part:
            name = second_part.capitalize()
        else:
            name = None

        measurement_text: str | None = self.d.ItemMeasureReferenceTextMetric
        design_text: str | None = self.d.ValidDesignText

        return ", ".join(attr for attr in (name, measurement_text, design_text) if attr)

    def get_image_url(self):
        images_raw: list[Any] = self.d.RetailItemImageList.RetailItemImage
        re_validate_image_url = re.compile(r"\.(png|jpg)$", re.IGNORECASE)
        all_images: dict[str, str] = {}

        for image in images_raw:
            image_url: Any = image.ImageUrl
            image_type: str = image.ImageType
            if isinstance(image_url, str):
                if re_validate_image_url.findall(image_url):
                    if image.ImageSize == "S5" and image_type != "LINE DRAWING":
                        self.image_url = Constants.BASE_URL + image_url
                        return
                    else:
                        all_images[image_url] = image.ImageSize

        for image, size in all_images.items():
            for acceptable_size in ("S4", "S3", "S2", "S1", "S0"):
                if size == acceptable_size:
                    self.image_url = Constants.BASE_URL + image
                    break

    def get_item_weight(self, item: dict[str, Any] | None = None) -> float:
        if not item:
            item = self.d

        measurement_list: list[
            Any
        ] = item.RetailItemCommPackageMeasureList.RetailItemCommPackageMeasure
        if not measurement_list:
            return 0.0

        weight = 0.0
        for measurement in measurement_list:
            if measurement.PackageMeasureType == "WEIGHT":
                if parsed_weight := parse_weight(measurement.PackageMeasureTextMetric):
                    weight += parsed_weight

        return weight

    def get_weight_and_child_items(self):
        if weight := self.get_item_weight():
            self.weight = round(weight, 2)

        raw_child_items: list[Box] = (
            self.d.RetailItemCommChildList.RetailItemCommChild or []
        )
        if not raw_child_items:
            return

        self.child_items = []
        for d in raw_child_items:
            item: dict[str, Any] = {
                "item_code": d.ItemNo,
                "item_name": self.get_name(d),
                "weight": self.get_item_weight(d),
                "qty": d.Quantity or 1,
            }
            self.weight: float = self.weight + item["weight"] * item["qty"]
            self.child_items.append(item)

        self.weight = round(self.weight, 2)

    def get_price(self):
        price_list: list[dict[Any, Any]] | dict[
            str, int
        ] | None = self.d.RetailItemCommPriceList.RetailItemCommPrice
        if not price_list:
            return

        self.price = (
            min(p.Price for p in price_list)
            if isinstance(price_list, list)
            else price_list.Price
        )

    def build_url(self):
        self.url = f"{Constants.BASE_URL}/ru/ru/p/-{'s' + self.item_code if self.is_combination else self.item_code}"

    def get_item_category_name_and_url(self):
        catalog_list: list[Any] | None = self.d.CatalogRefList.CatalogRef
        if not catalog_list:
            return

        idx = 0 if len(catalog_list) == 1 else 1
        category: list[dict[Any, Any]] | dict[Any, Any] = catalog_list[
            idx
        ].CatalogElementList.CatalogElement
        if isinstance(category, list):
            category = category[0]

        self.category_name = category.CatalogElementName
        self.category_url = (
            f"{Constants.BASE_URL}/ru/ru/cat/-{category.CatalogElementId}"
        )


def get_rid_of_dollars(d: dict[Any, Any]):
    d_json = json.dumps(d)
    d_json = re.sub(
        r'{"\$": ([^}]+)}', lambda x: x.group(1) if x.group(1) else "", d_json
    )
    return json.loads(d_json)


def parse_weight(weight: str):
    res = re.findall(r"[0-9.,]+", weight)
    if len(res) == 0:
        return
    return float(res[0].replace(",", "."))
