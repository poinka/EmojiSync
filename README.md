# EmojiSync
## Overview
**EmojiSync** is a vector search application that enables users to input text with emojis (e.g., "I'm so happy 😊🎉") and retrieve emotionally similar texts without emojis from a database. The system leverages `Sentence-BERT` for embedding generation, `Qdrant` for vector storage, and `Faiss` with `HNSW indexing` for fast similarity search. The project aims to capture the emotional context of emojis to match user queries with relevant texts, suitable for chat apps, social media, or sentiment analysis platforms.

This project is:
- Using an open-source dataset with ≥50,000 objects.
- Generating vector embeddings for text data.
- Implementing a similarity search algorithm.
- Evaluating performance with metrics like `Precision@k` and `Recall@k`.
- Conducting multiple iterations to compare approaches.

## Project Structure
The repository contains Jupyter notebooks for each project phase, as outlined below:

- `Iteration1.ipynb`: Baseline approach, treating emojis as unknown tokens (UNK) to assess their emotional contribution..
- `Iteration2.ipynb`: Uses `emoji.demojize` to convert emojis to text descriptions (e.g., 😊 → ":smiling_face_with_smiling_eyes:") to capture emotional richness.
- `Iteration3.ipynb`: Explores emoji2vec embeddings for advanced emoji handling (if time permits).
- `Database.ipynb`: Creates a vector database of emotionally rich texts without emojis.
- `Inference.ipynb`: Demonstrates the inference pipeline.

## Dataset
Source: GoEmotions from HuggingFace (~58,000 Reddit comments with 28 emotion labels).
Preprocessing: Emojis are removed to create a database of emotionally rich texts without emojis. The dataset is sliced to 50,000 objects, ensuring diversity across emotions (e.g., joy, anger, sadness) via stratified sampling.
Justification: GoEmotions provides a rich set of emotional annotations, ideal for matching user queries with emoji-driven emotional context.

## Key Technologies

Sentence-BERT (all-MiniLM-L6-v2): Generates 384D embeddings for texts (with and without emojis). Emojis are preprocessed using emoji.demojize for emotional context.
Qdrant: Stores vector embeddings for efficient retrieval.
Faiss (HNSW indexing): Performs fast approximate k-NN similarity search.
Python Libraries: sentence-transformers, qdrant-client, faiss-cpu, pandas, numpy, emoji.

## Installation
To set up the project locally:




## Usage


## Evaluation


## Iterations

1. Baseline (1st Iteration): Treat emojis as UNK tokens to evaluate their emotional impact.
2. Demojize (2nd Iteration): Convert emojis to text descriptions using emoji.demojize for better emotional capture.
3. Emoji2Vec (3rd Iteration): Use emoji2vec embeddings for advanced emoji handling (optional, time-permitting).


## Resources

GoEmotions Dataset
Sentence-Transformers Documentation
Qdrant Documentation
Faiss Wiki
Emoji Library
emoji2vec Paper
NLP Series: Day 5 — Handling Emojis

## License
MIT License
## Acknowledgments
This project was developed as part of an academic assignment to build a vector search application.
