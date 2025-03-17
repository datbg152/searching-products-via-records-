# 📌 Overview

This is a personal project designed to explore AI and search technologies. The system utilizes OpenAI's Whisper Small model to convert users' voice into text, which is then used to search for relevant products.

---

# 🛠 Technologies Used

- **Python** (Django, Spacy, Sounddevice, Numpy, Scipy)
- **Whisper** (OpenAI speech-to-text model)
- **Elasticsearch** (for indexing & searching products)
- **Docker** (optional, for running services)

---

# ✨ Features

- 🎤 **Voice recording & transcription** using Whisper
- 🔍 **Search optimization** with NLP (Spacy) to extract keywords
- 📊 **Product searching** with Elasticsearch
- 🛠 **Django-based backend** for query processing

---

# 🎯 Purpose of This Project

- Understand AI integration in web systems by using Whisper for voice processing.
- Learn how to use Elasticsearch indexing to improve search efficiency and latency.
- Experiment with NLP techniques for query filtering and keyword extraction.

---

# 🔄 Project Flow Overview

### 1️⃣ User Records Voice Command 🎤

- The user records a voice query (e.g., *"Find me Apple's products costing below \$1000."*)
- The recorded audio (`.wav` file) is saved in the `recordings/` folder.

### 2️⃣ Automatic Transcription with Whisper AI 📝

- The recorded `.wav` file is transcribed into a `.json` file.
- The JSON file contains:
  ```json
  {
      "filename": "20250311_201842.wav",
      "text": "Find me Apple's products costing below $1000.",
      "language": "en"
  }
  ```

### 3️⃣ Text Processing with Spacy 🧠

- The transcribed text is **filtered using Spacy's NLP model**.
- **Stopwords are removed**, and key entities (e.g., *brand names, price*) are extracted.
- Example of processed query:
  ```json
  {
      "query_text": "",
      "brand": "Apple",
      "max_price": 1000
  }
  ```

### 4️⃣ Searching Products in Elasticsearch 🔍

- The extracted **brand and price** are used as search parameters.
- Elasticsearch **queries the product database** and returns relevant products.
- Example response:
  ```json
  {
      "20250311_201842.json": [
          {
              "_index": "products",
              "_source": {
                  "brand": "Apple",
                  "model": "MacBook Air",
                  "price": 898.94
              }
          },
          {
              "_index": "products",
              "_source": {
                  "brand": "Apple",
                  "model": "MacBook Air",
                  "price": 998.0
              }
          }
      ]
  }
  ```

---

# 📌 Future Improvements

- Extend voice query support to multiple languages.
- Improve NLP entity extraction for more complex queries.
- Optimize Elasticsearch indexing for faster search performance.

---


