import time

start_time = time.time()
retrieve_articles(query, model, vectorizer, newsgroups.data)
end_time = time.time()
print(f"Retrieval time: {end_time - start_time:.4f} seconds")
