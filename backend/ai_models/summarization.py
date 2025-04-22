from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict
from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn") 

def group_by_similarity_threshold(statements, similarity_threshold=0.3):
    """Groups statements based on pairwise cosine similarity exceeding a threshold."""
    model = SentenceTransformer('all-mpnet-base-v2')
    embeddings = model.encode(statements)
    num_statements = len(statements)
    groups = defaultdict(list)
    assigned = [False] * num_statements
    group_id = 0

    for i in range(num_statements):
        if not assigned[i]:
            groups[group_id].append(statements[i])
            assigned[i] = True
            for j in range(i + 1, num_statements):
                if not assigned[j]:
                    similarity = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
                    if similarity >= similarity_threshold:
                        groups[group_id].append(statements[j])
                        assigned[j] = True
            group_id += 1
    return groups

def generate_llm_summary(cluster_statements):
    """Generates a summary for a group of statements using an LLM."""
    if not cluster_statements:
        return "No statements in this cluster."
    # Concatenate the statements with a separator
    text_to_summarize = " ".join(cluster_statements)
    try:
        summary = summarizer(text_to_summarize, max_length=10, min_length=5, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Could not generate summary."

statements = [
    "The cat sat on the mat.",
    "A feline was resting on the rug.",
    "Dogs are loyal companions and bring joy.",
    "My puppy loves to play fetch in the park.",
    "The sun is shining brightly today, making it warm.",
    "It's a sunny day with clear skies.",
    "I enjoy reading books of various genres.",
    "She likes to delve into classic and contemporary novels.",
    "Pizza is a delicious and popular food.",
    "Pasta with tomato sauce is also very tasty.",
    "Cats are often independent animals who groom themselves.",
    "A dog's loyalty to its owner is well-known."
]

similarity_threshold = 0.8
grouped_statements = group_by_similarity_threshold(statements, similarity_threshold)

group_summaries = {}
for group_id, group in grouped_statements.items():
    if group:
        group_summaries[group_id] = generate_llm_summary(group)

for group_id, summary in group_summaries.items():
    print(f"Group {group_id + 1} Summary: {summary}")
    print(f"  Statements: {grouped_statements[group_id]}")
    print("-" * 30)