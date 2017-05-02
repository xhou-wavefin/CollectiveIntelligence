from random import random, randint
import math

def winePrice(rating, age):
	peak_age = rating - 50
	price = rating / 2
	if age > peak_age:
		price = price * (5 - (age - peak_age))
	else:
		price = price * (5 * ((age + 1) / peak_age))

	if price < 0:
		price = 0

	return price

def wineSet1():
	rows = []

	for in range(300):
		rating = random() * 50 + 50
		age = random() * 50

		price = winePrice(rating, age)

		price *= (random() * 0.4 + 0.8)

		rows.append({'input':(rating, age),
			'result': price})

	return rows

