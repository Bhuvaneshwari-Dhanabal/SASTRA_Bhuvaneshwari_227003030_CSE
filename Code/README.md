# Source Code — AUTOSAR HLD Document Analysis Assistant

## 1. Overview

The `Code/` directory contains the source code for the **AI-Powered AUTOSAR High-Level Design (HLD) Document Analysis Assistant**. The application enables users to upload AUTOSAR HLD documents, retrieve relevant technical information, and obtain context-grounded answers to their questions using a Retrieval-Augmented Generation (RAG) pipeline.

The application follows a client-server architecture, separating the user interface from backend processing, document retrieval, and language-model inference.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js, Vite |
| Backend | Python, Flask |
| PDF Text Extraction | PyMuPDF |
| Text Embeddings | Sentence Transformers |
| Vector Search | FAISS |
| Large Language Model | Ollama with `qwen2.5:3b` |
| Metadata Storage | SQLite |
| Document and Index Storage | Local filesystem |
| Containerization | Docker, Docker Compose |

## 3. Directory Structure

The source code is organized into frontend and backend components.

```text
Code/
├── dmbackend/
│   ├── app/
│   │   ├── routes/
│   │   ├── database.py
│   │   ├── ...
│   ├── ...
│   └── ...
└── ...
```

The exact subdirectory structure may vary according to the implementation. Refer to the actual source files for the complete module organization.

### Frontend

The frontend provides the user-facing interface for authentication, document interaction, conversation management, and question answering.

Responsibilities include:

- Providing the chat interface.
- Allowing users to interact with uploaded documents.
- Displaying generated answers and supporting references.
- Communicating with the Flask backend through API requests.
- Presenting document and conversation information.

### Backend

The backend manages application logic and coordinates the document question-answering workflow.

Responsibilities include:

- Handling API requests and responses.
- Processing uploaded PDF documents.
- Extracting and preparing document text.
- Generating embeddings and managing vector retrieval.
- Retrieving relevant document passages.
- Invoking the configured language model.
- Managing application metadata and conversation-related operations.
- Enforcing authentication and access controls.

## 4. RAG Processing Workflow

The application's document question-answering workflow consists of the following stages:

1. **Document Upload:** The user uploads an AUTOSAR HLD PDF.
2. **Text Extraction:** PyMuPDF extracts text from the PDF.
3. **Text Preparation:** Extracted text is divided into chunks for retrieval.
4. **Embedding Generation:** A Sentence Transformers model converts chunks into vector representations.
5. **Indexing:** FAISS stores and searches the document vectors.
6. **Question Processing:** The backend receives the user's question.
7. **Context Retrieval:** Relevant passages are retrieved from the indexed document content.
8. **Answer Generation:** Ollama runs the configured language model to generate a response using the retrieved context.
9. **Response Presentation:** The answer and available supporting references are returned to the frontend.

## 5. Configuration and Execution

Before running the application, ensure that the required Python and Node.js dependencies are installed and that the configured Ollama model is available.

The project can be started using the existing Docker Compose configuration or the individual frontend and backend development commands documented in their respective directories.

Do not commit passwords, API keys, access tokens, private configuration files, or other secrets to version control.

## 6. Evaluation

The application's evaluation results are maintained in the `Evaluation_Results/` directory.

Evaluation may include:

- Retrieval relevance.
- Answer generation success and failure.
- Response latency.
- Citation availability.
- Evidence-grounding and answer-quality review.
- User-specific evaluation records, where implemented.

Operational success alone does not establish semantic correctness. Accuracy and grounding claims should be supported by a defined evaluation dataset and documented test results.

## 7. Security and Responsible AI

- Uploaded documents must be handled according to the application's access-control and storage policies.
- User-specific conversations and evaluation records must be protected by backend authorization checks.
- Retrieved document passages should be treated as untrusted input rather than executable instructions.
- Responses should be grounded in retrieved evidence wherever possible.
- The assistant should communicate when the available evidence is insufficient.
- Generated technical recommendations should be reviewed by a qualified human before being used in an engineering implementation.

## 8. Maintenance

When modifying the source code:

1. Preserve existing functionality unless a change is explicitly required.
2. Update relevant configuration and documentation when behavior changes.
3. Run the appropriate frontend and backend tests.
4. Verify document upload, retrieval, answer generation, and authentication.
5. Record evaluation results and retain reproducible test evidence.
6. Review changes before committing them to the repository.

## 9. Project Scope

This codebase supports the development and evaluation of an AI-assisted AUTOSAR HLD document analysis workflow. It is intended to help engineers and students locate, understand, and review information in design documents. It does not replace formal AUTOSAR compliance validation, system verification, or engineering approval.
