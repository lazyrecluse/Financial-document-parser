from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import (SimpleDirectoryReader, VectorStoreIndex, 
                              StorageContext
                            )
from google import genai
from google.genai import types
from llama_index.core.llms import ChatMessage
from llama_index.core.extractors import  (SummaryExtractor,
    QuestionsAnsweredExtractor, KeywordExtractor
    )
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from config import embed_model


# --- Load documents ---
reader = SimpleDirectoryReader(input_dir="./files")
document = reader.load_data()

# --- Build & persist index ---
# vector_index = VectorStoreIndex.from_documents(
#     document, embed_model=embed_model, show_progress=True)

# vector_index.storage_context.persist(persist_dir="storage")

index = VectorStoreIndex.from_documents(document,
    transformations=[SemanticSplitterNodeParser(
    buffer_size=3, breakpoint_percentile_threshold=95, embed_model=embed_model),

        #SummaryExtractor(),
        #QuestionsAnsweredExtractor(),
        #KeywordExtractor(),
        
    ],

)
index.storage_context.persist(persist_dir="storage")


