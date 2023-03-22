import asyncio
import os
from typing import Any

import pytest
import ujson as json

from lsp.lsp.client import ClientCapabilities
from lsp.lsp.messages import InitializeParams, InitializeResult
from lsp.protocol import JsonRpcRequest, JsonRpcResponse, Message


class TestMessage:

    def test_message_roundtrip(self) -> None:
        data = json.dumps(JsonRpcRequest(id=1, jsonrpc="2.0", method='whatever', params={'a':
                                                                                         'refactor.exact'})).encode()
        msg_bytes = (f'Content-Length: {len(data)}\r\n'
                     f'Content-Type: application/vscode-jsonrpc; charset=utf-8\r\n\r\n').encode() + data
        msg: Message[JsonRpcRequest[Any]]
        read, msg = Message.parse(msg_bytes)
        assert read == len(msg_bytes)
        assert msg.content_len == len(data)
        assert msg.content_bytes == data
        assert msg.content['method'] == 'whatever'
        assert bytes(msg) == msg_bytes


@pytest.mark.usefixtures('lsp_server')
async def test_language_server_init(lsp_server_port: int) -> None:
    reader, writer = await asyncio.open_connection(port=lsp_server_port)
    request = Message(content=JsonRpcRequest(
        id=1,
        jsonrpc="2.0",
        method='initialize',
        params=InitializeParams(processId=os.getpid(), rootUri=None, capabilities=ClientCapabilities())))
    writer.write(bytes(request))
    await writer.drain()
    response: Message[JsonRpcResponse[InitializeResult]]
    _, response = Message.parse(await asyncio.wait_for(reader.read(1024), 1))
    init_res = response.content.get('result')
    assert init_res is not None
    assert init_res['capabilities'] == {}
