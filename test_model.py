import spacy

# Try loading the model
try:
    nlp = spacy.load("en_ner_bionlp13cg_md")
    doc = nlp("The patient was prescribed ibuprofen for inflammation.")
    print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])
except Exception as e:
    print("ERROR:", e)