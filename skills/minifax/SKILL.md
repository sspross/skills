---
name: minifax
description: Send something to a MiniFax, the thermal printer that prints messages on paper. Use when the user wants text, a todo list, or an image printed on their MiniFax or someone else's.
---

Every send goes through `scripts/minifax.py` in this skill's directory (Python 3 stdlib). It reads `MINIFAX_API_KEY` from the environment and talks to `https://server.minifax.app` (override with `MINIFAX_SERVER_URL`).

## Recipient

Send to `$MINIFAX_DEFAULT_FAX` by omitting `--to`. Pass `--to <id|name|location>` only when the user names a different MiniFax. When the name is ambiguous, run `--list` and pick the match, or ask.

## Sending

```sh
python3 scripts/minifax.py --text "Dinner at 7"
python3 scripts/minifax.py --todo $'Milk\nBread\nEggs' --to Office
python3 scripts/minifax.py --text "Look at this" --image ~/Desktop/cat.jpg
python3 scripts/minifax.py --list
```

Items print in the order given, up to 10 per message. `--todo` prints one checkbox per line.

## Writing for the printer

The paper is 576px wide, black and white, read standing next to the printer. Write short lines and short messages; paper is the medium. Images print dithered, so photos and simple graphics work, while fine text inside an image does not.

## Done

The script prints `Sent message <id> to <MiniFax>`. Relay that line to the user, including when the MiniFax is offline (it prints once it reconnects). On an error, relay the server's detail.
