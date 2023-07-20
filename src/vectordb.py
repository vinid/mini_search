import pandas as pd


class AbstractDB:

    def __init__(self):
        pass

    def create_index(self, **kwargs):
        pass

    def vector_search(self, vector, k=1):
        pass


class LanceDB(AbstractDB):
    """
    LanceDB is a vector database that uses Lance to store and search vectors.
    """
    def __init__(self):
        super().__init__()

        pass

    def create_index(self, table_name, embeddings, texts, ids):
        import lance
        import pyarrow as pa
        from lance.vector import vec_to_table

        data = pd.DataFrame({"text": texts, "id": ids})
        table = vec_to_table(embeddings)

        combined = pa.Table.from_pandas(data).append_column("vector", table["vector"])
        ds = lance.write_dataset(combined, "../chatbot.lance", mode="overwrite")

        ds.create_index("vector",
                             index_type="IVF_PQ",
                             num_partitions=64,  # IVF
                             num_sub_vectors=96)  # PQ


    def vector_search(self, vector, k=1):
        import lance
        self.ds = lance.dataset("../chatbot.lance")
        return self.ds.to_table(
            nearest={
                "column": "vector",
                "k": k,
                "q": vector,
                "nprobes": 20,
                "refine_factor": 100
            }).to_pandas()