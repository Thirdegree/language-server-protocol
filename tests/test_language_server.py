from __future__ import annotations

from typing import Any, Type

import pytest

from lsp import LanguageServer
from lsp.lsp.common import DocumentUri, MessageData, Position, Range
from lsp.lsp.messages import InitializeParams, InitializeResult
from lsp.lsp.server import (CodeAction, CodeActionContext, CodeActionParams, Command, SemanticTokens,
                            SemanticTokensDeltaParams, TextDocumentIdentifier)
from lsp.protocol import LspProtocol
from tests.conftest import RequstFn


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
async def lsp_class() -> Type[ExampleLanguageServer]:
    return ExampleLanguageServer


async def test_code_action_title(lsp_client: LspProtocol[Any], make_request: RequstFn[MessageData]) -> None:
    lsp_client.write_message(
        make_request(
            'textDocument/codeAction',
            CodeActionParams(textDocument=TextDocumentIdentifier(uri=DocumentUri("")),
                             range=Range(start=Position(line=0, character=2), end=Position(line=3, character=4)),
                             context=CodeActionContext(diagnostics=[]))))

    message = await lsp_client.read_message()
    res = message.content.get('result')
    assert res is not None
    assert res[0]['title'] == '0:2-3:4'


async def test_request(lsp_client: LspProtocol[Any], make_request: RequstFn[MessageData]) -> None:
    lsp_client.write_message(make_request('textDocument/semanticTokens/full/delta',
                                          SemanticTokensDeltaParams()))  # type: ignore[typeddict-item]

    message = await lsp_client.read_message()
    res = message.content.get('result')
    assert res is not None
    assert res['data'] == [12, 3]
