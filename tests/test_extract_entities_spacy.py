from app.services import nlp
import transformers
import pytest
from app.services import nlp
from app.services import nlp as nlp_mod

def test_extract_entities_bad_method():
    with pytest.raises(ValueError):
        nlp.extract_entities("sample text", method="invalid")

class DummyNLP:
    def __call__(self, text):
        return [
            {"word": "diabetes", "entity_group": "DISEASE"},
            {"word": "hypertension", "entity_group": "DISEASE"},
        ]

def test_extract_entities_transformer(monkeypatch: pytest.MonkeyPatch):
    fake = [
        {"entity_group": "ORG", "word": "OpenAI"},
        {"entity_group": "PER", "word": "Alice"},
    ]
    monkeypatch.setattr("app.services.nlp._ner_pipeline", lambda txt: fake)
    out = nlp_mod.extract_entities("whatever", method="transformer")
    assert out == {"ORG": ["OpenAI"], "PER": ["Alice"]}
