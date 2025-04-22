import re
import nltk
import string
import numpy as np
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from collections import defaultdict
import hdbscan
from sklearn.metrics.pairwise import cosine_distances

# Compute cosine distance matrix

# Download NLTK stopwords if not already available
# nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Step 1: Sample feedback
feedback_list = [
    "Orders with no payments are the ones on lot",
    "Really love the new dark mode feature!",
    "I wish the response was faster.",
    "Takes too long",
    "Incorrect query",
    "Wrong output",
    "Orders table is incomplete",
    "Payments should be null for cars on lot in orders table",
]

# Step 2: Text cleaning
def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    tokens = text.split()
    filtered = [word for word in tokens if word not in stop_words]
    return " ".join(filtered)

cleaned_feedback = [clean_text(fb) for fb in feedback_list]

# Step 3: Embeddings
embedder = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedder.encode(cleaned_feedback)

# distance_matrix = cosine_distances(embeddings)

# Step 4: HDBSCAN clustering
clusterer = hdbscan.HDBSCAN(min_cluster_size=2)
labels = clusterer.fit_predict(embeddings)

# Fallback to KMeans if HDBSCAN fails to produce any valid clusters
if all(label == -1 for label in labels):
    print("HDBSCAN found no clusters, falling back to KMeans...")
    num_clusters = 3
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)

# Step 5: Group feedback by cluster
grouped_feedback = defaultdict(list)
for original_text, label in zip(feedback_list, labels):
    grouped_feedback[label].append(original_text)

# Step 6: Summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

print("\n=== Feedback Group Summaries ===\n")

for label, group in grouped_feedback.items():
    if label == -1:
        print("Outliers (not grouped):")
        for f in group:
            print(f"- {f}")
        print()
        continue

    text = " ".join(group)
    text = text[:1024]  # Truncate to summarizer input limit
    summary = summarizer(text, max_length=30, min_length=5, do_sample=False)[0]['summary_text']
    
    print(f"\nGroup {label} Summary: {summary}")
    print()
    for f in group:
        print(f"- {f}")
    print("\n"*2)
