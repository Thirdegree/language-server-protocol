import asyncio

from lsp import LanguageServer
from lsp.lsp.messages import InitializeParams, InitializeResult


class DummyLanguageServer(LanguageServer):

    async def initialize(self, params: InitializeParams) -> InitializeResult:
        return InitializeResult(capabilities={})


async def amain() -> None:
    async with DummyLanguageServer().serve() as server:
        await server.wait()


def main() -> None:
    asyncio.run(amain())


if __name__ == '__main__':
    main()
