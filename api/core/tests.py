from faker import Faker
fake = Faker('it_IT')
for _ in range(10):
    print(fake.name())