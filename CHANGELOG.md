# Changelog

<!--next-version-placeholder-->

## v0.3.5 (2021-08-26)
### Fix
* Return empty dict in `get_purchase_info` if couldn't get purchase info ([`5a8bfe1`](https://github.com/vrslev/ikea-api-wrapped/commit/5a8bfe14ba28d11764036b418b61a6f962c85d5a))

## v0.3.4 (2021-08-26)
### Fix
* Dump ikea-api version ([`4cf8e50`](https://github.com/vrslev/ikea-api-wrapped/commit/4cf8e50740e09b0604e17ac51f4ede7fbfd37772))

## v0.3.3 (2021-08-25)
### Fix
* **iows:** Return `None` instead of empty Box if no category specified ([`e4bbd4a`](https://github.com/vrslev/ikea-api-wrapped/commit/e4bbd4a5a8c83c2375658f29edef66ff7a2f986c))

## v0.3.2 (2021-08-23)
### Fix
* **get_items:** Don't fetch child items in ingka item, ([`6fdd1fa`](https://github.com/vrslev/ikea-api-wrapped/commit/6fdd1fa4769882449245e66e80fe41671ab66f84))

## v0.3.1 (2021-08-21)
### Fix
* Force str over int in item_code type ([`2b3d990`](https://github.com/vrslev/ikea-api-wrapped/commit/2b3d990d45c9c968a9c4913f397f7b23c0854830))

## v0.3.0 (2021-08-21)
### Feature
* Allow list and int types in `get_item_codes` ([`61cc94e`](https://github.com/vrslev/ikea-api-wrapped/commit/61cc94edc460ac77eaa3b46be2cc6aee44f8a45a))

## v0.2.2 (2021-08-21)
### Fix
* Include item parsers ([`6ff9ffe`](https://github.com/vrslev/ikea-api-wrapped/commit/6ff9ffe25c9e2775cc28078fa7bc12ff3ef2475b))

## v0.2.1 (2021-08-21)
### Fix
* **Item PIP:** Parse category name and url ([`90f9a52`](https://github.com/vrslev/ikea-api-wrapped/commit/90f9a5250a71d5169cd5e6cb8254e1e4b5758253))
* **Item IOWS:** Add comma between first and second name parts ([`01d2f1e`](https://github.com/vrslev/ikea-api-wrapped/commit/01d2f1ef0e90035bbfefc18f4dca1ffe316537b6))
* Add fields for `AnyParsedItem` for type completion ([`a4e94bf`](https://github.com/vrslev/ikea-api-wrapped/commit/a4e94bf99ea69e1d0dbceac338f6ee11e6f2c4a9))

## v0.2.0 (2021-08-21)
### Feature
* Add `AnyParsedItem` alias ([`a2d897a`](https://github.com/vrslev/ikea-api-wrapped/commit/a2d897a837c1f9f8e80109a78c6fee571d85641b))

## v0.1.0 (2021-08-21)
### Feature
* Release ([`2599364`](https://github.com/vrslev/ikea-api-wrapped/commit/259936474ad63e9a372f6c53b3a1d744ea17ff36))
