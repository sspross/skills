#!/usr/bin/env python3
import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

DEFAULT_SERVER_URL = "https://server.minifax.app"
# 2x the 576px printer width; larger photos only add upload bytes.
PHOTO_MAX_WIDTH = 1152


def server_url():
    return os.environ.get("MINIFAX_SERVER_URL", DEFAULT_SERVER_URL).rstrip("/")


def request(method, path, body=None):
    headers = {"Content-Type": "application/json"}
    api_key = os.environ.get("MINIFAX_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        server_url() + path, data=data, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        try:
            detail = json.load(error).get("detail", "")
        except ValueError:
            detail = ""
        sys.exit(f"MiniFax server answered {error.code}: {detail or error.reason}")


def list_devices():
    return request("GET", "/api/devices/")


def device_label(device):
    return device["location"] or device["name"]


def resolve_device(target):
    devices = list_devices()
    if target.isdigit():
        matches = [d for d in devices if d["id"] == int(target)]
    else:
        wanted = target.casefold()
        matches = [
            d
            for d in devices
            if wanted in (d["name"].casefold(), (d["location"] or "").casefold())
        ]
        if not matches:
            matches = [
                d
                for d in devices
                if wanted in d["name"].casefold()
                or wanted in (d["location"] or "").casefold()
            ]
    if len(matches) == 1:
        return matches[0]
    known = ", ".join(f"{d['id']}={device_label(d)}" for d in devices)
    problem = "matches several MiniFaxes" if matches else "matches no MiniFax"
    sys.exit(f"'{target}' {problem}. Known: {known}")


def image_width(path):
    out = subprocess.run(
        ["sips", "-g", "pixelWidth", path], check=True, capture_output=True, text=True
    ).stdout
    return int(out.split()[-1])


def encode_image(path):
    if shutil.which("sips") and image_width(path) > PHOTO_MAX_WIDTH:
        with tempfile.TemporaryDirectory() as tmp:
            scaled = os.path.join(tmp, "photo.jpg")
            subprocess.run(
                ["sips", "--resampleWidth", str(PHOTO_MAX_WIDTH),
                 "-s", "format", "jpeg", "-s", "formatOptions", "85",
                 path, "--out", scaled],
                check=True, capture_output=True,
            )
            with open(scaled, "rb") as f:
                return base64.b64encode(f.read()).decode("ascii")
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def todo_text(lines):
    return "\n".join(f"[] {line}" for line in lines if line.strip())


def build_items(args):
    items = []
    for kind, value in args.items:
        if kind == "text":
            items.append({"type": "text", "value": value})
        elif kind == "todo":
            items.append({"type": "text", "value": todo_text(value.split("\n"))})
        else:
            items.append({"type": "image", "value": encode_image(value)})
    return items


class AppendItem(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        namespace.items.append((self.dest, value))


def main():
    parser = argparse.ArgumentParser(
        description="Send text, todos and images to a MiniFax printer."
    )
    parser.add_argument("--list", action="store_true", help="list MiniFaxes")
    parser.add_argument(
        "--to", help="device id, name or location (default: $MINIFAX_DEFAULT_FAX)"
    )
    parser.set_defaults(items=[])
    parser.add_argument("--text", dest="text", action=AppendItem)
    parser.add_argument("--todo", dest="todo", action=AppendItem,
                        help="one todo per line")
    parser.add_argument("--image", dest="image", action=AppendItem,
                        help="path to an image file")
    args = parser.parse_args()

    if args.list:
        devices = list_devices()
        if not devices:
            print("No MiniFax visible. Is MINIFAX_API_KEY set?")
        for d in devices:
            state = "online" if d["is_online"] else "offline"
            print(f"{d['id']}\t{device_label(d)}\t{d['name']}\t{state}")
        return

    target = args.to or os.environ.get("MINIFAX_DEFAULT_FAX")
    if not target:
        sys.exit("No recipient: pass --to or set MINIFAX_DEFAULT_FAX.")
    if not args.items:
        sys.exit("Nothing to send: pass --text, --todo or --image.")

    device = resolve_device(target)
    message = request(
        "POST", f"/api/devices/{device['id']}/messages/", {"items": build_items(args)}
    )
    state = "online" if device["is_online"] else "offline, prints when it reconnects"
    print(f"Sent message {message['id']} to {device_label(device)} ({state}).")


if __name__ == "__main__":
    main()
