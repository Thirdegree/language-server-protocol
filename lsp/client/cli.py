import asyncio
import logging

import click
import ujson as json

from lsp.client import Client
from lsp.lsp.common import MessageData

logging.basicConfig(level='INFO')


async def amain(lsp: list[str], method: str, params: MessageData) -> None:
    async with Client().run(lsp) as client:
        client.write_request(method, params)
        while msg := await client.protocol.read_message():
            print(msg)


@click.command
@click.argument('lsp', nargs=-1)
@click.option('--method', nargs=1)
@click.option('--params', nargs=1)
def main(lsp: list[str], method: str, params: str) -> None:
    """
    Note that lspclient is _very_ beta and has almost no functionality. The underlying Client() class technically is a
    full implementation of the protocol, but no batteries included
    """
    if not lsp:
        raise click.UsageError("Must supply language server command")
    asyncio.run(amain(lsp, method, json.loads(params)))
