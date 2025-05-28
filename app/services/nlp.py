from typing import Dict, List
from transformers import pipeline
from transformers import logging
import spacy

# Suppress HF warnings
logging.set_verbosity_error()

# Load SciSpaCy model
spacy_model = spacy.load("en_ner_bionlp13cg_md")

# Initialize HuggingFace NER pipeline
_ner_pipeline = pipeline(
    "ner",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    aggregation_strategy="simple"
)


def extract_entities_transformer(text: str) -> Dict[str, List[str]]:
    """
    Extract entities using HuggingFace transformer-based model.
    Groups words by entity labels.
    """
    raw_ents = _ner_pipeline(text)
    out: Dict[str, List[str]] = {}
    for ent in raw_ents:
        label = ent.get("entity_group") or ent.get("entity") or ent.get("label")
        word = ent.get("word") or ent.get("entity") or ""
        out.setdefault(label, []).append(word)
    return out


def extract_entities(text: str, method: str = "transformer") -> Dict[str, List[str]]:
    """
    General entity extraction dispatcher.
    Uses either transformer-based or SciSpaCy-based model.
    """
    if method == "transformer":
        try:
            return extract_entities_transformer(text)
        except Exception as e:
            print(f"[Transformer Entity Extraction Error] {e}")
            return {}
    elif method == "spacy":
        try:
            doc = spacy_model(text)
            entities: Dict[str, List[str]] = {}
            for ent in doc.ents:
                entities.setdefault(ent.label_, []).append(ent.text)
            return entities
        except Exception as e:
            print(f"[SpaCy Entity Extraction Error] {e}")
            return {}
    else:
        raise ValueError(f"Unknown method: {method}")
