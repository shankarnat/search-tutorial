from sentence_transformers import SentenceTransformer


def gen_embeddings(statement: str ):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(statement)
    return embedding



