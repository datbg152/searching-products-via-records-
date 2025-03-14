import csv
from searchingPart.models import Product

def import_laptops(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Product.objects.create(
                brand=row['Company'],  # Mapping CSV field to model field
                model=row['Product'],
                processor=row['CPU_model'],
                ram=row['Ram'],
                storage=row['PrimaryStorage'],
                price=row['Price_euros']
            )
    print("Data imported successfully!")

# Run this function with your CSV file
import_laptops('/Users/ducanhtran/Downloads/laptop_prices.csv')