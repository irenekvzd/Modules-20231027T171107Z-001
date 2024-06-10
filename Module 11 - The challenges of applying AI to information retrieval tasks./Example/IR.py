def retrieve_articles(query, model, vectorizer, data, top_n=5):
    # Transform the query into a TF-IDF vector
    query_vec = vectorizer.transform([query])
    
    # Get the model's predictions (probabilities)
    pred_probs = model.predict_proba(query_vec)[0]
    
    # Get the top N most relevant articles
    top_indices = pred_probs.argsort()[-top_n:][::-1]
    
    return [(data[i], pred_probs[i]) for i in top_indices]

# Example query
query = "space exploration"
retrieved_articles = retrieve_articles(query, model, vectorizer, newsgroups.data)

# Display the retrieved articles
for i, (article, score) in enumerate(retrieved_articles):
    print(f"Article {i+1} (Score: {score:.4f}):\n{article[:200]}...\n")
