from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Awaitable, Callable, Literal, Self

from lsp.lsp.common import Location, LocationLink
from lsp.lsp.messages import (InitializedParams, InitializeParams,
                               InitializeResult)
from lsp.lsp.server import (CallHierarchyIncomingCall,
                             CallHierarchyIncomingCallsParams,
                             CallHierarchyItem, CallHierarchyOutgoingCall,
                             CallHierarchyOutgoingCallsParams,
                             CallHierarchyPrepareParams, CodeAction,
                             CodeActionParams, CodeLens, CodeLensParams,
                             ColorInformation, Command, CompletionItem,
                             CompletionList, CompletionParams,
                             DeclarationParams, DefinitionParams,
                             DidChangeTextDocumentParams,
                             DidCloseTextDocumentParams,
                             DidOpenTextDocumentParams,
                             DidSaveTextDocumentParams, DocumentColorParams,
                             DocumentFormattingParams, DocumentHighlight,
                             DocumentHighlightParams, DocumentLink,
                             DocumentLinkParams, DocumentSymbol,
                             DocumentSymbolParam, ExecuteCommandParams,
                             FoldingRange, FoldingRangeParams, Hover,
                             HoverParams, ImplementationParams, InlayHint,
                             InlayHintParams, InlineValue, InlineValueParams,
                             Moniker, MonikerParams, ReferenceParams,
                             SelectionRange, SelectionRangeParams,
                             SemanticTokens, SemanticTokensDelta,
                             SemanticTokensDeltaParams, SemanticTokensParams,
                             SemanticTokensRangeParams, SignatureHelp,
                             SignatureHelpParams, SymbolInformation, TextEdit,
                             TypeDefinitionParams, TypeHierarchyItem,
                             TypeHierarchyPrepareParams,
                             TypeHierarchySubtypesParams,
                             TypeHierarchySupertypesParams,
                             WillSaveTextDocumentParams)
from lsp.protocol import JsonRpcError, JsonRpcResponse, LspProtocol, Message

Json = dict[str, Any]
JSONRPC_VERSION: Literal["2.0"] = "2.0"

LocationResponse = Location | list[Location] | list[LocationLink] | None


def camel_to_snake(s: str) -> str:
    return ''.join(['_' + c.lower() if c.isupper() else c
                    for c in s]).lstrip('_')


@dataclass
class LanguageServer(ABC):
    protocol: LspProtocol = field(default_factory=LspProtocol)
    _serve_task: asyncio.Task[None] | None = None

    def transform_method(self, method: str) -> str:
        left, _, right = method.partition('/')
        if not right:
            return camel_to_snake(left)
        return f'{camel_to_snake(left)}__{camel_to_snake(right)}'

    async def _handle_messages(self) -> None:
        while True:
            msg = await self.protocol.read_message()
            msg_id = msg.content.get('id')
            cb: Callable[[Json | None], Awaitable[Json]] | None = getattr(
                self, self.transform_method(msg.content['method']), None)
            if cb is None:
                if msg_id is not None:
                    self.protocol.write_message(
                        Message(content=JsonRpcResponse(
                            jsonrpc=JSONRPC_VERSION,
                            id=msg_id,
                            error=JsonRpcError(
                                code=-32601,
                                message=f"Method {msg.content['method']!r} not found"))
                                ))
                continue
            try:
                result = await cb(msg.content.get('params'))
                if msg_id is not None and result:
                    # otherwise, it's a notification and no response required
                    self.protocol.write_message(
                        Message(content=JsonRpcResponse(
                            jsonrpc=JSONRPC_VERSION, id=msg_id,
                            result=result)))
            except (Exception, NotImplementedError, AssertionError) as e:
                if msg_id is not None:
                    self.protocol.write_message(
                        Message(content=JsonRpcResponse(
                            jsonrpc=JSONRPC_VERSION,
                            id=msg_id,
                            error=JsonRpcError(code=-32603, message=str(e)))))

    async def wait(self) -> None:
        if self._serve_task is None:
            return
        await self._serve_task

    @asynccontextmanager
    async def serve(self, host: str, port: int) -> AsyncIterator[Self]:
        async with await asyncio.get_event_loop().create_server(
                lambda: self.protocol, host=host,
                port=port) as server, asyncio.TaskGroup() as tg:
            self._serve_task = tg.create_task(server.serve_forever())
            handle = tg.create_task(self._handle_messages())
            yield self
            self._serve_task.cancel()
            handle.cancel()

    @abstractmethod
    async def initialize(self, params: InitializeParams) -> InitializeResult:
        raise NotImplementedError

    async def shutdown(self, params: None) -> None:
        pass

    async def text_document__declaration(
            self, params: DeclarationParams) -> LocationResponse:
        pass

    async def text_document__definition(
            self, params: DefinitionParams) -> LocationResponse:
        pass

    async def text_document__type_definition(
            self, params: TypeDefinitionParams) -> LocationResponse:
        pass

    async def text_document__implementation(
            self, params: ImplementationParams) -> LocationResponse:
        pass

    async def text_document__references(
            self, params: ReferenceParams) -> list[Location] | None:
        pass

    async def text_document__prepare_call_hierarchy(
            self, params: CallHierarchyPrepareParams
    ) -> list[CallHierarchyItem] | None:
        pass

    async def call_hierarchy__incoming_calls(
        self, params: CallHierarchyIncomingCallsParams
    ) -> list[CallHierarchyIncomingCall] | None:
        pass

    async def call_hierarchy__outgoing_calls(
        self, params: CallHierarchyOutgoingCallsParams
    ) -> list[CallHierarchyOutgoingCall] | None:
        pass

    async def text_document__prepare_type_hierarchy(
            self, params: TypeHierarchyPrepareParams
    ) -> list[TypeHierarchyItem] | None:
        pass

    async def type_hierarchy__supertypes(
        self, params: TypeHierarchySupertypesParams
    ) -> list[TypeHierarchyItem] | None:
        pass

    async def type_hierarchy__subtypes(
            self, params: TypeHierarchySubtypesParams
    ) -> list[TypeHierarchyItem] | None:
        pass

    async def text_document__document_highlight(
            self,
            params: DocumentHighlightParams) -> list[DocumentHighlight] | None:
        pass

    async def text_document__document_link(
            self, params: DocumentLinkParams) -> list[DocumentLink] | None:
        pass

    async def document_link__resolve(self,
                                     params: DocumentLink) -> DocumentLink:
        raise NotImplementedError

    async def text_document__hover(self, params: HoverParams) -> Hover | None:
        pass

    async def text_document__code_lens(
            self, params: CodeLensParams) -> CodeLens | None:
        pass

    async def code_lens__resolve(self, params: CodeLens) -> CodeLens:
        raise NotImplementedError

    async def text_document__folding_range(
            self, params: FoldingRangeParams) -> list[FoldingRange] | None:
        pass

    async def text_document__selection_range(
            self, params: SelectionRangeParams) -> list[SelectionRange] | None:
        pass

    async def text_document__document_symbol(
        self, params: DocumentSymbolParam
    ) -> list[DocumentSymbol] | list[SymbolInformation] | None:
        pass

    async def text_document__semantic_tokens__full(
            self, params: SemanticTokensParams) -> SemanticTokens | None:
        pass

    async def text_document__semantic_tokens__full__delta(
        self, params: SemanticTokensDeltaParams
    ) -> SemanticTokens | SemanticTokensDelta | None:
        pass

    async def text_document__semantic_tokens__range(
            self, params: SemanticTokensRangeParams) -> SemanticTokens | None:
        pass

    async def text_document__inline_value(
            self, params: InlineValueParams) -> list[InlineValue] | None:
        pass

    async def text_document__inlay_hint(
            self, params: InlayHintParams) -> list[InlayHint] | None:
        pass

    async def inlay_hint__resolve(self, params: InlayHint) -> InlayHint:
        raise NotImplementedError

    async def text_document__moniker(
            self, params: MonikerParams) -> list[Moniker] | None:
        pass

    async def text_document__completion(
        self, params: CompletionParams
    ) -> list[CompletionItem] | CompletionList | None:
        pass

    async def completion_item__resolve(
            self, params: CompletionItem) -> CompletionItem:
        raise NotImplementedError

    async def text_document__signature_help(
            self, params: SignatureHelpParams) -> SignatureHelp | None:
        pass

    async def text_document__code_action(
            self,
            params: CodeActionParams) -> list[Command | CodeAction] | None:
        pass

    async def code_action__resolve(self, params: CodeAction) -> CodeAction:
        raise NotImplementedError

    async def text_document__document_color(
            self, params: DocumentColorParams) -> list[ColorInformation]:
        raise NotImplementedError

    async def text_document__formatting(
            self, params: DocumentFormattingParams) -> list[TextEdit] | None:
        pass

    async def workspace__execute_command(
            self, params: ExecuteCommandParams) -> Any | None:
        pass

    # TODO
    # textDocument/colorPresentation
    # textDocument/rangeFormatting
    # textDocument/onTypeFormatting
    # textDocument/rename
    # textDocument/prepareRename
    # textDocument/linkedEditingRange
    # workspace/symbol
    # workspaceSymbol/resolve
    # workspace/didChangeConfiguration
    # workspace/didChangeWorkspaceFolders
    # workspace/willCreateFiles
    # workspace/didCreateFiles
    # workspace/willRenameFiles
    # workspace/didRenameFiles
    # workspace/willDeleteFiles
    # workspace/didDeleteFiles
    # workspace/didChangeWatchedFiles

    # notifications

    async def initialized(self, params: InitializedParams) -> None:
        pass

    async def text_document__did_open(
            self, params: DidOpenTextDocumentParams) -> None:
        pass

    async def text_document__did_change(
            self, params: DidChangeTextDocumentParams) -> None:
        pass

    async def text_document__will_save(
            self, params: WillSaveTextDocumentParams) -> None:
        pass

    async def text_document__will_save_wait_until(
            self, params: WillSaveTextDocumentParams) -> list[TextEdit] | None:
        pass

    async def text_document__did_save(
            self, params: DidSaveTextDocumentParams) -> None:
        pass

    async def text_document__did_close(
            self, params: DidCloseTextDocumentParams) -> None:
        pass
