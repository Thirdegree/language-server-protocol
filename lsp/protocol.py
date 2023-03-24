from __future__ import annotations

import asyncio
import logging
from contextlib import suppress
from dataclasses import dataclass
from email.message import Message as EmailMessage
from typing import Any, Generic, Literal, NotRequired, Self, TypedDict, TypeVar

import ujson as json

from lsp.lsp.common import T_Message

log = logging.getLogger(__name__)

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
    _encoding: str = 'utf-8'
    _content_len: int | None = None
    _content_type: str | None = None

    def __bytes__(self) -> bytes:
        return (f'Content-Length: {self.content_len}\r\n'
                f'Content-Type: {self.content_type}\r\n\r\n').encode() + self.content_bytes

    def __repr__(self) -> str:
        return f"Message(content={self.content!r})"

    @classmethod
    def parse(cls, data: bytes) -> tuple[int, Self]:
        headers, rest = data.split(b'\r\n\r\n', maxsplit=1)
        # trailing sep for the headers is consumed above, so it's ok to just split
        content_len: int | None = None
        content_type: bytes | None = None
        for header in headers.split(b'\r\n'):
            if header.startswith(b'Content-Type: '):
                content_type = header[14:]
            elif header.startswith(b'Content-Length: '):
                content_len = int(header[16:])
        if content_len is None:
            raise ValueError("Invalid content")
        header_len = len(headers)
        content = json.loads(rest[:content_len] or b'{}')
        return header_len + content_len + 4, cls(content=content,
                                                 _content_len=content_len,
                                                 _content_type=None if content_type is None else content_type.decode(),
                                                 _content_bytes=rest[:content_len])

    @property
    def content_type(self) -> str:
        if self._content_type is None:
            self._content_type = f'application/vscode-jsonrpc; charset={self.encoding}'
        return self._content_type

    @property
    def content_len(self) -> int:
        if self._content_len is None:
            self._content_len = len(self.content_bytes)
        return self._content_len

    @property
    def content_bytes(self) -> bytes:
        if self._content_bytes is None:
            self._content_bytes = json.dumps(self.content).encode(self.encoding)
        return self._content_bytes

    @property
    def encoding(self) -> str:
        if self._encoding is None:
            msg = EmailMessage()
            msg['Content-Type'] = self.content_type
            self._encoding = msg.get_param('charset', 'utf-8')
        return self._encoding


class LspProtocol(asyncio.BufferedProtocol, Generic[T_Content]):
    """
    Implement the `base protocol`_ for lanaguge server protocol messages.

    .. _base protocol: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#baseProtocol
    """  # noqa: E501

    def __init__(self) -> None:
        self.buf_size = 1024
        self.buffer = memoryview(bytearray(b'*' * self.buf_size))
        self.cursor = 0
        self.out_queue: asyncio.Queue[Message[T_Content]] = asyncio.Queue()
        self.transport: asyncio.WriteTransport

    def get_buffer(self, sizehint: int) -> memoryview:
        """
        Get the next writable section of the buffer. Double the size if there is no remaining free buffer.
        """
        _ = sizehint
        log.debug("get buffer, cursor: %s, buffer: %s", self.cursor, self.buf_size)
        if self.cursor >= self.buf_size - 1:
            self.double_buffer()
        return self.buffer[self.cursor:]

    def double_buffer(self) -> None:
        log.debug("Doubling buffer size, %s to %s", self.buf_size, self.buf_size * 2)
        new_buf = memoryview(bytearray(b'*' * self.buf_size * 2))
        new_buf[:len(self.buffer)] = self.buffer
        self.buf_size = self.buf_size * 2
        self.buffer = new_buf

    def buffer_updated(self, nbytes: int) -> None:
        """
        Parse new data into new message, and shift data up
        """
        # FIXME: we're just kinda assuming that all invalid content is just incomplete
        # NOTE: It's possible that we get multiple full messages here,
        #       and are doing wasteful copies. However, this is pretty rare given the
        #       back and forth nature of the protocol
        self.cursor += nbytes
        with suppress(ValueError):
            msg: Message[T_Content]
            read, msg = Message.parse(bytes(self.buffer[:self.cursor]))
            self.buffer[:self.cursor - read] = self.buffer[read:self.cursor]
            self.out_queue.put_nowait(msg)
            self.cursor = self.cursor - read

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        assert isinstance(transport, asyncio.Transport)
        self.transport = transport

    def write_message(self, msg: Message[JsonRpcResponse[Any] | JsonRpcRequest[Any]]) -> None:
        """
        Write a jsonrpc :py:class:`Message`
        """
        log.debug("Writing message %s", msg)
        self.transport.write(bytes(msg))

    async def read_message(self) -> Message[T_Content]:
        """
        Return the next availible JsonRpcRequest Message
        """
        return await self.out_queue.get()
