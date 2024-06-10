# Example of checking for missing values
missing_values = sum(1 for doc in newsgroups.data if not doc.strip())
print(f"Number of empty documents: {missing_values}")
