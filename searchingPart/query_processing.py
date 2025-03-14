import spacy
import re

nlp = spacy.load("en_core_web_sm")

EXCLUDED_WORDS = {"find", "me", "an", "a", "the", "product", "products", "costing", "below", "under", "more", "than", "$", "'s", "’s"}

KNOWN_BRANDS = {"Apple", "Samsung", "Sony", "Dell", "Lenovo", "HP"}

def process_query(query):
    doc = nlp(query.lower())
    price_match = re.search(r"(\d+)", query)
    price = int(price_match.group(1)) if price_match else None
    query_no_price = re.sub(r"\d+", "", query.lower())

    keywords = [token.text for token in nlp(query_no_price) if token.text not in EXCLUDED_WORDS and token.is_alpha]

    brands = [word.capitalize() for word in keywords if word.capitalize() in KNOWN_BRANDS]

    keywords = [word for word in keywords if word.capitalize() not in KNOWN_BRANDS]

    return {
        "query_text": " ".join(keywords),
        "brand": brands[0] if brands else None,
        "max_price": price
    }