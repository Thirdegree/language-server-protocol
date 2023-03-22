from __future__ import annotations

from typing import Any, Literal, NotRequired, TypedDict

from lsp.lsp.common import (URI, CodeActionKind, CodeActionTriggerKind, DocumentHighlightKind, DocumentUri, EmptyDict,
                            FileOperationPatternKind, FoldingRangeKind, InsertTextMode, Location, MarkupKind,
                            MessageData, MonikerKind, Position, PositionEncodingKind, Range, SymbolKind, SymbolTag,
                            UniquenessLevel, WorkDoneProgressOptions, WorkspaceFolder)


class FileOperationPatternOptions(MessageData):
    #
    # The pattern should be matched ignoring casing.
    #
    ignoreCase: NotRequired[bool]


class FileOperationPattern(MessageData):
    #
    # The glob pattern to match. Glob patterns can have the following syntax:
    # - `*` to match one or more characters in a path segment
    # - `?` to match on one character in a path segment
    # - `**` to match any number of path segments, including none
    # - `{}` to group sub patterns into an OR expression. (e.g. `**​/*.{ts,js}`
    #   matches all TypeScript and JavaScript files)
    # - `[]` to declare a range of characters to match in a path segment
    #   (e.g., `example.[0-9]` to match on `example.0`, `example.1`, …)
    # - `[!...]` to negate a range of characters to match in a path segment
    #   (e.g., `example.[!0-9]` to match on `example.a`, `example.b`, but
    #   not `example.0`)
    #
    glob: str

    #
    # Whether to match files or folders with this pattern.
    #
    # Matches both if undefined.
    #
    matches: NotRequired[FileOperationPatternKind]

    #
    # Additional options used during matching.
    #
    options: NotRequired[FileOperationPatternOptions]


class FileOperationFilter(MessageData):
    #
    # A Uri like `file` or `untitled`.
    #
    scheme: NotRequired[str]

    #
    # The actual file operation pattern.
    #
    pattern: FileOperationPattern


class FileOperationRegistrationOptions(MessageData):
    #
    # The actual filters.
    #
    filters: list[FileOperationFilter]


class ServerCapabilitiesWorkspaceFileOperations(MessageData):
    #
    # The server is interested in receiving didCreateFiles
    # notifications.
    #
    didCreate: NotRequired[FileOperationRegistrationOptions]

    #
    # The server is interested in receiving willCreateFiles requests.
    #
    willCreate: NotRequired[FileOperationRegistrationOptions]

    #
    # The server is interested in receiving didRenameFiles
    # notifications.
    #
    didRename: NotRequired[FileOperationRegistrationOptions]

    #
    # The server is interested in receiving willRenameFiles requests.
    #
    willRename: NotRequired[FileOperationRegistrationOptions]

    #
    # The server is interested in receiving didDeleteFiles file
    # notifications.
    #
    didDelete: NotRequired[FileOperationRegistrationOptions]

    #
    # The server is interested in receiving willDeleteFiles file
    # requests.
    #
    willDelete: NotRequired[FileOperationRegistrationOptions]


class WorkspaceFoldersServerCapabilities(MessageData):
    #
    # The server has support for workspace folders
    #
    supported: NotRequired[bool]

    #
    # Whether the server wants to receive workspace folder
    # change notifications.
    #
    # If a string is provided, the string is treated as an ID
    # under which the notification is registered on the client
    # side. The ID can be used to unregister for these events
    # using the `client/unregisterCapability` request.
    #
    changeNotifications: NotRequired[str | bool]


class ServerCapabilitiesWorkspace(MessageData):
    #
    # The server supports workspace folder.
    #
    # @since 3.6.0
    #
    workspaceFolders: NotRequired[WorkspaceFoldersServerCapabilities]

    #
    # The server is interested in file notifications/requests.
    #
    # @since 3.16.0
    #
    fileOperations: NotRequired[ServerCapabilitiesWorkspaceFileOperations]


# None=0, Full=1, Incremental=2
TextDocumentSyncKind = Literal[0, 1, 2]


class TextDocumentSyncOptions(MessageData):
    #
    # Open and close notifications are sent to the server. If omitted open
    # close notifications should not be sent.
    #
    openClose: NotRequired[bool]

    #
    # Change notifications are sent to the server. See
    # TextDocumentSyncKind.None, TextDocumentSyncKind.Full and
    # TextDocumentSyncKind.Incremental. If omitted it defaults to
    # TextDocumentSyncKind.None.
    #
    change: NotRequired[TextDocumentSyncKind]


class NotebookDocumentSyncOptionsNotebookSelectorCells(MessageData):
    langugage: str


class NotebookDocumentFilterRequireScheme(MessageData):
    #  The type of the enclosing notebook.
    notebookType: NotRequired[str]

    #  A Uri [scheme](#Uri.scheme), like `file` or `untitled`.
    scheme: str

    #  A glob pattern.
    pattern: NotRequired[str]


class NotebookDocumentFilterRequirePattern(MessageData):
    #  The type of the enclosing notebook.
    notebookType: NotRequired[str]

    #  A Uri [scheme](#Uri.scheme), like `file` or `untitled`.
    scheme: NotRequired[str]

    #  A glob pattern.
    pattern: str


class NotebookDocumentFilterRequireNotebookType(MessageData):
    #  The type of the enclosing notebook.
    notebookType: str

    #  A Uri [scheme](#Uri.scheme), like `file` or `untitled`.
    scheme: NotRequired[str]

    #  A glob pattern.
    pattern: NotRequired[str]


NotebookDocumentFilter = (NotebookDocumentFilterRequireScheme
                          | NotebookDocumentFilterRequireNotebookType
                          | NotebookDocumentFilterRequirePattern)


class NotebookDocumentSyncOptionsNotebookSelectorOptionalNotebook(MessageData):
    #
    # The notebook to be synced. If a string
    # value is provided it matches against the
    # notebook type. '*' matches every notebook.
    #
    notebook: NotRequired[str | NotebookDocumentFilter]

    #
    # The cells of the matching notebook to be synced.
    #
    cells: list[NotebookDocumentSyncOptionsNotebookSelectorCells]


class NotebookDocumentSyncOptionsNotebookSelectorOptionalCells(MessageData):
    #
    # The notebook to be synced. If a string
    # value is provided it matches against the
    # notebook type. '*' matches every notebook.
    #
    notebook: str | NotebookDocumentFilter

    #
    # The cells of the matching notebook to be synced.
    #
    cells: NotRequired[list[NotebookDocumentSyncOptionsNotebookSelectorCells]]


NotebookSelector = (NotebookDocumentSyncOptionsNotebookSelectorOptionalCells
                    | NotebookDocumentSyncOptionsNotebookSelectorOptionalNotebook)


class NotebookDocumentSyncOptions(MessageData):
    #
    # The notebooks to be synced
    #
    notebookSelector: list[NotebookSelector]

    #
    # Whether save notification should be forwarded to
    # the server. Will only be honored if mode === `notebook`.
    #
    save: NotRequired[bool]


class StaticRegistrationOptions(MessageData):
    #
    # The id used to register the request. The id can be used to deregister
    # the request again. See also Registration#id.
    #
    id: NotRequired[str]


class NotebookDocumentSyncRegistrationOptions(NotebookDocumentSyncOptions, StaticRegistrationOptions):
    pass


class CompletionOptionsCompletionItem(MessageData):
    #
    # The server has support for completion item label
    # details (see also `CompletionItemLabelDetails`) when receiving
    # a completion item in a resolve call.
    #
    # @since 3.17.0
    #
    labelDetailsSupport: NotRequired[bool]


class HoverOptions(WorkDoneProgressOptions):
    pass


class CompletionOptions(WorkDoneProgressOptions):
    #
    # The additional characters, beyond the defaults provided by the client (typically
    # [a-zA-Z]), that should automatically trigger a completion request. For example
    # `.` in JavaScript represents the beginning of an object property or method and is
    # thus a good candidate for triggering a completion request.
    #
    # Most tools trigger a completion request automatically without explicitly
    # requesting it using a keyboard shortcut (e.g. Ctrl+Space). Typically they
    # do so when the user starts to type an identifier. For example if the user
    # types `c` in a JavaScript file code complete will automatically pop up
    # present `console` besides others as a completion item. Characters that
    # make up identifiers don't need to be listed here.
    #
    triggerCharacters: NotRequired[list[str]]

    #
    # The list of all possible characters that commit a completion. This field
    # can be used if clients don't support individual commit characters per
    # completion item. See client capability
    # `completion.completionItem.commitCharactersSupport`.
    #
    # If a server provides both `allCommitCharacters` and commit characters on
    # an individual completion item the ones on the completion item win.
    #
    # @since 3.2.0
    #
    allCommitCharacters: NotRequired[list[str]]

    #
    # The server provides support to resolve additional
    # information for a completion item.
    #
    resolveProvider: NotRequired[bool]

    #
    # The server supports the following `CompletionItem` specific
    # capabilities.
    #
    # @since 3.17.0
    #
    completionItem: NotRequired[CompletionOptionsCompletionItem]


class SignatureHelpOptions(WorkDoneProgressOptions):
    #
    # The characters that trigger signature help
    # automatically.
    #
    triggerCharacters: NotRequired[list[str]]

    #
    # List of characters that re-trigger signature help.
    #
    # These trigger characters are only active when signature help is already
    # showing. All trigger characters are also counted as re-trigger
    # characters.
    #
    # @since 3.15.0
    #
    retriggerCharacters: NotRequired[list[str]]


class DeclarationOptions(WorkDoneProgressOptions):
    pass


class DocumentFilter(MessageData):
    #
    # A language id, like `typescript`.
    #
    language: NotRequired[str]

    #
    # A Uri [scheme](#Uri.scheme), like `file` or `untitled`.
    #
    scheme: NotRequired[str]

    #
    # A glob pattern, like `*.{ts,js}`.
    #
    # Glob patterns can have the following syntax:
    # - `*` to match one or more characters in a path segment
    # - `?` to match on one character in a path segment
    # - `**` to match any number of path segments, including none
    # - `{}` to group sub patterns into an OR expression. (e.g. `**​/*.{ts,js}`
    #   matches all TypeScript and JavaScript files)
    # - `[]` to declare a range of characters to match in a path segment
    #   (e.g., `example.[0-9]` to match on `example.0`, `example.1`, …)
    # - `[!...]` to negate a range of characters to match in a path segment
    #   (e.g., `example.[!0-9]` to match on `example.a`, `example.b`, but
    #   not `example.0`)
    #
    pattern: NotRequired[str]


DocumentSelector = list[DocumentFilter]


class TextDocumentRegistrationOptions(MessageData):
    #
    # A document selector to identify the scope of the registration. If set to
    # null the document selector provided on the client side will be used.
    #
    documentSelector: DocumentSelector | None


class DeclarationRegistrationOptions(DeclarationOptions, TextDocumentRegistrationOptions, StaticRegistrationOptions):
    pass


class DefinitionOptions(WorkDoneProgressOptions):
    pass


class TypeDefinitionOptions(WorkDoneProgressOptions):
    pass


class TypeDefinitionRegistrationOptions(WorkDoneProgressOptions):
    pass


class ImplementationOptions(WorkDoneProgressOptions):
    pass


class ImplementationRegistrationOptions(TextDocumentRegistrationOptions, ImplementationOptions,
                                        StaticRegistrationOptions):
    pass


class ReferenceOptions(WorkDoneProgressOptions):
    pass


class DocumentHighlightOptions(WorkDoneProgressOptions):
    pass


class DocumentSymbolOptions(WorkDoneProgressOptions):
    #
    # A human-readable string that is shown when multiple outlines trees
    # are shown for the same document.
    #
    # @since 3.16.0
    #
    label: NotRequired[str]


class CodeActionOptions(WorkDoneProgressOptions):
    #
    # CodeActionKinds that this server may return.
    #
    # The list of kinds may be generic, such as `CodeActionKind.Refactor`,
    # or the server may list out every specific kind they provide.
    #
    codeActionKinds: NotRequired[list[CodeActionKind]]

    #
    # The server provides support to resolve additional
    # information for a code action.
    #
    # @since 3.16.0
    #
    resolveProvider: NotRequired[bool]


class CodeLensOptions(WorkDoneProgressOptions):
    #
    # Code lens has a resolve provider as well.
    #
    resolveProvider: NotRequired[bool]


class DocumentLinkOptions(WorkDoneProgressOptions):
    #
    # Document links have a resolve provider as well.
    #
    resolveProvider: NotRequired[bool]


class DocumentColorOptions(WorkDoneProgressOptions):
    pass


class DocumentColorRegistrationOptions(TextDocumentRegistrationOptions, StaticRegistrationOptions,
                                       DocumentColorOptions):
    pass


class DocumentFormattingOptions(WorkDoneProgressOptions):
    pass


class DocumentRangeFormattingOptions(WorkDoneProgressOptions):
    pass


class DocumentOnTypeFormattingOptions(MessageData):
    #
    # A character on which formatting should be triggered, like `{`.
    #
    firstTriggerCharacter: str

    #
    # More trigger characters.
    #
    moreTriggerCharacter: NotRequired[list[str]]


class RenameOptions(WorkDoneProgressOptions):
    #
    # Renames should be checked and tested before being executed.
    #
    prepareProvider: NotRequired[bool]


class FoldingRangeOptions(WorkDoneProgressOptions):
    pass


class FoldingRangeRegistrationOptions(TextDocumentRegistrationOptions, FoldingRangeOptions, StaticRegistrationOptions):
    pass


class ExecuteCommandOptions(WorkDoneProgressOptions):
    commands: list[str]


class SelectionRangeOptions(WorkDoneProgressOptions):
    pass


class SelectionRangeRegistrationOptions(SelectionRangeOptions, TextDocumentRegistrationOptions,
                                        StaticRegistrationOptions):
    pass


class LinkedEditingRangeOptions(WorkDoneProgressOptions):
    pass


class LinkedEditingRangeRegistrationOptions(TextDocumentRegistrationOptions, LinkedEditingRangeOptions,
                                            StaticRegistrationOptions):
    pass


class CallHierarchyOptions(WorkDoneProgressOptions):
    pass


class CallHierarchyRegistrationOptions(TextDocumentRegistrationOptions, CallHierarchyOptions,
                                       StaticRegistrationOptions):
    pass


class SemanticTokensOptionsFull(WorkDoneProgressOptions):
    delta: NotRequired[bool]


class SemanticTokensLegend(MessageData):
    #
    # The token types a server uses.
    #
    tokenTypes: list[str]

    #
    # The token modifiers a server uses.
    #
    tokenModifiers: list[str]


class SemanticTokensOptions(WorkDoneProgressOptions):
    #
    # The legend used by the server
    #
    legend: SemanticTokensLegend

    #
    # Server supports providing semantic tokens for a specific range
    # of a document.
    #
    range: NotRequired[bool | EmptyDict]

    #
    # Server supports providing semantic tokens for a full document.
    #
    full: NotRequired[bool | SemanticTokensOptionsFull]


class SemanticTokensRegistrationOptions(TextDocumentRegistrationOptions, SemanticTokensOptions,
                                        StaticRegistrationOptions):
    pass


class MonikerOptions(WorkDoneProgressOptions):
    pass


class MonikerRegistrationOptions(TextDocumentRegistrationOptions, MonikerOptions):
    pass


class TypeHierarchyOptions(WorkDoneProgressOptions):
    pass


class TypeHierarchyRegistrationOptions(TextDocumentRegistrationOptions, TypeHierarchyOptions,
                                       StaticRegistrationOptions):
    pass


class InlineValueOptions(WorkDoneProgressOptions):
    pass


class InlineValueRegistrationOptions(InlineValueOptions, TextDocumentRegistrationOptions, StaticRegistrationOptions):
    pass


class InlayHintOptions(WorkDoneProgressOptions):
    #
    # Document links have a resolve provider as well.
    #
    resolveProvider: NotRequired[bool]


class InlayHintRegistrationOptions(InlayHintOptions, TextDocumentRegistrationOptions, StaticRegistrationOptions):
    pass


class WorkspaceSymbolOptions(WorkDoneProgressOptions):
    #
    # Document links have a resolve provider as well.
    #
    resolveProvider: NotRequired[bool]


class DiagnosticOptions(WorkDoneProgressOptions):

    #
    # An optional identifier under which the diagnostics are
    # managed by the client.
    #
    identifier: NotRequired[str]

    #
    # Whether the language has inter file dependencies meaning that
    # editing code in one file can result in a different diagnostic
    # set in another file. Inter file dependencies are common for
    # most programming languages and typically uncommon for linters.
    #
    interFileDependencies: bool

    #
    # The server provides support for workspace diagnostics as well.
    #
    workspaceDiagnostics: bool


class DiagnosticRegistrationOptions(TextDocumentRegistrationOptions, DiagnosticOptions, StaticRegistrationOptions):
    pass


class ServerCapabilities(MessageData):

    #
    # The position encoding the server picked from the encodings offered
    # by the client via the client capability `general.positionEncodings`.
    #
    # If the client didn't provide any position encodings the only valid
    # value that a server can return is 'utf-16'.
    #
    # If omitted it defaults to 'utf-16'.
    #
    # @since 3.17.0
    #
    positionEncoding: NotRequired[PositionEncodingKind]

    #
    # Defines how text documents are synced. Is either a detailed structure
    # defining each notification or for backwards compatibility the
    # TextDocumentSyncKind number. If omitted it defaults to
    # `TextDocumentSyncKind.None`.
    #
    textDocumentSync: NotRequired[TextDocumentSyncOptions | TextDocumentSyncKind]

    #
    # Defines how notebook documents are synced.
    #
    # @since 3.17.0
    #
    notebookDocumentSync: NotRequired[NotebookDocumentSyncOptions | NotebookDocumentSyncRegistrationOptions]

    #
    # The server provides completion support.
    #
    completionProvider: NotRequired[CompletionOptions]

    #
    # The server provides hover support.
    #
    hoverProvider: NotRequired[bool | HoverOptions]

    #
    # The server provides signature help support.
    #
    signatureHelpProvider: NotRequired[SignatureHelpOptions]

    #
    # The server provides go to declaration support.
    #
    # @since 3.14.0
    #
    declarationProvider: NotRequired[bool | DeclarationOptions | DeclarationRegistrationOptions]

    #
    # The server provides goto definition support.
    #
    definitionProvider: NotRequired[bool | DefinitionOptions]

    #
    # The server provides goto type definition support.
    #
    # @since 3.6.0
    #
    typeDefinitionProvider: NotRequired[bool | TypeDefinitionOptions | TypeDefinitionRegistrationOptions]

    #
    # The server provides goto implementation support.
    #
    # @since 3.6.0
    #
    implementationProvider: NotRequired[bool | ImplementationOptions | ImplementationRegistrationOptions]

    #
    # The server provides find references support.
    #
    referencesProvider: NotRequired[bool | ReferenceOptions]

    #
    # The server provides document highlight support.
    #
    documentHighlightProvider: NotRequired[bool | DocumentHighlightOptions]

    #
    # The server provides document symbol support.
    #
    documentSymbolProvider: NotRequired[bool | DocumentSymbolOptions]

    #
    # The server provides code actions. The `CodeActionOptions` return type is
    # only valid if the client signals code action literal support via the
    # property `textDocument.codeAction.codeActionLiteralSupport`.
    #
    codeActionProvider: NotRequired[bool | CodeActionOptions]

    #
    # The server provides code lens.
    #
    codeLensProvider: NotRequired[CodeLensOptions]

    #
    # The server provides document link support.
    #
    documentLinkProvider: NotRequired[DocumentLinkOptions]

    #
    # The server provides color provider support.
    #
    # @since 3.6.0
    #
    colorProvider: NotRequired[bool | DocumentColorOptions | DocumentColorRegistrationOptions]

    #
    # The server provides document formatting.
    #
    documentFormattingProvider: NotRequired[bool | DocumentFormattingOptions]

    #
    # The server provides document range formatting.
    #
    documentRangeFormattingProvider: NotRequired[bool | DocumentRangeFormattingOptions]

    #
    # The server provides document formatting on typing.
    #
    documentOnTypeFormattingProvider: NotRequired[DocumentOnTypeFormattingOptions]

    #
    # The server provides rename support. RenameOptions may only be
    # specified if the client states that it supports
    # `prepareSupport` in its initial `initialize` request.
    #
    renameProvider: NotRequired[bool | RenameOptions]

    #
    # The server provides folding provider support.
    #
    # @since 3.10.0
    #
    foldingRangeProvider: NotRequired[bool | FoldingRangeOptions | FoldingRangeRegistrationOptions]

    #
    # The server provides execute command support.
    #
    executeCommandProvider: NotRequired[ExecuteCommandOptions]

    #
    # The server provides selection range support.
    #
    # @since 3.15.0
    #
    selectionRangeProvider: NotRequired[bool | SelectionRangeOptions | SelectionRangeRegistrationOptions]

    #
    # The server provides linked editing range support.
    #
    # @since 3.16.0
    #
    linkedEditingRangeProvider: NotRequired[bool | LinkedEditingRangeOptions | LinkedEditingRangeRegistrationOptions]

    #
    # The server provides call hierarchy support.
    #
    # @since 3.16.0
    #
    callHierarchyProvider: NotRequired[bool | CallHierarchyOptions | CallHierarchyRegistrationOptions]

    #
    # The server provides semantic tokens support.
    #
    # @since 3.16.0
    #
    semanticTokensProvider: NotRequired[SemanticTokensOptions | SemanticTokensRegistrationOptions]

    #
    # Whether server provides moniker support.
    #
    # @since 3.16.0
    #
    monikerProvider: NotRequired[bool | MonikerOptions | MonikerRegistrationOptions]

    #
    # The server provides type hierarchy support.
    #
    # @since 3.17.0
    #
    typeHierarchyProvider: NotRequired[bool | TypeHierarchyOptions | TypeHierarchyRegistrationOptions]

    #
    # The server provides inline values.
    #
    # @since 3.17.0
    #
    inlineValueProvider: NotRequired[bool | InlineValueOptions | InlineValueRegistrationOptions]

    #
    # The server provides inlay hints.
    #
    # @since 3.17.0
    #
    inlayHintProvider: NotRequired[bool | InlayHintOptions | InlayHintRegistrationOptions]

    #
    # The server has support for pull model diagnostics.
    #
    # @since 3.17.0
    #
    diagnosticProvider: NotRequired[DiagnosticOptions | DiagnosticRegistrationOptions]

    #
    # The server provides workspace symbol support.
    #
    workspaceSymbolProvider: NotRequired[bool | WorkspaceSymbolOptions]

    #
    # Workspace specific server capabilities
    #
    workspace: NotRequired[ServerCapabilitiesWorkspace]

    #
    # Experimental server capabilities.
    #
    experimental: NotRequired[Any]


class TextDocumentItem(MessageData):
    #
    # The text document's URI.
    #
    uri: DocumentUri

    #
    # The text document's language identifier.
    #
    languageId: str

    #
    # The version number of this document (it will increase after each
    # change, including undo/redo).
    #
    version: int

    #
    # The content of the opened text document.
    #
    text: str


class DidOpenTextDocumentParams(MessageData):
    #
    # The document that was opened.
    #
    textDocument: TextDocumentItem


class TextDocumentIdentifier(MessageData):
    #
    # The text document's URI.
    #
    uri: DocumentUri


class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    #
    # The version number of this document.
    #
    # The version number of a document will increase after each change,
    # including undo/redo. The number doesn't need to be consecutive.
    #
    version: int


class TextDocumentContentChangeEventSimple(MessageData):
    text: str


class TextDocumentContentChangeEventRange(MessageData):
    #
    # The range of the document that changed.
    #
    range: Range

    #
    # The optional length of the range that got replaced.
    #
    # @deprecated use range instead.
    #
    rangeLength: NotRequired[int]

    #
    # The new text for the provided range.
    #
    text: str


TextDocumentContentChangeEvent = TextDocumentContentChangeEventRange | TextDocumentContentChangeEventSimple


class DidChangeTextDocumentParams(MessageData):
    #
    # The document that did change. The version number points
    # to the version after all provided content changes have
    # been applied.
    #
    textDocument: VersionedTextDocumentIdentifier

    #
    # The actual content changes. The content changes describe single state
    # changes to the document. So if there are two content changes c1 (at
    # array index 0) and c2 (at array index 1) for a document in state S then
    # c1 moves the document from S to S' and c2 from S' to S''. So c1 is
    # computed on the state S and c2 is computed on the state S'.
    #
    # To mirror the content of a document using change events use the following
    # approach:
    # - start with the same initial content
    # - apply the 'textDocument/didChange' notifications in the order you
    #   receive them.
    # - apply the `TextDocumentContentChangeEvent`s in a single notification
    #   in the order you receive them.
    #
    contentChanges: list[TextDocumentContentChangeEvent]


TextDocumentSaveReason = Literal[

    #
    # Manually triggered, e.g. by the user pressing save, by starting
    # debugging, or by an API call.
    #
    1,  # Manual

    #
    # Automatic after a delay.
    #
    2,  # AfterDelay

    #
    # When the editor lost focus.
    #
    3,  # FocusOut
]


class WillSaveTextDocumentParams(MessageData):
    #
    # The document that will be saved.
    #
    textDocument: TextDocumentIdentifier

    #
    # The 'TextDocumentSaveReason'.
    #
    reason: TextDocumentSaveReason


class TextEdit(MessageData):
    #
    # The range of the text document to be manipulated. To insert
    # text into a document create a range where start === end.
    #
    range: Range

    #
    # The string to be inserted. For delete operations use an
    # empty string.
    #
    newText: str


class DidSaveTextDocumentParams(MessageData):
    #
    # The document that was saved.
    #
    textDocument: TextDocumentIdentifier

    #
    # Optional the content when saved. Depends on the includeText value
    # when the save notification was requested.
    #
    text: NotRequired[str]


class DidCloseTextDocumentParams(MessageData):
    #
    # The document that was closed.
    #
    textDocument: TextDocumentIdentifier


class TextDocumentPositionParams(MessageData):
    #
    # The text document.
    #
    textDocument: TextDocumentIdentifier

    #
    # The position inside the text document.
    #
    position: Position


ProgressToken = int | str


class WorkDoneProgressParams(MessageData):
    #
    # An optional token that a server can use to report work done progress.
    #
    workDoneToken: NotRequired[ProgressToken]


class PartialResultParams(MessageData):
    #
    # An optional token that a server can use to report partial results (e.g.
    # streaming) to the client.
    #
    partialResultToken: NotRequired[ProgressToken]


class DeclarationParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    pass


class DefinitionParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    pass


class TypeDefinitionParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    pass


class ImplementationParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    pass


class ReferenceContext(MessageData):
    #
    # Include the declaration of the current symbol.
    #
    includeDeclaration: bool


class ReferenceParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    context: ReferenceContext


class CallHierarchyPrepareParams(TextDocumentPositionParams, WorkDoneProgressParams):
    pass


class CallHierarchyItem(MessageData):
    #
    # The name of this item.
    #
    name: str

    #
    # The kind of this item.
    #
    kind: SymbolKind

    #
    # Tags for this item.
    #
    tags: NotRequired[list[SymbolTag]]

    #
    # More detail for this item, e.g. the signature of a function.
    #
    detail: NotRequired[str]

    #
    # The resource identifier of this item.
    #
    uri: DocumentUri

    #
    # The range enclosing this symbol not including leading/trailing whitespace
    # but everything else, e.g. comments and code.
    #
    range: Range

    #
    # The range that should be selected and revealed when this symbol is being
    # picked, e.g. the name of a function. Must be contained by the
    # [`range`](#CallHierarchyItem.range).
    #
    selectionRange: Range

    #
    # A data entry field that is preserved between a call hierarchy prepare and
    # incoming calls or outgoing calls requests.
    #
    data: NotRequired[Any]


# because "from"
CallHierarchyIncomingCall = TypedDict('CallHierarchyIncomingCall', {
    'from': CallHierarchyItem,
    'fromRange': list[Range]
})


class CallHierarchyIncomingCallsParams(WorkDoneProgressParams, PartialResultParams):
    item: CallHierarchyItem


class CallHierarchyOutgoingCall(MessageData):

    #
    # The item that is called.
    #
    to: CallHierarchyItem

    #
    # The range at which this item is called. This is the range relative to
    # the caller, e.g the item passed to `callHierarchy/outgoingCalls` request.
    #
    fromRanges: list[Range]


class CallHierarchyOutgoingCallsParams(WorkDoneProgressParams, PartialResultParams):
    item: CallHierarchyItem


class TypeHierarchyItem(MessageData):
    #
    # The name of this item.
    #
    name: str

    #
    # The kind of this item.
    #
    kind: SymbolKind

    #
    # Tags for this item.
    #
    tags: NotRequired[list[SymbolTag]]

    #
    # More detail for this item, e.g. the signature of a function.
    #
    detail: NotRequired[str]

    #
    # The resource identifier of this item.
    #
    uri: DocumentUri

    #
    # The range enclosing this symbol not including leading/trailing whitespace
    # but everything else, e.g. comments and code.
    #
    range: Range

    #
    # The range that should be selected and revealed when this symbol is being
    # picked, e.g. the name of a function. Must be contained by the
    # [`range`](#TypeHierarchyItem.range).
    #
    selectionRange: Range

    #
    # A data entry field that is preserved between a type hierarchy prepare and
    # supertypes or subtypes requests. It could also be used to identify the
    # type hierarchy in the server, helping improve the performance on
    # resolving supertypes and subtypes.
    #
    data: NotRequired[Any]


class TypeHierarchyPrepareParams(TextDocumentPositionParams, WorkDoneProgressParams):
    pass


class TypeHierarchySupertypesParams(WorkDoneProgressParams, PartialResultParams):
    item: TypeHierarchyItem


class TypeHierarchySubtypesParams(WorkDoneProgressParams, PartialResultParams):
    item: TypeHierarchyItem


class DocumentHighlightParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    pass


class DocumentHighlight(MessageData):
    #
    # The range this highlight applies to.
    #
    range: Range

    #
    # The highlight kind, default is DocumentHighlightKind.Text.
    #
    kind: NotRequired[DocumentHighlightKind]


class DocumentLinkParams(WorkDoneProgressParams, PartialResultParams):
    textDocument: TextDocumentIdentifier


class DocumentLink(MessageData):
    #
    # The range this link applies to.
    #
    range: Range

    #
    # The uri this link points to. If missing a resolve request is sent later.
    #
    target: NotRequired[URI]

    #
    # The tooltip text when you hover over this link.
    #
    # If a tooltip is provided, is will be displayed in a string that includes
    # instructions on how to trigger the link, such as `{0} (ctrl + click)`.
    # The specific instructions vary depending on OS, user settings, and
    # localization.
    #
    # @since 3.15.0
    #
    tooltip: NotRequired[str]

    #
    # A data entry field that is preserved on a document link between a
    # DocumentLinkRequest and a DocumentLinkResolveRequest.
    #
    data: NotRequired[Any]


class HoverParams(TextDocumentPositionParams, WorkDoneProgressParams):
    pass


class MarkedStringDict(MessageData):
    lanaguge: str
    value: str


MarkedString = str | MarkedStringDict


class MarkupContent(MessageData):
    #
    # The type of the Markup
    #
    kind: MarkupKind

    #
    # The content itself
    #
    value: str


class Hover(MessageData):
    #
    # The hover's content
    #
    contents: MarkedString | list[MarkedString] | MarkupContent

    #
    # An optional range is a range inside a text document
    # that is used to visualize a hover, e.g. by changing the background color.
    #
    range: NotRequired[Range]


class CodeLensParams(MessageData):
    textDocument: TextDocumentIdentifier


class Command(MessageData):
    #
    # Title of the command, like `save`.
    #
    title: str
    #
    # The identifier of the actual command handler.
    #
    command: str
    #
    # Arguments that the command handler should be
    # invoked with.
    #
    arguments: NotRequired[list[Any]]


class CodeLens(MessageData):
    #
    # The range in which this code lens is valid. Should only span a single
    # line.
    #
    range: Range

    #
    # The command this code lens represents.
    command: NotRequired[Command]

    #
    # A data entry field that is preserved on a code lens item between
    # a code lens and a code lens resolve request.
    #
    data: NotRequired[Any]


class FoldingRangeParams(WorkDoneProgressParams, PartialResultParams):
    textDocument: TextDocumentIdentifier


class FoldingRange(MessageData):

    #
    # The zero-based start line of the range to fold. The folded area starts
    # after the line's last character. To be valid, the end must be zero or
    # larger and smaller than the number of lines in the document.
    #
    startLine: int

    #
    # The zero-based character offset from where the folded range starts. If
    # not defined, defaults to the length of the start line.
    #
    startCharacter: NotRequired[int]

    #
    # The zero-based end line of the range to fold. The folded area ends with
    # the line's last character. To be valid, the end must be zero or larger
    # and smaller than the number of lines in the document.
    #
    endLine: int

    #
    # The zero-based character offset before the folded range ends. If not
    # defined, defaults to the length of the end line.
    #
    endCharacter: NotRequired[int]

    #
    # Describes the kind of the folding range such as `comment` or `region`.
    # The kind is used to categorize folding ranges and used by commands like
    # 'Fold all comments'. See [FoldingRangeKind](#FoldingRangeKind) for an
    # enumeration of standardized kinds.
    #
    kind: NotRequired[FoldingRangeKind]

    #
    # The text that the client should show when the specified range is
    # collapsed. If not defined or not supported by the client, a default
    # will be chosen by the client.
    #
    # @since 3.17.0 - proposed
    #
    collapsedText: NotRequired[str]


class SelectionRangeParams(WorkDoneProgressParams, PartialResultParams):

    #
    # The text document.
    #
    textDocument: TextDocumentIdentifier

    #
    # The positions inside the text document.
    #
    positions: list[Position]


class SelectionRange(MessageData):
    #
    # The [range](#Range) of this selection range.
    #
    range: Range
    #
    # The parent selection range containing this range. Therefore
    # `parent.range` must contain `this.range`.
    #
    parent: NotRequired[SelectionRange]


class DocumentSymbolParam(WorkDoneProgressParams, PartialResultParams):

    #
    # The text document.
    #
    textDocument: TextDocumentIdentifier


class DocumentSymbol(MessageData):
    #
    # The name of this symbol. Will be displayed in the user interface and
    # therefore must not be an empty str or a string only consisting of
    # white spaces.
    #
    name: str

    #
    # More detail for this symbol, e.g the signature of a function.
    #
    detail: NotRequired[str]

    #
    # The kind of this symbol.
    #
    kind: SymbolKind

    #
    # Tags for this document symbol.
    #
    # @since 3.16.0
    #
    tags: NotRequired[list[SymbolTag]]

    #
    # Indicates if this symbol is deprecated.
    #
    # @deprecated Use tags instead
    #
    deprecated: NotRequired[bool]

    #
    # The range enclosing this symbol not including leading/trailing whitespace
    # but everything else like comments. This information is typically used to
    # determine if the clients cursor is inside the symbol to reveal in the
    # symbol in the UI.
    #
    range: Range

    #
    # The range that should be selected and revealed when this symbol is being
    # picked, e.g. the name of a function. Must be contained by the `range`.
    #
    selectionRange: Range

    #
    # Children of this symbol, e.g. properties of a class.
    #
    children: NotRequired[list[DocumentSymbol]]


class SymbolInformation(MessageData):
    #
    # The name of this symbol.
    #
    name: str

    #
    # The kind of this symbol.
    #
    kind: SymbolKind

    #
    # Tags for this symbol.
    #
    # @since 3.16.0
    #
    tags: NotRequired[list[SymbolTag]]

    #
    # Indicates if this symbol is deprecated.
    #
    # @deprecated Use tags instead
    #
    deprecated: NotRequired[bool]

    #
    # The location of this symbol. The location's range is used by a tool
    # to reveal the location in the editor. If the symbol is selected in the
    # tool the range's start information is used to position the cursor. So
    # the range usually spans more then the actual symbol's name and does
    # normally include things like visibility modifiers.
    #
    # The range doesn't have to denote a node range in the sense of an abstract
    # syntax tree. It can therefore not be used to re-construct a hierarchy of
    # the symbols.
    #
    location: Location

    #
    # The name of the symbol containing this symbol. This information is for
    # user interface purposes (e.g. to render a qualifier in the user interface
    # if necessary). It can't be used to re-infer a hierarchy for the document
    # symbols.
    #
    containerName: NotRequired[str]


class SemanticTokensParams(WorkDoneProgressParams, PartialResultParams):
    #
    # The text document.
    #
    textDocument: TextDocumentIdentifier


class SemanticTokens(MessageData):
    #
    # An optional result id. If provided and clients support delta updating
    # the client will include the result id in the next semantic token request.
    # A server can then instead of computing all semantic tokens again simply
    # send a delta.
    #
    resultId: NotRequired[str]

    #
    # The actual tokens.
    #
    data: list[int]


class SemanticTokensDeltaParams(WorkDoneProgressParams, PartialResultParams):
    #
    # The text document.
    #
    textDocument: TextDocumentIdentifier

    #
    # The result id of a previous response. The result Id can either point to
    # a full response or a delta response depending on what was received last.
    #
    previousResultId: str


class SemanticTokensDelta(MessageData):
    resultId: NotRequired[str]
    #
    # The semantic token edits to transform a previous result into a new
    # result.
    #
    edits: list[SemanticTokensEdit]


class SemanticTokensEdit(MessageData):
    #
    # The start offset of the edit.
    #
    start: int

    #
    # The count of elements to remove.
    #
    deleteCount: int

    #
    # The elements to insert.
    #
    data: NotRequired[list[int]]


class SemanticTokensRangeParams(WorkDoneProgressParams, PartialResultParams):
    #
    # The text document.
    #
    textDocument: TextDocumentIdentifier

    #
    # The range the semantic tokens are requested for.
    #
    range: Range


class InlineValueContext(MessageData):
    #
    # The stack frame (as a DAP Id) where the execution has stopped.
    #
    frameId: int

    #
    # The document range where execution has stopped.
    # Typically the end position of the range denotes the line where the
    # inline values are shown.
    #
    stoppedLocation: Range


class InlineValueParams(WorkDoneProgressParams):
    #
    # The text document.
    #
    textDocument: TextDocumentIdentifier

    #
    # The document range for which inline values should be computed.
    #
    range: Range

    #
    # Additional information about the context in which inline values were
    # requested.
    #
    context: InlineValueContext


class InlineValueText(MessageData):
    #
    # The document range for which the inline value applies.
    #
    range: Range

    #
    # The text of the inline value.
    #
    text: str


class InlineValueVariableLookup(MessageData):
    #
    # The document range for which the inline value applies.
    # The range is used to extract the variable name from the underlying
    # document.
    #
    range: Range

    #
    # If specified the name of the variable to look up.
    #
    variableName: NotRequired[str]

    #
    # How to perform the lookup.
    #
    caseSensitiveLookup: bool


class InlineValueEvaluatableExpression(MessageData):
    #
    # The document range for which the inline value applies.
    # The range is used to extract the evaluatable expression from the
    # underlying document.
    #
    range: Range

    #
    # If specified the expression overrides the extracted expression.
    #
    expression: NotRequired[str]


#
# Inline value information can be provided by different means:
# - directly as a text value (class InlineValueText).
# - as a name to use for a variable lookup (class InlineValueVariableLookup)
# - as an evaluatable expression (class InlineValueEvaluatableExpression)
# The InlineValue types combines all inline value types into one type.
#
# @since 3.17.0
#

InlineValue = InlineValueText | InlineValueVariableLookup | InlineValueEvaluatableExpression


class InlayHintParams(WorkDoneProgressParams):
    #
    # The text document.
    #
    textDocument: TextDocumentIdentifier

    #
    # The visible document range for which inlay hints should be computed.
    #
    range: Range


class InlayHintLabelPart(MessageData):

    #
    # The value of this label part.
    #
    value: str

    #
    # The tooltip text when you hover over this label part. Depending on
    # the client capability `inlayHint.resolveSupport` clients might resolve
    # this property late using the resolve request.
    #
    tooltip: NotRequired[str | MarkupContent]

    #
    # An optional source code location that represents this
    # label part.
    #
    # The editor will use this location for the hover and for code navigation
    # features: This part will become a clickable link that resolves to the
    # definition of the symbol at the given location (not necessarily the
    # location itself), it shows the hover that shows at the given location,
    # and it shows a context menu with further code navigation commands.
    #
    # Depending on the client capability `inlayHint.resolveSupport` clients
    # might resolve this property late using the resolve request.
    #
    location: NotRequired[Location]

    #
    # An optional command for this label part.
    #
    # Depending on the client capability `inlayHint.resolveSupport` clients
    # might resolve this property late using the resolve request.
    #
    command: NotRequired[Command]


InlayHintKind = Literal[
    #
    # An inlay hint that for a type annotation.
    #
    1,  # Type=

    #
    # An inlay hint that is for a parameter.
    #
    2,  # Parameter
]


class InlayHint(MessageData):

    #
    # The position of this hint.
    #
    position: Position

    #
    # The label of this hint. A human readable string or an array of
    # InlayHintLabelPart label parts.
    #
    # *Note* that neither the string nor the label part can be empty.
    #
    label: str | list[InlayHintLabelPart]

    #
    # The kind of this hint. Can be omitted in which case the client
    # should fall back to a reasonable default.
    #
    kind: NotRequired[InlayHintKind]

    #
    # Optional text edits that are performed when accepting this inlay hint.
    #
    # *Note* that edits are expected to change the document so that the inlay
    # hint (or its nearest variant) is now part of the document and the inlay
    # hint itself is now obsolete.
    #
    # Depending on the client capability `inlayHint.resolveSupport` clients
    # might resolve this property late using the resolve request.
    #
    textEdits: NotRequired[list[TextEdit]]

    #
    # The tooltip text when you hover over this item.
    #
    # Depending on the client capability `inlayHint.resolveSupport` clients
    # might resolve this property late using the resolve request.
    #
    tooltip: NotRequired[str | MarkupContent]

    #
    # Render padding before the hint.
    #
    # Note: Padding should use the editor's background color, not the
    # background color of the hint itself. That means padding can be used
    # to visually align/separate an inlay hint.
    #
    paddingLeft: NotRequired[bool]

    #
    # Render padding after the hint.
    #
    # Note: Padding should use the editor's background color, not the
    # background color of the hint itself. That means padding can be used
    # to visually align/separate an inlay hint.
    #
    paddingRight: NotRequired[bool]

    #
    # A data entry field that is preserved on an inlay hint between
    # a `textDocument/inlayHint` and a `inlayHint/resolve` request.
    #
    data: NotRequired[Any]


class MonikerParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    pass


class Moniker(MessageData):
    #
    # The scheme of the moniker. For example tsc or .Net
    #
    scheme: str

    #
    # The identifier of the moniker. The value is opaque in LSIF however
    # schema owners are allowed to define the structure if they want.
    #
    identifier: str

    #
    # The scope in which the moniker is unique
    #
    unique: UniquenessLevel

    #
    # The moniker kind if known.
    #
    kind: NotRequired[MonikerKind]


CompletionTriggerKind = Literal[
    # Completion was triggered by typing an identifier (24x7 code
    # complete), manual invocation (e.g Ctrl+Space) or via API.
    #
    1,  # Invoked

    #
    # Completion was triggered by a trigger character specified by
    # the `triggerCharacters` properties of the
    # `CompletionRegistrationOptions`.
    #
    2,  # TriggerCharacter

    #
    # Completion was re-triggered as the current completion list is incomplete.
    #
    3,  # TriggerForIncompleteCompletions;
]


class CompletionContext(MessageData):
    #
    # How the completion was triggered.
    #
    triggerKind: CompletionTriggerKind

    #
    # The trigger character (a single character) that has trigger code
    # complete. Is undefined if
    # `triggerKind !== CompletionTriggerKind.TriggerCharacter`
    #
    triggerCharacter: NotRequired[str]


class CompletionParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    #
    # The completion context. This is only available if the client specifies
    # to send this using the client capability
    # `completion.contextSupport === true`
    #
    context: NotRequired[CompletionContext]


class CompletionListItemDefaultsEditRange(MessageData):
    insert: Range
    replace: Range


InsertTextFormat = Literal[
    1,  # PlainText
    #
    # The primary text to be inserted is treated as a snippet.
    #
    # A snippet can define tab stops and placeholders with `$1`, `$2`
    # and `${3:foo}`. `$0` defines the final tab stop, it defaults to
    # the end of the snippet. Placeholders with equal identifiers are linked,
    # that is typing in one will update others too.
    #
    2,  # Snippet
]


class CompletionListItemDefaults(MessageData):
    #
    # A default commit character set.
    #
    # @since 3.17.0
    #
    commitCharacters: NotRequired[list[str]]

    #
    # A default edit range
    #
    # @since 3.17.0
    #
    editRange: NotRequired[Range | CompletionListItemDefaultsEditRange]

    #
    # A default insert text format
    #
    # @since 3.17.0
    #
    insertTextFormat: NotRequired[InsertTextFormat]

    #
    # A default insert text mode
    #
    # @since 3.17.0
    #
    insertTextMode: NotRequired[InsertTextMode]

    #
    # A default data value.
    #
    # @since 3.17.0
    #
    data: NotRequired[Any]


class CompletionItemLabelDetails(MessageData):

    #
    # An optional string which is rendered less prominently directly after
    # {@link CompletionItem.label label}, without any spacing. Should be
    # used for function signatures or type annotations.
    #
    detail: NotRequired[str]

    #
    # An optional string which is rendered less prominently after
    # {@link CompletionItemLabelDetails.detail}. Should be used for fully qualified
    # names or file path.
    #
    description: NotRequired[str]


CompletionItemKind = Literal[1,  # Text
                             2,  # Method
                             3,  # Function
                             4,  # Constructor
                             5,  # Field
                             6,  # Variable
                             7,  # Class
                             8,  # Interface
                             9,  # Module
                             10,  # Property
                             11,  # Unit
                             12,  # Value
                             13,  # Enum
                             14,  # Keyword
                             15,  # Snippet
                             16,  # Color
                             17,  # File
                             18,  # Reference
                             19,  # Folder
                             20,  # EnumMember
                             21,  # Constant
                             22,  # Struct
                             23,  # Event
                             24,  # Operator
                             25,  # TypeParameter
                             ]

CompletionItemTag = Literal[1,  # Deprecated
                            ]


class InsertReplaceEdit(MessageData):
    #
    # The string to be inserted.
    #
    newText: str

    #
    # The range if the insert is requested
    #
    insert: Range

    #
    # The range if the replace is requested.
    #
    replace: Range


class CompletionItem(MessageData):

    #
    # The label of this completion item.
    #
    # The label property is also by default the text that
    # is inserted when selecting this completion.
    #
    # If label details are provided the label itself should
    # be an unqualified name of the completion item.
    #
    label: str

    #
    # Additional details for the label
    #
    # @since 3.17.0
    #
    labelDetails: NotRequired[CompletionItemLabelDetails]

    #
    # The kind of this completion item. Based of the kind
    # an icon is chosen by the editor. The standardized set
    # of available values is defined in `CompletionItemKind`.
    #
    kind: NotRequired[CompletionItemKind]

    #
    # Tags for this completion item.
    #
    # @since 3.15.0
    #
    tags: NotRequired[list[CompletionItemTag]]

    #
    # A human-readable str with additional information
    # about this item, like type or symbol information.
    #
    detail: NotRequired[str]

    #
    # A human-readable str that represents a doc-comment.
    #
    documentation: NotRequired[str | MarkupContent]

    #
    # Indicates if this item is deprecated.
    #
    # @deprecated Use `tags` instead if supported.
    #
    deprecated: NotRequired[bool]

    #
    # Select this item when showing.
    #
    # *Note* that only one completion item can be selected and that the
    # tool / client decides which item that is. The rule is that the *first*
    # item of those that match best is selected.
    #
    preselect: NotRequired[bool]

    #
    # A str that should be used when comparing this item
    # with other items. When omitted the label is used
    # as the sort text for this item.
    #
    sortText: NotRequired[str]

    #
    # A str that should be used when filtering a set of
    # completion items. When omitted the label is used as the
    # filter text for this item.
    #
    filterText: NotRequired[str]

    #
    # A str that should be inserted into a document when selecting
    # this completion. When omitted the label is used as the insert text
    # for this item.
    #
    # The `insertText` is subject to interpretation by the client side.
    # Some tools might not take the str literally. For example
    # VS Code when code complete is requested in this example
    # `con<cursor position>` and a completion item with an `insertText` of
    # `console` is provided it will only insert `sole`. Therefore it is
    # recommended to use `textEdit` instead since it avoids additional client
    # side interpretation.
    #
    insertText: NotRequired[str]

    #
    # The format of the insert text. The format applies to both the
    # `insertText` property and the `newText` property of a provided
    # `textEdit`. If omitted defaults to `InsertTextFormat.PlainText`.
    #
    # Please note that the insertTextFormat doesn't apply to
    # `additionalTextEdits`.
    #
    insertTextFormat: NotRequired[InsertTextFormat]

    #
    # How whitespace and indentation is handled during completion
    # item insertion. If not provided the client's default value depends on
    # the `textDocument.completion.insertTextMode` client capability.
    #
    # @since 3.16.0
    # @since 3.17.0 - support for `textDocument.completion.insertTextMode`
    #
    insertTextMode: NotRequired[InsertTextMode]

    #
    # An edit which is applied to a document when selecting this completion.
    # When an edit is provided the value of `insertText` is ignored.
    #
    # *Note:* The range of the edit must be a single line range and it must
    # contain the position at which completion has been requested.
    #
    # Most editors support two different operations when accepting a completion
    # item. One is to insert a completion text and the other is to replace an
    # existing text with a completion text. Since this can usually not be
    # predetermined by a server it can report both ranges. Clients need to
    # signal support for `InsertReplaceEdit`s via the
    # `textDocument.completion.completionItem.insertReplaceSupport` client
    # capability property.
    #
    # *Note 1:* The text edit's range as well as both ranges from an insert
    # replace edit must be a [single line] and they must contain the position
    # at which completion has been requested.
    # *Note 2:* If an `InsertReplaceEdit` is returned the edit's insert range
    # must be a prefix of the edit's replace range, that means it must be
    # contained and starting at the same position.
    #
    # @since 3.16.0 additional type `InsertReplaceEdit`
    #
    textEdit: NotRequired[TextEdit | InsertReplaceEdit]

    #
    # The edit text used if the completion item is part of a CompletionList and
    # CompletionList defines an item default for the text edit range.
    #
    # Clients will only honor this property if they opt into completion list
    # item defaults using the capability `completionList.itemDefaults`.
    #
    # If not provided and a list's default range is provided the label
    # property is used as a text.
    #
    # @since 3.17.0
    #
    textEditText: NotRequired[str]

    #
    # An optional array of additional text edits that are applied when
    # selecting this completion. Edits must not overlap (including the same
    # insert position) with the main edit nor with themselves.
    #
    # Additional text edits should be used to change text unrelated to the
    # current cursor position (for example adding an import statement at the
    # top of the file if the completion item will insert an unqualified type).
    #
    additionalTextEdits: NotRequired[list[TextEdit]]

    #
    # An optional set of characters that when pressed while this completion is
    # active will accept it first and then type that character. *Note* that all
    # commit characters should have `length=1` and that superfluous characters
    # will be ignored.
    #
    commitCharacters: NotRequired[list[str]]

    #
    # An optional command that is executed *after* inserting this completion.
    # *Note* that additional modifications to the current document should be
    # described with the additionalTextEdits-property.
    #
    command: NotRequired[Command]

    #
    # A data entry field that is preserved on a completion item between
    # a completion and a completion resolve request.
    #
    data: NotRequired[Any]


class CompletionList(MessageData):
    #
    # This list is not complete. Further typing should result in recomputing
    # this list.
    #
    # Recomputed lists have all their items replaced (not appended) in the
    # incomplete completion sessions.
    #
    isIncomplete: bool

    #
    # In many cases the items of an actual completion result share the same
    # value for properties like `commitCharacters` or the range of a text
    # edit. A completion list can therefore define item defaults which will
    # be used if a completion item itself doesn't specify the value.
    #
    # If a completion list specifies a default value and a completion item
    # also specifies a corresponding value the one from the item is used.
    #
    # Servers are only allowed to return default values if the client
    # signals support for this via the `completionList.itemDefaults`
    # capability.
    #
    # @since 3.17.0
    #
    itemDefaults: NotRequired[CompletionListItemDefaults]

    #
    # The completion items.
    #
    items: list[CompletionItem]


class ParameterInformation(MessageData):

    #
    # The label of this parameter information.
    #
    # Either a string or an inclusive start and exclusive end offsets within
    # its containing signature label. (see SignatureInformation.label). The
    # offsets are based on a UTF-16 string representation as `Position` and
    # `Range` does.
    #
    # *Note*: a label of type string should be a substring of its containing
    # signature label. Its intended use case is to highlight the parameter
    # label part in the `SignatureInformation.label`.
    #
    label: str | tuple[int, int]

    #
    # The human-readable doc-comment of this parameter. Will be shown
    # in the UI but can be omitted.
    #
    documentation: NotRequired[str | MarkupContent]


class SignatureInformation(MessageData):
    #
    # The label of this signature. Will be shown in
    # the UI.
    #
    label: str

    #
    # The human-readable doc-comment of this signature. Will be shown
    # in the UI but can be omitted.
    #
    documentation: NotRequired[str | MarkupContent]

    #
    # The parameters of this signature.
    #
    parameters: NotRequired[list[ParameterInformation]]

    #
    # The index of the active parameter.
    #
    # If provided, this is used in place of `SignatureHelp.activeParameter`.
    #
    # @since 3.16.0
    #
    activeParameter: NotRequired[int]


class SignatureHelp(MessageData):
    #
    # One or more signatures. If no signatures are available the signature help
    # request should return `null`.
    #
    signatures: list[SignatureInformation]

    #
    # The active signature. If omitted or the value lies outside the
    # range of `signatures` the value defaults to zero or is ignore if
    # the `SignatureHelp` as no signatures.
    #
    # Whenever possible implementors should make an active decision about
    # the active signature and shouldn't rely on a default value.
    #
    # In future version of the protocol this property might become
    # mandatory to better express this.
    #
    activeSignature: NotRequired[int]

    #
    # The active parameter of the active signature. If omitted or the value
    # lies outside the range of `signatures[activeSignature].parameters`
    # defaults to 0 if the active signature has parameters. If
    # the active signature has no parameters it is ignored.
    # In future version of the protocol this property might become
    # mandatory to better express the active parameter if the
    # active signature does have any.
    #
    activeParameter: NotRequired[int]


SignatureHelpTriggerKind = Literal[
    #
    # Signature help was invoked manually by the user or by a command.
    #
    1,  # Invoked
    #
    # Signature help was triggered by a trigger character.
    #
    2,  # TriggerCharacter
    #
    # Signature help was triggered by the cursor moving or by the document
    # content changing.
    #
    3,  # ContentChange=
]


class SignatureHelpContext(MessageData):
    #
    # Action that caused signature help to be triggered.
    #
    triggerKind: SignatureHelpTriggerKind

    #
    # Character that caused signature help to be triggered.
    #
    # This is undefined when triggerKind !==
    # SignatureHelpTriggerKind.TriggerCharacter
    #
    triggerCharacter: NotRequired[str]

    #
    # `true` if signature help was already showing when it was triggered.
    #
    # Retriggers occur when the signature help is already active and can be
    # caused by actions such as typing a trigger character, a cursor move, or
    # document content changes.
    #
    isRetrigger: bool

    #
    # The currently active `SignatureHelp`.
    #
    # The `activeSignatureHelp` has its `SignatureHelp.activeSignature` field
    # updated based on the user navigating through available signatures.
    #
    activeSignatureHelp: NotRequired[SignatureHelp]


class SignatureHelpParams(TextDocumentPositionParams, WorkDoneProgressParams):
    #
    # The signature help context. This is only available if the client
    # specifies to send this using the client capability
    # `textDocument.signatureHelp.contextSupport === true`
    #
    # @since 3.15.0
    #
    context: NotRequired[SignatureHelpContext]


DiagnosticSeverity = Literal[  #
    # Reports an error.
    #
    1,  # Error
    #
    # Reports a warning.
    #
    2,  # Warning
    #
    # Reports an information.
    #
    3,  # Information
    #
    # Reports a hint.
    #
    4,  # Hint
]


class CodeDescription(MessageData):
    #
    # An URI to open with more information about the diagnostic error.
    #
    href: URI


DiagnosticTag = Literal[  #
    # Unused or unnecessary code.
    #
    # Clients are allowed to render diagnostics with this tag faded out
    # instead of having an error squiggle.
    #
    1,  # Unnecessary
    #
    # Deprecated or obsolete code.
    #
    # Clients are allowed to rendered diagnostics with this tag strike through.
    #
    2,  # Deprecated
]


class DiagnosticRelatedInformation(MessageData):
    #
    # The location of this related diagnostic information.
    #
    location: Location

    #
    # The message of this related diagnostic information.
    #
    message: str


class Diagnostic(MessageData):
    #
    # The range at which the message applies.
    #
    range: Range

    #
    # The diagnostic's severity. Can be omitted. If omitted it is up to the
    # client to interpret diagnostics as error, warning, info or hint.
    #
    severity: NotRequired[DiagnosticSeverity]

    #
    # The diagnostic's code, which might appear in the user interface.
    #
    code: NotRequired[int | str]

    #
    # An optional property to describe the error code.
    #
    # @since 3.16.0
    #
    codeDescription: NotRequired[CodeDescription]

    #
    # A human-readable string describing the source of this
    # diagnostic, e.g. 'typescript' or 'super lint'.
    #
    source: NotRequired[str]

    #
    # The diagnostic's message.
    #
    message: str

    #
    # Additional metadata about the diagnostic.
    #
    # @since 3.15.0
    #
    tags: NotRequired[list[DiagnosticTag]]

    #
    # An array of related diagnostic information, e.g. when symbol-names within
    # a scope collide all definitions can be marked via this property.
    #
    relatedInformation: NotRequired[list[DiagnosticRelatedInformation]]

    #
    # A data entry field that is preserved between a
    # `textDocument/publishDiagnostics` notification and
    # `textDocument/codeAction` request.
    #
    # @since 3.16.0
    #
    data: NotRequired[Any]


class CodeActionContext(MessageData):
    #
    # An array of diagnostics known on the client side overlapping the range
    # provided to the `textDocument/codeAction` request. They are provided so
    # that the server knows which errors are currently presented to the user
    # for the given range. There is no guarantee that these accurately reflect
    # the error state of the resource. The primary parameter
    # to compute code actions is the provided range.
    #
    diagnostics: list[Diagnostic]

    #
    # Requested kind of actions to return.
    #
    # Actions not of this kind are filtered out by the client before being
    # shown. So servers can omit computing them.
    #
    only: NotRequired[list[CodeActionKind]]

    #
    # The reason why code actions were requested.
    #
    # @since 3.17.0
    #
    triggerKind: NotRequired[CodeActionTriggerKind]


class CodeActionParams(WorkDoneProgressParams, PartialResultParams):
    #
    # The document in which the command was invoked.
    #
    textDocument: TextDocumentIdentifier

    #
    # The range for which the command was invoked.
    #
    range: Range

    #
    # Context carrying additional information.
    #
    context: CodeActionContext


class Color(MessageData):

    #
    # The red component of this color in the range [0-1].
    #
    red: int

    #
    # The green component of this color in the range [0-1].
    #
    green: int

    #
    # The blue component of this color in the range [0-1].
    #
    blue: int

    #
    # The alpha component of this color in the range [0-1].
    #
    alpha: int


class DocumentColorParams(WorkDoneProgressParams, PartialResultParams):
    #
    # The text document.
    #
    textDocument: TextDocumentIdentifier

    # The range in the document where this color appears.
    #
    range: Range

    #
    # The actual color value for this color range.
    #
    color: Color


class ColorInformation(MessageData):
    #
    # The range in the document where this color appears.
    #
    range: Range

    #
    # The actual color value for this color range.
    #
    color: Color


class FormattingOptions(MessageData):
    #
    # Size of a tab in spaces.
    #
    tabSize: int

    #
    # Prefer spaces over tabs.
    #
    insertSpaces: bool

    #
    # Trim trailing whitespace on a line.
    #
    # @since 3.15.0
    #
    trimTrailingWhitespace: NotRequired[bool]

    #
    # Insert a newline character at the end of the file if one does not exist.
    #
    # @since 3.15.0
    #
    insertFinalNewline: NotRequired[bool]

    #
    # Trim all newlines after the final newline at the end of the file.
    #
    # @since 3.15.0
    #
    trimFinalNewlines: NotRequired[bool]

    #
    # Signature for further properties.

    # [key: string]: boolean | integer | string


class DocumentFormattingParams(WorkDoneProgressParams):
    #
    # The document to format.
    #
    textDocument: TextDocumentIdentifier

    #
    # The format options.
    #
    options: FormattingOptions


class ExecuteCommandParams(WorkDoneProgressParams):

    #
    # The identifier of the actual command handler.
    #
    command: str
    #
    # Arguments that the command should be invoked with.
    #
    arguments: NotRequired[list[Any]]


ChangeAnnotationIdentifier = str


class ChangeAnnotation(MessageData):
    #
    # A human-readable string describing the actual change. The string
    # is rendered prominent in the user interface.
    #
    label: str

    #
    # A flag which indicates that user confirmation is needed
    # before applying the change.
    #
    needsConfirmation: NotRequired[bool]

    #
    # A human-readable string which is rendered less prominent in
    # the user interface.
    #
    description: NotRequired[str]


class OptionalVersionedTextDocumentIdentifier(TextDocumentIdentifier):
    #
    # The version number of this document. If an optional versioned text document
    # identifier is sent from the server to the client and the file is not
    # open in the editor (the server has not received an open notification
    # before) the server can send `null` to indicate that the version is
    # known and the content on disk is the master (as specified with document
    # content ownership).
    #
    # The version number of a document will increase after each change,
    # including undo/redo. The number doesn't need to be consecutive.
    #
    version: int | None


class AnnotatedTextEdit(TextEdit):
    #
    # The actual annotation identifier.
    #
    annotationId: ChangeAnnotationIdentifier


class TextDocumentEdit(MessageData):
    #
    # The text document to change.
    #
    textDocument: OptionalVersionedTextDocumentIdentifier

    #
    # The edits to be applied.
    #
    # @since 3.16.0 - support for AnnotatedTextEdit. This is guarded by the
    # client capability `workspace.workspaceEdit.changeAnnotationSupport`
    #
    edits: list[TextEdit | AnnotatedTextEdit]


class CreateFileOptions(MessageData):
    #
    # Overwrite existing file. Overwrite wins over `ignoreIfExists`
    #
    overwrite: NotRequired[bool]

    #
    # Ignore if exists.
    #
    ignoreIfExists: NotRequired[bool]


class CreateFile(MessageData):
    #
    # A create
    #
    kind: Literal['create']

    #
    # The resource to create.
    #
    uri: DocumentUri

    #
    # Additional options
    #
    options: NotRequired[CreateFileOptions]

    #
    # An optional annotation identifier describing the operation.
    #
    # @since 3.16.0
    #
    annotationId: NotRequired[ChangeAnnotationIdentifier]


class RenameFileOptions(MessageData):
    #
    # Overwrite target if existing. Overwrite wins over `ignoreIfExists`
    #
    overwrite: NotRequired[bool]

    #
    # Ignores if target exists.
    #
    ignoreIfExists: NotRequired[bool]


class RenameFile(MessageData):
    #
    # A rename
    #
    kind: Literal['rename']

    #
    # The old (existing) location.
    #
    oldUri: DocumentUri

    #
    # The new location.
    #
    newUri: DocumentUri

    #
    # Rename options.
    #
    options: NotRequired[RenameFileOptions]

    #
    # An optional annotation identifier describing the operation.
    #
    # @since 3.16.0
    #
    annotationId: NotRequired[ChangeAnnotationIdentifier]


class DeleteFileOptions(MessageData):
    #
    # Delete the content recursively if a folder is denoted.
    #
    recursive: NotRequired[bool]

    #
    # Ignore the operation if the file doesn't exist.
    #
    ignoreIfNotExists: NotRequired[bool]


class DeleteFile(MessageData):
    #
    # A delete
    #
    kind: Literal['delete']

    #
    # The file to delete.
    #
    uri: DocumentUri

    #
    # Delete options.
    #
    options: NotRequired[DeleteFileOptions]

    #
    # An optional annotation identifier describing the operation.
    #
    # @since 3.16.0
    #
    annotationId: NotRequired[ChangeAnnotationIdentifier]


class WorkspaceEdit(MessageData):
    #
    # Holds changes to existing resources.
    #
    changes: NotRequired[dict[DocumentUri, list[TextEdit]]]

    #
    # Depending on the client capability
    # `workspace.workspaceEdit.resourceOperations` document changes are either
    # an array of `TextDocumentEdit`s to express changes to n different text
    # documents where each text document edit addresses a specific version of
    # a text document. Or it can contain above `TextDocumentEdit`s mixed with
    # create, rename and delete file / folder operations.
    #
    # Whether a client supports versioned document edits is expressed via
    # `workspace.workspaceEdit.documentChanges` client capability.
    #
    # If a client neither supports `documentChanges` nor
    # `workspace.workspaceEdit.resourceOperations` then only plain `TextEdit`s
    # using the `changes` property are supported.
    #
    documentChanges: NotRequired[(list[TextDocumentEdit]
                                  | list[(TextDocumentEdit | CreateFile | RenameFile | DeleteFile)])]

    #
    # A map of change annotations that can be referenced in
    # `AnnotatedTextEdit`s or create, rename and delete file / folder
    # operations.
    #
    # Whether clients honor this property depends on the client capability
    # `workspace.changeAnnotationSupport`.
    #
    # @since 3.16.0
    #
    changeAnnotations: NotRequired[dict[ChangeAnnotationIdentifier, ChangeAnnotation]]


class CodeActionDisabled(MessageData):

    #
    # Human readable description of why the code action is currently
    # disabled.
    #
    # This is displayed in the code actions UI.
    #
    reason: str


class CodeAction(MessageData):

    #
    # A short, human-readable, title for this code action.
    #
    title: str

    #
    # The kind of the code action.
    #
    # Used to filter code actions.
    #
    kind: NotRequired[CodeActionKind]

    #
    # The diagnostics that this code action resolves.
    #
    diagnostics: NotRequired[list[Diagnostic]]

    #
    # Marks this as a preferred action. Preferred actions are used by the
    # `auto fix` command and can be targeted by keybindings.
    #
    # A quick fix should be marked preferred if it properly addresses the
    # underlying error. A refactoring should be marked preferred if it is the
    # most reasonable choice of actions to take.
    #
    # @since 3.15.0
    #
    isPreferred: NotRequired[bool]

    #
    # Marks that the code action cannot currently be applied.
    #
    # Clients should follow the following guidelines regarding disabled code
    # actions:
    #
    # - Disabled code actions are not shown in automatic lightbulbs code
    #   action menus.
    #
    # - Disabled actions are shown as faded out in the code action menu when
    #   the user request a more specific type of code action, such as
    #   refactorings.
    #
    # - If the user has a keybinding that auto applies a code action and only
    #   a disabled code actions are returned, the client should show the user
    #   an error message with `reason` in the editor.
    #
    # @since 3.16.0
    #
    disabled: NotRequired[CodeActionDisabled]

    #
    # The workspace edit this code action performs.
    #
    edit: NotRequired[WorkspaceEdit]

    #
    # A command this code action executes. If a code action
    # provides an edit and a command, first the edit is
    # executed and then the command.
    #
    command: NotRequired[Command]

    #
    # A data entry field that is preserved on a code action between
    # a `textDocument/codeAction` and a `codeAction/resolve` request.
    #
    # @since 3.16.0
    #
    data: NotRequired[Any]


class ColorPresentationParams(WorkDoneProgressParams, PartialResultParams):
    #
    # The text document.
    #
    textDocument: TextDocumentIdentifier

    #
    # The color information to request presentations for.
    #
    color: Color

    #
    # The range where the color would be inserted. Serves as a context.
    #
    range: Range


class ColorPresentation(MessageData):
    # The label of this color presentation. It will be shown on the color
    # picker header. By default this is also the text that is inserted when
    # selecting this color presentation.
    #
    label: str
    #
    # An [edit](#TextEdit) which is applied to a document when selecting
    # this presentation for the color. When omitted the
    # [label](#ColorPresentation.label) is used.
    #
    textEdit: NotRequired[TextEdit]
    #
    # An optional array of additional [text edits](#TextEdit) that are applied
    # when selecting this color presentation. Edits must not overlap with the
    # main [edit](#ColorPresentation.textEdit) nor with themselves.
    #
    additionalTextEdits: NotRequired[list[TextEdit]]


class DocumentRangeFormattingParams(WorkDoneProgressParams):
    #
    # The document to format.
    #
    textDocument: TextDocumentIdentifier

    #
    # The range to format
    #
    range: Range

    #
    # The format options
    #
    options: FormattingOptions


class DocumentOnTypeFormattingParams(MessageData):

    #
    # The document to format.
    #
    textDocument: TextDocumentIdentifier

    #
    # The position around which the on type formatting should happen.
    # This is not necessarily the exact position where the character denoted
    # by the property `ch` got typed.
    #
    position: Position

    #
    # The character that has been typed that triggered the formatting
    # on type request. That is not necessarily the last character that
    # got inserted into the document since the client could auto insert
    # characters as well (e.g. like automatic brace completion).
    #
    ch: str

    #
    # The formatting options.
    #
    options: FormattingOptions


class RenameParams(TextDocumentPositionParams, WorkDoneProgressParams):
    #
    # The new name of the symbol. If the given name is not valid the
    # request must return a [ResponseError](#ResponseError) with an
    # appropriate message set.
    #
    newName: str


class PrepareRenameParams(TextDocumentPositionParams, WorkDoneProgressParams):
    pass


class PrepareRenameResponsePlaceholder(MessageData):
    range: Range
    placeholder: str


class DefaultBehavior(MessageData):
    defaultBehavior: bool


PrepareRenameResponse = Range | PrepareRenameResponsePlaceholder | DefaultBehavior | None


class LinkedEditingRangeParams(TextDocumentPositionParams, WorkDoneProgressParams):
    pass


class LinkedEditingRanges(MessageData):
    #
    # A list of ranges that can be renamed together. The ranges must have
    # identical length and contain identical text content. The ranges cannot
    # overlap.
    #
    ranges: list[Range]

    #
    # An optional word pattern (regular expression) that describes valid
    # contents for the given ranges. If no pattern is provided, the client
    # configuration's word pattern will be used.
    #
    wordPattern: NotRequired[str]


class WorkspaceSymbolParams(WorkDoneProgressParams, PartialResultParams):
    #
    # A query string to filter symbols by. Clients may send an empty
    # string here to request all symbols.
    #
    query: str


class WorkspaceSymbol(MessageData):
    #
    # The name of this symbol.
    #
    name: str

    #
    # The kind of this symbol.
    #
    kind: SymbolKind

    #
    # Tags for this completion item.
    #
    tags: NotRequired[list[SymbolTag]]

    #
    # The name of the symbol containing this symbol. This information is for
    # user interface purposes (e.g. to render a qualifier in the user interface
    # if necessary). It can't be used to re-infer a hierarchy for the document
    # symbols.
    #
    containerName: NotRequired[str]

    #
    # The location of this symbol. Whether a server is allowed to
    # return a location without a range depends on the client
    # capability `workspace.symbol.resolveSupport`.
    #
    # See also `SymbolInformation.location`.
    #
    location: Location | dict[str, DocumentUri]

    #
    # A data entry field that is preserved on a workspace symbol between a
    # workspace symbol request and a workspace symbol resolve request.
    #
    data: NotRequired[Any]


class DidChangeConfigurationParams(MessageData):
    #
    # The actual changed settings
    #
    settings: Any


class WorkspaceFoldersChangeEvent(MessageData):
    #
    # The array of added workspace folders
    #
    added: list[WorkspaceFolder]

    #
    # The array of the removed workspace folders
    #
    removed: list[WorkspaceFolder]


class DidChangeWorkspaceFoldersParams(MessageData):
    #
    # The actual workspace folder change event.
    #
    event: WorkspaceFoldersChangeEvent


class FileCreate(MessageData):

    #
    # A file:// URI for the location of the file/folder being created.
    #
    uri: str


class CreateFilesParams(MessageData):

    #
    # An array of all files/folders created in this operation.
    #
    files: list[FileCreate]


class FileRename(MessageData):

    #
    # A file:// URI for the original location of the file/folder being renamed.
    #
    oldUri: str

    #
    # A file:// URI for the new location of the file/folder being renamed.
    #
    newUri: str


class RenameFilesParams(MessageData):

    #
    # An array of all files/folders renamed in this operation. When a folder
    # is renamed, only the folder will be included, and not its children.
    #
    files: list[FileRename]


class FileDelete(MessageData):

    #
    # A file:// URI for the location of the file/folder being deleted.
    #
    uri: str


class DeleteFilesParams(MessageData):

    #
    # An array of all files/folders deleted in this operation.
    #
    files: list[FileDelete]


class DidChangeWatchedFilesParams(MessageData):
    #
    # The actual file events.
    #
    changes: list[FileEvent]


FileChangeType = Literal[1, 2, 3]


class FileEvent(MessageData):
    #
    # The file's URI.
    #
    uri: DocumentUri
    #
    # The change type.
    #
    type: FileChangeType
