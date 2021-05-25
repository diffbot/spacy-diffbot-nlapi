import argparse
import spacy
import spacy_diffbot_nlapi

parser = argparse.ArgumentParser()
parser.add_argument('--token', required=True, help='Diffbot Token')
args = parser.parse_args()

nlp = spacy.blank("en")
nlp.add_pipe("diffbot", config={"token":args.token})

doc = nlp("Mike Tung is the founder and CEO of Diffbot. He is also an adviser at the StartX accelerator, and the leader of Stanford's entry in the DARPA Robotics Challenge. In a previous life, he was a grad student in the Stanford AI Lab, and a software engineer at eBay, Yahoo, and Microsoft. Tung studied electrical engineering and computer science at UC Berkeley and artificial intelligence at Stanford.")

print(doc)
for ent in doc.ents:
    print(f'{ent.text:>25}\t\t{ent.label_:>15}\t{ent.kb_id_:>25}\t{ent._.uris}')

"""
Prints:
                Mike Tung		         person	  ESGMaGV9uP0SuTmfPTtNEoA	['http://www.wikidata.org/entity/Q24050958']
                  founder		      job title	                       13	[]
                      CEO		      job title	                       15	[]
                  Diffbot		   organization	  EYX1i02YVPsuT7fPLUYgRhQ	['http://www.wikidata.org/entity/Q17052069']
                       He		         person	  ESGMaGV9uP0SuTmfPTtNEoA	['http://www.wikidata.org/entity/Q24050958']
                  adviser		      job title	                       14	[]
                   StartX		   organization	  EMMR7kK7EPO6Hb0MF_77NLg	['http://www.wikidata.org/entity/Q16981419']
                 Stanford		   organization	  EYIgQu0uKMdqz5168f_zH4Q	['http://www.wikidata.org/entity/Q41506']
 DARPA Robotics Challenge		          other	  Eot2uNj3HOW-YoO-evt-waA	['http://www.wikidata.org/entity/Q5204292']
                       he		         person	  ESGMaGV9uP0SuTmfPTtNEoA	['http://www.wikidata.org/entity/Q24050958']
          Stanford AI Lab		   organization	                        3	[]
        software engineer		      job title	                       16	[]
                     eBay		   organization	  EaaPCLxDtMDa0AujpWXF5TA	['http://www.wikidata.org/entity/Q58024']
                    Yahoo		   organization	  Em5UEtgzXML-jvN81wXljeQ	['http://www.wikidata.org/entity/Q37093']
                Microsoft		   organization	  EIsFKrN_ZNLSWsvxdQfWutQ	['http://www.wikidata.org/entity/Q2283']
                     Tung		         person	  ESGMaGV9uP0SuTmfPTtNEoA	['http://www.wikidata.org/entity/Q24050958']
   electrical engineering		          skill	  EgTVF40VgPY6KgukTD_9MTw	['http://www.wikidata.org/entity/Q43035']
         computer science		          skill	  ETezqyVyRMgCMXNzqF5S5Mg	['http://www.wikidata.org/entity/Q21198']
              UC Berkeley		   organization	  EbCgyZqjxNa-1luiX4LQ4sQ	['http://www.wikidata.org/entity/Q168756']
  artificial intelligence		          skill	  E_lYDrjmAMlKKwXaDf958zg	['http://www.wikidata.org/entity/Q11660']
                 Stanford		   organization	  EYIgQu0uKMdqz5168f_zH4Q	['http://www.wikidata.org/entity/Q41506']
"""