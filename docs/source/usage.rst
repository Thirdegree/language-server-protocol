Usage
=====

.. _installation:

Installation
------------

To use Language Server Protocol, first install it using pip:

.. code-block:: console

   (.venv) $ pip install language-server-protocol

Creating a simple language server
---------------------------------

In order to create a simple language server, override :py:func:`lsp.LanguageServer.initialize`. For example:

.. code-block:: python

   import asyncio
   from lsp import LanguageServer
   from lsp.lsp.messages import InitializeParams, InitializeResult 


   class SimpleLanguageServer(LanguageServer):
       async def Initialize(self, params: InitializeParams) -> InitializeResult: 
           return InitializeResult(capabilities={})

   async def amain() -> None:
       async with SimpleLanguageServer().listen() as server:
           await server.wait()

   if __name__ == '__main__':
       asyncio.run(amain())
