from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterable
from typing import Any

import pytest

from lsp import LanguageServer
from lsp.lsp.client import ClientCapabilities
from lsp.lsp.common import DocumentUri, Position, Range, T_Message
from lsp.lsp.messages import InitializeParams, InitializeResult
from lsp.lsp.server import (CodeAction, CodeActionContext, CodeActionParams, Command, SemanticTokens,
                            SemanticTokensDeltaParams, TextDocumentIdentifier)
from lsp.protocol import JsonRpcRequest, JsonRpcResponse, LspProtocol, Message


def request(method: str, params: T_Message) -> Message[JsonRpcRequest[T_Message] | JsonRpcResponse[T_Message]]:
    return Message(content=JsonRpcRequest(jsonrpc="2.0", id=1, method=method, params=params))


@pytest.fixture
async def lsp_client(event_loop: asyncio.AbstractEventLoop, lsp_server: ExampleLanguageServer,
                     lsp_server_port: int) -> AsyncIterable[LspProtocol[Any]]:
    protocol: LspProtocol[Any] = LspProtocol()
    transport, _ = await event_loop.create_connection(lambda: protocol, port=lsp_server_port)
    yield protocol
    transport.close()


class ExampleLanguageServer(LanguageServer):

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
async def lsp_server() -> AsyncIterable[ExampleLanguageServer]:
    async with ExampleLanguageServer().serve(std=False) as server:
        yield server


@pytest.fixture
async def lsp_server_port(lsp_server: ExampleLanguageServer) -> int:
    assert lsp_server._listening_on is not None
    return lsp_server._listening_on


@pytest.fixture
async def initialized_lsp_server(lsp_server: ExampleLanguageServer,
                                 lsp_client: LspProtocol[Any]) -> ExampleLanguageServer:
    lsp_client.write_message(
        Message(content=JsonRpcRequest(jsonrpc="2.0",
                                       id=1,
                                       method='initialize',
                                       params=InitializeParams(rootUri=None, processId=os.getpid(), capabilities={}))))
    message = await lsp_client.read_message()
    res = message.content.get('result')
    assert res is not None
    return lsp_server


@pytest.mark.usefixtures('initialized_lsp_server')
async def test_code_action_title(lsp_client: LspProtocol[Any]) -> None:
    lsp_client.write_message(
        request(
            'textDocument/codeAction',
            CodeActionParams(textDocument=TextDocumentIdentifier(uri=DocumentUri("")),
                             range=Range(start=Position(line=0, character=2), end=Position(line=3, character=4)),
                             context=CodeActionContext(diagnostics=[]))))

    message = await lsp_client.read_message()
    res = message.content.get('result')
    assert res is not None
    assert res[0]['title'] == '0:2-3:4'


@pytest.mark.usefixtures('initialized_lsp_server')
async def test_request_multiple_slashes(lsp_client: LspProtocol[Any]) -> None:
    lsp_client.write_message(request('textDocument/semanticTokens/full/delta',
                                     SemanticTokensDeltaParams()))  # type: ignore[typeddict-item]

    message = await lsp_client.read_message()
    res = message.content.get('result')
    assert res is not None
    assert res['data'] == [12, 3]


@pytest.mark.usefixtures('lsp_server')
async def test_language_server_init(lsp_client: LspProtocol[Any]) -> None:
    lsp_client.write_message(
        Message(content=JsonRpcRequest(id=1,
                                       jsonrpc="2.0",
                                       method='initialize',
                                       params=InitializeParams(
                                           processId=os.getpid(), rootUri=None, capabilities=ClientCapabilities()))))
    response = await lsp_client.read_message()
    init_res = response.content.get('result')
    assert init_res is not None
    assert init_res['capabilities'] == {}
