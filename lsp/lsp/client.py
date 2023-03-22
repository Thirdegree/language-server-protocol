from typing import Any, Literal, NotRequired, TypedDict

from lsp.lsp.common import (CodeActionKind, EmptyDict, FailureHandlingKind, FoldingRangeKind, InsertTextMode,
                            MarkupKind, PositionEncodingKind, ResourceOperationKind, SymbolKind, SymbolTag, TokenFormat)


class ClientWorkspaceCapabilitiesFileOptions(TypedDict):
    #
    # Whether the client supports dynamic registration for file
    # requests/notifications.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # The client has support for sending didCreateFiles notifications.
    #
    didCreate: NotRequired[bool]

    #
    # The client has support for sending willCreateFiles requests.
    #
    willCreate: NotRequired[bool]

    #
    # The client has support for sending didRenameFiles notifications.
    #
    didRename: NotRequired[bool]

    #
    # The client has support for sending willRenameFiles requests.
    #
    willRename: NotRequired[bool]

    #
    # The client has support for sending didDeleteFiles notifications.
    #
    didDelete: NotRequired[bool]

    #
    # The client has support for sending willDeleteFiles requests.
    #
    willDelete: NotRequired[bool]


class WorkspaceEditClientCapabilitiesChangeAnnotationSupport(TypedDict):
    #
    # Whether the client groups edits with equal labels into tree nodes,
    # for instance all edits labelled with "Changes in Strings" would
    # be a tree node.
    #
    groupsOnLabel: NotRequired[bool]


class WorkspaceEditClientCapabilities(TypedDict):
    #
    # The client supports versioned document changes in `WorkspaceEdit`s
    #
    documentChanges: NotRequired[bool]

    #
    # The resource operations the client supports. Clients should at least
    # support 'create', 'rename' and 'delete' files and folders.
    # @since 3.13.0
    #
    resourceOperations: NotRequired[list[ResourceOperationKind]]

    #
    # The failure handling strategy of a client if applying the workspace edit
    # fails.
    # @since 3.13.0
    #
    failureHandling: NotRequired[FailureHandlingKind]

    #
    # Whether the client normalizes line endings to the client specific
    # setting.
    # If set to `true` the client will normalize line ending characters
    # in a workspace edit to the client specific new line character(s).
    # @since 3.16.0
    #
    normalizesLineEndings: NotRequired[bool]

    #
    # Whether the client in general supports change annotations on text edits,
    # create file, rename file and delete file changes.
    # @since 3.16.0
    #
    changeAnnotationSupport: NotRequired[WorkspaceEditClientCapabilitiesChangeAnnotationSupport]


class DidChangeConfigurationClientCapabilities(TypedDict):
    #
    # Did change configuration notification supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]


class DidChangeWatchedFilesClientCapabilities(TypedDict):
    #
    # Did change watched files notification supports dynamic registration.
    # Please note that the current protocol doesn't support static
    # configuration for file changes from the server side.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # Whether the client has support for relative patterns
    # or not.
    #
    # @since 3.17.0
    #
    relativePatternSupport: NotRequired[bool]


class WorkspaceSymbolClientCapabilitiesSymbolKind(TypedDict):
    #
    # The symbol kind values the client supports. When this
    # property exists the client also guarantees that it will
    # handle values outside its set gracefully and falls back
    # to a default value when unknown.
    #
    # If this property is not present the client only supports
    # the symbol kinds from `File` to `Array` as defined in
    # the initial version of the protocol.
    #
    valueSet: NotRequired[list[SymbolKind]]


class WorkspaceSymbolClientCapabilitiesTagSupport(TypedDict):
    #
    # The tags supported by the client.
    #
    valueSet: list[SymbolTag]


class WorkspaceSymbolClientCapabilitiesResolveSupport(TypedDict):
    #
    # The properties that a client can resolve lazily. Usually
    # `location.range`
    #
    properties: list[str]


class WorkspaceSymbolClientCapabilities(TypedDict):
    #
    # Symbol request supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # Specific capabilities for the `SymbolKind` in the `workspace/symbol`
    # request.
    #
    symbolKind: NotRequired[WorkspaceSymbolClientCapabilitiesSymbolKind]

    #
    # The client supports tags on `SymbolInformation` and `WorkspaceSymbol`.
    # Clients supporting tags have to handle unknown tags gracefully.
    #
    # @since 3.16.0
    #
    tagSupport: NotRequired[WorkspaceSymbolClientCapabilitiesTagSupport]

    #
    # The client support partial workspace symbols. The client will send the
    # request `workspaceSymbol/resolve` to the server to resolve additional
    # properties.
    #
    # @since 3.17.0 - proposedState
    #
    resolveSupport: NotRequired[WorkspaceSymbolClientCapabilitiesResolveSupport]


class ExecuteCommandClientCapabilities(TypedDict):
    #
    # Execute command supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]


class SemanticTokensWorkspaceClientCapabilities(TypedDict):
    #
    # Whether the client implementation supports a refresh request sent from
    # the server to the client.
    #
    # Note that this event is global and will force the client to refresh all
    # semantic tokens currently shown. It should be used with absolute care
    # and is useful for situation where a server for example detect a project
    # wide change that requires such a calculation.
    #
    refreshSupport: NotRequired[bool]


class CodeLensWorkspaceClientCapabilities(TypedDict):
    #
    # Whether the client implementation supports a refresh request sent from the
    # server to the client.
    #
    # Note that this event is global and will force the client to refresh all
    # code lenses currently shown. It should be used with absolute care and is
    # useful for situation where a server for example detect a project wide
    # change that requires such a calculation.
    #
    refreshSupport: NotRequired[bool]


class InlineValueWorkspaceClientCapabilities(TypedDict):
    #
    # Whether the client implementation supports a refresh request sent from
    # the server to the client.
    #
    # Note that this event is global and will force the client to refresh all
    # inline values currently shown. It should be used with absolute care and
    # is useful for situation where a server for example detect a project wide
    # change that requires such a calculation.
    #

    refreshSupport: NotRequired[bool]


class InlayHintWorkspaceClientCapabilities(TypedDict):
    #
    # Whether the client implementation supports a refresh request sent from
    # the server to the client.
    #
    # Note that this event is global and will force the client to refresh all
    # inlay hints currently shown. It should be used with absolute care and
    # is useful for situation where a server for example detects a project wide
    # change that requires such a calculation.
    #
    refreshSupport: NotRequired[bool]


class DiagnosticWorkspaceClientCapabilities(TypedDict):
    #
    # Whether the client implementation supports a refresh request sent from
    # the server to the client.
    #
    # Note that this event is global and will force the client to refresh all
    # inlay hints currently shown. It should be used with absolute care and
    # is useful for situation where a server for example detects a project wide
    # change that requires such a calculation.
    #
    refreshSupport: NotRequired[bool]


class ClientWorkspaceCapabilities(TypedDict):
    #
    # The client supports applying batch edits
    # to the workspace by supporting the request
    # 'workspace/applyEdit'
    #
    applyEdit: NotRequired[bool]
    #
    # Capabilities specific to `WorkspaceEdit`s
    #
    workspaceEdit: NotRequired[WorkspaceEditClientCapabilities]
    #
    # Capabilities specific to the `workspace/didChangeConfiguration`
    # notification.
    #
    didChangeConfiguration: NotRequired[DidChangeConfigurationClientCapabilities]
    #
    # Capabilities specific to the `workspace/didChangeWatchedFiles`
    # notification.
    #
    didChangeWatchedFiles: NotRequired[DidChangeWatchedFilesClientCapabilities]
    #
    # Capabilities specific to the `workspace/symbol` request.
    #
    symbol: NotRequired[WorkspaceSymbolClientCapabilities]
    #
    # Capabilities specific to the `workspace/executeCommand` request.
    #
    executeCommand: NotRequired[ExecuteCommandClientCapabilities]
    #
    # The client has support for workspace folders.
    # @since 3.6.0
    #
    workspaceFolders: NotRequired[bool]
    #
    # The client supports `workspace/configuration` requests.
    # @since 3.6.0
    #
    configuration: NotRequired[bool]
    #
    # Capabilities specific to the semantic token requests scoped to the
    # workspace.
    # @since 3.16.0
    #
    semanticTokens: NotRequired[SemanticTokensWorkspaceClientCapabilities]
    #
    # Capabilities specific to the code lens requests scoped to the
    # workspace.
    # @since 3.16.0
    #
    codeLens: NotRequired[CodeLensWorkspaceClientCapabilities]
    #
    # The client has support for file requests/notifications.
    # @since 3.16.0
    #
    fileOperations: NotRequired[ClientWorkspaceCapabilitiesFileOptions]
    #
    # Client workspace capabilities specific to inline values.
    # @since 3.17.0
    #
    inlineValue: NotRequired[InlineValueWorkspaceClientCapabilities]
    #
    # Client workspace capabilities specific to inlay hints.
    # @since 3.17.0
    #
    inlayHint: NotRequired[InlayHintWorkspaceClientCapabilities]
    #
    # Client workspace capabilities specific to diagnostics.
    # @since 3.17.0.
    #
    diagnostics: NotRequired[DiagnosticWorkspaceClientCapabilities]


class ShowMessageRequestClientCapabilitiesMessageActionItem(TypedDict):
    #
    # Whether the client supports additional attributes which
    # are preserved and sent back to the server in the
    # request's response.
    #
    additionalPropertiesSupport: NotRequired[bool]


class ShowMessageRequestClientCapabilities(TypedDict):
    #
    # Capabilities specific to the `MessageActionItem` type.
    #
    messageActionItem: NotRequired[ShowMessageRequestClientCapabilitiesMessageActionItem]


class ShowDocumentClientCapabilities(TypedDict):
    support: bool


class ClientCapabilitiesWindow(TypedDict):

    #
    # It indicates whether the client supports server initiated
    # progress using the `window/workDoneProgress/create` request.
    # The capability also controls Whether client supports handling
    # of progress notifications. If set servers are allowed to report a
    # `workDoneProgress` property in the request specific server
    # capabilities.
    # @since 3.15.0
    #
    workDoneProgress: NotRequired[bool]

    #
    # Capabilities specific to the showMessage request
    # @since 3.16.0
    #
    showMessage: NotRequired[ShowMessageRequestClientCapabilities]

    #
    # Client capabilities for the show document request.
    # @since 3.16.0
    #
    showDocument: NotRequired[ShowDocumentClientCapabilities]


class ClientCapabilitiesGeneralStaleRequestSupport(TypedDict):
    #
    # The client will actively cancel the request.
    #
    cancel: bool

    #
    # The list of requests for which the client
    # will retry the request if it receives a
    # response with error code `ContentModified``
    #
    retryOnContentModified: list[str]


class RegularExpressionsClientCapabilities(TypedDict):
    #
    # The engine's name.
    #
    engine: str

    #
    # The engine's version.
    #
    version: NotRequired[str]


class MarkdownClientCapabilities(TypedDict):
    #
    # The name of the parser.
    #
    parser: str

    #
    # The version of the parser.
    #
    version: NotRequired[str]

    #
    # A list of HTML tags that the client allows / supports in
    # Markdown.
    #
    # @since 3.17.0
    #
    allowedTags: NotRequired[list[str]]


class ClientCapabilitiesGeneral(TypedDict):
    #
    # Client capability that signals how the client
    # handles stale requests (e.g. a request
    # for which the client will not process the response
    # anymore since the information is outdated).
    # @since 3.17.0
    #
    staleRequestSupport: NotRequired[ClientCapabilitiesGeneralStaleRequestSupport]

    #
    # Client capabilities specific to regular expressions.
    # @since 3.16.0
    #
    regularExpressions: NotRequired[RegularExpressionsClientCapabilities]

    #
    # Client capabilities specific to the client's markdown parser.
    # @since 3.16.0
    #
    markdown: NotRequired[MarkdownClientCapabilities]

    #
    # The position encodings supported by the client. Client and server
    # have to agree on the same position encoding to ensure that offsets
    # (e.g. character position in a line) are interpreted the same on both
    # side.
    # To keep the protocol backwards compatible the following applies: if
    # the value 'utf-16' is missing from the array of position encodings
    # servers can assume that the client supports UTF-16. UTF-16 is
    # therefore a mandatory encoding.
    # If omitted it defaults to ['utf-16'].
    # Implementation considerations: since the conversion from one encoding
    # into another requires the content of the file / line the conversion
    # is best done where the file is read which is usually on the server
    # side.
    # @since 3.17.0
    #
    positionEncodings: NotRequired[list[PositionEncodingKind]]


class TextDocumentSyncClientCapabilities(TypedDict):
    #
    # Whether text document synchronization supports dynamic registration.
    # /
    dynamicRegistration: NotRequired[bool]

    #
    # The client supports sending will save notifications.
    # /
    willSave: NotRequired[bool]

    #
    # The client supports sending a will save request and
    # waits for a response providing text edits which will
    # be applied to the document before it is saved.
    # /
    willSaveWaitUntil: NotRequired[bool]

    #
    # The client supports did save notifications.
    # /
    didSave: NotRequired[bool]


# Deprecated=1
CompletionItemTag = Literal[1]


class CompletionClientCapabilitiesCompletionItemTagSupport(TypedDict):
    #
    # The tags supported by the client.
    # /
    valueSet: list[CompletionItemTag]


class CompletionClientCapabilitiesCompletionItemResolveSuport(TypedDict):
    #
    # The properties that a client can resolve lazily.
    # /
    properties: list[str]


class CompletionClientCapabilitiesCompletionItemInsertTextModeSupport(TypedDict):
    valueSet: list[InsertTextMode]


class CompletionClientCapabilitiesCompletionItem(TypedDict):
    #
    # Client supports snippets as insert text.
    #
    # A snippet can define tab stops and placeholders with `$1`, `$2`
    # and `${3:foo}`. `$0` defines the final tab stop, it defaults to
    # the end of the snippet. Placeholders with equal identifiers are
    # linked, that is typing in one will update others too.
    # /
    snippetSupport: NotRequired[bool]

    #
    # Client supports commit characters on a completion item.
    # /
    commitCharactersSupport: NotRequired[bool]

    #
    # Client supports the follow content formats for the documentation
    # property. The order describes the preferred format of the client.
    # /
    documentationFormat: NotRequired[list[MarkupKind]]

    #
    # Client supports the deprecated property on a completion item.
    # /
    deprecatedSupport: NotRequired[bool]

    #
    # Client supports the preselect property on a completion item.
    # /
    preselectSupport: NotRequired[bool]

    #
    # Client supports the tag property on a completion item. Clients
    # supporting tags have to handle unknown tags gracefully. Clients
    # especially need to preserve unknown tags when sending a completion
    # item back to the server in a resolve call.
    #
    # @since 3.15.0
    # /
    tagSupport: NotRequired[CompletionClientCapabilitiesCompletionItemTagSupport]

    #
    # Client supports insert replace edit to control different behavior if
    # a completion item is inserted in the text or should replace text.
    #
    # @since 3.16.0
    # /
    insertReplaceSupport: NotRequired[bool]

    #
    # Indicates which properties a client can resolve lazily on a
    # completion item. Before version 3.16.0 only the predefined properties
    # `documentation` and `detail` could be resolved lazily.
    #
    # @since 3.16.0
    # /
    resolveSupport: NotRequired[CompletionClientCapabilitiesCompletionItemResolveSuport]

    #
    # The client supports the `insertTextMode` property on
    # a completion item to override the whitespace handling mode
    # as defined by the client (see `insertTextMode`).
    #
    # @since 3.16.0
    # /
    insertTextModeSupport: NotRequired[CompletionClientCapabilitiesCompletionItemInsertTextModeSupport]

    #
    # The client has support for completion item label
    # details (see also `CompletionItemLabelDetails`).
    #
    # @since 3.17.0
    # /
    labelDetailsSupport: NotRequired[bool]


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


class CompletionClientCapabilitiesCompletionItemKind(TypedDict):
    #
    # The completion item kind values the client supports. When this
    # property exists the client also guarantees that it will
    # handle values outside its set gracefully and falls back
    # to a default value when unknown.
    #
    # If this property is not present the client only supports
    # the completion items kinds from `Text` to `Reference` as defined in
    # the initial version of the protocol.
    # /
    valueSet: NotRequired[list[CompletionItemKind]]


class CompletionClientCapabilitiesCompletionList(TypedDict):
    #
    # The client supports the following itemDefaults on
    # a completion list.
    #
    # The value lists the supported property names of the
    # `CompletionList.itemDefaults` object. If omitted
    # no properties are supported.
    #
    # @since 3.17.0
    # /
    itemDefaults: NotRequired[list[str]]


class CompletionClientCapabilities(TypedDict):
    #
    # Whether completion supports dynamic registration.
    # /
    dynamicRegistration: NotRequired[bool]

    #
    # The client supports the following `CompletionItem` specific
    # capabilities.
    # /
    completionItem: NotRequired[CompletionClientCapabilitiesCompletionItem]

    completionItemKind: NotRequired[CompletionClientCapabilitiesCompletionItemKind]

    #
    # The client supports to send additional context information for a
    # `textDocument/completion` request.
    # /
    contextSupport: NotRequired[bool]

    #
    # The client's default when the completion item doesn't provide a
    # `insertTextMode` property.
    #
    # @since 3.17.0
    # /
    insertTextMode: NotRequired[InsertTextMode]

    #
    # The client supports the following `CompletionList` specific
    # capabilities.
    #
    # @since 3.17.0
    # /
    completionList: NotRequired[CompletionClientCapabilitiesCompletionList]


class HoverClientCapabilities(TypedDict):
    #
    # Whether hover supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # Client supports the follow content formats if the content
    # property refers to a `literal of type MarkupContent`.
    # The order describes the preferred format of the client.
    #
    contentFormat: NotRequired[list[MarkupKind]]


class SignatureHelpClientCapabilitiesSignatureInformationParameterInformation(TypedDict):
    #
    # The client supports processing label offsets instead of a
    # simple label string.
    #
    # @since 3.14.0
    #
    labelOffsetSupport: NotRequired[bool]


class SignatureHelpClientCapabilitiesSignatureInformation(TypedDict):
    #
    # Client supports the follow content formats for the documentation
    # property. The order describes the preferred format of the client.
    #
    documentationFormat: NotRequired[list[MarkupKind]]

    #
    # Client capabilities specific to parameter information.
    #
    parameterInformation: NotRequired[SignatureHelpClientCapabilitiesSignatureInformationParameterInformation]

    #
    # The client supports the `activeParameter` property on
    # `SignatureInformation` literal.
    #
    # @since 3.16.0
    #
    activeParameterSupport: NotRequired[bool]


class SignatureHelpClientCapabilities(TypedDict):
    #
    # Whether signature help supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # The client supports the following `SignatureInformation`
    # specific properties.
    #
    signatureInformation: NotRequired[SignatureHelpClientCapabilitiesSignatureInformation]

    #
    # The client supports to send additional context information for a
    # `textDocument/signatureHelp` request. A client that opts into
    # contextSupport will also support the `retriggerCharacters` on
    # `SignatureHelpOptions`.
    #
    # @since 3.15.0
    #
    contextSupport: NotRequired[bool]


class DeclarationClientCapabilities(TypedDict):
    #
    # Whether declaration supports dynamic registration. If this is set to
    # `true` the client supports the new `DeclarationRegistrationOptions`
    # return value for the corresponding server capability as well.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # The client supports additional metadata in the form of declaration links.
    #
    linkSupport: NotRequired[bool]


class DefinitionClientCapabilities(TypedDict):
    #
    # Whether definition supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # The client supports additional metadata in the form of definition links.
    #
    # @since 3.14.0
    #
    linkSupport: NotRequired[bool]


class TypeDefinitionClientCapabilities(TypedDict):
    #
    # Whether implementation supports dynamic registration. If this is set to
    # `true` the client supports the new `TypeDefinitionRegistrationOptions`
    # return value for the corresponding server capability as well.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # The client supports additional metadata in the form of definition links.
    #
    # @since 3.14.0
    #
    linkSupport: NotRequired[bool]


class ImplementationClientCapabilities(TypedDict):
    #
    # Whether implementation supports dynamic registration. If this is set to
    # `true` the client supports the new `ImplementationRegistrationOptions`
    # return value for the corresponding server capability as well.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # The client supports additional metadata in the form of definition links.
    #
    # @since 3.14.0
    #
    linkSupport: NotRequired[bool]


class ReferenceClientCapabilities(TypedDict):
    #
    # Whether references supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]


class DocumentHighlightClientCapabilities(TypedDict):
    #
    # Whether document highlight supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]


class DocumentSymbolClientCapabilitiesSymbolKind(TypedDict):
    #
    # The symbol kind values the client supports. When this
    # property exists the client also guarantees that it will
    # handle values outside its set gracefully and falls back
    # to a default value when unknown.
    #
    # If this property is not present the client only supports
    # the symbol kinds from `File` to `Array` as defined in
    # the initial version of the protocol.
    #
    valueSet: NotRequired[list[SymbolKind]]


class DocumentSymbolClientCapabilitiesTagSupport(TypedDict):
    #
    # The tags supported by the client.
    #
    valueSet: list[SymbolTag]


class DocumentSymbolClientCapabilities(TypedDict):
    #
    # Whether document symbol supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # Specific capabilities for the `SymbolKind` in the
    # `textDocument/documentSymbol` request.
    #
    symbolKind: NotRequired[DocumentSymbolClientCapabilitiesSymbolKind]

    #
    # The client supports hierarchical document symbols.
    #
    hierarchicalDocumentSymbolSupport: NotRequired[bool]

    #
    # The client supports tags on `SymbolInformation`. Tags are supported on
    # `DocumentSymbol` if `hierarchicalDocumentSymbolSupport` is set to true.
    # Clients supporting tags have to handle unknown tags gracefully.
    #
    # @since 3.16.0
    #
    tagSupport: NotRequired[DocumentSymbolClientCapabilitiesTagSupport]

    #
    # The client supports an additional label presented in the UI when
    # registering a document symbol provider.
    #
    # @since 3.16.0
    #
    labelSupport: NotRequired[bool]


class CodeActionClientCapabilitiesCodeActionLiteralSupportCodeActionKind(TypedDict):
    #
    # The code action kind values the client supports. When this
    # property exists the client also guarantees that it will
    # handle values outside its set gracefully and falls back
    # to a default value when unknown.
    #
    valueSet: list[CodeActionKind]


class CodeActionClientCapabilitiesCodeActionLiteralSupport(TypedDict):
    #
    # The code action kind is supported with the following value
    # set.
    #
    codeActionKind: CodeActionClientCapabilitiesCodeActionLiteralSupportCodeActionKind


class CodeActionClientCapabilitiesResolveSupport(TypedDict):
    #
    # The properties that a client can resolve lazily.
    #
    properties: list[str]


class CodeActionClientCapabilities(TypedDict):
    #
    # Whether code action supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # The client supports code action literals as a valid
    # response of the `textDocument/codeAction` request.
    #
    # @since 3.8.0
    #
    codeActionLiteralSupport: NotRequired[CodeActionClientCapabilitiesCodeActionLiteralSupport]

    #
    # Whether code action supports the `isPreferred` property.
    #
    # @since 3.15.0
    #
    isPreferredSupport: NotRequired[bool]

    #
    # Whether code action supports the `disabled` property.
    #
    # @since 3.16.0
    #
    disabledSupport: NotRequired[bool]

    #
    # Whether code action supports the `data` property which is
    # preserved between a `textDocument/codeAction` and a
    # `codeAction/resolve` request.
    #
    # @since 3.16.0
    #
    dataSupport: NotRequired[bool]

    #
    # Whether the client supports resolving additional code action
    # properties via a separate `codeAction/resolve` request.
    #
    # @since 3.16.0
    #
    resolveSupport: NotRequired[CodeActionClientCapabilitiesResolveSupport]

    #
    # Whether the client honors the change annotations in
    # text edits and resource operations returned via the
    # `CodeAction#edit` property by for example presenting
    # the workspace edit in the user interface and asking
    # for confirmation.
    #
    # @since 3.16.0
    #
    honorsChangeAnnotations: NotRequired[bool]


class CodeLensClientCapabilities(TypedDict):
    #
    # Whether code lens supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]


class DocumentLinkClientCapabilities(TypedDict):
    #
    # Whether document link supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # Whether the client supports the `tooltip` property on `DocumentLink`.
    #
    # @since 3.15.0
    #
    tooltipSupport: NotRequired[bool]


class DocumentColorClientCapabilities(TypedDict):
    #
    # Whether document color supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]


class DocumentFormattingClientCapabilities(TypedDict):
    #
    # Whether formatting supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]


class DocumentRangeFormattingClientCapabilities(TypedDict):
    #
    # Whether formatting supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]


class DocumentOnTypeFormattingClientCapabilities(TypedDict):
    #
    # Whether on type formatting supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]


# Identifier=1
PrepareSupportDefaultBehavior = Literal[1]


class RenameClientCapabilities(TypedDict):
    #
    # Whether rename supports dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # Client supports testing for validity of rename operations
    # before execution.
    #
    # @since version 3.12.0
    #
    prepareSupport: NotRequired[bool]

    #
    # Client supports the default behavior result
    # (`{ defaultBehavior: bool }`).
    #
    # The value indicates the default behavior used by the
    # client.
    #
    # @since version 3.16.0
    #
    prepareSupportDefaultBehavior: NotRequired[PrepareSupportDefaultBehavior]

    #
    # Whether the client honors the change annotations in
    # text edits and resource operations returned via the
    # rename request's workspace edit by for example presenting
    # the workspace edit in the user interface and asking
    # for confirmation.
    #
    # @since 3.16.0
    #
    honorsChangeAnnotations: NotRequired[bool]


DiagnosticTag = Literal[1, 2]


class PublishDiagnosticsClientCapabilitiesTagSupport(TypedDict):
    #
    # The tags supported by the client.
    #
    valueSet: list[DiagnosticTag]


class PublishDiagnosticsClientCapabilities(TypedDict):
    #
    # Whether the clients accepts diagnostics with related information.
    #
    relatedInformation: NotRequired[bool]

    #
    # Client supports the tag property to provide meta data about a diagnostic.
    # Clients supporting tags have to handle unknown tags gracefully.
    #
    # @since 3.15.0
    #
    tagSupport: NotRequired[PublishDiagnosticsClientCapabilitiesTagSupport]

    #
    # Whether the client interprets the version property of the
    # `textDocument/publishDiagnostics` notification's parameter.
    #
    # @since 3.15.0
    #
    versionSupport: NotRequired[bool]

    #
    # Client supports a codeDescription property
    #
    # @since 3.16.0
    #
    codeDescriptionSupport: NotRequired[bool]

    #
    # Whether code action supports the `data` property which is
    # preserved between a `textDocument/publishDiagnostics` and
    # `textDocument/codeAction` request.
    #
    # @since 3.16.0
    #
    dataSupport: NotRequired[bool]


class FoldingRangeClientCapabilitiesFoldingRangeKind(TypedDict):
    #
    # The folding range kind values the client supports. When this
    # property exists the client also guarantees that it will
    # handle values outside its set gracefully and falls back
    # to a default value when unknown.
    #
    valueSet: NotRequired[list[FoldingRangeKind]]


class FoldingRangeClientCapabilitiesFoldingRange(TypedDict):

    #
    # If set, the client signals that it supports setting collapsedText on
    # folding ranges to display custom labels instead of the default text.
    #
    # @ since 3.17.0
    # /
    collapsedText: NotRequired[bool]


class FoldingRangeClientCapabilities(TypedDict):
    #
    # Whether implementation supports dynamic registration for folding range
    # providers. If this is set to `true` the client supports the new
    # `FoldingRangeRegistrationOptions` return value for the corresponding
    # server capability as well.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # The maximum number of folding ranges that the client prefers to receive
    # per document. The value serves as a hint, servers are free to follow the
    # limit.
    #
    rangeLimit: NotRequired[int]

    #
    # If set, the client signals that it only supports folding complete lines.
    # If set, client will ignore specified `startCharacter` and `endCharacter`
    # properties in a FoldingRange.
    #
    lineFoldingOnly: NotRequired[bool]

    #
    # Specific options for the folding range kind.
    #
    # @since 3.17.0
    #
    foldingRangeKind: NotRequired[FoldingRangeClientCapabilitiesFoldingRangeKind]

    #
    # Specific options for the folding range.
    # @since 3.17.0
    #
    foldingRange: NotRequired[FoldingRangeClientCapabilitiesFoldingRange]


class SelectionRangeClientCapabilities(TypedDict):
    #
    # Whether implementation supports dynamic registration for selection range
    # providers. If this is set to `true` the client supports the new
    # `SelectionRangeRegistrationOptions` return value for the corresponding
    # server capability as well.
    #
    dynamicRegistration: NotRequired[bool]


class LinkedEditingRangeClientCapabilities(TypedDict):
    #
    # Whether the implementation supports dynamic registration.
    # If this is set to `true` the client supports the new
    # `(TextDocumentRegistrationOptions & StaticRegistrationOptions)`
    # return value for the corresponding server capability as well.
    #
    dynamicRegistration: NotRequired[bool]


class CallHierarchyClientCapabilities(TypedDict):
    #
    # Whether implementation supports dynamic registration. If this is set to
    # `true` the client supports the new `(TextDocumentRegistrationOptions &
    # StaticRegistrationOptions)` return value for the corresponding server
    # capability as well.
    #
    dynamicRegistration: NotRequired[bool]


class SemanticTokensClientCapabilitiesRequestsFull(TypedDict):
    #
    # The client will send the `textDocument/semanticTokens/full/delta`
    # request if the server provides a corresponding handler.
    #
    delta: NotRequired[bool]


class SemanticTokensClientCapabilitiesRequests(TypedDict):
    #
    # The client will send the `textDocument/semanticTokens/range` request
    # if the server provides a corresponding handler.
    #
    range: NotRequired[bool | EmptyDict]

    #
    # The client will send the `textDocument/semanticTokens/full` request
    # if the server provides a corresponding handler.
    #
    full: NotRequired[bool | SemanticTokensClientCapabilitiesRequestsFull]


class SemanticTokensClientCapabilities(TypedDict):
    #
    # Whether implementation supports dynamic registration. If this is set to
    # `true` the client supports the new `(TextDocumentRegistrationOptions &
    # StaticRegistrationOptions)` return value for the corresponding server
    # capability as well.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # Which requests the client supports and might send to the server
    # depending on the server's capability. Please note that clients might not
    # show semantic tokens or degrade some of the user experience if a range
    # or full request is advertised by the client but not provided by the
    # server. If for example the client capability `requests.full` and
    # `request.range` are both set to true but the server only provides a
    # range provider the client might not render a minimap correctly or might
    # even decide to not show any semantic tokens at all.
    #
    requests: SemanticTokensClientCapabilitiesRequests

    #
    # The token types that the client supports.
    #
    tokenTypes: list[str]

    #
    # The token modifiers that the client supports.
    #
    tokenModifiers: list[str]

    #
    # The formats the clients supports.
    #
    formats: list[TokenFormat]

    #
    # Whether the client supports tokens that can overlap each other.
    #
    overlappingTokenSupport: NotRequired[bool]

    #
    # Whether the client supports tokens that can span multiple lines.
    #
    multilineTokenSupport: NotRequired[bool]

    #
    # Whether the client allows the server to actively cancel a
    # semantic token request, e.g. supports returning
    # ErrorCodes.ServerCancelled. If a server does the client
    # needs to retrigger the request.
    #
    # @since 3.17.0
    #
    serverCancelSupport: NotRequired[bool]

    #
    # Whether the client uses semantic tokens to augment existing
    # syntax tokens. If set to `true` client side created syntax
    # tokens and semantic tokens are both used for colorization. If
    # set to `false` the client only uses the returned semantic tokens
    # for colorization.
    #
    # If the value is `undefined` then the client behavior is not
    # specified.
    #
    # @since 3.17.0
    #
    augmentsSyntaxTokens: NotRequired[bool]


class MonikerClientCapabilities(TypedDict):
    #
    # Whether implementation supports dynamic registration. If this is set to
    # `true` the client supports the new `(TextDocumentRegistrationOptions &
    # StaticRegistrationOptions)` return value for the corresponding server
    # capability as well.
    #
    dynamicRegistration: NotRequired[bool]


class TypeHierarchyClientCapabilities(TypedDict):
    #
    # Whether implementation supports dynamic registration. If this is set to
    # `true` the client supports the new `(TextDocumentRegistrationOptions &
    # StaticRegistrationOptions)` return value for the corresponding server
    # capability as well.
    #
    dynamicRegistration: NotRequired[bool]


class InlineValueClientCapabilities(TypedDict):
    #
    # Whether implementation supports dynamic registration for inline
    # value providers.
    #
    dynamicRegistration: NotRequired[bool]


class InlayHintClientCapabilitiesResolveSupport(TypedDict):

    #
    # The properties that a client can resolve lazily.
    #
    properties: list[str]


class InlayHintClientCapabilities(TypedDict):

    #
    # Whether inlay hints support dynamic registration.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # Indicates which properties a client can resolve lazily on an inlay
    # hint.
    #
    resolveSupport: NotRequired[InlayHintClientCapabilitiesResolveSupport]


class DiagnosticClientCapabilities(TypedDict):
    #
    # Whether implementation supports dynamic registration. If this is set to
    # `true` the client supports the new
    # `(TextDocumentRegistrationOptions & StaticRegistrationOptions)`
    # return value for the corresponding server capability as well.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # Whether the clients supports related documents for document diagnostic
    # pulls.
    #
    relatedDocumentSupport: NotRequired[bool]


class TextDocumentClientCapabilities(TypedDict):

    synchronization: NotRequired[TextDocumentSyncClientCapabilities]

    #
    # Capabilities specific to the `textDocument/completion` request.
    completion: NotRequired[CompletionClientCapabilities]

    #
    # Capabilities specific to the `textDocument/hover` request.
    hover: NotRequired[HoverClientCapabilities]

    #
    # Capabilities specific to the `textDocument/signatureHelp` request.
    signatureHelp: NotRequired[SignatureHelpClientCapabilities]

    #
    # Capabilities specific to the `textDocument/declaration` request.
    #
    # @since 3.14.0
    declaration: NotRequired[DeclarationClientCapabilities]

    #
    # Capabilities specific to the `textDocument/definition` request.
    definition: NotRequired[DefinitionClientCapabilities]

    #
    # Capabilities specific to the `textDocument/typeDefinition` request.
    #
    # @since 3.6.0
    typeDefinition: NotRequired[TypeDefinitionClientCapabilities]

    #
    # Capabilities specific to the `textDocument/implementation` request.
    #
    # @since 3.6.0
    implementation: NotRequired[ImplementationClientCapabilities]

    #
    # Capabilities specific to the `textDocument/references` request.
    references: NotRequired[ReferenceClientCapabilities]

    #
    # Capabilities specific to the `textDocument/documentHighlight` request.
    documentHighlight: NotRequired[DocumentHighlightClientCapabilities]

    #
    # Capabilities specific to the `textDocument/documentSymbol` request.
    documentSymbol: NotRequired[DocumentSymbolClientCapabilities]

    #
    # Capabilities specific to the `textDocument/codeAction` request.
    codeAction: NotRequired[CodeActionClientCapabilities]

    #
    # Capabilities specific to the `textDocument/codeLens` request.
    codeLens: NotRequired[CodeLensClientCapabilities]

    #
    # Capabilities specific to the `textDocument/documentLink` request.
    documentLink: NotRequired[DocumentLinkClientCapabilities]

    #
    # Capabilities specific to the `textDocument/documentColor` and the
    # `textDocument/colorPresentation` request.
    #
    # @since 3.6.0
    colorProvider: NotRequired[DocumentColorClientCapabilities]

    #
    # Capabilities specific to the `textDocument/formatting` request.
    formatting: NotRequired[DocumentFormattingClientCapabilities]

    #
    # Capabilities specific to the `textDocument/rangeFormatting` request.
    rangeFormatting: NotRequired[DocumentRangeFormattingClientCapabilities]

    #  request.
    # Capabilities specific to the `textDocument/onTypeFormatting` request.
    onTypeFormatting: NotRequired[DocumentOnTypeFormattingClientCapabilities]

    #
    # Capabilities specific to the `textDocument/rename` request.
    rename: NotRequired[RenameClientCapabilities]

    #
    # Capabilities specific to the `textDocument/publishDiagnostics`
    # notification.
    publishDiagnostics: NotRequired[PublishDiagnosticsClientCapabilities]

    #
    # Capabilities specific to the `textDocument/foldingRange` request.
    #
    # @since 3.10.0
    foldingRange: NotRequired[FoldingRangeClientCapabilities]

    #
    # Capabilities specific to the `textDocument/selectionRange` request.
    #
    # @since 3.15.0
    selectionRange: NotRequired[SelectionRangeClientCapabilities]

    #
    # Capabilities specific to the `textDocument/linkedEditingRange` request.
    #
    # @since 3.16.0
    linkedEditingRange: NotRequired[LinkedEditingRangeClientCapabilities]

    #
    # Capabilities specific to the various call hierarchy requests.
    #
    # @since 3.16.0
    callHierarchy: NotRequired[CallHierarchyClientCapabilities]

    #
    # Capabilities specific to the various semantic token requests.
    #
    # @since 3.16.0
    semanticTokens: NotRequired[SemanticTokensClientCapabilities]

    #
    # Capabilities specific to the `textDocument/moniker` request.
    #
    # @since 3.16.0
    moniker: NotRequired[MonikerClientCapabilities]

    #
    # Capabilities specific to the various type hierarchy requests.
    #
    # @since 3.17.0
    typeHierarchy: NotRequired[TypeHierarchyClientCapabilities]

    #
    # Capabilities specific to the `textDocument/inlineValue` request.
    #
    # @since 3.17.0
    inlineValue: NotRequired[InlineValueClientCapabilities]

    #
    # Capabilities specific to the `textDocument/inlayHint` request.
    #
    # @since 3.17.0
    inlayHint: NotRequired[InlayHintClientCapabilities]

    #
    # Capabilities specific to the diagnostic pull model.
    #
    # @since 3.17.0
    diagnostic: NotRequired[DiagnosticClientCapabilities]


class NotebookDocumentSyncClientCapabilities(TypedDict):
    #
    # Whether implementation supports dynamic registration. If this is
    # set to `true` the client supports the new
    # `(TextDocumentRegistrationOptions & StaticRegistrationOptions)`
    # return value for the corresponding server capability as well.
    #
    dynamicRegistration: NotRequired[bool]

    #
    # The client supports sending execution summary data per cell.
    #
    executionSummarySupport: NotRequired[bool]


class NotebookDocumentClientCapabilities(TypedDict):
    #
    # Capabilities specific to notebook document synchronization
    #
    # @since 3.17.0
    #
    synchronization: NotebookDocumentSyncClientCapabilities


class ClientCapabilities(TypedDict):
    #
    # Workspace specific client capabilities.
    #
    workspace: NotRequired[ClientWorkspaceCapabilities]
    #
    # Text document specific client capabilities.
    #
    textDocument: NotRequired[TextDocumentClientCapabilities]
    #
    # Capabilities specific to the notebook document support.
    # @since 3.17.0
    #
    notebookDocument: NotRequired[NotebookDocumentClientCapabilities]
    #
    # Window specific client capabilities.
    #
    window: NotRequired[ClientCapabilitiesWindow]
    #
    # General client capabilities.
    # @since 3.16.0
    #
    general: NotRequired[ClientCapabilitiesGeneral]

    #
    # Experimental client capabilities.
    #
    experimental: NotRequired[Any]
