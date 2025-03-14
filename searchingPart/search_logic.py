import json
import os
from elasticsearch import Elasticsearch
from searchingPart.query_processing import process_query

RECORDINGS_PATH = "recordings/"
es = Elasticsearch("http://localhost:9200")

def load_json_transcription(filename):
    file_path = os.path.join(RECORDINGS_PATH, filename)
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["text"].strip()

def search_products(query):
    processed_query = process_query(query)

    search_body = {
        "query": {
            "bool": {
                "must": [{"match_all": {}}] if not processed_query["query_text"] else [
                    {"match": {"model": processed_query["query_text"]}}
                ],
                "filter": []
            }
        }
    }

    if processed_query["max_price"]:
        search_body["query"]["bool"]["filter"].append({
            "range": {"price": {"lte": processed_query["max_price"]}}
        })

    if processed_query["brand"]:
        search_body["query"]["bool"]["filter"].append({
            "match": {
                "brand": {
                    "query": processed_query["brand"],
                    "operator": "and",
                    "fuzziness": "AUTO"
                }
            }})

    print("\n🔍 Elasticsearch Query:\n", json.dumps(search_body, indent=4))

    response = es.search(index="products", body=search_body)
    return response["hits"]["hits"]

def search_from_json(filename):
    transcription = load_json_transcription(filename)
    if isinstance(transcription, dict):
        query_text = transcription.get("text", "")
    else:
        query_text = transcription
    results = search_products(query_text)
    return results