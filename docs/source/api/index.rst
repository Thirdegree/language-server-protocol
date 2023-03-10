
API
===

.. autoclass:: lsp.LanguageServer
   :members:  serve, wait, initialize,  shutdown,  exit,  text_document__declaration,  text_document__definition,  text_document__type_definition,  text_document__implementation,  text_document__references,  text_document__prepare_call_hierarchy,  call_hierarchy__incoming_calls,  call_hierarchy__outgoing_calls,  text_document__prepare_type_hierarchy,  type_hierarchy__supertypes,  type_hierarchy__subtypes,  text_document__document_highlight,  text_document__document_link,  document_link__resolve,  text_document__hover,  text_document__code_lens,  code_lens__resolve,  text_document__folding_range,  text_document__selection_range,  text_document__document_symbol,  text_document__semantic_tokens__full,  text_document__semantic_tokens__full__delta,  text_document__semantic_tokens__range,  text_document__inline_value,  text_document__inlay_hint,  inlay_hint__resolve,  text_document__moniker,  text_document__completion,  completion_item__resolve,  text_document__signature_help,  text_document__code_action,  code_action__resolve,  text_document__document_color,  text_document__formatting,  workspace__execute_command,  initialized,  text_document__did_open,  text_document__did_change,  text_document__will_save,  text_document__will_save_wait_until,  text_document__did_save,  text_document__did_close, 
   :member-order: bysource
   :undoc-members:



 




.. autoclass:: lsp.protocol.LspProtocol
   :members: write_message, read_message
   :show-inheritance:

.. autoclass:: lsp.protocol.Message
   :members:

Language Server Protocol Messages
---------------------------------

.. toctree::
   :maxdepth: 2

   messages
   server
   client
   common
