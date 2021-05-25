import aiohttp
import asyncio
import itertools
from spacy.language import Language
from spacy.tokens import Span

class NaturalLanguage:
    def __init__(self, token, lang, concurrent_connections):
        self.url = "https://nl.diffbot.com/v1/?fields=entities,facts&token={}".format(token)
        self.concurrent_connections = concurrent_connections
        self.lang = lang
        if not Span.has_extension("uris"):
            Span.set_extension("uris", default=[])
    
    def __call__(self, doc):
        return next(self.pipe([doc], 1))

    def pipe(self, docs, batch_size):
        items = iter(docs)
        while True:
            batch = list(itertools.islice(items, int(batch_size)))
            if len(batch) == 0:
                break
            loop = asyncio.get_event_loop()
            for doc in loop.run_until_complete(self._process_batch(batch)):
                yield doc

    async def _process_batch(self, docs):
        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=self.concurrent_connections)) as session:
            for doc in docs:
                task = asyncio.ensure_future(self._process_doc(session, doc))
                tasks.append(task)
            return await asyncio.gather(*tasks)

    async def _process_doc(self, session, doc):
        response = await self._request_json(session, doc.text)
        if response is None:
            return doc # failed to process the doc
        seen_tokens = set() # spaCy doesn't support overlapping mentions
        if "entities" in response:
            response["entities"].sort(reverse=True, key=lambda x: x["confidence"])
            ents = []
            for cluster_id, entity in enumerate(response["entities"]):
                allTypes = entity["allTypes"]
                if len(allTypes) == 0:
                    continue
                label = allTypes[0]["name"]
                kb_id = entity["diffbotUri"].rsplit('/', 1)[-1] if "diffbotUri" in entity else str(cluster_id)
                uris = entity["allUris"] if "allUris" in entity else []
                for mention in entity["mentions"]:
                    ent = doc.char_span(mention["beginOffset"], mention["endOffset"], label=label, kb_id=kb_id, alignment_mode="expand")
                    ent._.uris = uris
                    overlapping = False
                    for i in range(ent.start, ent.end):
                        if i in seen_tokens:
                            overlapping= True
                        seen_tokens.add(i)
                    if not overlapping:
                        ents.append(ent)
            doc.set_ents(ents, default="outside")
        return doc

    async def _request_json(self, session, text, tries=3):
        if tries == 0:
            return None
        document = {
            "content": text,
            "format" : "plain text",
            "lang": self.lang,
        }
        try:
            async with session.post(self.url, json=document) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 500:
                    return await self._request_json(session, text, tries-1)
                else:
                    return None
        except aiohttp.ClientConnectorError as e:
            await asyncio.sleep(1 if tries == 3 else 10)
            return await self._request_json(session, text, tries-1)


@Language.factory(
    "diffbot",
    assigns=["doc.ents", "token.ent_iob", "token.ent_type"],
    default_config={
        "lang": "en",
        "concurrent_connections": 10
    },
)
def diffbot_component(nlp, name, token, lang, concurrent_connections):
    return NaturalLanguage(token, lang, concurrent_connections)