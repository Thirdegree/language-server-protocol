import asyncio
from asyncio import StreamReader, StreamWriter
from typing import AsyncIterable, Callable

import pytest

from lspy import LanguageServer
from lspy.lsp.messages import InitializeParams, InitializeResult
from lspy.lsp.server import CodeAction, CodeActionParams, Command


class TestLanguageServer(LanguageServer):

    async def initialize(self, params: InitializeParams) -> InitializeResult:
        return InitializeResult(capabilities={})

    async def add(self, params: dict[str, int] | None) -> int:
        assert params is not None
        return params['a'] + params['b']

    async def text_document__code_action(
            self,
            params: CodeActionParams) -> list[Command | CodeAction] | None:
        title = f"{params['range']['start']['line']}"
        title += f":{params['range']['start']['charecter']}"
        title += f"-{params['range']['end']['line']}"
        title += f":{params['range']['end']['charecter']}"
        return [CodeAction(title=title)]


@pytest.fixture
async def lsp_server_port(unused_tcp_port_factory: Callable[[], int]) -> int:
    return unused_tcp_port_factory()


@pytest.fixture
async def lsp_server(
        lsp_server_port: int) -> AsyncIterable[TestLanguageServer]:
    async with TestLanguageServer().serve('localhost',
                                          lsp_server_port) as server:
        yield server


@pytest.fixture
async def lsp_client(
        lsp_server: TestLanguageServer, lsp_server_port: int
) -> AsyncIterable[tuple[StreamReader, StreamWriter]]:
    reader, writer = await asyncio.open_connection(port=lsp_server_port)
    yield reader, writer
    writer.close()
