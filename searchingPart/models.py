from django.db import models
from django.contrib.postgres.search import SearchVectorField

class Product(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=200)
    processor = models.CharField(max_length=200)
    ram = models.CharField(max_length=50)
    storage = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.brand} {self.model}"
    
class Transcription(models.Model):
    filename = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    search_vector = SearchVectorField(null=True)  # Enables full-text search
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['text']),  # Speeds up text searches
        ]

    def __str__(self):
        return self.filename