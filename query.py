import os
from vectordb import LanceDB
from chatgpt import ChatGPTWrapper
from embedder import SentenceTransformerEmbedder
import argparse

def main(query):

    db = LanceDB()

    # embed with sentence transformer
    encoder = SentenceTransformerEmbedder("paraphrase-MiniLM-L6-v2", device="cpu")
    search_vector = encoder.embed([query])[0]

    # embed with sentence transformer
    best_text = db.vector_search(search_vector, k=3)

    # we build some context for the question
    text = "\n\n".join(best_text['text'].tolist())

    # query prompt for chatgpt
    prompt = f"Please answer this question {query}\n\nhere's the context you should use:\n\n{text}"

    output = ChatGPTWrapper(os.environ['OPENAI_API_KEY']).sample(prompt)

    print(f"Question: {prompt}")
    print()
    print(f"Answer: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, help='query to search')

    args = parser.parse_args()
    main(args.query)
