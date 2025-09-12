from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import (SimpleDirectoryReader, VectorStoreIndex, 
                              StorageContext, load_index_from_storage
                            )
from pydantic import BaseModel, ConfigDict
from llama_index.core.llms import ChatMessage
from chat import chat_memory
from config import embed_model
from workflows import Workflow, step
from workflows.events import Event, StartEvent, StopEvent

#User defined type to hold index returned after parsing
class ParsedDocument(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)#so pydantic ignores storage
                                                           #context's complex dtype
    storage_context: StorageContext
    
#Event to be emitted for streamlit to consume   
class ParsedEvent(Event):
    success_message: str
    data: ParsedDocument
#workflow defining how event is generated for storageflow to trigger
class ParseFlow(Workflow):
    #parses document and triggers event start
    @step
    async def parse_doc(self, ev: StartEvent) -> ParsedEvent:
        doc = ev.doc #takes document from the user and writes to StartEvent
                                        
        document = doc.load_data()
        index = VectorStoreIndex.from_documents(document,
            transformations=[SemanticSplitterNodeParser(
            buffer_size=3, breakpoint_percentile_threshold=95, embed_model=embed_model),
        
        ] )
        index.storage_context.persist(persist_dir="storage")
        data = ParsedDocument(storage_context=index.storage_context)
        success_message = "Document parsed and stored successfully"
        return ParsedEvent(success_message=success_message, data=data)
    
    @step
    async def create_engine(self, ev: ParsedEvent) -> StopEvent:
        parsed_data = ev.data #access data written to parsed event
        storage_context = parsed_data.storage_context #accesss storage context within data
        index = load_index_from_storage(storage_context, embed_model= embed_model)
        chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=chat_memory,
    system_prompt=(
        "You are a chatbot, able to parse financial documents and offer crucial"
        "to your users. Ensure you do your best in offering your aid"
    ),
)
        return StopEvent(result = chat_engine)  

async def main():
    w = ParseFlow(timeout=60, verbose=False)
    reader = SimpleDirectoryReader(input_dir="./files")
    result = await w.run(doc=reader)
    print(str(result))
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())