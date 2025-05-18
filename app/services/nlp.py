# app/services/nlp.py

import os
from typing import Dict, List

import spacy
from transformers import pipeline

# spaCy singleton
SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")
_spacy_nlp = spacy.load(SPACY_MODEL)

# Hugging-Face NER pipeline
HF_NER_MODEL = os.getenv("HF_NER_MODEL", "d4data/biomedical-ner-all")
_ner_pipeline = pipeline(
    "ner",
    model=HF_NER_MODEL,
    aggregation_strategy="simple"
)

def extract_entities_spacy(text: str) -> Dict[str, List[str]]:
    doc = _spacy_nlp(text)
    out: Dict[str, List[str]] = {}
    for ent in doc.ents:
        out.setdefault(ent.label_, []).append(ent.text)
    return out

def extract_entities_transformer(text: str) -> Dict[str, List[str]]:
    raw_ents = _ner_pipeline(text)
    out: Dict[str, List[str]] = {}
    for ent in raw_ents:
        label = ent.get("entity_group", ent["entity"])
        span  = ent["word"]
        out.setdefault(label, []).append(span)
    return out

def extract_entities(text: str, method: str = "transformer") -> Dict[str, List[str]]:
    """
    method: "transformer" (default) or "spacy"
    """
    if method.lower() == "spacy":
        return extract_entities_spacy(text)
    return extract_entities_transformer(text)
