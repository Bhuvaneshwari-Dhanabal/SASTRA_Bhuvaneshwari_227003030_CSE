
import json
import os
from pathlib import Path

# In Docker, the backend application is normally located at /app.
APP_ROOT = Path(__file__).resolve().parents[1]

# Search locations for the shared configuration directory.
CANDIDATE_CONFIG_DIRS = [
    APP_ROOT / "Model_Prompts_Config",
    APP_ROOT.parent / "Model_Prompts_Config",
    Path("/app/Model_Prompts_Config"),
    Path("/Model_Prompts_Config"),
]

CONFIG_DIR = next(
    (
        path
        for path in CANDIDATE_CONFIG_DIRS
        if (path / "model_config.json").is_file()
        and (path / "rag_prompt.txt").is_file()
    ),
    CANDIDATE_CONFIG_DIRS[0],
)

CONFIG_PATH = CONFIG_DIR / "model_config.json"
RAG_PROMPT_PATH = CONFIG_DIR / "rag_prompt.txt"


def load_model_config():
    if not CONFIG_PATH.is_file():
        raise FileNotFoundError(
            f"Model configuration not found: {CONFIG_PATH}. "
            "Ensure Model_Prompts_Config is copied into the backend image."
        )

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_rag_prompt():
    if not RAG_PROMPT_PATH.is_file():
        raise FileNotFoundError(
            f"RAG prompt not found: {RAG_PROMPT_PATH}. "
            "Ensure Model_Prompts_Config is copied into the backend image."
        )

    prompt = RAG_PROMPT_PATH.read_text(encoding="utf-8").strip()

    if not prompt:
        raise ValueError(f"RAG prompt is empty: {RAG_PROMPT_PATH}")

    return prompt