from __future__ import annotations

import asyncio
import logging
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

log = logging.getLogger(__name__)


def camel_to_snake(s: str) -> str:
    return ''.join(['_' + c.lower() if c.isupper() else c
                    for c in s]).lstrip('_')


@dataclass
class LanguageServer(ABC):
    protocol: LspProtocol = field(default_factory=LspProtocol)
    _serve_task: asyncio.Task[None] | None = None
    _netcat_task: asyncio.Task[None] | None = None
    _listening_on: int | None = None
    _shutdown_received: bool = False

    def transform_method(self, method: str) -> str:
        parts = method.split('/')
        return '__'.join(camel_to_snake(p) for p in parts)

    async def _handle_messages(self) -> None:
        while True:
            msg = await self.protocol.read_message()
            msg_id = msg.content.get('id')
            cb: Callable[[Json | None], Awaitable[Json]] | None = getattr(
                self, self.transform_method(msg.content['method']), None)
            log.debug("Found cb %s for method %s", cb,
                      self.transform_method(msg.content['method']))
            if cb is None:
                if msg_id is not None:
                    self.protocol.write_message(
                        Message(content=JsonRpcResponse(
                            jsonrpc=JSONRPC_VERSION,
                            id=msg_id,
                            error=JsonRpcError(
                                code=-32601,
                                message=
                                f"Method {msg.content['method']!r} not found"))
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
                log.exception("Something happened in %s",
                              msg.content['method'])
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
    async def serve(self, std: bool = True) -> AsyncIterator[Self]:
        async with await asyncio.get_event_loop().create_server(
                lambda: self.protocol,
                host='localhost') as server, asyncio.TaskGroup() as tg:
            self._serve_task = tg.create_task(server.serve_forever())
            self._listening_on = server.sockets[0].getsockname()[1]
            assert self._listening_on is not None
            if std:
                self._netcat_task = tg.create_task(
                    self._netcat(self._listening_on))
            handle = tg.create_task(self._handle_messages())
            yield self
            self._serve_task.cancel()
            if self._netcat_task:
                self._netcat_task.cancel()
            handle.cancel()

    async def _netcat(self, port: int) -> None:
        await asyncio.create_subprocess_exec('nc', 'localhost', str(port))

    @abstractmethod
    async def initialize(self, params: InitializeParams) -> InitializeResult:
        """
        The initialize request is sent as the first request from the client to the server.
        If the server receives a request or notification before the initialize request it should act as follows:

        * For a request the response should be an error with code: -32002. The message can be picked by the server.
        * Notifications should be dropped, except for the exit notification.
          This will allow the exit of a server without an initialize request.

        """
        raise NotImplementedError

    async def shutdown(self, params: None) -> None:
        """
        The shutdown request is sent from the client to the server.
        It asks the server to shut down, but to not exit (otherwise the response might not be delivered correctly to the client).
        There is a separate :py:func:`exit` notification that asks the server to exit.
        Clients must not send any notifications other than exit or requests to a server to which they have sent a shutdown request.
        Clients should also wait with sending the exit notification until they have received a response from the shutdown request.
        """  # noqa: E501

        self._shutdown_received = True

    async def exit(self, params: None) -> None:
        """
        A notification to ask the server to exit its process.
        The server should exit with success code 0 if the shutdown request has been received before; otherwise with error code 1.
        """  # noqa: E501

        if self._shutdown_received:
            exit(0)
        else:
            exit(1)

    async def text_document__declaration(
            self, params: DeclarationParams) -> LocationResponse:
        """
        The go to declaration request is sent from the client to the server to resolve the
        declaration location of a symbol at a given text document position.
        """
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
        log.info("Did initialized")

    async def text_document__did_open(
            self, params: DidOpenTextDocumentParams) -> None:
        log.info("Did text_document__did_open")

    async def text_document__did_change(
            self, params: DidChangeTextDocumentParams) -> None:
        log.info("Did text_document__did_change")

    async def text_document__will_save(
            self, params: WillSaveTextDocumentParams) -> None:
        log.info("Did text_document__will_save")

    async def text_document__will_save_wait_until(
            self, params: WillSaveTextDocumentParams) -> list[TextEdit] | None:
        log.info("Did text_document__will_save_wait_until")
        raise NotImplementedError

    async def text_document__did_save(
            self, params: DidSaveTextDocumentParams) -> None:
        log.info("Did text_document__did_save")

    async def text_document__did_close(
            self, params: DidCloseTextDocumentParams) -> None:
        log.info("Did text_document__did_close")
