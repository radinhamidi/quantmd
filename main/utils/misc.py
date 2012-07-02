#coding=utf-8
import string
import random

def generate_random_string(length=32):
    chars = string.ascii_lowercase + string.digits
    return "".join(random.sample(chars, length))

