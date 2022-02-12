import json
import os

import psutil
import psutil._common as psc
from maubot import MessageEvent, Plugin
from maubot.handlers import command
from mautrix.types import Format, MessageType, TextMessageEventContent


def to_human(data):
    output = {}
    for name in data._fields:
        value = getattr(data, name)
        if name != "percent":
            value = psc.bytes2human(value)
        output[name] = value
    return output


class LoadBot(Plugin):
    @command.new("load", help="Get load average.")
    @command.argument("message", pass_raw=True)
    async def load_handler(self, evt: MessageEvent, message: str) -> None:
        load = str(os.getloadavg())
        content = TextMessageEventContent(
            msgtype=MessageType.NOTICE,
            format=Format.HTML,
            body=f"{load}",
            formatted_body=f"{load}",
        )
        await evt.respond(content)

    @command.new("mem", help="Get system memory usage.")
    @command.argument("message", pass_raw=True)
    async def memory_handler(self, evt: MessageEvent, message: str) -> None:
        rawmem = psutil.virtual_memory()
        rawswap = psutil.swap_memory()
        mem = {}

        mem["virt"] = to_human(rawmem)
        mem["swap"] = to_human(rawswap)

        mem = json.dumps(mem, indent=2)
        content = TextMessageEventContent(
            msgtype=MessageType.NOTICE,
            format=Format.HTML,
            body=f"{mem}",
            formatted_body=f"{mem}",
        )
        await evt.respond(content)

    @command.new("disk", help="Get system disk usage.")
    @command.argument("message", pass_raw=True)
    async def disk_handler(self, evt: MessageEvent, message: str) -> None:
        result = {}
        parts = psutil.disk_partitions()

        for part in parts:
            usage = psutil.disk_usage(part.mountpoint)
            result[str(part.mountpoint)] = to_human(usage)

        result = json.dumps(result, indent=2)
        content = TextMessageEventContent(
            msgtype=MessageType.NOTICE,
            format=Format.HTML,
            body=f"{result}",
            formatted_body=f"{result}",
        )
        await evt.respond(content)
