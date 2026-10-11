# Input Data — AUTOSAR HLD Document Analysis Assistant

## 1. Overview

The `Input_Data/` directory contains the document files and supporting artifacts used by the AI-Powered AUTOSAR High-Level Design (HLD) Document Analysis Assistant.

It organizes sample HLD documents, uploaded PDFs, extracted text, document embeddings, and FAISS vector indexes used by the document-processing and Retrieval-Augmented Generation (RAG) pipeline.

These resources support document ingestion, semantic retrieval, and context-grounded question answering.

## 2. Directory Structure

```text
Input_Data/
├── README.md
├── embeddings/
│   └── document_1_fixed_minilm.npy
├── extracted/
│   └── b7c7e877e2c44e72ab5fbaf95d72bc88.txt
├── sample_hld/
│   ├── 28402823a03e45229526926546333d57.pdf
│   ├── d3bef121d7b34531a25181f3c73274d9.pdf
│   └── e5841e6bebcf4638873f77ad253fbf7b.pdf
├── uploads/
│   └── b7c7e877e2c44e72ab5fbaf95d72bc88.pdf
└── vectorstores/
    └── document_1__fixed__minilm/
        ├── index.faiss
        └── metadata.json
```

## 3. Directory and File Descriptions

### 3.1 `sample_hld/`

Contains sample AUTOSAR HLD PDF documents used as input for document analysis and demonstration.

**Purpose:**
- Provide sample technical documents for testing document ingestion.
- Demonstrate PDF text extraction and retrieval.
- Support testing of document-based question answering.

The directory currently contains three PDF files. Their exact technical contents and document versions should be verified from the original documents.

### 3.2 `uploads/`

Stores uploaded PDF documents processed or managed by the application.

**Purpose:**
- Retain source PDF files for document processing.
- Provide the original document corresponding to extracted text and generated retrieval artifacts.
- Support document-based question answering.

The current directory contains one PDF file identified by a generated filename.

### 3.3 `extracted/`

Stores text extracted from PDF documents.

**Purpose:**
- Preserve extracted document text for downstream processing.
- Supply textual content for chunking and embedding generation.
- Support the retrieval pipeline without repeatedly extracting text from the original PDF when the application reuses the stored extraction.

The current directory contains one extracted text file. Its generated filename corresponds to the PDF filename in `uploads/`.

### 3.4 `embeddings/`

Contains NumPy (`.npy`) files storing embedding-related numerical data.

**Current file:**
- `document_1_fixed_minilm.npy`

**Purpose:**
- Store vector representations or embedding data generated during document processing.
- Support semantic retrieval and experimentation with embedding configurations.

The exact shape, dimensionality, normalization, and relationship between this file and the indexed chunks depend on the embedding-generation implementation.

### 3.5 `vectorstores/`

Contains vector-search indexes and associated metadata.

**Current subdirectory:**
- `document_1__fixed__minilm/`

Files within this directory:

| File | Description |
|---|---|
| `index.faiss` | FAISS index used to search stored document vectors. |
| `metadata.json` | Associated metadata used to map indexed vectors to document chunks or source information, according to the implementation. |

**Purpose:**
- Enable efficient similarity search over indexed document content.
- Retrieve relevant passages for user questions.
- Associate retrieved vectors with their corresponding document metadata.

The index and metadata must remain compatible with one another. If the source document, chunking strategy, or embedding model changes, the corresponding index may need to be regenerated.

## 4. Data Processing Workflow

The directory supports the following general workflow:

1. **Sample or Uploaded PDF:** A source document is selected or uploaded.
2. **Text Extraction:** The backend extracts readable text from the PDF.
3. **Text Storage:** Extracted content is stored in `extracted/`.
4. **Embedding Generation:** The configured embedding model generates numerical vector representations.
5. **Vector Index Creation:** FAISS stores vectors in a searchable index.
6. **Metadata Storage:** Associated metadata is stored alongside the vector index.
7. **Semantic Retrieval:** The application retrieves relevant document passages in response to a question.
8. **Answer Generation:** The retrieved passages are provided to the language model as context for generating an answer.

The precise processing order, persistence behavior, and indexing strategy are determined by the backend implementation.

## 5. Relationship Between the Files

The files in these directories represent different stages or outputs of document processing.

| Resource | Role in the pipeline |
|---|---|
| `sample_hld/*.pdf` | Sample source documents |
| `uploads/*.pdf` | Uploaded source documents |
| `extracted/*.txt` | Extracted document text |
| `embeddings/*.npy` | Stored embedding-related numerical data |
| `vectorstores/*/index.faiss` | Searchable vector index |
| `vectorstores/*/metadata.json` | Metadata associated with the indexed content |

Generated filenames and identifiers should be preserved when they are referenced by the application's database or document-processing logic.

## 6. Data Management and Maintenance

To maintain consistency and reproducibility:

- Preserve the association between each source PDF and its extracted text.
- Keep each FAISS index synchronized with its corresponding metadata.
- Regenerate embeddings and indexes when their source content or relevant model settings change.
- Avoid manually editing binary embedding or FAISS index files.
- Remove obsolete generated artifacts only after confirming that they are no longer referenced by the application.
- Document changes to the sample documents or stored data artifacts.
- Verify that document processing and retrieval still work after modifying or regenerating the data.

## 7. Privacy and Repository Management

Uploaded documents and extracted text may contain confidential or proprietary technical information.

- Confirm that documents are permitted for use and distribution in the project.
- Do not commit confidential or restricted documents to a public repository.
- Apply appropriate access controls to uploaded PDFs and derived text.
- Avoid exposing extracted document content through public endpoints or unrestricted logs.
- Ensure that the application's authorization rules protect user-specific documents.
- Review repository contents before committing generated artifacts.

Whether uploaded documents and generated artifacts should be committed depends on their size, sensitivity, licensing, and role in reproducing the project.

## 8. Limitations

- Text extraction quality depends on the structure and readability of the source PDF.
- Scanned PDFs may require OCR; OCR support should not be assumed unless implemented and tested.
- Tables, diagrams, and graphical architecture representations may not be fully captured by text extraction.
- Embedding files and vector indexes depend on the embedding model and preprocessing configuration used to create them.
- Retrieved passages may not contain sufficient information to answer every question.
- A generated answer should not be considered correct merely because a relevant passage was retrieved.

## 9. Evaluation and Reproducibility

The documents and generated retrieval artifacts can be used to evaluate document retrieval and question answering.

Recommended evaluation activities include:

- Testing questions against known document sections.
- Checking whether the retrieved passages contain the required evidence.
- Verifying citation correctness.
- Identifying questions that cannot be answered from the available documents.
- Recording response latency and operational failures.
- Comparing retrieval configurations using a consistent test dataset.

Store evaluation questions, test outputs, and documented results in the project's `Evaluation_Results/` directory.

## 10. Intended Use

The `Input_Data/` directory supports the development, demonstration, and evaluation of an AI-assisted AUTOSAR HLD document analysis workflow.

The stored documents and retrieval artifacts help the system locate relevant technical information and generate evidence-grounded responses. The resulting answers are intended to assist technical analysis and document navigation, not to replace formal AUTOSAR validation, safety assessment, or engineering review.
