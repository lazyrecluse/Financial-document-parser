from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import (SimpleDirectoryReader, VectorStoreIndex, 
                              StorageContext
                            )
from google import genai
from llama_index.core.llms import ChatMessage
# from llama_index.core.extractors import  (SummaryExtractor,
#     QuestionsAnsweredExtractor, KeywordExtractor
#     )
from config import embed_model
from workflows import Workflow, step
from workflows.events import Event, StartEvent, StopEvent

#Event to be emitted for streamlit to consume
class ParsedEvent(Event):
    success_message: str
    
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

        ])
        index.storage_context.persist(persist_dir="storage")
        return ParsedEvent('Document parsed and stored successfully')
    @step
    async def StopFlow(self, ev: Event) -> StopEvent:
        return StopEvent()

async def main():
    w = ParseFlow(timeout=60, verbose=False)
    reader = SimpleDirectoryReader(input_dir="./files")
    result = await w.run(doc=reader)
    print(str(result))
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())