
from app.config_loader import load_model_config

from app.embeddings.sentence_transformer import (
    SentenceTransformerProvider,
)


class EmbeddingRegistry:

    def __init__(self):
        self._providers = {}
        self._config = load_model_config()

        self._models = self._config.get(
            "embedding_models", {}
        )

        self._default_model = self._config.get(
            "default_embedding_model", "minilm"
        )

        if not self._models:
            raise ValueError(
                "No embedding models are configured in "
                "Model_Prompts_Config/model_config.json"
            )

        if self._default_model not in self._models:
            raise ValueError(
                f"Default embedding model "
                f"'{self._default_model}' is not configured."
            )

    def available_models(self):
        """Return all configured embedding model keys."""
        return list(self._models.keys())

    def get_config(self, model_key):
        """Return the configuration for a model."""
        if model_key not in self._models:
            raise ValueError(
                f"Unknown embedding model: {model_key}"
            )

        return self._models[model_key]

    def get(self, model_key=None):
        """Return a cached sentence-transformer provider."""
        if model_key is None:
            model_key = self._default_model

        if model_key not in self._models:
            raise ValueError(
                f"Unknown embedding model: {model_key}"
            )

        if model_key not in self._providers:
            config = self._models[model_key]

            if config.get("provider") != "sentence-transformers":
                raise ValueError(
                    f"Unsupported embedding provider for "
                    f"'{model_key}': {config.get('provider')}"
                )

            model_name = config.get("model_name")

            if not model_name:
                raise ValueError(
                    f"Missing model_name for '{model_key}'"
                )

            self._providers[model_key] = (
                SentenceTransformerProvider(model_name)
            )

        return self._providers[model_key]


embedding_registry = EmbeddingRegistry()
