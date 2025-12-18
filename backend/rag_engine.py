import os
import math
from openai import OpenAI

# Simple in-memory vector store
# format: [{"text": str, "embedding": list[float]}]
VECTOR_STORE = []

class RAGSystem:
    def __init__(self):
        # API key is read from env automatically by OpenAI client usually,
        # but we can also pass it explicitly if needed.
        self.client = OpenAI()
        self.db = VECTOR_STORE

    def get_embedding(self, text):
        response = self.client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def cosine_similarity(self, v1, v2):
        "Compute cosine similarity between two vectors."
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm_v1 = math.sqrt(sum(a * a for a in v1))
        norm_v2 = math.sqrt(sum(b * b for b in v2))
        return dot_product / (norm_v1 * norm_v2) if norm_v1 > 0 and norm_v2 > 0 else 0.0

    def ingest(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Simple splitting by double newline to get paragraphs
            chunks = [c.strip() for c in text.split('\n\n') if c.strip()]
            
            # If chunks are too large, we might want to split them further, 
            # but for this manual, paragraphs are likely fine.
            # Let's ensure no chunk is huge (arbitrary limit).
            final_chunks = []
            for chunk in chunks:
                if len(chunk) > 1000:
                   # Very naive split if too long
                   final_chunks.extend([chunk[i:i+1000] for i in range(0, len(chunk), 1000)])
                else:
                   final_chunks.append(chunk)

            self.db.clear()
            print(f"Embedding {len(final_chunks)} chunks...")
            
            for chunk in final_chunks:
                embedding = self.get_embedding(chunk)
                self.db.append({"text": chunk, "embedding": embedding})
            
            print("Ingestion complete.")
            return True
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error during ingestion: {e}")
            return False

    def query(self, query_text):
        if not self.db:
            return "Systemet har inte läst in manualen ännu. Ladda upp manual.txt först."
        
        try:
            # 1. Embed query
            query_embedding = self.get_embedding(query_text)
            
            # 2. Search (Calculate similarity with all chunks)
            # This is O(N) but fine for < 1000 chunks.
            scored_chunks = []
            for item in self.db:
                score = self.cosine_similarity(query_embedding, item["embedding"])
                scored_chunks.append((score, item["text"]))
            
            # 3. Sort and get top k
            scored_chunks.sort(key=lambda x: x[0], reverse=True)
            top_k = scored_chunks[:3]
            
            context = "\n\n".join([text for score, text in top_k])
            
            # 4. Generate answer
            messages = [
                {"role": "system", "content": "Du är en hjälpsam support-assistent för FRAPP. Svara baserat på följande information. Om svaret inte finns i texten, säg det."},
                {"role": "user", "content": f"Information:\n{context}\n\nFråga: {query_text}"}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Ett fel uppstod vid sökning: {e}"
