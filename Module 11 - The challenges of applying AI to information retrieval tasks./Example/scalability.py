# Simulate scalability challenge
large_data = newsgroups.data * 10  # Pretend we have 10 times more data
large_X = vectorizer.fit_transform(large_data)
print(f"Shape of large TF-IDF matrix: {large_X.shape}")
