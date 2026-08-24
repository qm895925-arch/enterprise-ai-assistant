from fastembed import TextEmbedding


class EmbeddingService:
    MODEL_NAME = "BAAI/bge-small-zh-v1.5"

    def __init__(self):
        self.model = TextEmbedding(
            model_name=self.MODEL_NAME
        )

    def embed_text(self, text: str) -> list[float]:
        embeddings = list(
            self.model.embed([text])
        )

        if not embeddings:
            raise ValueError("Embedding result is empty")

        return embeddings[0].tolist()