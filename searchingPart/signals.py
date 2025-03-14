from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from .elasticsearch_index import index_product, delete_product

# Automatically index new or updated products
@receiver(post_save, sender=Product)
def index_product_signal(sender, instance, **kwargs):
    index_product(instance)  # Index the product in Elasticsearch

# Automatically delete product from Elasticsearch when removed
@receiver(post_delete, sender=Product)
def delete_product_signal(sender, instance, **kwargs):
    delete_product(instance.id)  # Delete from Elasticsearch