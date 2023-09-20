# from inspect import signature
from random import randint
from faker import Faker

import re

import string as s
from random import SystemRandom as sr


def slugify(slug_name):
    slug_name = slug_name.lower().strip()
    slug_name = re.sub(r'[^\w\s-]', '', slug_name)
    slug_name = re.sub(r'[\s_-]+', '-', slug_name)
    slug_name = re.sub(r'^-+|-+$', '', slug_name)
    return slug_name


def rand_ratio():
    return randint(840, 900), randint(473, 573)


fake = Faker('pt_BR')


def make_strong_string():
    print("".join(sr().choices(s.ascii_letters + s.punctuation, k=64)))


# print(signature(fake.random_number))

