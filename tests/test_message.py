import asyncio
from collections.abc import Callable, Iterator
from contextlib import suppress
from typing import Any, AsyncIterable

import hypothesis.strategies as st
import pytest
from hypothesis import given

from lsp.lsp.client import ClientWorkspaceCapabilities
from lsp.protocol import JsonRpcRequest, JsonRpcResponse, LspProtocol, Message


@pytest.fixture(scope="module")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='module')
async def lsp_port(unused_tcp_port_factory: Callable[[], int]) -> int:
    return unused_tcp_port_factory()


@pytest.fixture(scope='module')
async def lsp_server(event_loop: asyncio.AbstractEventLoop, lsp_port: int) -> AsyncIterable[LspProtocol[Any]]:
    protocol: LspProtocol[Any] = LspProtocol()
    async with await event_loop.create_server(lambda: protocol, port=lsp_port) as server:
        serv = asyncio.create_task(server.serve_forever())

        async def echo() -> None:
            while not serv.done():
                with suppress(asyncio.TimeoutError):
                    msg = await asyncio.wait_for(protocol.read_message(), 0.1)
                    protocol.write_message(msg)

        t = asyncio.create_task(echo())

        yield protocol
        serv.cancel()
        with suppress(asyncio.CancelledError):
            await serv
        await t


@pytest.fixture(scope='module')
async def lsp_client(event_loop: asyncio.AbstractEventLoop, lsp_port: int,
                     lsp_server: LspProtocol[Any]) -> AsyncIterable[LspProtocol[Any]]:
    _ = lsp_server
    protocol: LspProtocol[Any] = LspProtocol()
    transport, _ = await event_loop.create_connection(lambda: protocol, port=lsp_port)
    yield protocol
    transport.close()


@st.composite
def jsonrpcrequest(draw: st.DrawFn) -> JsonRpcRequest[ClientWorkspaceCapabilities]:
    return JsonRpcRequest(id=draw(st.integers()),
                          jsonrpc="2.0",
                          method=draw(st.text()),
                          params=draw(st.from_type(ClientWorkspaceCapabilities)))


@given(request=jsonrpcrequest())
async def test_message_roundtrip(request: JsonRpcRequest[Any], lsp_client: LspProtocol[Any]) -> None:
    msg: Message[JsonRpcRequest[Any] | JsonRpcResponse[Any]] = Message(content=request)
    lsp_client.write_message(msg)
    response = await lsp_client.read_message()
    assert bytes(msg) == bytes(response)
    assert msg == response
