#A* pathfinding algorithm implemented and written by Bahram Esmailian

import numpy as np

#g score is the length from the starting point to the node. h score is the heuristic shortest estimated path from the node to the goal. f score is the total length from start to goal
#if the path goes through the arbitrary node. f = g + h

#Pythagorean Theorem to find the straight line distance between a node and the end node
def h(node): return ((goal.x - node.x)**2 + (goal.y - node.y)**2)**(1/2)

#constructs and returns the shortest path
def construct_path(current):
	path = [current]
	while current.camefrom != None:
		path = [current.camefrom] + path
		current = current.camefrom
	return path


class Node(object):
	"""An arbutrary position within a map with position (x,y)"""

	def __init__(self, x, y, goal = False):
		
		self.x = x
		self.y = y
		self.camefrom = None
		self.gscore = float(np.inf)
		if goal != True:
			self.hscore = h(self)
		else:
			self.hscore = 0
		self.fscore = float(np.inf)

	def look(self):
		#all possible locations of the node's neighbors in [y,x] form WARNING THIS ASSUMES THAT YOUR POSITION CAN MOVE DIAGONALLY
		neighbor_p = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		self.neighbors = []
		#checks if the neighbor position is inside of the map and adds it to the node's neighbor list
		for neighbor in neighbor_p:
			if self.y+neighbor[0] >= n or self.y+neighbor[0] < 0 or self.x+neighbor[1] >= m or self.x+neighbor[1] < 0:
				continue
			else:
				self.neighbors.append(node_map[int(self.y+neighbor[0])][int(self.x+neighbor[1])])

#insert start/goal positions in (x,y) form, build your n x m matrix/map
def a_star(start_position, goal_position, rows, columns):
	global node_map, n, m, goal

	goal = Node(goal_position[0], goal_position[1], goal = True)
	start = Node(start_position[0], start_position[1])
	n = rows
	m = columns

	node_map = [[0]*m for i in range(n)]

	#filling the 2D node array with node objects corresponding to their position within the array
	for i in range(n):
		for j in range(m):
			node_map[i][j] = Node(j,i)

	#overriding start and stop nodes in the 2D array
	node_map[goal.y][goal.x] = goal
	node_map[start.y][start.x] = start

	start.gscore = 0

	openset = [start]

	while len(openset) > 0:
		fscore_min = openset[0].fscore
		smallest = 0
		#searches through the openset for the smallest f value and sets the corresponding node to current
		for i in range(len(openset)):
			if openset[i].fscore < fscore_min:
				fscore_min = openset[i].fscore
				smallest = i

		current = openset.pop(smallest)

		if current == goal:
			return construct_path(current)

		#find neighbors for current node
		current.look()

		#for each neighbor of current node the gscores are compared and replaced if the current path is faster than the previous
		#adds neighbors to openset if a shorter path if found
		for neighbor in current.neighbors:
			tentative_gscore = current.gscore + 1
			if tentative_gscore < neighbor.gscore:
				neighbor.gscore = tentative_gscore
				neighbor.camefrom = current
				neighbor.fscore = neighbor.gscore + neighbor.hscore
				if neighbor not in openset:
					openset.append(neighbor)


#at its current state the function will return the shortest path to the goal, however there are no "walls" or "obstacles"
#walls/obstacles are left up to the reader to create, HINT: If a node cannot "see" one of its neighbors, it cannot reach it, therefore it acts as a barrier
#one EASY way you could do this is to create a function that removes the obstacle position in node.neighbors from a node istance
#for example, an obstacle is to the left of a node, the neighbor that you want to remove is [0,-1], remember the coordinates are in [y,x] form 

#runs the algorithm for a 10x10 matrix with start at the top left and goal at bottom right
a_star((0,0),(9,9),10,10)
