#Imports from repository below
import queue
import time
import sys

#Heuristic class to perform all the heuristic calculations
#rowPosition finds the row position of each item in the list
#columnPosition get the column position of each item in the list
#returns the cost of each heauristics
class heuristic:

    def __init__(self, heuristicCost, currentState,goalcurrentState, function):
        self.heuristicCost = heuristicCost
        self.currentState = currentState
        self.goalcurrentState = goalcurrentState
        self.function = function

    def rowPosition(self,index):
        if index in [0,1,2]:
            return 1
        elif index in [3,4,5]:
            return 2
        elif index in [6,7,8]:
            return 3

    def columnPosition(self,index):
        if index in [0,3,6]:
            return 1
        elif index in [1,4,7]:
            return 2
        elif index in [2,5,8]:
            return 3

    def heuristicsCost(self):

        # the number of puzzle pieces out of place
        if self.function == 'outOfPosition':
            for position in zip(self.currentState, self.goalcurrentState):
                if position[0] != position[1]:
                    self.heuristicCost += 1
                else:
                    continue
        # manhattan distance of the puzzle pieces
        elif self.function == 'manhattanDistance':
                for position in self.goalcurrentState:
                    if position != 0:
                        self.heuristicCost += (abs(self.rowPosition(self.goalcurrentState.index(position)) - self.rowPosition(self.currentState.index(position))) + abs(self.columnPosition(self.goalcurrentState.index(position)) - self.columnPosition(self.currentState.index(position))))

        # chebyshev cost function, returns the maximum of the total column movement and row movements
        elif self.function == "chebyshev":
            horizintal = 0
            vertical = 0
            for position in self.goalcurrentState:
                if position != 0:
                    horizintal += abs(self.rowPosition(self.goalcurrentState.index(position)) - self.rowPosition(self.currentState.index(position)))
                    vertical += abs(self.columnPosition(self.goalcurrentState.index(position)) - self.columnPosition(self.currentState.index(position)))
            self.heuristicCost = max(horizintal,vertical)*2

        #calculates then sequence plus the total distance
        elif self.function == 'hheuristics':
            for position in self.goalcurrentState:
                if position != 0:
                    if self.goalcurrentState.index(position) - self.currentState.index(position) != 0:
                        if self.currentState.index(position) == 4:
                            self.heuristicCost += ((1*3)+(abs(self.rowPosition(self.goalcurrentState.index(position)) - self.rowPosition(self.currentState.index(position))) + abs(self.columnPosition(self.goalcurrentState.index(position)) - self.columnPosition(self.currentState.index(position)))))
                        elif self.currentState.index(position) != 4:
                            self.heuristicCost += ((1*3)+(abs(self.rowPosition(self.goalcurrentState.index(position)) - self.rowPosition(self.currentState.index(position))) + abs(self.columnPosition(self.goalcurrentState.index(position)) - self.columnPosition(self.currentState.index(position)))))

                    elif self.goalcurrentState.index(position) - self.currentState.index(position) == 0:
                        self.heuristicCost += 0


        else:
            for x in self.goalcurrentState:
                self.heuristicCost += (self.goalcurrentState.index(x) - self.currentState.index(x))**2

        return self.heuristicCost



#list of accoumulators used for storing nodes
#visitedNodes stores all the visited Nodes
#pathToSolution stores the path to the solution after a solution is found
#parentNodes stores all the parents Nodes
#children stored all the child nodes

visitedNodes = queue.Queue()
pathToSolution = queue.Queue()
parentNodes = queue.Queue()
children = queue.Queue()
depth = 0
priority = 1
goalState = [1,2,3,8,0,4,7,6,5]

#class to modify the inputs in form of list
# searchZeroLocation searches for the location of zero in the list
#positionDictionary looks for all the posible moves
#positionSwap makes the moves and stores in the queue
#confirmAfunction confirms if an input is valid or not
class filterInput:

    def __init__(self, list):
        self.myList = list
        self.indexOfZero = 0
        self.depth = 0
        self.priority = 0

    def searchZeroLocation(self):
        """
        Returns the position of zero in the Function
        """
        if self.myList.count(0) > 0:
              self.indexOfZero = self.myList.index(0)
              return self.indexOfZero;
        else:
            return "Wrong initial"


    def positionDictionary(self):
        """
        identies the swap spots for different item... swapping with the zero location
        """
        zeroLocation = self.searchZeroLocation()
        global depth
        switcher = {
            0: [3,1],
            1: [0,4,2],
            2: [1,5],
            3: [0,6,4],
            4: [3,1,7,5],
            5: [4,2,8],
            6: [3,7],
            7: [6,4,8],
            8: [7,5]
        }
        depth = depth + 1
        return switcher.get(zeroLocation, "nothing")

    def positionSwap(self):
        locationDictionary = self.positionDictionary()
        myList1 = []
        myList2 = []
        for num in locationDictionary:
            del myList1[:]
            myList1.extend(self.myList)
            indexOfZero = myList1.index(0)
            myList1[indexOfZero], myList1[num] = myList1[num], myList1[indexOfZero]
            if list(myList1[::])not in parentNodes.queue and list(myList1[::]) not in children.queue:
                myList2.append(list(myList1[::]))
                self.priority = priority + 1
                #print(priority)
        parentNodes.put(self.myList)
        children.put(myList2)
        return myList2

    def positionDictionary2(self):
        """
        identies the swap spots for different item... swapping with the zero location
        """
        zeroLocation = self.searchZeroLocation()
        global depth
        switcher = {
            0: [1,3],
            1: [2,4,0],
            2: [5,1],
            3: [4,6,0],
            4: [5,7,1,3],
            5: [8,2,4],
            6: [7,3],
            7: [8,4,6],
            8: [5,7]
        }
        return switcher.get(zeroLocation, "nothing")

    def positionSwap2(self):
        locationDictionary = self.positionDictionary2()
        myList1 = []
        myList2 = []
        for num in locationDictionary:
            del myList1[:]
            myList1.extend(self.myList)
            indexOfZero = myList1.index(0)
            myList1[indexOfZero], myList1[num] = myList1[num], myList1[indexOfZero]
            if list(myList1[::])not in parentNodes and list(myList1[::]) not in children:
                myList2.append(list(myList1[::]))
                self.priority = priority + 1
                #print(priority)
        parentNodes.append(self.myList)
        children.append(myList2)
        return myList2



def confirmAfunction(myList = [], *args):
    """
    confirm if an input is valid...
    """
    greaterThanEight = filter(lambda num:num>8, myList)
    if list(greaterThanEight) == [] and myList.count(0) == 1 and len(myList) == 9:
        return True
    else:
        return False


#the buildInput input function is used to build the input and return list, depth, and algorithm name
def buildInput():
    depp = 0
    #get input(INITIAL STATE) for the console in the list format 1,2,3,4,5,5,6,7,8
    initial = input("Enter the initial state:  ")
    input1 = initial.split(",")
    input11 = list(map(int, input1))
    checker1 = confirmAfunction(input11)

    while(checker1 == False):
        initial = input("Re-Enter the initial state Format:- 1,2,3,4,5:  ")
        input1 = initial.split(",")
        input11 = list(map(int, input1))
        checker1 = confirmAfunction(input11)

    strategyType = input("Select Strategy from list below\n Enter:- \n 'A' for Depth First...........\n 'B' for breadth First..........\n 'C' for Iterative Depending..........\n 'D' for Heuristics.........\n")
    print("")


    if strategyType.upper() == "A":
        strategyType = "depthFirst"
        depp = input("Enter depth limt you want to reach: ")
    elif strategyType.upper() == "B":
        strategyType = "breadthFirst"
    elif strategyType.upper() == "C":
        strategyType = "iterativeDeepening"
    elif strategyType.upper() == "D":
        strategyType = input("Select Heuristic type\n\n Enter:- \n 'A' for Tile Out Of Place..........\n 'B' for Manhanttan..........\n 'C' for H heuristic..........\n 'D' Chevychev..........\n")
        print(">>>>>>>>>>>>>>>>>")
        print(">>>>>>A,B,C OR D?")

        if strategyType.upper() == "A":
            strategyType = "outOfPosition"
        elif strategyType.upper() == "B":
            strategyType = "manhattanDistance"
        elif strategyType.upper() == "C":
            strategyType = "hheuristics"
        elif strategyType.upper() == "D":
            strategyType = "chebyshev"
        else:
            strategyType = input("Select correct strate between A TO D\n Enter A for Tile Out Of Place, B for Manhanttan, C for H heuristic and D Chevychev\n")
            print(">>>>>>>>>>>>>>>>>")
            print(">>>>>>A,B,C OR D?")
    return input11, strategyType, int(depp)

def searchZeroLocation2(myList = [], *args):
    """
    Returns the position of zero in the Function
    """
    if myList.count(0) > 0:
          indexOfZero = myList.index(0)
          return indexOfZero;
    else:
        return "Wrong initial"

input11, strategyType, depp = buildInput()

#function for breadth first calculations
def breadthFirst(input, algorithm):
    allNodes = queue.Queue()
    allNodes.put((0,input))

    #add to the queue if not already in there
    def itterate(depth, myList = [], *args):
        global priority
        swappedTiles = []
        depth +=1
        swappedTiles = filterInput(myList).positionSwap()
        for tile in swappedTiles:
            priority += 1
            if tile not in allNodes.queue:
                allNodes.put((depth,tile))

    currentNode = input
    while not allNodes.empty() and currentNode != goalState:
        depth,currentNode = allNodes.get()

        if currentNode not in visitedNodes.queue:
            visitedNodes.put(currentNode)
            itterate(depth,currentNode)
        if currentNode == goalState:
            forPrint = []
            for item in visitedNodes.queue:
                forPrint.append(item)
            print("Visited list =\n {}".format(forPrint))
            print("..............................................................................\n")
            print("Algorith is {}".format(algorithm))
            print("total number of visited nodes is {}".format(visitedNodes.qsize()))
            print("total number of generated nodes is {}".format(priority))
            print("Depth to the solution is {}".format(depth))


#this functions does all the heuristic calculations
def heuristics(input, algorithm):
    start_time = time.time()
    allNodes = queue.PriorityQueue()
    allNodes.put((0, input11, 0))

    #add to the queue if not already in there
    def itterate(prio, depth, myList = [], *args):
        global priority
        swappedTiles = []
        swappedTiles = filterInput(myList).positionSwap()
        de = depth +1
        for tile in swappedTiles:
            priority += 1
            if tile not in allNodes.queue:
                if  algorithm in ["outOfPosition", "manhattanDistance","hheuristics","chebyshev"]:
                    pp = de + heuristic(0,tile, goalState, algorithm).heuristicsCost()
                    depth +=de
                    allNodes.put((pp, tile, de))
                else:
                    pp = de + 1
                    depth +=de
                    allNodes.put((pp, tile, de))

    currentNode = input
    print("Wait for the processing...")
    while not allNodes.empty() and currentNode != goalState:
        priori,currentNode,ddd = allNodes.get()

        if currentNode not in visitedNodes.queue:
            visitedNodes.put((currentNode))
            itterate(priori, ddd, currentNode)

        if currentNode == goalState:
            forPrint = []
            for item in visitedNodes.queue:
                forPrint.append(item)
            print("Path to the solution nodes=\n {}".format(forPrint))
            print("..............................................................................\n")
            print("Strategy type is {}".format( algorithm))
            print("Total number of visited nodes is {}".format(visitedNodes.qsize()))
            print("Depth to the solution is {}".format(ddd))
            print("Total  number of visited nodes is {}".format(priority))
            print("--- %s seconds ---" % (time.time() - start_time))



#function for dpeth first calculations
def depthFirst(dep, input, algorithm):
    allNodes = queue.LifoQueue()
    allNodes.put((0, input))

    #add to the queue if not already in there
    def itterate(depth, myList = [], *args):
        swappedTiles = []
        global priority
        de = depth+1
        swappedTiles = filterInput(myList).positionSwap()
        for tile in swappedTiles:
            priority = priority+1
            if tile not in allNodes.queue:
                allNodes.put((de,tile))

    currentNode = input11
    print("Wait for the processing...")
    while not allNodes.empty() and currentNode != goalState:
        start_time = time.time()
        depth, currentNode = allNodes.get()

        if currentNode not in visitedNodes.queue and depth <= dep:
            visitedNodes.put(currentNode)
            itterate(depth,currentNode)
        elif depth > dep:
            print("No solution at this point")
        else:
            continue

        if currentNode == goalState:
            forPrint = []
            for item in visitedNodes.queue:
                forPrint.append(item)
            print("Visited list =\n {}".format(forPrint))
            print("..............................................................................\n")
            print("Strategy type is {}".format( algorithm))
            print("total number of visited nodes is {}".format(visitedNodes.qsize()))
            print("Total number of generated nodes {}".format(priority))
            print("Depth to the solution is {}".format(depth))
            print("--- %s seconds ---" % (time.time() - start_time))




#function for iterative deepening calculations
def iterativeDeepening(dep, input, algorithm):
    allNodes = queue.LifoQueue()
    allNodes.put((0, input))

    #add to the queue if not already in there
    def itterate(depth, myList = [], *args):
        global priority
        swappedTiles = []
        de = depth+1
        swappedTiles = filterInput(myList).positionSwap()
        for tile in swappedTiles:
            priority +=1
            if tile not in allNodes.queue:
                allNodes.put((de,tile))

    currentNode = input11
    print("Wait for the processing...")
    while not allNodes.empty() and currentNode != goalState:
        start_time = time.time()
        depth, currentNode = allNodes.get()

        if currentNode not in visitedNodes.queue:
            visitedNodes.put(currentNode)
            itterate(depth,currentNode)
        elif depth > dep:
            print("No solution at this point")
            break
        else:
            continue

        if currentNode == goalState:
            forPrint = []
            for item in visitedNodes.queue:
                forPrint.append(item)
            print("Visited list =\n {}".format(forPrint))
            print("..............................................................................\n")
            print("Strategy type is {}".format( algorithm))
            print("total number of visited nodes is {}".format(visitedNodes.qsize()))
            print("Total number of generated nodes {}".format(priority))
            print("--- %s seconds ---" % (time.time() - start_time))
            exit()




#run program according to the inputs and stra chosen.......
#breadthFirst calls breadthFirst function
#if strategyTypes one of the heauristics, call the heuristic function
#dept calls the depthFirst function
#iterativeDeepening calls the iterativeDeepening function

if strategyType == "breadthFirst":
    breadthFirst(input11, strategyType)
elif strategyType in ["outOfPosition", "manhattanDistance", "hheuristics", "chebyshev"]:
    heuristics(input11, strategyType)
elif strategyType == "depthFirst":
    depthFirst(depp, input11,strategyType)
elif strategyType == "iterativeDeepening":
    countter =0
    while countter < sys.maxsize:
        iterativeDeepening(countter, input11,strategyType)
        countter+=1
