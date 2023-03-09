from __future__ import annotations

import asyncio
from dataclasses import dataclass
from email.message import Message as EmailMessage
from typing import (TYPE_CHECKING, Any, Generic, Literal, NotRequired, Self,
                    TypedDict, TypeVar)

import ujson as json

from lsp.lsp.common import T_Message

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer

JSONRPC_VERSION: Literal["2.0"] = "2.0"

T_Content = TypeVar('T_Content', bound='JsonRpcContent')
T = TypeVar('T')


class JsonRpcContent(TypedDict):
    jsonrpc: Literal["2.0"]
    id: NotRequired[int]


class JsonRpcRequest(JsonRpcContent, Generic[T_Message]):
    method: str
    params: NotRequired[T_Message]


class JsonRpcError(TypedDict):
    code: int
    message: str
    data: NotRequired[Any]


class JsonRpcResponse(JsonRpcContent, Generic[T]):
    # FIXME: way overbroad result time,
    #        can be limited to only messages and lists of message
    result: NotRequired[T]
    error: NotRequired[JsonRpcError]


@dataclass
class Message(Generic[T_Content]):
    content: T_Content
    _content_bytes: bytes | None = None
    _encoding: str | None = None
    _content_len: int | None = None
    _content_type: str | None = None

    def __bytes__(self) -> bytes:
        return (f'Content-Length: {self.content_len}\r\n'
                f'Content-Type: {self.content_type}\r\n\r\n'
                ).encode() + self.content_bytes

    @classmethod
    def parse(cls, data: bytes) -> tuple[int, Self]:
        headers, rest = data.split(b'\r\n\r\n', maxsplit=1)
        # trailing sep for the headers is consumed above, so it's ok to just split
        content_len: int | None = None
        content_type: bytes | None = None
        for header in sorted(headers.split(b'\r\n')):
            if header.startswith(b'Content-Type: '):
                content_type = header[14:]
            elif header.startswith(b'Content-Length: '):
                content_len = int(header[16:])
        if content_len is None:
            raise ValueError("Invalid content")
        header_len = len(headers)
        content = json.loads(rest[:content_len] or b'{}')
        return header_len + content_len + 4, cls(
            content=content,
            _content_len=content_len,
            _content_type=content_type.decode() if content_type else None,
            _content_bytes=rest[:content_len])

    @property
    def content_type(self) -> str:
        if self._content_type is None:
            self._content_type = 'application/vscode-jsonrpc; charset=utf-8'
        return self._content_type

    @property
    def content_len(self) -> int:
        if self._content_len is None:
            self._content_len = len(self.content_bytes)
        return self._content_len

    @property
    def content_bytes(self) -> bytes:
        if self._content_bytes is None:
            self._content_bytes = json.dumps(self.content).encode(
                self.encoding)
        return self._content_bytes

    @property
    def encoding(self) -> str:
        if self._encoding is None:
            msg = EmailMessage()
            msg['Content-Type'] = self.content_type
            self._encoding = msg.get_param('charset', 'utf-8')  # type: ignore
        return self._encoding  # type: ignore


class LspProtocol(asyncio.BufferedProtocol):

    def __init__(self) -> None:
        self.buffer = memoryview(bytearray(b'*' * 1024))
        self.cursor = 0
        self.out_queue: asyncio.Queue[Message[
            JsonRpcRequest[Any]]] = asyncio.Queue()
        self.transport: asyncio.Transport

    def get_buffer(self, sizehint: int) -> ReadableBuffer:
        # FIXME: we're assuming that we never have a message larger than 1024 bytes.
        return self.buffer[self.cursor:]

    def buffer_updated(self, nbytes: int) -> None:
        # FIXME: wer're just kinda assuming that all invalid content is just incomplete
        try:
            msg: Message[JsonRpcRequest[Any]]
            read, msg = Message.parse(bytes(self.buffer[:self.cursor +
                                                        nbytes]))
            self.buffer[:self.cursor + nbytes -
                        read] = self.buffer[read:self.cursor + nbytes]
            self.out_queue.put_nowait(msg)
            self.cursor = 0
        except ValueError:
            self.cursor += nbytes

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        assert isinstance(transport, asyncio.Transport)
        self.transport = transport

    def write_message(self, msg: Message[JsonRpcResponse[Any]]) -> None:
        self.transport.write(bytes(msg))

    async def read_message(self) -> Message[JsonRpcRequest[Any]]:
        return await self.out_queue.get()
