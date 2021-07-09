import argparse
import spacy
from spacy.tokens import DocBin
import spacy_diffbot_nlapi

parser = argparse.ArgumentParser()
parser.add_argument('--token', required=True, help='Diffbot Token')
args = parser.parse_args()

# Run nlapi on texts and save to disk
nlp = spacy.blank("en")
nlp.add_pipe("diffbot", config={"token":args.token, "lang":"en", "concurrent_connections":10})

texts = [
    """AMD’s rise has come at the expense of Intel, which saw its share of the top 500 supercomputers shrink from 470 last June to 431 this year.""",
]
doc_bin = DocBin(attrs=["ENT_IOB", "ENT_TYPE", "ENT_KB_ID"], store_user_data=True)

for doc in nlp.pipe(texts):
    doc_bin.add(doc)

doc_bin.to_disk('tmp.spacy')

# Deserialize later
nlp = spacy.blank("en")
doc_bin = DocBin().from_disk('tmp.spacy')
docs = list(doc_bin.get_docs(nlp.vocab))

for doc in docs:
    print(doc)
    print(f'\t{"sentiment:":<15}{doc._.sentiment}')
    for ent in doc.ents:
        if ent.label_ != "organization":
            continue
        coref_cluster = ent._.coref_cluster
        print(f'\n{ent.text:<25}')
        print(f'\t{"cluster id:":<15}{coref_cluster["id"]}')
        print(f'\t{"name:":<15}{coref_cluster["name"]}')
        print(f'\t{"diffbotUri:":<15}{coref_cluster["diffbotUri"]}')
        print(f'\t{"sentiment:":<15}{coref_cluster["sentiment"]}')
        print(f'\t{"salience:":<15}{coref_cluster["salience"]}')
        print(f'\t{"uris:":<15}{",".join(coref_cluster["uris"])}')
        print(f'\t{"types:":<15}{",".join([ t["name"] for t in coref_cluster["types"]])}')

"""
Prints:
AMD’s rise has come at the expense of Intel, which saw its share of the top 500 supercomputers shrink from 470 last June to 431 this year.
	sentiment:     -0.8212621

AMD                      
	cluster id:    3
	name:          Advanced Micro Devices
	diffbotUri:    https://diffbot.com/entity/EbFKs23aHO_qdYiWKisqivA
	sentiment:     0.5173442
	salience:      0.97275597
	uris:          http://www.wikidata.org/entity/Q128896
	types:         organization

Intel                    
	cluster id:    0
	name:          Intel
	diffbotUri:    https://diffbot.com/entity/ExZ5EetfQM1m4UBAm6QAWCQ
	sentiment:     -0.8819347
	salience:      0.9801893
	uris:          http://www.wikidata.org/entity/Q248
	types:         organization

its                      
	cluster id:    0
	name:          Intel
	diffbotUri:    https://diffbot.com/entity/ExZ5EetfQM1m4UBAm6QAWCQ
	sentiment:     -0.8819347
	salience:      0.9801893
	uris:          http://www.wikidata.org/entity/Q248
	types:         organization
"""