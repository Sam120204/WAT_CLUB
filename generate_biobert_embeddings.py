import json
import numpy as np
from transformers import BertTokenizer, BertModel
import torch

# Load pre-trained model tokenizer for BioBERT
tokenizer = BertTokenizer.from_pretrained('dmis-lab/biobert-base-cased-v1.1')

# Load pre-trained BioBERT model (weights)
model = BertModel.from_pretrained('dmis-lab/biobert-base-cased-v1.1')
model.eval()

def get_biobert_embeddings(texts):
    embeddings = []
    with torch.no_grad():
        for text in texts:
            # Encode text
            inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
            outputs = model(**inputs)
            # Get the mean pooling of the token embeddings
            embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().numpy())
    return np.array(embeddings)

if __name__ == "__main__":
    # Load data
    with open('pubmed_data.json', 'r') as f:
        data = json.load(f)

    articles = [f"{article['title']} {article.get('summary', '')}" for article in data]

    # Generate BioBERT embeddings
    biobert_embeddings = get_biobert_embeddings(articles)

    # Debug: Print shape and first few embeddings
    print(f"Generated BioBERT Embeddings shape: {biobert_embeddings.shape}")
    print(f"First embedding sample: {biobert_embeddings[0][:5]}")

    # Save embeddings to a file
    np.save("biobert_embeddings.npy", biobert_embeddings)
