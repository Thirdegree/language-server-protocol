from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterable
from typing import Any

import pytest

from examples.spongebob_text_lsp import Spongebob
from lsp.lsp.common import DocumentUri, Position, Range, T_Message
from lsp.lsp.messages import InitializeParams
from lsp.lsp.server import (CodeAction, CodeActionContext, CodeActionParams, DidOpenTextDocumentParams,
                            TextDocumentIdentifier, TextDocumentItem)
from lsp.protocol import JsonRpcRequest, JsonRpcResponse, LspProtocol, Message


def request(method: str, params: T_Message) -> Message[JsonRpcRequest[T_Message] | JsonRpcResponse[T_Message]]:
    return Message(content=JsonRpcRequest(jsonrpc="2.0", id=1, method=method, params=params))


@pytest.fixture
async def lsp_client(event_loop: asyncio.AbstractEventLoop, lsp_server: Spongebob,
                     lsp_server_port: int) -> AsyncIterable[LspProtocol[Any]]:
    protocol: LspProtocol[Any] = LspProtocol()
    transport, _ = await event_loop.create_connection(lambda: protocol, port=lsp_server_port)
    yield protocol
    transport.close()
    protocol.write_message(request('shutdown', None))
    protocol.write_message(request('exit', None))


@pytest.fixture
async def lsp_server() -> AsyncIterable[Spongebob]:
    async with Spongebob().serve(std=False) as server:
        yield server


@pytest.fixture
async def lsp_server_port(lsp_server: Spongebob) -> int:
    assert lsp_server._listening_on is not None
    return lsp_server._listening_on


@pytest.fixture
async def spongebob(lsp_server: Spongebob, lsp_client: LspProtocol[Any]) -> Spongebob:
    lsp_client.write_message(
        request('initialize', InitializeParams(rootUri=None, processId=os.getpid(), capabilities={})))
    message = await lsp_client.read_message()
    res = message.content.get('result')
    assert res is not None
    return lsp_server


@pytest.mark.usefixtures('spongebob')
async def test_codeaction_range(lsp_client: LspProtocol[Any]) -> None:
    content = 'this is some text for the document'
    uri = DocumentUri('file:///foo')
    lsp_client.write_message(
        request(
            'textDocument/didOpen',
            DidOpenTextDocumentParams(
                textDocument=TextDocumentItem(uri=uri, languageId='python', version=1, text=content))))
    lsp_client.write_message(
        request(
            'textDocument/codeAction',
            CodeActionParams(textDocument=TextDocumentIdentifier(uri=uri),
                             range=Range(start=Position(line=0, character=5), end=Position(line=0, character=10)),
                             context=CodeActionContext(diagnostics=[]))))
    codeaction: JsonRpcResponse[list[CodeAction]] = (await lsp_client.read_message()).content
    assert 'result' in codeaction
    assert codeaction['result'][0]['title'] == 'Spongebob selection or word'
    assert 'edit' in codeaction['result'][0]
    assert 'changes' in codeaction['result'][0]['edit']
    assert codeaction['result'][0]['edit']['changes'][uri][0]['newText'] == 'Is sO'
