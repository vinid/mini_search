class AbstractEmbedder:
    def __init__(self, **kwargs):
       pass


class SentenceTransformerEmbedder(AbstractEmbedder):
    """
    Embedder that uses the SentenceTransformer library.
    """
    def __init__(self, model_path, device="cpu"):
        super().__init__()
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_path)
        self.model.to(device)

    def embed(self, sentences):
        return self.model.encode(sentences, show_progress_bar=True)