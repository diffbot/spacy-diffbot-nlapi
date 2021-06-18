import argparse
import spacy
import spacy_diffbot_nlapi

parser = argparse.ArgumentParser()
parser.add_argument('--token', required=True, help='Diffbot Token')
args = parser.parse_args()

"""
You can use Diffbot with other pipeline components e.g. lemmatizer, vectors, etc. Here as an example we load en_core_web_md to output entity vectors, Diffbot provides NER so we can exclude that.
"""
nlp = spacy.load("en_core_web_md", exclude=["ner"])
nlp.add_pipe("diffbot", config={"token":args.token})

doc = nlp("Mike Tung is the founder and CEO of Diffbot. He is also an adviser at the StartX accelerator, and the leader of Stanford's entry in the DARPA Robotics Challenge. In a previous life, he was a grad student in the Stanford AI Lab, and a software engineer at eBay, Yahoo, and Microsoft. Tung studied electrical engineering and computer science at UC Berkeley and artificial intelligence at Stanford.")

print(doc)
for ent in doc.ents:
    print(f'{ent.text:>25}\t\t{ent.label_:>15}\t{ent.kb_id_:>25}\t{ent.vector if ent.has_vector else None}')