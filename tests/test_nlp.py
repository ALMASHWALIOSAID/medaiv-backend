import pytest
from typing import Dict, List
from app.services.nlp import extract_entities
import app.services.nlp as nlp_mod

def test_extract_entities_transformer(monkeypatch):
    # craft fake HuggingFace pipeline output
    fake = [
        {"entity_group": "ORG", "word": "OpenAI"},
        {"entity_group": "PER", "word": "Alice"},
    ]
    monkeypatch.setattr("app.services.nlp._ner_pipeline", lambda txt: fake)
    out: Dict[str, List[str]] = nlp_mod.extract_entities("whatever", method="transformer")
    assert out == {"ORG": ["OpenAI"], "PER": ["Alice"]}

def test_extract_entities_transformer_fallback(monkeypatch):
    # simulate old output style: key "entity" instead of entity_group
    fake = [
        {"entity": "LOC", "word": "Paris"},
        {"entity": "LOC", "word": "London"},
    ]
    monkeypatch.setattr("app.services.nlp._ner_pipeline", lambda txt: fake)
    out = nlp_mod.extract_entities("whocares", method="transformer")
    assert out == {"LOC": ["Paris", "London"]}

class DummySpan:
    def __init__(self, text, label_):
        self.text = text
        self.label_ = label_

class DummyDoc:
    ents = [DummySpan("Berlin", "GPE"), DummySpan("Bob", "PER")]

class DummyNLP:
    def __call__(self, txt):
        return DummyDoc()



def test_extract_entities_spacy():
    text = "The patient was diagnosed with diabetes and prescribed ibuprofen."
    result = extract_entities(text, method="spacy")
    assert isinstance(result, dict)
    assert any(result.values())  # Should not be empty if entities are found
    class DummyNLP:
        def __call__(self, text):
            return [{"word": "diabetes", "entity_group": "DISEASE"}]

    monkeypatch.setattr(nlp_mod, "_ner_pipeline", DummyNLP())
    result = nlp_mod.extract_entities("dummy text", method="spacy")
    assert result == {"DISEASE": ["diabetes"]}

def test_extract_entities_bad_method():
    with pytest.raises(ValueError):
        nlp_mod.extract_entities("x", method="unknown")
