from dataclasses import dataclass
from typing import Final


@dataclass
class Model:
    tag: str
    name: str
    description: str
    n_ctx: int = 4096


LLAMA_8B = Model(
    "circlet:llama3.1-8b",
    "Llama-3.1 8B",
    "The Meta Llama 3.1 collection of multilingual large language models (LLMs) is a collection of pretrained and instruction tuned generative models which are optimized for multilingual dialogue use cases and outperform many of the available open source and closed chat models on common industry benchmarks.",
    n_ctx=32768,
)

LLAMA_70B = Model(
    "circlet:llama3.1-70b",
    "Llama-3.1 70B",
    "The Meta Llama 3.1 collection of multilingual large language models (LLMs) is a collection of pretrained and instruction tuned generative models which are optimized for multilingual dialogue use cases and outperform many of the available open source and closed chat models on common industry benchmarks.",
    n_ctx=32768,
)

NEMOTRON = Model(
    "circlet:nemotron",
    "Nemotron 70B",
    "Nemotron Large (Llama-3.1-Nemotron-70B-Instruct) is a large language model customized by NVIDIA to improve the helpfulness of LLM generated responses to user queries.",
    n_ctx=32768,
)

REFLECTION = Model(
    "circlet:reflection",
    "Reflection 70B",
    "Reflection 70B is an open-source LLM fine-tuned from Llama-3.1 70B, trained with a new technique called Reflection-Tuning that teaches a LLM to detect mistakes in its reasoning and correct course.",
    n_ctx=32768,
)

NEMOTRON_MINI = Model(
        "nemotron-mini:4b-instruct-q6_K",
        "Nemotron Mini",
        "Nemotron Mini (Nemotron-Mini-4B-Instruct) is a model for generating responses for roleplaying, retrieval augmented generation, and function calling. It is a small language model (SLM) optimized through distillation, pruning and quantization for speed and on-device deployment. This instruct model is optimized for roleplay, RAG QA, and function calling in English. It supports a context length of 4096 tokens.",
        4096,
    )
    
MODELS: Final[list[Model]] = [
    LLAMA_8B,
    LLAMA_70B,
    # NEMOTRON,
    REFLECTION,
    # NEMOTRON_MINI,
]
MODELS_BY_TAG: Final[dict[str, Model]] = {model.tag: model for model in MODELS}
MODELS_BY_NAME: Final[dict[str, Model]] = {model.name: model for model in MODELS}
