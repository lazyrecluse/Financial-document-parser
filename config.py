import time 
import os
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()
token = os.getenv("GEMINI_API_KEY")
    
class RateLimitedEmbedding(GoogleGenAIEmbedding):
    # Declare sleep_time so Pydantic knows about it
    sleep_time: float = 1.0  

    def __init__(self, **kwargs):
        # Pass everything else to the parent init
        super().__init__(**kwargs)

    def get_text_embedding_batch(self, texts, **kwargs):
        """Override batching to add rate limiting."""
        kwargs.pop("show_progress", None)
        embeddings = super().get_text_embedding_batch(texts)  # call parent method
        time.sleep(self.sleep_time)  # sleep after each batch
        return embeddings

embed_model = RateLimitedEmbedding(
    model_name="text-embedding-004",
    embed_batch_size=800,
    api_key=token,
    sleep_time=5   # sleep 5s between batches (tweak if still hitting 429s)
)
llm = GoogleGenAI(model_name="gemini-2.0-flash", api_key=token)

Settings.embed_model = embed_model
Settings.llm = llm