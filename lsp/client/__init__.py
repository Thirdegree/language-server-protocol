"""
Interactive client, mainly for testing/debugging purposes
"""
import asyncio
import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any, Self

from lsp import JSONRPC_VERSION
from lsp.lsp.client import ClientCapabilities
from lsp.lsp.common import MessageData
from lsp.lsp.messages import InitializedParams, InitializeParams
from lsp.protocol import (JsonRpcRequest, JsonRpcResponse, LspProtocol, Message, T_Content)

log = logging.getLogger('client')
log_send = logging.getLogger('client.send')
log_recv = logging.getLogger('client.recv')


class ExitedError(Exception):
    pass


class LspProtocolSubprocess(asyncio.SubprocessProtocol, LspProtocol[T_Content]):

    def __init__(self) -> None:
        super().__init__()
        self.proctransport: asyncio.SubprocessTransport
        self.exited_event: asyncio.Event = asyncio.Event()

    def pipe_data_received(self, fd: int, data: bytes) -> None:

        remaining = len(data)
        while remaining:
            buf = self.get_buffer(remaining)
            buflen = len(buf)
            write = min(buflen, remaining)
            buf[:write] = data[:write]
            remaining -= write
            data = data[write:]
            self.buffer_updated(write)

    def pipe_connection_lost(self, fd: int, exc: Exception | None) -> None:
        self.proctransport.kill()

    def process_exited(self) -> None:
        logging.info("exited")
        self.eof_received()
        self.exited_event.set()

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        assert isinstance(transport, asyncio.SubprocessTransport)
        writeable = transport.get_pipe_transport(0)
        assert isinstance(writeable, asyncio.WriteTransport)
        self.transport = writeable
        self.proctransport = transport

    async def read_message(self) -> Message[T_Content]:
        done, _ = await asyncio.wait(
            [asyncio.create_task(super().read_message()),
             asyncio.create_task(self.exited_event.wait())],
            return_when=asyncio.FIRST_COMPLETED)
        if True in [d.result() for d in done]:
            # exited
            raise ExitedError
        msg = next(d.result() for d in done)
        assert isinstance(msg, Message)
        log_recv.info("Received: %s", msg.content)
        return msg


@dataclass
class Client:
    protocol: LspProtocolSubprocess[JsonRpcResponse[Any]] = field(default_factory=LspProtocolSubprocess)
    _server: asyncio.subprocess.Process | None = None
    cur_id: int = 1

    @asynccontextmanager
    async def run(self, cmd: list[str]) -> AsyncIterator[Self]:
        loop = asyncio.get_event_loop()
        transport, _ = await loop.subprocess_exec(lambda: self.protocol, *cmd, stderr=None)
        self.write_request('initialize',
                           InitializeParams(processId=os.getpid(), rootUri=None, capabilities=ClientCapabilities()))
        await self.protocol.read_message()
        self.write_request('initialized', InitializedParams(), notification=True)
        yield self
        transport.kill()

    def write_request(self, method: str, params: MessageData, notification: bool = False) -> None:
        request = JsonRpcRequest(jsonrpc=JSONRPC_VERSION, method=method, params=params)
        if not notification:
            request['id'] = self.cur_id
            self.cur_id += 1
        log_send.info("Sent: %s", request)
        self.protocol.write_message(Message(content=request))
