import os
from vectordb import LanceDB
from chatgpt import ChatGPTWrapper
from embedder import SentenceTransformerEmbedder
import argparse
from fetch_abstracts import Fetcher

def main(query):

    search_role = "You are a search engine that replies to query based on context. Answer with " \
                  "information provided within the context otherwise reply with 'I don't know'"

    text_to_query_role = "You are a tool that transforms text into a query for a medical search engine. "

    prompt_query = f"Please transform this text into a query for a medical search engine {query}:\n\n"
    output = ChatGPTWrapper(os.environ['OPENAI_API_KEY']).sample(prompt_query, role=text_to_query_role)
    print("DB Query", output)

    ft = Fetcher()

    best_text = ft.fetcher(output)

    # we build some context for the question
    text = "\n\n".join(best_text)

    # query prompt for chatgpt
    prompt = f"Please answer this question {query}\n\nhere's the context you should use:\n\n{text}"

    output = ChatGPTWrapper(os.environ['OPENAI_API_KEY']).sample(prompt, role=search_role)
    print()
    print()
    print(f"Answer using context: {output}")

    output = ChatGPTWrapper(os.environ['OPENAI_API_KEY']).sample(query, role="You are an helpful assistant")
    print()
    print()
    print(f"Answer without the context: {output}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, help='query to search')

    args = parser.parse_args()
    main(args.query)
