from google.genai import Client
from google.genai import types

client = Client()
output_dimension_size = 3072 

text = "Machine learning helps computers learn from data."
model_name = "gemini-embedding-001"
result = client.models.embed_content(
    model=model_name,
    contents=text,
    config=types.EmbedContentConfig(
        output_dimensionality=output_dimension_size
    )
)
print("embedding size", len(result.embeddings[0].values))
# print("Embedding length:", len(res.data[0].embedding))
# print(res.data[0].embedding[:10], "...")   # preview
