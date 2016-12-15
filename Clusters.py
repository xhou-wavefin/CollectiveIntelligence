def readFile(filename):
	lines = [line for line in file(filename)]

	# First line is the column titles
	colnames = lines[0].strip().split('\t')[1:]

	rownames = []
	data = []
	for line in lines[1:]:
		p = line.strip().split('\t')
		# First column in each row is the rowname
		rownames.append(p[0])
		# The data for this row is the remainder of the row
		data.append([float(x) for x in p[1:]])

	return rownames, colnames, data

from math import sqrt
def pearson(v1, v2):
	# Simple sums
	sum1 = sum(v1)
	sum2 = sum(v2)

	# Sums of the squares
	sum1Sq = sum([pow(v, 2) for v in v1])
	sum2Sq = sum([pow(v, 2) for v in v2])

	# Sum of the products
	pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

	# Caluculate Pearson score
	num = pSum - (sum1 * sum2 / len(v1))
	den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
	if den ==0:
		return 0

	return 1.0 - num / den

class bicluster:
	def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):
		self.left = left
		self.right = right
		self.vec = vec
		self.id = id
		self.distance = distance

def hcluster(rows, distance = pearson):
	distances = {}
	currentClustId = -1

	clust = [bicluster(rows[i], id = i) for i in range(len(rows))]

	while len(clust) > 1:
		lowestPair = (0, 1)
		closest = distance(clust[0].vec, clust[1].vec)

		# Loop through every pair looking for the smallest distance
		for i in range(len(clust)):
			for j in range(i + 1, len(clust)):
				# Distance is the cache of distance calculations
				if (clust[i].id, clust[j].id) not in distances:
					distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

				d = distances[(clust[i].id, clust[j].id)]

				if d < closest:
					closest = d
					lowestPair = (i, j)

		# Calculate the average of the two clusters
		mergeVec = [
		(clust[lowestPair[0]].vec[i] + clust[lowestPair[1]].vec[i]) / 2.0
		for i in range(len(clust[0].vec))
		]

		# Create the new cluster
		newCluster = bicluster(mergeVec, left = clust[lowestPair[0]],
							right = clust[lowestPair[1]],
							distance = closest, id = currentClustId)

		# Cluster ids that weren't in the original set are negative
		currentClustId -= 1
		del clust[lowestPair[1]]
		del clust[lowestPair[0]]
		clust.append(newCluster)

	return clust[0]

def printClust(clust, labels = None, n = 0):
	# Indent to make a hierarchy layout
	for i in range(n): print ' ',

	if clust.id < 0:
	# Negative id means that this is branch
		print '-'

	else:
		# Positive id means that this is an endpoint
		if labels == None: print clust.id
		else: print labels[clust.id]

	# Now print the right and left branches
	if clust.left != None: printClust(clust.left, labels = labels, n = n + 1)
	if clust.right != None: printClust(clust.right, labels = labels, n = n + 1)

from PIL import Image, ImageDraw

def getHeight(clust):
	# Is this an endpoint, if so the height is just 1
	if clust.left == None and clust.right == None: return 1

	# Otherwise the height is the same of the heights of each branch
	return getHeight(clust.left) + getHeight(clust.right)

def getDepth(clust):
	# The distance of an endpoint is 0.0
	if clust.left == None and clust.right == None: return 0

	# The depth of a branch is the greater of its two sides plus its own distance
	return max(getDepth(clust.left), getDepth(clust.right)) + clust.distance

def drawDendrogram(clust, labels, bmp = 'Clusters.bmp'):
	# Height and width
	h = getHeight(clust) * 20
	w = 1200

	depth = getDepth(clust)

	# Width is fixes, so scale distances accordingly
	scaling = float(w - 150) / depth

	# Create a new image with a white background
	img = Image.new('RGB', (w, h), (255, 255, 255))
	draw = ImageDraw.Draw(img)

	# Draw the first node
	drawNode(draw, clust, 10, (h / 2), scaling, labels)
	img.save(bmp)

def drawNode(draw, clust, x, y, scaling, labels):
	if clust.id < 0:
		h1 = getHeight(clust.left) * 20
		h2 = getHeight(clust.right) * 20
		top = y - (h1 + h2) / 2
		bottom = y + (h1 + h2) / 2
		# Line length
		ll = clust.distance * scaling
		# Vertical line from this cluster to children
		draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill = (255, 0, 0))

		# Horizontal line to left item
		draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill = (255, 0, 0))

		# Horizontal line to right item
		draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill = (255, 0, 0))

		# Call the function to draw the left and right nodes
		drawNode(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
		drawNode(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)

	else:
		# If this is an endpoint, draw the item label
		draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))

