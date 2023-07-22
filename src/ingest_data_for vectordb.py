import random
from vectordb import LanceDB
from embedder import SentenceTransformerEmbedder
import pandas as pd

if __name__ == "__main__":

    encode_max = 10000

    data = pd.read_csv("../pubmed_abstracts.csv")

    all_abstracts = []

    for category in ['deep_learning', 'covid_19', 'human_connectome',
                     'virtual_reality', 'brain_machine_interfaces', 'electroactive_polymers',
                     'pedot_electrodes', 'neuroprosthetics']:
        all_abstracts.extend(data[category].dropna().tolist())

    random.seed(12)
    random.shuffle(all_abstracts)

    encoder = SentenceTransformerEmbedder("paraphrase-MiniLM-L6-v2", device="cpu")

    # for some reason these docs have a weird prefix and suffix
    all_abstracts = [doc[3:-2].strip() for doc in all_abstracts]

    # filtering out short docs
    all_abstracts = list(filter(lambda x: len(x) > 50, all_abstracts))

    docs = all_abstracts[:encode_max]

    embeddings = encoder.embed(docs)
    ids = list(range(0, len(embeddings)))

    db = LanceDB()
    db.create_index("test", embeddings, docs, ids)
