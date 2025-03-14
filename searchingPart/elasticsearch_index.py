from elasticsearch import Elasticsearch, helpers
from searchingPart.models import Product  # Adjust import if needed
import django
import os

# Load Django settings
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "searchProject.settings")
    django.setup()

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

def reindex_data():
    """ Delete old index and reindex all products from PostgreSQL to Elasticsearch. """
    es.indices.delete(index="products", ignore=[400, 404])
    
    index_mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "brand": {"type": "keyword"},
                "model": {"type": "text"},
                "price": {"type": "float"}
            }
        }
    }
    
    es.indices.create(index="products", body=index_mapping, ignore=400)

    products = Product.objects.all()
    actions = [
        {
            "_index": "products",
            "_id": product.id,
            "_source": {
                "id": product.id,
                "brand": product.brand,
                "model": product.model,
                "price": float(product.price)
            }
        }
        for product in products
    ]

    helpers.bulk(es, actions)
    print(f"✅ Reindexed {len(products)} products successfully!")

# 🔹 Add Missing Functions (Fix ImportError)
def index_product(product):
    """ Index a single product in Elasticsearch. """
    es.index(index="products", id=product.id, body={
        "id": product.id,
        "brand": product.brand,
        "model": product.model,
        "price": float(product.price)
    })

def delete_product(product_id):
    """ Delete a product from Elasticsearch by ID. """
    es.delete(index="products", id=product_id, ignore=[400, 404])

# Run this function when the script is executed directly
if __name__ == "__main__":
    reindex_data()