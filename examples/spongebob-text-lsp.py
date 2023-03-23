#!/usr/bin/env python
"""
For if and when arguments over snake_case, camelCase, PascalCase, etc. get a LiTtLe ToO TiRiNg.
"""
import asyncio
from contextlib import suppress
import logging
from contextlib import suppress
from dataclasses import dataclass

from more_itertools.more import split_at

from lsp import LanguageServer
from lsp.lsp.common import Position, Range
from lsp.lsp.messages import InitializeParams, InitializeResult
from lsp.lsp.server import (CodeAction, CodeActionParams, Command, DidChangeTextDocumentParams,
                            DidOpenTextDocumentParams, OptionalVersionedTextDocumentIdentifier, ServerCapabilities,
                            TextDocumentEdit, TextEdit, WorkspaceEdit)

logging.basicConfig(level='INFO')


def word_under_cursor(line: str, char_pos: int) -> tuple[int, int, str]:
    if char_pos >= len(line):
        return 0, 0, ""
    found = 0
    for _word in split_at(line, lambda c: not (c.isalnum() or c == '_')):
        word = ''.join(_word)
        new_found = found + len(word)
        if char_pos >= found and char_pos <= new_found:
            return found, new_found, ''.join(word)
        found = new_found + 1
    return 0, 0, ""


def spongebob(text: str) -> str:
    return ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))


@dataclass
class Spongebob(LanguageServer):
    content: str | None = None

    async def initialize(self, params: InitializeParams) -> InitializeResult:
        logging.info("initialize")
        logging.debug("client capabilities %s", params["capabilities"])
        return InitializeResult(capabilities=ServerCapabilities(
            codeActionProvider=True,
            textDocumentSync=1,
        ))

    async def text_document__code_action(self, params: CodeActionParams) -> list[Command | CodeAction] | None:
        assert self.content is not None
        logging.info("params: %s", params)
        if params['range']['start'] == params['range']['end']:
            # point selection, take the nearest word
            line = self.content.splitlines()[params['range']['start']['line']]
            line_no = params['range']['start']['line']
            start_char, end_char, word = word_under_cursor(line, params['range']['start']['character'])
            start = Position(line=line_no, character=start_char)
            end = Position(line=line_no, character=end_char)

        else:
            start, end = params['range']['start'], params['range']['end']
            lines = self.content.splitlines()[start['line']:end['line'] + 1]
            lines[0] = lines[0][start['character']:]
            lines[-1] = lines[-1][:end['character']]
            word = '\n'.join(lines)
        return [
            CodeAction(
                title='Spongebob selection or word',
                edit=WorkspaceEdit(documentChanges=[
                    TextDocumentEdit(textDocument=OptionalVersionedTextDocumentIdentifier(
                        uri=params['textDocument']['uri'], version=None),
                                     edits=[TextEdit(newText=spongebob(word), range=Range(start=start, end=end))])
                ]))
        ]

    async def text_document__did_open(self, params: DidOpenTextDocumentParams) -> None:
        logging.info("Didopen with new content")
        self.content = params['textDocument']['text']

    async def text_document__did_change(self, params: DidChangeTextDocumentParams) -> None:
        self.content = params['contentChanges'][0]['text']


async def amain() -> None:
    async with Spongebob().serve() as server:
        # 60 second timer on it because I'm too lazy to implement proper exit on parent exit logic here
        await asyncio.wait_for(server.wait(), 60)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(amain())
