#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["bring-api==1.1.2", "aiohttp"]
# ///
import argparse
import asyncio
import json
import os
import sys

import aiohttp
from bring_api import Bring, BringItemOperation

EMAIL = os.environ.get("BRING_EMAIL", "")
PASSWORD = os.environ.get("BRING_PASSWORD", "")


def parse_item(raw: str) -> tuple[str, str]:
    name, _, spec = raw.partition(":")
    return name.strip(), spec.strip()


def find_list(lists, name: str | None, default_uuid: str):
    if name is None:
        return next(entry for entry in lists if entry.listUuid == default_uuid)
    matches = [entry for entry in lists if entry.name.casefold() == name.casefold()]
    if not matches:
        names = ", ".join(entry.name for entry in lists)
        sys.exit(f"No list named '{name}'. Lists: {names}")
    return matches[0]


def find_purchase(items, name: str):
    matches = [item for item in items.purchase if item.itemId.casefold() == name.casefold()]
    if not matches:
        on_list = ", ".join(item.itemId for item in items.purchase) or "(empty)"
        sys.exit(f"'{name}' is not on the list. To buy: {on_list}")
    return matches[0]


def as_dict(item) -> dict:
    return {"name": item.itemId, "spec": item.specification}


async def run(args) -> dict:
    async with aiohttp.ClientSession() as session:
        bring = Bring(session, EMAIL, PASSWORD)
        auth = await bring.login()
        lists = (await bring.load_lists()).lists

        if args.command == "lists":
            return {"lists": [entry.name for entry in lists]}

        shopping_list = find_list(lists, args.list, auth.bringListUUID)
        list_uuid = shopping_list.listUuid
        items = (await bring.get_list(list_uuid)).items

        if args.command == "show":
            return {
                "list": shopping_list.name,
                "to_buy": [as_dict(item) for item in items.purchase],
                "recently": [as_dict(item) for item in items.recently],
            }

        if args.command == "add":
            changes = [
                {"itemId": name, "spec": spec, "uuid": None}
                for name, spec in map(parse_item, args.items)
            ]
            await bring.batch_update_list(list_uuid, changes, BringItemOperation.ADD)
        else:
            operation = {
                "complete": BringItemOperation.COMPLETE,
                "remove": BringItemOperation.REMOVE,
            }[args.command]
            targets = [find_purchase(items, parse_item(raw)[0]) for raw in args.items]
            changes = [
                {"itemId": item.itemId, "spec": item.specification, "uuid": item.uuid}
                for item in targets
            ]
            await bring.batch_update_list(list_uuid, changes, operation)

        items = (await bring.get_list(list_uuid)).items
        return {"list": shopping_list.name, "to_buy": [as_dict(item) for item in items.purchase]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Edit Bring! shopping lists.")
    parser.add_argument("--list", help="list name (default: the account's default list)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("lists", help="show all list names")
    commands.add_parser("show", help="show items to buy and recently bought")
    for command, help_text in [
        ("add", "add items, or update the spec of an item already on the list"),
        ("complete", "check off items (moves them to recently bought)"),
        ("remove", "delete items from the list"),
    ]:
        sub = commands.add_parser(command, help=help_text)
        sub.add_argument("items", nargs="+", metavar="ITEM", help='"Name" or "Name:spec"')
    args = parser.parse_args()

    if not (EMAIL and PASSWORD):
        sys.exit("Set EMAIL and PASSWORD in bring.py, or BRING_EMAIL and BRING_PASSWORD in the environment.")

    print(json.dumps(asyncio.run(run(args)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
