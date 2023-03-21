import asyncio

import click

from lsp.client import Client


async def amain(lsp: list[str]) -> None:
    async with Client().run(lsp):
        await asyncio.sleep(0.1)


@click.command
@click.argument('lsp', nargs=-1)
def main(lsp: list[str]) -> None:
    """
    Note that lspclient is _very_ beta and has almost no functionality. The underlying Client() class technically is a
    full implementation of the protocol, but no batteries included
    """
    if not lsp:
        raise click.UsageError("Must supply language server command")
    asyncio.run(amain(lsp))
