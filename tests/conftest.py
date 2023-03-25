from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterable, Callable
from typing import Any, Type

import pytest

from lsp import LanguageServer
from lsp.lsp.common import T_Message
from lsp.lsp.messages import InitializeParams
from lsp.protocol import JsonRpcRequest, JsonRpcResponse, LspProtocol, Message

RequstFn = Callable[[str, T_Message], Message[JsonRpcRequest[T_Message] | JsonRpcResponse[T_Message]]]


@pytest.fixture
def make_request() -> RequstFn[T_Message]:
    id = 0

    def _request(method: str, params: T_Message) -> Message[JsonRpcRequest[T_Message] | JsonRpcResponse[T_Message]]:
        nonlocal id
        id += 1
        return Message(content=JsonRpcRequest(jsonrpc="2.0", id=id, method=method, params=params))

    return _request


@pytest.fixture
async def lsp_client(event_loop: asyncio.AbstractEventLoop, lsp_server_port: int,
                     make_request: RequstFn[Any]) -> AsyncIterable[LspProtocol[Any]]:
    protocol: LspProtocol[Any] = LspProtocol()
    transport, _ = await event_loop.create_connection(lambda: protocol, port=lsp_server_port)
    protocol.write_message(
        make_request('initialize', InitializeParams(rootUri=None, processId=os.getpid(), capabilities={})))
    message = await protocol.read_message()
    res = message.content.get('result')
    assert res is not None
    yield protocol
    transport.close()


@pytest.fixture
async def lsp_server_port(lsp_server: LanguageServer) -> int:
    assert lsp_server._listening_on is not None
    return lsp_server._listening_on


@pytest.fixture
async def lsp_server(lsp_class: Type[LanguageServer]) -> AsyncIterable[LanguageServer]:
    async with lsp_class().serve(std=False) as server:
        yield server
