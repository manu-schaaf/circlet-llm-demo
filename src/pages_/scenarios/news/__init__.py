from pathlib import Path

import yaml

DOCUMENT_PATH = Path(__file__).parent / "bbc-ce31w8dzepno.yaml"
DOCUMENT_YAML: dict = yaml.safe_load(
    DOCUMENT_PATH.open("r"),
)
