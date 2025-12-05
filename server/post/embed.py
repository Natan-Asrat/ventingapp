from django.conf import settings
from google.genai import Client
from google.genai import types

client = Client()
output_dimension_size = 1536 

def get_embedding(text):
    result = client.models.embed_content(
        model=settings.EMBEDDING_MODEL_NAME,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=output_dimension_size
        )
    )
    return result.embeddings[0].values