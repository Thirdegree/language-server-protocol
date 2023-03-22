import asyncio
from asyncio import StreamReader, StreamWriter
from typing import AsyncIterable

import pytest

from lsp import LanguageServer
from lsp.lsp.messages import InitializeParams, InitializeResult
from lsp.lsp.server import (CodeAction, CodeActionParams, Command, SemanticTokens, SemanticTokensDeltaParams)


class TestLanguageServer(LanguageServer):

    async def initialize(self, params: InitializeParams) -> InitializeResult:
        return InitializeResult(capabilities={})

    async def add(self, params: dict[str, int] | None) -> int:
        assert params is not None
        return params['a'] + params['b']

    async def text_document__code_action(self, params: CodeActionParams) -> list[Command | CodeAction]:
        title = f"{params['range']['start']['line']}"
        title += f":{params['range']['start']['character']}"
        title += f"-{params['range']['end']['line']}"
        title += f":{params['range']['end']['character']}"
        return [CodeAction(title=title)]

    async def text_document__semantic_tokens__full__delta(self, params: SemanticTokensDeltaParams) -> SemanticTokens:
        return SemanticTokens(data=[12, 3])


@pytest.fixture
async def lsp_server() -> AsyncIterable[TestLanguageServer]:
    async with TestLanguageServer().serve(std=False) as server:
        yield server


@pytest.fixture
async def lsp_server_port(lsp_server: TestLanguageServer) -> int:
    assert lsp_server._listening_on is not None
    return lsp_server._listening_on


@pytest.fixture
async def lsp_client(lsp_server: TestLanguageServer,
                     lsp_server_port: int) -> AsyncIterable[tuple[StreamReader, StreamWriter]]:
    reader, writer = await asyncio.open_connection(port=lsp_server_port)
    yield reader, writer
    writer.close()
