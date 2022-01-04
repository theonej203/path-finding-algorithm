import pygame, math
from color import*
from queue import PriorityQueue
clock = pygame.time.Clock()


class node:
    def __init__(self,col,row,space,colAndRow,nodeNum,window):
        self.num = nodeNum
        self.col = col
        self.row = row
        self.x = col*space
        self.y = row*space
        self.width = space
        self.color = WHITE
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.lastNode = None     #the node it comes from
        self.window = window
        self.gridColRow = colAndRow

        #a*
        self.gCost = float("inf")#
        self.hCost = float("inf")#
        self.fCost = self.gCost + self.hCost
        #a*
        
        

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getCol(self):#x
        return self.col

    def getRow(self):#y
        return self.row
        
    def getWidth(self):
        return self.width

    def getColor(self):
        return self.color

    def setObsticle(self):
        self.color = BLACK
        node.drawNode(self)

    def clear(self):
        self.color = WHITE
        node.drawNode(self)
    
    def setStart(self):
        self.color = BLUE
        node.drawNode(self)

    def setEnd(self):
        self.color = YELLOW
        node.drawNode(self)

    def discovered(self):
        self.color = RED
        node.drawNode(self)
    
    def available(self):
        self.color = GREEN
        node.drawNode(self)

    def setPath(self):
        self.color = CYAN
        node.drawNode(self)
        ##pygame.display.flip()

    def drawNode(self):
        pygame.draw.rect(self.window,self.color,(self.x,self.y,self.width,self.width),0)
        ##pygame.display.flip()



    def findPath(self): #find the path that have been found by the algorithm
        
        
        currentNode = self
        currentNode.color = YELLOW
        
        keepLooping = currentNode.lastNode != None

        while keepLooping:
            clock.tick(20)
            
            node.drawNode(currentNode)
            drawGridLine(currentNode.window,currentNode.gridColRow,(currentNode.width*currentNode.gridColRow))
            pygame.display.flip()

            currentNode = currentNode.lastNode
            currentNode.color = CYAN
            tOrF= currentNode.lastNode != None
            keepLooping = tOrF


    
        

    
def drawGridLine(window, colAndRow,width):
    space = width//colAndRow
    for i in range (colAndRow+1):  #column
        pygame.draw.line(window,BLACK,(space*i,0),(space*i,width))
        for j in range(colAndRow+1):
            pygame.draw.line(window,BLACK,(0,space*j),(width,space*j))




def allClear(nodeList):
    row = len(nodeList)
    for i in range(row):
        column = len(nodeList[i])
        for j in range(column):
            theRow = nodeList[i] 
            theNode = theRow[j]
            node.clear(theNode)
    
    

def findNode(x,y,space,listOfNode):
    column = x//space
    row = y//space

    theRow = listOfNode[row] #list of nodes in that rows
    theNode = theRow[column] # that specific node
    return theNode


def findNodeRowCol(col,row,listOfNode):

    theRow = listOfNode[row]
    theNode = theRow[col]
    return theNode



def setNeighbor(nodeList):

    row = len(nodeList)  #y coordinate of the grid
    for i in range(row): 
        
        column = len(nodeList[i])  #x coordinate of the grid
        for j in range(column):

            currentNode = findNodeRowCol(j,i,nodeList)
            

            if currentNode.color != BLACK: #only set neighbor if the color is not black

                if (currentNode.row != 0): #check the row above the currentNode
                    
                    checkNode = findNodeRowCol(currentNode.col,currentNode.row-1,nodeList)
                    
                    if checkNode.color != BLACK:
                        currentNode.up = checkNode
                        
                    else:
                        currentNode.up = None
                        
                        

                if (currentNode.row != currentNode.gridColRow-1):  #check node below the current node
                    
                    checkNode = findNodeRowCol((currentNode.col),currentNode.row+1,nodeList)
                    
                    
                    if checkNode.color != BLACK:
                        currentNode.down = checkNode
                        
                    else:
                        currentNode.down = None
                        

                if(currentNode.col != 0):   #check the left of the column
                
                    checkNode = findNodeRowCol(currentNode.col-1, currentNode.row,nodeList)
                    
                    
                    
                    if checkNode.color != BLACK:
                        currentNode.left = checkNode
                            
                    else:
                        currentNode.left = None
                        

                if(currentNode.col != currentNode.gridColRow-1):  #check the right of the column
                
                    checkNode = findNodeRowCol(currentNode.col+1, currentNode.row,nodeList)
                    
                    
                    if checkNode.color != BLACK:
                        currentNode.right = checkNode
                        
                        
                        
                    else:
                        currentNode.right = None




def checkFCost(nodeList): #for a star calorithm debigging

    row = len(nodeList)  #y
    for i in range(row): 
         
        column = len(nodeList[i])  #x
        for j in range(column):
            currentNode = findNodeRowCol(j,i,nodeList)
            print("node: ",currentNode.num,"  g cost: ", currentNode.gCost," h cost: ",currentNode.hCost,"  f cost  ", currentNode.fCost)
                


def findHCost(currentPos, endPos): #take in column and row, not x and y
    x1,y1 = currentPos
    x2,y2 = endPos

    return  abs(x1-x2)+abs(y1-y2)


def initBreadthFirst(startNode, endNode, listOfNode):
    setNeighbor(listOfNode)

    thisQueue = []
    thisQueue.append(startNode)


    while(len(thisQueue)>0):
        clock.tick(20)   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        currentNode = thisQueue.pop(0)
        


        if(currentNode.up != None):
            tempNode = currentNode.up
            if tempNode.color == WHITE:
                thisQueue.append(tempNode)
                tempNode.available()
                tempNode.lastNode = currentNode

            elif (tempNode.num == endNode.num) :
                tempNode.lastNode = currentNode
                tempNode.findPath()
                return True

                

        if(currentNode.right != None):
            tempNode = currentNode.right
            if tempNode.color == WHITE:
                thisQueue.append(tempNode)
                tempNode.available()
                tempNode.lastNode = currentNode

            elif (tempNode.num == endNode.num) :
                tempNode.lastNode = currentNode
                tempNode.findPath()
                return True


        if(currentNode.down != None):
            tempNode = currentNode.down
            if tempNode.color == WHITE:
                thisQueue.append(tempNode)
                tempNode.available()
                tempNode.lastNode = currentNode

            elif (tempNode.num == endNode.num) :
                tempNode.lastNode = currentNode 
                tempNode.findPath()
                return True


        if(currentNode.left != None):
            tempNode = currentNode.left
            if tempNode.color == WHITE:
                thisQueue.append(tempNode)
                tempNode.available()
                tempNode.lastNode = currentNode 


            elif (tempNode.num == endNode.num) :
                tempNode.lastNode = currentNode 
                tempNode.findPath()
                return True          


                






        if (currentNode != startNode):
            currentNode.discovered()
            drawGridLine(currentNode.window,currentNode.gridColRow,(currentNode.width*currentNode.gridColRow))

            pygame.display.flip()


    

    return False

def initAStar(startNode, endNode, listOfNode):         
    setNeighbor(listOfNode)
    count = 1
    

    thisQueue = PriorityQueue()
    startNode.gCost = 0
    startNode.hCost = findHCost((startNode.col,startNode.row),(endNode.col,endNode.row))
    thisQueue.put((startNode.fCost,count,startNode))
    potentialNodes = [startNode]

        


    while len(potentialNodes) > 0:
        clock.tick(20)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            
        currentNode = thisQueue.get()[2] #get the actual node
        potentialNodes.remove(currentNode)
            

        if (currentNode == endNode):
            print("hi") 
            currentNode.findPath()
            return True

            
            
        if (currentNode.up != None):# and (currentNode.up.color != RED):
                
            upNode = currentNode.up
            tempGCost = currentNode.gCost +1

            if tempGCost < upNode.gCost:
                upNode.lastNode = currentNode
                upNode.gCost = tempGCost
                upNode.hCost = findHCost((upNode.col,upNode.row),(endNode.col,endNode.row))
                upNode.fCost = upNode.gCost + upNode.hCost
            
                if upNode not in potentialNodes:
                    count += 1
                    potentialNodes.append(upNode)
                    thisQueue.put((upNode.fCost,count,upNode))
                    upNode.available()
                    drawGridLine(currentNode.window,currentNode.gridColRow,(currentNode.width*currentNode.gridColRow))

            
        if (currentNode.down != None):# and (currentNode.down.color != RED):
            
            downNode = currentNode.down
            tempGCost = currentNode.gCost +1

            if tempGCost < downNode.gCost:
                downNode.lastNode = currentNode
                downNode.gCost = tempGCost
                downNode.hCost = findHCost((downNode.col,downNode.row),(endNode.col,endNode.row))
                downNode.fCost = downNode.gCost + downNode.hCost
                
                if downNode not in potentialNodes:
                    count += 1
                    potentialNodes.append(downNode)
                    thisQueue.put((downNode.fCost,count,downNode))
                    downNode.available()
                    drawGridLine(currentNode.window,currentNode.gridColRow,(currentNode.width*currentNode.gridColRow))

            
        if (currentNode.left != None):# and (currentNode.left.color != RED):
            
            leftNode = currentNode.left
            tempGCost = currentNode.gCost +1

            if tempGCost < leftNode.gCost:
                leftNode.lastNode = currentNode
                leftNode.gCost = tempGCost
                leftNode.hCost = findHCost((leftNode.col,leftNode.row),(endNode.col,endNode.row))
                leftNode.fCost = leftNode.gCost + leftNode.hCost
                
                if leftNode not in potentialNodes:
                    count +=1
                    potentialNodes.append(leftNode)
                    thisQueue.put(  (leftNode.fCost , count , leftNode )  )
                    leftNode.available()
                    drawGridLine(currentNode.window,currentNode.gridColRow,(currentNode.width*currentNode.gridColRow))

            
        if (currentNode.right != None):# and ( currentNode.right.color != RED):
                
            rightNode = currentNode.right
            tempGCost = currentNode.gCost +1

            if tempGCost < rightNode.gCost:
                rightNode.lastNode = currentNode
                rightNode.gCost = tempGCost
                rightNode.hCost = findHCost((rightNode.col,rightNode.row),(endNode.col,endNode.row))
                rightNode.fCost = rightNode.gCost + rightNode.hCost
                
                if rightNode not in potentialNodes:
                    count +=1
                    potentialNodes.append(rightNode)
                    thisQueue.put((rightNode.fCost,count,rightNode))
                    rightNode.available()
                    drawGridLine(currentNode.window,currentNode.gridColRow,(currentNode.width*currentNode.gridColRow))



        if (currentNode != startNode):
            currentNode.discovered()
            drawGridLine(currentNode.window,currentNode.gridColRow,(currentNode.width*currentNode.gridColRow))

            pygame.display.flip()
                
    return False
            

            






    