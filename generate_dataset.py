import polars as pl
import numpy as np
from faker import Faker
import random
import datetime


fake = Faker('en_US')


products_amnt = 250
product_names = set()

while len(product_names) < products_amnt:
    product_names.add(fake.unique.word())

products = [(name, round(random.uniform(10, 1000), 2)) for name in product_names]

buyers_amnt = 1000
buyers = [(f'{fake.first_name()} {fake.last_name()}', fake.phone_number()) 
          for _ in range(buyers_amnt)]

sellers_amnt = 50
sellers = [(f'{fake.first_name()} {fake.last_name()}', fake.phone_number()) 
           for _ in range(sellers_amnt)]

expected_amnt = 10_000_000
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2025, 1, 1)
delta_days = (end_date - start_date).days

sales_data = []

for _ in range(expected_amnt):
    product_tuple = random.choice(products)
    buyer_tuple = random.choice(buyers)
    seller_tuple = random.choice(sellers)

    product = product_tuple[0]

    buyer = buyer_tuple[0]
    buyer_phone = buyer_tuple[1]
    shipped_to = fake.address()

    seller = seller_tuple[0]
    seller_phone = seller_tuple[1]

    date = start_date + datetime.timedelta(days=random.randint(0, delta_days))
    base_price = product_tuple[1]
    sale_price = round(base_price * (1 + random.uniform(-0.1, 0.1)), 2)
    units_sold = random.randint(1, 10)

    sales_data.append(
        (product, buyer, buyer_phone, shipped_to, seller, seller_phone, date, sale_price, units_sold))

df = pl.DataFrame(
    sales_data,
    schema=['product', 'buyer', 'buyer_phone', 'shipped_to', 
            'seller', 'seller_phone', 'date', 'sale_price', 'units_sold'],
)

df.write_csv('sales.csv')

print('File "sales.csv" saved!')
