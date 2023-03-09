import asyncio
import sys

from lsp import LanguageServer
from lsp.lsp.messages import InitializeParams, InitializeResult


class DummyLanguageServer(LanguageServer):

    async def initialize(self, params: InitializeParams) -> InitializeResult:
        return InitializeResult(capabilities={})


async def amain() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5555
    async with DummyLanguageServer().serve('localhost', port) as server:
        await server.wait()


def main() -> None:
    asyncio.run(amain())


if __name__ == '__main__':
    main()
