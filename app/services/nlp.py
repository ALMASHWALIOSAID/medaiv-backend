# app/services/nlp.py

import os
import spacy
from typing import Dict, List

# Transformer imports
from transformers import pipeline

# Load spaCy inside a singleton
spacy_nlp = spacy.load("en_core_web_sm")

# Load HF NER pipeline once (cache model directory)
MODEL_NAME = os.getenv("HF_NER_MODEL", "d4data/biomedical-ner-all")
ner_pipeline = pipeline("ner", model=MODEL_NAME, grouped_entities=True)

def extract_entities_spacy(text: str) -> Dict[str, List[str]]:
    doc = spacy_nlp(text)
    out: Dict[str, List[str]] = {}
    for ent in doc.ents:
        out.setdefault(ent.label_, []).append(ent.text)
    return out

def extract_entities_transformer(text: str) -> Dict[str, List[str]]:
    """
    Uses a grouped NER pipeline to return mappings
    from entity label (like DISEASE, CHEMICAL) to list of strings.
    """
    raw_ents = ner_pipeline(text)
    out: Dict[str, List[str]] = {}
    for ent in raw_ents:
        label = ent.get("entity_group") or ent["entity"]
        span  = ent["word"]
        out.setdefault(label, []).append(span)
    return out

def extract_entities(text: str, method: str = "transformer") -> Dict[str, List[str]]:
    """
    method: "transformer" or "spacy"
    """
    if method == "spacy":
        return extract_entities_spacy(text)
    return extract_entities_transformer(text)
