# AI-Enabled  AUTOSAR HLD Document Analysis Assistant

## Project Overview

The **AI-Enabled AUTOSAR HLD Document Analysis Assistant** is an AI-based engineering support system designed to help engineers analyze and retrieve information from AUTOSAR High-Level Design (HLD) documents. 

The system utilizes **Retrieval-Augmented Generation (RAG)** to provide grounded answers based on approved HLD documents, along with source and page citations.

## Objectives

* **Analyze** AUTOSAR HLD documents seamlessly.
* **Extract** relevant architectural information automatically.
* **Provide** natural-language question answering for design files.
* **Retrieve** relevant HLD sections using semantic vector search.
* **Generate** grounded, hallucination-resistant responses using an LLM.
* **Provide** explicit page and section citations for verification.
* **Support** architecture analysis and engineering knowledge reuse.
* **Assist** engineers without replacing core human engineering decisions.

## Planned Technologies

* **Language:** Python
* **Core Architecture:** Retrieval-Augmented Generation (RAG)
* **AI Models:** Large Language Model (LLM) & Embedding Model
* **Vector Databases:** FAISS  
* **Frontend Interface:** REACT (Vite)  
* **Backend Interface:**  Flask
* **APIs:** REST APIs
* **Deployment:** Docker & Docker Compose

---

## Docker Hub — Pull and Run

You can use the pre-built Docker images of the **AUTOSAR AI Assistant** without building the application from source code.

### Available Docker Images

| Component | Docker Image | Link |
| :--- | :--- | :--- |
| **Frontend** | `bhuvaneshwarid48/autosar-ai-frontend` | [Docker Hub Registry](https://hub.docker.com/r/bhuvaneshwarid48/autosar-ai-frontend) |
| **Backend** | `bhuvaneshwarid48/autosar-ai-backend` | [Docker Hub Registry](https://hub.docker.com/r/bhuvaneshwarid48/autosar-ai-backend) |

### Pull the Images

Make sure Docker runtime is installed and running on your system, then execute:

```bash
docker pull bhuvaneshwarid48/autosar-ai-frontend:latest

docker pull bhuvaneshwarid48/autosar-ai-backend:latest

docker pull ollama/ollama:latest
```

### Customize and Build Your Own Version

This project is open for community modifications and extensions. You can:

* **Pull** the published Docker images directly to test run the application.
* **Fork** this repository and modify the source code files.
* **Add** or update software dependencies within your fork.
* **Build** customized frontend and backend images locally.
* **Publish** your modified images under your own Docker Hub container registry.
* **Create** and maintain your own versions completely independently.

For example, to build and publish a customized backend image:

```bash
# Build the image from the backend source subdirectory
docker build -t YOUR_DOCKERHUB_USERNAME/autosar-ai-backend:v1.0.0 ./Code/dmbackend

# Push your customized container to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/autosar-ai-backend:v1.0.0
```

> 💡 **Quick Note:** Make sure to replace `YOUR_DOCKERHUB_USERNAME` with your actual personal Docker Hub handle before running the command blocks above.

### Important Notes

* **Dependencies Packaged:** The Docker images package the core application environment and its installed python dependencies. Application runtime configurations, environment variables, and local dataset files must be mounted separately.
* **Model Download Required:** The standard `ollama/ollama` image does not include the pre-downloaded weights for the `qwen2.5:3b` model. You must pull the model footprint down manually via the Ollama execution layer once the container starts up.
* **Security First:** Never package sensitive API keys, database credentials, `.env` file contexts, or private architecture assets inside public Docker images or open repositories.
* **Independent Registry Rights:** To build and publish custom configuration images under your own workspace profile, you do not need administrative write access to the root author's upstream Docker Hub repository ecosystem.

---

* **Docker Hub Ecosystem:** [View Frontend Image](https://hub.docker.com/r/bhuvaneshwarid48/autosar-ai-frontend) · [View Backend Image](https://hub.docker.com/r/bhuvaneshwarid48/autosar-ai-backend)
* **Code Repository:** [GitHub Upstream Source](https://github.com/Bhuvaneshwari-Dhanabal/SASTRA_Bhuvaneshwari_227003030_CSE)
