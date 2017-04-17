import re
import math

def getWords(doc):
	splitter = re.compile('\\W*')

	words = [s.lower() for s in splitter.split(doc) if len(s) > 2 and len(s) < 20]

	return dict([(w, 1) for w in words])

class classifier:
	def __init__(self, getFeatures, filename = None):
		self.featureCatCount = {}
		self.catCount = {}
		self.getFeatures = getFeatures

	def incFeatureCatCount(self, f, cat):
		self.featureCatCount.setdefault(f, {})
		self.featureCatCount[f].setdefault(cat, 0)
		self.featureCatCount[f][cat] += 1

	def incCatCount(self, cat):
		self.catCount.setdefault(cat, 0)
		self.catCount[cat] += 1

	def featureCount(self, f, cat):
		if f in self.featureCatCount and cat in self.featureCatCount[f]:
			return float(self.featureCatCount[f][cat])
		return 0.0

	def itemCount(self, cat):
		if cat in self.catCount:
			return float(self.catCount[cat])
		return 0

	def totalItemCount(self):
		return sum(self.catCount.values())

	def categories(self):
		return self.catCount.keys()

	def train(self, item, cat):
		features = self.getFeatures(item)

		for f in features:
			self.incFeatureCatCount(f, cat)

		self.incCatCount(cat)
		
