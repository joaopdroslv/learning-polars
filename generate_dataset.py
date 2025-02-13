import polars as pl
import numpy as np
from faker import Faker
import random
import datetime


fake = Faker()


qtt_products = 50
products = set()
while len(products) < qtt_products:
    products.add(fake.word())
products = list(products)

qtt_buyers = 100
buyers = set()
while len(buyers) < qtt_buyers:
    buyers.add(f'{fake.first_name()} {fake.last_name()}')
buyers = list(buyers)

qtt_sellers = 25
sellers = set()
while len(sellers) < qtt_sellers:
    sellers.add(f'{fake.first_name()} {fake.last_name()}')
sellers = list(sellers)


qtt = 10000000

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2025, 1, 1)
delta_days = (end_date - start_date).days

data = {
    "product": [random.choice(products) for _ in range(qtt)],
    "buyer": [random.choice(buyers) for _ in range(qtt)],
    "seller": [random.choice(sellers) for _ in range(qtt)],
    "date": [start_date + datetime.timedelta(days=random.randint(0, delta_days)) for _ in range(qtt)],
    "sale_price": [round(random.uniform(10, 1000), 2) for _ in range(qtt)],
    "units_sold": [random.randint(1, 10) for _ in range(qtt)],
}

df = pl.DataFrame(data)
df.write_csv("sales.csv")

print("File 'sales.csv' saved!")
