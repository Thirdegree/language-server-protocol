#!/usr/bin/env python
import asyncio
from collections.abc import Iterator

from lsp import LanguageServer
from lsp.lsp.messages import InitializeParams, InitializeResult
from lsp.lsp.server import (CodeAction, CodeActionParams, Command, ServerCapabilities, TextEdit, WorkspaceEdit)


def fib() -> Iterator[int]:
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b


class Fib(LanguageServer):

    async def initialize(self, params: InitializeParams) -> InitializeResult:
        return InitializeResult(capabilities=ServerCapabilities(codeActionProvider=True))

    async def text_document__code_action(self, params: CodeActionParams) -> list[Command | CodeAction] | None:
        start, end = params['range']['start'], params['range']['end']
        if start['line'] != end['line']:
            return None
        f = fib()
        val = f'{next(f)}'
        while len(val) < abs(end['character'] - start['character']):
            val += f',{next(f)}'
        val = val[:abs(end['character'] - start['character'])]
        if val.endswith(','):
            val = val[:-1]
        return [
            CodeAction(title='Next fib',
                       edit=WorkspaceEdit(
                           changes={params['textDocument']['uri']: [TextEdit(range=params['range'], newText=val)]}))
        ]


async def amain() -> None:
    async with Fib().serve() as server:
        await server.wait()


if __name__ == "__main__":
    asyncio.run(amain())
