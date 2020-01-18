import heapq
from random import randint

class Astar:
    def __init__(self):
        pass

class greedy:
    def __init__(self):
        pass


class Struct:
    def __init__(self):
        self.parent = [] # No parent
        self.node = {}

    def addNode(self,parent, node, cost, g):
        if not node in self.node:
            self.createNode(node, parent, cost, g)

    def getNode(self, node):
        if not node in self.node:
            return self.createNode(node)
        else:
            return self.node[node]
    
    def exists(self, node):
        return node in self.node

    def createNode(self,node, parent=0, cost=0, g=0):
        self.node[node] = {
                'parent':parent,
                'cost':cost,
                'g':g
            }
        return self.node[node]

# The biggest value first therefor priority is negative
class Queue:
    def __init__(self):
        self.elements = []
    def isEmpty(self):
        return len(self.elements) == 0
    def add(self, item, priority):
        heapq.heappush(self.elements,(priority,item))

    def remove(self):
        return heapq.heappop(self.elements)[1]
    def printArray(self):
        return self.elements
