from typing import Literal, NewType, NotRequired, TypedDict, TypeVar

DocumentUri = NewType('DocumentUri', str)
URI = NewType('URI', str)
TraceValue = Literal['off', 'message', 'verbose']
ResourceOperationKind = Literal['create', 'rename', 'delete']
FailureHandlingKind = Literal['abort', 'transactional', 'undo',
                              'textOnlyTransactional']
PositionEncodingKind = Literal['utf-8', 'utf-16', 'utf-32']
FoldingRangeKind = Literal['comment', 'imports', 'region']
TokenFormat = Literal['relative']
FileOperationPatternKind = Literal['file', 'folder']
MonikerKind = Literal['import', 'export', 'local']
UniquenessLevel = Literal['document', 'project', 'group', 'scheme', 'global']

# Deprecated=1
SymbolTag = Literal[1]
# asIs (1):
#  The insertion or replace strings is taken as it is. If the
#  value is multi line the lines below the cursor will be
#  inserted using the indentation defined in the string value.
#  The client will not apply any kind of adjustments to the
#  string.
#
# adjustIndentation (2)
# The editor adjusts leading whitespace of new lines so that
# they match the indentation up to the cursor of the line for
# which the item is accepted.
#
# Consider a line like this: <2tabs><cursor><3tabs>foo. Accepting a
# multi line completion item is indented using 2 tabs and all
# following lines inserted will be indented using 2 tabs as well.
#
InsertTextMode = Literal[1, 2]

SymbolKind = Literal[1,  # File
                     2,  # Module
                     3,  # Namespace
                     4,  # Package
                     5,  # Class
                     6,  # Method
                     7,  # Property
                     8,  # Field
                     9,  # Constructor
                     10,  # Enum
                     11,  # Interface
                     12,  # Function
                     13,  # Variable
                     14,  # Constant
                     15,  # String
                     16,  # Number
                     17,  # Boolean
                     18,  # Array
                     19,  # Object
                     20,  # Key
                     21,  # Null
                     22,  # EnumMember
                     23,  # Struct
                     24,  # Event
                     25,  # Operator
                     26,  # TypeParameter
                     ]
DocumentHighlightKind = Literal[
    #
    # A textual occurrence.
    #
    1,  # Text

    #
    # Read-access of a symbol, like reading a variable.
    #
    2,  # Read

    #
    # Write-access of a symbol, like writing to a variable.
    #
    3,  # Write
]

MarkupKind = Literal['plaintext', 'markdown']
CodeActionTriggerKind = Literal[
    #
    # Code actions were explicitly requested by the user or by an extension.
    #
    1,  # Invoked

    #
    # Code actions were requested automatically.
    #
    # This typically happens when current selection in a file changes, but can
    # also be triggered when file content changes.
    #
    2,  # Automatic
]
CodeActionKind = Literal[

    #
    # Empty kind.
    #
    '',  # Empty

    #
    # Base kind for quickfix actions: 'quickfix'.
    #
    'quickfix',  # QuickFix

    #
    # Base kind for refactoring actions: 'refactor'.
    #
    'refactor',  # Refactor

    #
    # Base kind for refactoring extraction actions: 'refactor.extract'.
    #
    # Example extract actions:
    #
    # - Extract method
    # - Extract function
    # - Extract variable
    # - Extract interface from class
    # - ...
    #
    'refactor.extract',  # RefactorExtract

    #
    # Base kind for refactoring inline actions: 'refactor.inline'.
    #
    # Example inline actions:
    #
    # - Inline function
    # - Inline variable
    # - Inline constant
    # - ...
    #
    'refactor.inline',  # RefactorInline

    #
    # Base kind for refactoring rewrite actions: 'refactor.rewrite'.
    #
    # Example rewrite actions:
    #
    # - Convert JavaScript function to class
    # - Add or remove parameter
    # - Encapsulate field
    # - Make method static
    # - Move method to base class
    # - ...
    #
    'refactor.rewrite',  # RefactorRewrite

    #
    # Base kind for source actions: `source`.
    #
    # Source code actions apply to the entire file.
    #
    'source',  # Source

    #
    # Base kind for an organize imports source action:
    # `source.organizeImports`.
    #
    'source.organizeImports',  # SourceOrganizeImports

    #
    # Base kind for a 'fix all' source action: `source.fixAll`.
    #
    # 'Fix all' actions automatically fix errors that have a clear fix that
    # do not require user input. They should not suppress errors or perform
    # unsafe fixes such as generating new types or classes.
    #
    # @since 3.17.0
    #
    'source.fixAll',  # SourceFixAll
]

T_Message = TypeVar('T_Message', bound='MessageData')


class MessageData(TypedDict):
    pass


class WorkDoneProgressOptions(MessageData):
    workDoneProgress: NotRequired[bool]


class EmptyDict(MessageData):
    pass


class ClientInfo(MessageData):
    name: str
    version: NotRequired[str]


class ServerInfo(MessageData):
    name: str
    version: NotRequired[str]


class WorkspaceFolder(MessageData):
    pass


class Position(MessageData):
    line: int
    charecter: int


class Range(MessageData):
    #
    # The range's start position.
    #
    start: Position

    #
    # The range's end position.
    #
    end: Position


class Location(MessageData):
    uri: DocumentUri
    range: Range


class LocationLink(MessageData):

    #
    # Span of the origin of this link.
    #
    # Used as the underlined span for mouse interaction. Defaults to the word
    # range at the mouse position.
    #
    originSelectionRange: NotRequired[Range]

    #
    # The target resource identifier of this link.
    #
    targetUri: DocumentUri

    #
    # The full target range of this link. If the target for example is a symbol
    # then target range is the range enclosing this symbol not including
    # leading/trailing whitespace but everything else like comments. This
    # information is typically used to highlight the range in the editor.
    #
    targetRange: Range

    #
    # The range that should be selected and revealed when this link is being
    # followed, e.g the name of a function. Must be contained by the
    # `targetRange`. See also `DocumentSymbol#range`
    #
    targetSelectionRange: Range
