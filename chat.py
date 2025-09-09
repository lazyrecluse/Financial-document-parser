from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
import os

persist_path =  "chat_history.json"

if os.path.exists(persist_path):
    chat_store= SimpleChatStore.from_persist_path(persist_path)
    
else:
    chat_store = SimpleChatStore()

chat_memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)