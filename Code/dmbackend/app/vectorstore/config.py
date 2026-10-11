import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "..",
    )
)

VECTORSTORE_BASE_DIR = os.path.join(
    PROJECT_ROOT,
    "Input_Data",
    "vectorstores",
)
DEFAULT_TOP_K = 5

SUPPORTED_INDEX_TYPE = "IndexFlatIP"
SUPPORTED_METRIC = "cosine_similarity"