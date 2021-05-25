# spaCy wrapper for Diffbot Natural Language API

Extracts entities (e.g., people, organizations, locations) and facts about these entities from natural language text using Diffbot's natural language api (https://diffbot.com/products/natural-language/)

## Installation

```bash
pip install spacy-diffbot-nlapi
```

## Usage

```python
import spacy
import spacy_diffbot_nlapi

nlp = spacy.blank("en")
nlp.add_pipe("diffbot", config={"token":DIFFBOT_TOKEN, "lang":"en", "concurrent_connections":10})

texts = [
    "Mike Tung is the founder and CEO of Diffbot. He is also an adviser at the StartX accelerator, and the leader of Stanford's entry in the DARPA Robotics Challenge. In a previous life, he was a grad student in the Stanford AI Lab, and a software engineer at eBay, Yahoo, and Microsoft. Tung studied electrical engineering and computer science at UC Berkeley and artificial intelligence at Stanford.",
    "Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services.",
    "Facebook (FB) said Friday that it had acquired Giphy, a popular search engine for short, looping videos and animations called GIFs. The service will become part of Facebook's Instagram team, making it easier for people to find relevant GIFs for their Stories and direct messages.",
]

for doc in nlp.pipe(texts):
    print(doc)
    for ent in doc.ents:
        print(f'{ent.text:>25}\t\t{ent.label_:>15}\t{ent.kb_id_:>25}\t{ent._.uris}')
```

## Learn more

- [Documentation](https://docs.diffbot.com/docs/en/nl-index)
- [Demo](https://demo.nl.diffbot.com)