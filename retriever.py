from llama_index.core import (VectorStoreIndex, get_response_synthesizer, 
        StorageContext, load_index_from_storage
        )
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from config import embed_model
# build index
storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(storage_context, embed_model= embed_model)
# configure retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)

# configure response synthesizer
response_synthesizer = get_response_synthesizer()

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.2)],
)

response = query_engine.query("What assets were invested in by the ARM ethical fund the year of the report?")
print(response)