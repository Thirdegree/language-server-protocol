import asyncio
import os
from asyncio import StreamReader, StreamWriter

import pytest

from lsp import LanguageServer
from lsp.lsp.common import DocumentUri, Position, Range, T_Message
from lsp.lsp.messages import InitializeParams, InitializeResult
from lsp.lsp.server import (CodeAction, CodeActionContext, CodeActionParams,
                            TextDocumentIdentifier)
from lsp.protocol import JsonRpcRequest, JsonRpcResponse, Message


def request(method: str,
            params: T_Message) -> Message[JsonRpcRequest[T_Message]]:
    return Message(content=JsonRpcRequest(
        jsonrpc="2.0", id=1, method=method, params=params))


@pytest.fixture
async def initialized_lsp_server(
        lsp_server: LanguageServer,
        lsp_client: tuple[StreamReader, StreamWriter]) -> LanguageServer:
    reader, writer = lsp_client
    writer.write(
        bytes(
            Message(content=JsonRpcRequest(
                jsonrpc="2.0",
                id=1,
                method='initialize',
                params=InitializeParams(
                    rootUri=None, processId=os.getpid(), capabilities={})))))
    message: Message[JsonRpcResponse[InitializeResult]]
    _, message = Message.parse(await asyncio.wait_for(reader.read(1024), 1))
    res = message.content.get('result')
    assert res is not None
    return lsp_server


@pytest.mark.usefixtures('initialized_lsp_server')
async def test_code_action_title(
        lsp_client: tuple[StreamReader, StreamWriter]) -> None:
    reader, writer = lsp_client
    writer.write(
        bytes(
            request(
                'textDocument/codeAction',
                CodeActionParams(
                    textDocument=TextDocumentIdentifier(uri=DocumentUri("")),
                    range=Range(start=Position(line=0, charecter=2),
                                end=Position(line=3, charecter=4)),
                    context=CodeActionContext(diagnostics=[])))))
    await writer.drain()

    message: Message[JsonRpcResponse[list[CodeAction]]]
    _, message = Message.parse(await asyncio.wait_for(reader.read(1024), 1))
    res = message.content.get('result')
    assert res is not None
    assert res[0]['title'] == '0:2-3:4'
