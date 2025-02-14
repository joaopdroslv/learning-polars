import polars as pl
import numpy as np
from faker import Faker
import random
import datetime
from datetime import date


faker = Faker('en_US')

payment_methods = [
    'Credit Card (Visa)',
    'Credit Card (MasterCard)',
    'Credit Card (American Express)',
    'Debit Card',
    'Pix',
    'Cash',
    'Bank Transfer',
    'Cryptocurrency (Bitcoin)',
    'Cryptocurrency (Ethereum)',
    'PayPal',
    'Google Pay',
    'Apple Pay'
]

products_amnt = 250
product_names = set()

while len(product_names) < products_amnt:
    product_names.add(faker.unique.word())

products = [(name, round(random.uniform(10, 1000), 2)) for name in product_names]

buyers_amnt = 1000
buyers = [faker.profile() for _ in range(buyers_amnt)]

sellers_amnt = 50
sellers = [faker.profile() for _ in range(sellers_amnt)]

start_date = datetime.date(2010, 1, 1)
end_date = datetime.date(2025, 1, 1)
delta_days = (end_date - start_date).days

expected_amnt = 10_000_000
sales_data = []

for _ in range(expected_amnt):
    buyer_profile = random.choice(buyers)
    buyer_name = buyer_profile['name']
    buyer_sex = buyer_profile['sex']
    buyer_age = random.randint(21, 75)
    buyer_address = buyer_profile['address']
    buyer_contact = buyer_profile['mail']

    seller_profile = random.choice(sellers)
    seller_name = seller_profile['name']
    seller_sex = seller_profile['sex']
    seller_age = random.randint(21, 50)
    seller_address = seller_profile['address']
    seller_contact = seller_profile['mail']

    product_tuple = random.choice(products)
    product_name = product_tuple[0]
    base_price = product_tuple[1]

    sale_date = start_date + datetime.timedelta(days=random.randint(0, delta_days))
    units_sold = random.randint(1, 10)
    unit_price = round(base_price * (1 + random.uniform(-0.1, 0.1)), 2)

    payment_method = random.choice(payment_methods)

    discount = True if random.choice([1, 3, 5, 7, 10]) % 2 == 0 else False 
    discount_perc = random.randint(5, 10) if discount else 0

    sales_data.append(
        (product_name, buyer_name, buyer_sex, buyer_age, buyer_address, buyer_contact, 
         seller_name, seller_sex, seller_age, seller_address, seller_contact, sale_date,
         units_sold, unit_price, payment_method, discount, discount_perc))

df = pl.DataFrame(
    sales_data,
    schema=['product_name', 'buyer_name', 'buyer_sex', 'buyer_age', 'buyer_address', 'buyer_contact', 
            'seller_name', 'seller_sex', 'seller_age', 'seller_address', 'seller_contact', 'sale_date',
            'units_sold', 'unit_price', 'payment_method', 'discount', 'discount_perc'],
)

df.write_csv('sales.csv')

print('File "sales.csv" saved!')
