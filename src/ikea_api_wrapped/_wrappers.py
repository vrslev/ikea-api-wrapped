from __future__ import annotations

from typing import Any

from ikea_api import IkeaApi
from ikea_api.endpoints import fetch_items_specs
from ikea_api.endpoints.item import parse_item_code
from ikea_api.endpoints.purchases import OrderInfoQuery
from ikea_api.errors import GraphqlError, ItemFetchError, OrderCaptureError

from ikea_api_wrapped._parsers.item.ingka import parse_ingka_item
from ikea_api_wrapped._parsers.item.iows import parse_iows_item
from ikea_api_wrapped._parsers.item.pip import parse_pip_item
from ikea_api_wrapped._parsers.order_capture import parse_delivery_options
from ikea_api_wrapped._parsers.purchases import (
    CostsOrder,
    StatusBannerOrder,
    parse_purchase_history,
)
from ikea_api_wrapped.types import (
    AddItemsToCartResponse,
    GetDeliveryServicesResponse,
    IngkaItemDict,
    NoDeliveryOptionsAvailableError,
    ParsedItem,
    PipItemDict,
    PurchaseHistoryItemDict,
    PurchaseInfoDict,
)


def get_purchase_history(api: IkeaApi) -> list[PurchaseHistoryItemDict]:
    response = api.Purchases.history()
    return parse_purchase_history(response)


def get_purchase_info(
    api: IkeaApi, purchase_id: str | int, email: str | None = None
) -> PurchaseInfoDict:
    status_banner, costs = api.Purchases.order_info(
        purchase_id,
        email=email,
        queries=[OrderInfoQuery.StatusBannerOrder, OrderInfoQuery.CostsOrder],
    )
    res: PurchaseInfoDict = StatusBannerOrder(status_banner)() | CostsOrder(costs)()  # type: ignore
    if not any(res.values()):
        return {}  # type: ignore
    return res


def get_delivery_services(
    api: IkeaApi, items: dict[str, int], zip_code: str
) -> GetDeliveryServicesResponse:
    cannot_add = add_items_to_cart(api, items)["cannot_add"]
    if not set(items.keys()) ^ set(cannot_add):  # if cannot add all items
        return GetDeliveryServicesResponse(delivery_options=[], cannot_add=cannot_add)

    try:
        response = api.OrderCapture(zip_code)
    except OrderCaptureError as e:
        if e.error_code in [60005, 60006]:
            raise NoDeliveryOptionsAvailableError
        else:
            raise

    options = parse_delivery_options(response)
    return GetDeliveryServicesResponse(delivery_options=options, cannot_add=cannot_add)


def add_items_to_cart(api: IkeaApi, items: dict[str, int]) -> AddItemsToCartResponse:
    api.Cart.clear()

    res = AddItemsToCartResponse(cannot_add=[], message=None)
    items_to_add = items.copy()

    while True:
        try:
            res["message"] = api.Cart.add_items(items_to_add)
            break
        except GraphqlError as exc:
            if not res["cannot_add"]:
                res["cannot_add"] = []

            if exc.errors is None:
                raise

            for error in exc.errors:
                if error["extensions"]["code"] == "INVALID_ITEM_NUMBER":
                    res["cannot_add"] += error["extensions"]["data"]["itemNos"]
                else:
                    raise

            for item in res["cannot_add"]:
                items_to_add.pop(item)

            if not items_to_add:
                break
    return res


def _get_iows_items(item_codes: list[str]):
    fetched: list[Any] = []
    try:
        fetched = fetch_items_specs.iows(item_codes)
    except ItemFetchError as e:
        if not "Wrong Item Code" in e.args[0]:
            raise
    return [parse_iows_item(item) for item in fetched]


def _bind_ingka_and_pip_objects(ingka: IngkaItemDict, pip: PipItemDict) -> ParsedItem:
    return ingka | pip  # type: ignore


def _get_ingka_pip_items(item_codes: list[str]):
    res: list[ParsedItem] = []
    items_ingka: list[IngkaItemDict] = []
    items_to_fetch_pip: dict[str, bool] = {}

    for chunk in fetch_items_specs.ingka(item_codes):
        for fetched_item in chunk["data"]:
            parsed_item = parse_ingka_item(fetched_item)
            items_ingka.append(parsed_item)
            items_to_fetch_pip[parsed_item["item_code"]] = parsed_item["is_combination"]

    fetched_items_map_pip: dict[str, PipItemDict] = {}
    for fetched_item in fetch_items_specs.pip(items_to_fetch_pip):
        parsed_item = parse_pip_item(fetched_item)
        fetched_items_map_pip[parsed_item["item_code"]] = parsed_item

    for item_ingka in items_ingka:
        item_pip: PipItemDict | None = fetched_items_map_pip.get(
            item_ingka["item_code"]
        )
        if item_pip is None:
            continue

        parsed_item = _bind_ingka_and_pip_objects(item_ingka, item_pip)
        res.append(parsed_item)

    return res


def get_items(item_codes: list[str]) -> list[ParsedItem]:
    items_to_fetch = parse_item_code(item_codes)
    fetched_items: list[ParsedItem] = []

    def update_items_to_fetch():
        nonlocal items_to_fetch
        items_to_fetch = [
            item
            for item in items_to_fetch
            if item not in (i["item_code"] for i in fetched_items)
        ]

    fetched_items += _get_iows_items(items_to_fetch)
    update_items_to_fetch()

    if not items_to_fetch:
        return fetched_items

    fetched_items += _get_ingka_pip_items(items_to_fetch)

    return fetched_items
