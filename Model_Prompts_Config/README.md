# Model_Prompts_Config

These files document the current RAG settings and system prompt.

- `model_config.json`: embedding model metadata, default embedding model, FAISS index type, metric, and retrieval top-k.
- `rag_prompt.txt`: the RAG system prompt copied from the supplied Python snippet.

Important: these files are not automatically loaded by the application. The current Python implementation uses constants defined in its existing modules. To make these files authoritative, update the corresponding Python modules to load this JSON and prompt file, then test the RAG pipeline before rebuilding/publishing Docker images.
