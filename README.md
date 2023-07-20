# Simple Query Engine with LanceDB and OpenAI GPT


## First Step

Data comes from [Kaggle](https://www.kaggle.com/datasets/bonhart/pubmed-abstracts) and the format is pretty weird.

```python
    pip install -r requirements.txt
```

## Ingest Data

To create the database and ingest the data, run the following command. This will create a vector databse in the
local directory.

```python
    python src/ingest.py
```

## Query Data

This will query the openai endpoint and return an answer. 
Requires the env variable ```os.environ['OPENAI_API_KEY']``` to be set to the OpenAI API key.

```python
    python src/query.py --query "What are Soft-tissue Sarcomas?"
```