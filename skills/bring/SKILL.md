---
name: bring
description: Read and edit the user's Bring! shopping lists (getbring.com). Use when the user wants to see, add to, check off, or remove items from their shopping list ("Einkaufsliste").
---

# bring

`bring.py` (next to this file) talks to the Bring! API through [bring-api](https://github.com/miaucl/bring-api). Run it with `uv run <skill-dir>/bring.py`; uv installs the dependencies on first run.

It reads the login from `EMAIL` and `PASSWORD` at the top of `bring.py`, which default to the `BRING_EMAIL` and `BRING_PASSWORD` environment variables. If the script reports a missing login, tell the user and stop.

## Commands

```sh
bring.py lists                         # list names
bring.py show                          # items to buy + recently bought
bring.py add Milch "Eier:6 Stück"      # add; "Name:spec" sets the spec
bring.py complete Milch Eier           # check off (moves to recently bought)
bring.py remove Milch                  # delete without checking off
bring.py --list Ferienhaus show        # any command on another list
```

- Without `--list`, commands act on the account's default list.
- Every write prints the list's items to buy afterwards. Use that output to confirm the change to the user.
- `add` on an item already on the list updates its spec.
- `complete` and `remove` match names case-insensitively against the items to buy. On no match the script exits and prints what is on the list; pick the intended item from that and retry.

## Item names

Use the item names the Bring! app uses in the list's language (German lists: "Milch", "Brot", "Tomaten"). Catalog names get the app's icon and section; other names land in "Own articles". Put quantities and details in the spec, never in the name.
