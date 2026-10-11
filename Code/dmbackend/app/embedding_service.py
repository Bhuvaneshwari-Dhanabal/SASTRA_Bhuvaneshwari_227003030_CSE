import os

import numpy as np
from app.config_loader import load_model_config 

from app.embeddings import (
    embedding_registry
)

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
    )
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "Input_Data",
)

EMBEDDINGS_DIR = os.path.join(
    DATA_DIR,
    "embeddings",
)

def ensure_embedding_directory():
    os.makedirs(
        EMBEDDINGS_DIR,
        exist_ok=True
    )


def create_embeddings(texts, model_key=None):
    config = load_model_config()

    if model_key is None:
        model_key = config["embeddings"]["default"]

    provider = embedding_registry.get(model_key)
    return provider.encode(texts)



def save_embeddings(
    vectors,
    document_id,
    model_key,
    chunking_strategy
):
    ensure_embedding_directory()

    filename = (
        f"document_{document_id}_"
        f"{chunking_strategy}_"
        f"{model_key}.npy"
    )

    path = os.path.join(
        EMBEDDINGS_DIR,
        filename
    )

    np.save(
        path,
        vectors
    )

    return path


def get_embedding_dimension(
    model_key
):
    provider = (
        embedding_registry.get(
            model_key
        )
    )

    return provider.dimension()


def get_embedding_model_name(
    model_key
):
    provider = (
        embedding_registry.get(
            model_key
        )
    )

    return provider.model_name()