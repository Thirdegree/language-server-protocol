#!/usr/bin/env python
"""
This language server will helpfully autocomplete the verses of "Never gonna give you up",
filling a critical niche in modern developer workflows.
"""
import asyncio
import logging

from lsp import LanguageServer
from lsp.lsp.messages import InitializeParams, InitializeResult
from lsp.lsp.server import (CompletionItem, CompletionList, CompletionOptions,
                            CompletionParams, ServerCapabilities)

logging.basicConfig(level='INFO')


class NeverGonna(LanguageServer):

    async def initialize(self, params: InitializeParams) -> InitializeResult:
        logging.info("initialize")
        logging.debug("client capabilities %s", params["capabilities"])
        return InitializeResult(capabilities=ServerCapabilities(
            completionProvider=CompletionOptions()))

    async def text_document__completion(
        self, params: CompletionParams
    ) -> list[CompletionItem] | CompletionList | None:
        logging.info("text_document__completion, %s", params)

        return [
            CompletionItem(label=stanza.split('\n', maxsplit=1)[0],
                           detail=stanza,
                           insertText=f'"""{stanza}"""',
                           insertTextMode=2) for stanza in set(LYRICS)
        ]


async def amain() -> None:
    async with NeverGonna().serve() as server:
        await server.wait()


LYRICS = set("""\
We're no strangers to love
You know the rules and so do I (do I)
A full commitment's what I'm thinking of

You wouldn't get this from any other guy
I just wanna tell you how I'm feeling

Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you

We've known each other for so long
Your heart's been aching, but you're too shy to say it (say it)
Inside, we both know what's been going on (going on)
We know the game and we're gonna play it

And if you ask me how I'm feeling
Don't tell me you're too blind to see

Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you

Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you

We've known each other for so long
Your heart's been aching, but you're too shy to say it (to say it)
Inside, we both know what's been going on (going on)
We know the game and we're gonna play it

I just wanna tell you how I'm feeling
Gotta make you understand

Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you

Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you

Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you""".split('\n\n'))

if __name__ == "__main__":
    asyncio.run(amain())
