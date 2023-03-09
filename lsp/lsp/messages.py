from typing import Any, NotRequired, TypedDict

from lsp.lsp.client import ClientCapabilities
from lsp.lsp.common import (ClientInfo, DocumentUri, ServerInfo, TraceValue,
                            WorkspaceFolder)
from lsp.lsp.server import ServerCapabilities


class InitializeParams(TypedDict):
    #
    # The process Id of the parent process that started the server. Is None if
    # the process has not been started by another process. If the parent
    # process is not alive then the server should exit (see exit notification)
    # its process.
    #
    processId: int | None

    #
    # Information about the client
    # @since 3.15.0
    #
    clientInfo: NotRequired[ClientInfo]
    #

    #
    # The locale the client is currently showing the user interface
    # in. This must not necessarily be the locale of the operating
    # system.
    # Uses IETF language tags as the value's syntax
    # (See https://en.wikipedia.org/wiki/IETF_language_tag)
    # @since 3.16.0
    #
    locale: NotRequired[str]

    #
    # The rootPath of the oorkspace. Is None
    # if no folder is open.
    # @deprecated in favour of `rootUri`.
    #
    rootPath: NotRequired[str | None]
    #
    # The rootUri of the workspace. Is None if no
    # folder is open. If both `rootPath` and `rootUri` are set
    # `rootUri` wins.
    # @deprecated in favour of `workspaceFolders`
    #
    rootUri: DocumentUri | None

    #
    # User provided initialization options.
    #
    initializationOptions: NotRequired[Any]

    #
    # The capabilities provided by the client (editor or tool)
    #
    capabilities: ClientCapabilities
    #
    # The initial trace setting. If omitted trace is disabled ('off').
    #
    trace: NotRequired[TraceValue]
    #
    # The workspace folders configured in the client when the server starts.
    # This property is only available if the client supports workspace folders.
    # It can be `None` if the client supports workspace folders but none are
    # configured.
    # @since 3.6.0
    #
    workspaceFolders: NotRequired[list[WorkspaceFolder] | None]


class InitializeResult(TypedDict):
    capabilities: ServerCapabilities
    serverInfo: NotRequired[ServerInfo]


class InitializedParams(TypedDict):
    pass
