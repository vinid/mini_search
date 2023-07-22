from eutils import Client
import os

class Fetcher:

    def __init__(self):
        self.ec = Client(api_key=os.environ.get("NCBI_API_KEY", None))


    def fetcher(self, query_terms):

        esr = self.ec.esearch(db='pubmed', term=query_terms)
        paset = self.ec.efetch(db='pubmed', id=esr.ids)

        abstracts = []
        for a in (paset):
            try:
                abstracts.append(a.abstract)
                if len(abstracts) == 3:
                    break
            except:
                print("Woop")
        return abstracts