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

To create a simple language server, you need to override :py:func:`lsp.LanguageServer.initialize`. For example:

.. code-block:: python

   from lsp import LanguageServer
   from lsp.lsp.messages import InitializeParams, InitializeResult 
   class SimpleLanguageServer(LanguageServer):
       async def Initialize(self, params: InitializeParams) -> InitializeResult: 
           return InitializeResult(capabilities={})

