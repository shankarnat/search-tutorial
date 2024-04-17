import json
from pprint import pprint
import os
import time
import embeddings

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()


class Search:
    def __init__(self):
        self.es = Elasticsearch('http://localhost:9200') # <-- connection options need to be added here
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)

    def create_index(self):
        self.es.indices.delete(index='my_documents', ignore_unavailable=True)
        self.es.indices.create(index='my_documents')

    def has_embedding(self):
        mapping = self.es.get_mappings(index='mydocuments')
        return 'embedding' in mapping['my_documents']['mapping']['properties']

    def insert_documents(self, documents, emb_type = False):
        operations = []
        for document in documents:   
            operations.append({'index': {'_index': 'my_documents'}})
            if (emb_type == False):
                operations.append(document)
            elif (emb_type == True):
                operations.append({
                **document,
                'embedding': embeddings.gen_embeddings(document['summary']),
                })
        return self.es.bulk(operations=operations)

    def reindex(self):
        self.create_index()
        with open('data.json', 'rt') as f:
            documents = json.loads(f.read())
        return self.insert_documents(documents)
    
    def reindex_embeddings(self):
        self.create_index()
        with open('data.json', 'rt') as f:
            documents = json.loads(f.read())
        return self.insert_documents(documents, True)
    
    def search(self, **query_args):
        return self.es.search(index='my_documents', **query_args)
    
    def retrieve_document(self, id):
        return self.es.get(index='my_documents', id=id)
    

