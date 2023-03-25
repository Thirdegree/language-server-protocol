from __future__ import annotations

from typing import TYPE_CHECKING, Any, Type

import pytest

from examples.never_gonna_lsp import NeverGonna
from examples.spongebob_text_lsp import Spongebob
from lsp import LanguageServer
from lsp.lsp.common import DocumentUri, MessageData, Position, Range
from lsp.lsp.server import (CodeAction, CodeActionContext, CodeActionParams, CompletionItem, CompletionParams,
                            DidOpenTextDocumentParams, TextDocumentIdentifier, TextDocumentItem)
from lsp.protocol import JsonRpcResponse, LspProtocol, Message

if TYPE_CHECKING:
    from tests.conftest import RequstFn


class TestSpongebobLSP:

    @pytest.fixture
    def lsp_class(self) -> Type[LanguageServer]:
        return Spongebob

    @pytest.fixture(autouse=True)
    async def set_content(self, lsp_client: LspProtocol[Any], make_request: RequstFn[MessageData]) -> None:
        content = 'this is some text for the document'
        uri = DocumentUri('')
        lsp_client.write_message(
            make_request(
                'textDocument/didOpen',
                DidOpenTextDocumentParams(
                    textDocument=TextDocumentItem(uri=uri, languageId='python', version=1, text=content))))

    async def test_codeaction_range(self, lsp_client: LspProtocol[Any], make_request: RequstFn[MessageData]) -> None:
        lsp_client.write_message(
            make_request(
                'textDocument/codeAction',
                CodeActionParams(textDocument=TextDocumentIdentifier(uri=DocumentUri('')),
                                 range=Range(start=Position(line=0, character=5), end=Position(line=0, character=10)),
                                 context=CodeActionContext(diagnostics=[]))))
        codeaction: JsonRpcResponse[list[CodeAction]] = (await lsp_client.read_message()).content
        assert 'result' in codeaction
        assert codeaction['result'][0]['title'] == 'Spongebob selection or word'
        assert 'edit' in codeaction['result'][0]
        assert 'changes' in codeaction['result'][0]['edit']
        assert codeaction['result'][0]['edit']['changes'][DocumentUri('')][0]['newText'] == 'Is sO'

    async def test_codeaction_point(self, lsp_client: LspProtocol[Any], make_request: RequstFn[MessageData]) -> None:
        lsp_client.write_message(
            make_request(
                'textDocument/codeAction',
                CodeActionParams(textDocument=TextDocumentIdentifier(uri=DocumentUri('')),
                                 range=Range(start=Position(line=0, character=10), end=Position(line=0, character=10)),
                                 context=CodeActionContext(diagnostics=[]))))
        codeaction: JsonRpcResponse[list[CodeAction]] = (await lsp_client.read_message()).content
        assert 'result' in codeaction
        assert codeaction['result'][0]['title'] == 'Spongebob selection or word'
        assert 'edit' in codeaction['result'][0]
        assert 'changes' in codeaction['result'][0]['edit']
        assert codeaction['result'][0]['edit']['changes'][DocumentUri('')][0]['newText'] == 'SoMe'
        assert codeaction['result'][0]['edit']['changes'][DocumentUri('')][0]['range'] == Range(
            start=Position(line=0, character=8), end=Position(line=0, character=12))


class TestNeverGonnaLsp:

    @pytest.fixture
    def lsp_class(self) -> Type[LanguageServer]:
        return NeverGonna

    async def test_completions(self, lsp_client: LspProtocol[Any], make_request: RequstFn[CompletionParams]) -> None:
        lsp_client.write_message(
            make_request(
                'textDocument/completion',
                CompletionParams(textDocument=TextDocumentIdentifier(uri=DocumentUri('')),
                                 position=Position(line=0, character=0))))
        resp: Message[JsonRpcResponse[list[CompletionItem]]] = await lsp_client.read_message()
        assert 'result' in resp.content
        assert {i['label']
                for i in resp.content['result']} == {
                    "And if you ask me how I'm feeling",
                    "Gotta make you understand",
                    "I just wanna tell you how I'm feeling",
                    "Never gonna give you up",
                    "We're no strangers to love",
                    "We've known each other for so long",
                    "You wouldn't get this from any other guy",
                }
