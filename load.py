import os

from maubot import MessageEvent, Plugin
from maubot.handlers import command
from mautrix.types import Format, MessageType, TextMessageEventContent


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
