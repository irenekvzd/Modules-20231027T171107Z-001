# Example of model interpretability
feature_names = vectorizer.get_feature_names_out()
top_features = sorted(zip(model.coef_[0], feature_names), reverse=True)[:10]
print("Top features for class 0:")
for coef, feat in top_features:
    print(f"{feat}: {coef:.4f}")
