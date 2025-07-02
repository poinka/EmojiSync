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
- `Iteration4.ipynb`: Directly encodes emoji-rich text using the pretrained `roberta-base-go_emotions` model, leveraging its ability to handle emojis without preprocessing
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
1. Clone the repository
```
git clone https://github.com/your-org/emojisync.git
cd emojisync

```
2. Build and start the containers
   
```
docker compose up --build

```
3. Wait for the system to load data. Initial embedding upload and vector indexing may take 4–5 minutes.

> Note: Due to repository size limits, the file selected_quotes_embeddings.csv is not included. However, it can be regenerated using the instructions in `Database.ipynb`

## Usage
Once the system is running:
* Open your browser and go to `http://localhost:3000`
* Enter emojis or emoji-rich text (e.g., 🥺, I'm feeling 😡 today)
* The system will return an emotionally matching quote retrieved from the vector database.
* Press the button once again to see another appropriate quote

## Evaluation
1. Latency:
On CPU, the system responds in:
* ~0.05–0.10 seconds for short emoji inputs (single emoji or short phrase)
* Up to ~0.25 seconds for longer, multi-emoji or text-rich inputs

2. Cold-start time:
After full container startup and loading of embeddings into Qdrant, the system is ready in ~250–280 seconds

3. Hardware requirements:
* 8 GB RAM
* 4-core CPU
* 3 GB on Disk space

## Iterations

1. Baseline (1st Iteration): Treat emojis as UNK tokens to evaluate their emotional impact.
2. Demojize (2nd Iteration): Convert emojis to text descriptions using emoji.demojize for better emotional capture.
3. Emoji2Vec (3rd Iteration): Use emoji2vec embeddings for advanced emoji handling (optional, time-permitting).
4. Raw Input (4th Iteration): Use roberta-base-go_emotions to process raw emoji-text input directly, relying on the model's pretrained emoji understanding.


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
