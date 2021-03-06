<!-- prettier-ignore-start -->
# Changelog

<!--next-version-placeholder-->

## v0.4.5 (2021-11-25)
### Fix
* Updated description for PyPi ([`9c3f0fa`](https://github.com/vrslev/ikea-api-wrapped/commit/9c3f0fac267b948d0aa4f2a33c8cfa1478cc9ad8))

## v0.4.4 (2021-11-25)
### Fix
* Add note that it is not supported anymore ([`d199cb9`](https://github.com/vrslev/ikea-api-wrapped/commit/d199cb9d03901558916aa4b3a1f810e22c669efe))

## v0.4.3 (2021-11-01)
### Fix
* **Item iows:** Children parsing when only one item in combo ([`c6a118e`](https://github.com/vrslev/ikea-api-wrapped/commit/c6a118e83e1d099ef340634619c4c05c2b7ed3ed))

## v0.4.2 (2021-10-25)
### Fix
* No event loop in parse_item_codes ([`2c382c0`](https://github.com/vrslev/ikea-api-wrapped/commit/2c382c0c00cae7d8af8fd5ff753534eca4adca78))

## v0.4.1 (2021-10-17)
### Fix
* **Cart, OrderCapture:** Handle case when no items can be added ([`dec13b8`](https://github.com/vrslev/ikea-api-wrapped/commit/dec13b8e95e10f1fc10c812bbae4c0e6d9ce85cc))

## v0.4.0 (2021-10-07)
### Feature
* Typing improvements ([#9](https://github.com/vrslev/ikea-api-wrapped/issues/9)) ([`0906fb2`](https://github.com/vrslev/ikea-api-wrapped/commit/0906fb2fafe50b9c8ff90cfa2d6939698b350a83))

## v0.3.11 (2021-10-07)
### Fix
* **OrderCapture:** Add type to unavailable item ([`9fa61b0`](https://github.com/vrslev/ikea-api-wrapped/commit/9fa61b0bccbb951a8773038599c228c424380659))

## v0.3.10 (2021-10-01)
### Fix
* Add missing return type hints ([`a15efd6`](https://github.com/vrslev/ikea-api-wrapped/commit/a15efd651229e7c2294d82830e881f95bb38b909))

## v0.3.9 (2021-10-01)
### Fix
* Add missing return type hints ([`533c4d5`](https://github.com/vrslev/ikea-api-wrapped/commit/533c4d5c4330d5d47730512e8798e4c9faefbfdc))

## v0.3.8 (2021-09-29)
### Fix
* Dump versions ([`bfd64c0`](https://github.com/vrslev/ikea-api-wrapped/commit/bfd64c0391541aee5e96866546635a00dc25333a))

## v0.3.7 (2021-08-31)
### Fix
* Bump ikea-api version ([`b98ae57`](https://github.com/vrslev/ikea-api-wrapped/commit/b98ae578ebe6177c587a09caded49c1c7957166f))

## v0.3.6 (2021-08-31)
### Fix
* Bump ikea-api version ([`b1e03a2`](https://github.com/vrslev/ikea-api-wrapped/commit/b1e03a2b58d5569637d8cce7068e4c0458a129eb))

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

<!-- prettier-ignore-end -->
