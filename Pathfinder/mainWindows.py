import pygame
from pygame.constants import*
from color import*
from nodeClass import*


pygame.init
pygame.font.init()

clock = pygame.time.Clock()
fps = 30

pygame.display.set_caption("Pathfinder")

global width
width = 600 #width and length of the window

global colAndRow 
colAndRow = 20   #number of columns and rows

global space # width of the individual nodes
space = width//colAndRow

window = pygame.display.set_mode((width+150, width)) #extra room to fit other user interface


def getMousePos(): #mouse position
    x,y = pygame.mouse.get_pos()
    return x,y



def drawGridNodes(colAndRow,space):# row then column
    nodeList = []
    nodeNum = 0
    for i in range (colAndRow):
        nodeList.append([])  #add row (y column)

        for j in range (colAndRow):  #create node along the current row (node moving along x)
            currentNode = node(j,i,space,colAndRow,nodeNum,window) # create a node object
            currentNode.drawNode()
            nodeNum += 1
            nodeList[i].append(currentNode)     #column
    return (nodeList)#return the 2d list holding the nodes



def runCode():
    run = True
    window.fill(WHITE)
    
    listOfNode = drawGridNodes(colAndRow,space)
    
    
    
    obsticle = False
    clear = False
    startNode = False
    endNode = False

    usingAStar = False
    usingBrth1St = False

    theStartNode = None
    theEndNode = None

    numOfStart = numOfEnd = 0 #set number of start and end node to zero
    
    while run:
        
        for event in pygame.event.get():

            

            
            
            font = pygame.font.SysFont(None, 30)
        

            pygame.draw.rect(window,DARKGREY,(width+25,25,100,30),0)
            window.blit(font.render("A*",True,WHITE),[width+65,30])


            pygame.draw.rect(window,DARKGREY,(width+25,70,100,30),0)
            window.blit(font.render("Brth-1st",True,WHITE),[width+30,75])

            pygame.draw.rect(window,GREEN,(width+25, 450,100,30),0)
            window.blit(font.render("Start",True,WHITE),[width+50,455])
            

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:   #menu
                x,y = getMousePos()
                if x > width:
                    if ((x>= width + 25) and (x <= width + 125)):
                        if ((y >= 25) and (y <= 55)):
                            print("selecting A* algorithm")
                            usingAStar = True
                            usingBrth1St = False

                        if ((y >= 70) and (y <= 100)):
                            print("selecting Breadth-first algorithm")
                            usingBrth1St = True
                            usingAStar = False

                        elif((y>= 450) and (y <= 480))and(numOfStart == numOfEnd ==1):
                            print("calculating path")
                            
                            if usingAStar:
                                initAStar(theStartNode,theEndNode,listOfNode)
                            
                            elif usingBrth1St:
                                initBreadthFirst(theStartNode,theEndNode,listOfNode)
                            
                           

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_o: #o for obsticles BLACK color
                    if (obsticle):                      
                        obsticle = False
                    else:
                        obsticle = True

                        clear = False
                        startNode = False
                        endNode = False 

                if event.key == pygame.K_c:  # c for clear WHITE color
                    if(clear):
                        clear = False
                    else:
                        clear = True

                        obsticle = False
                        startNode = False
                        endNode = False 

                if event.key == pygame.K_s: #s for start node BLUE color
                    if(startNode):
                        startNode = False
                    elif numOfStart <= 0:
                        startNode = True

                        obsticle = False
                        clear = False
                        endNode = False 

                if event.key == pygame.K_e: #e for end node YELLOW color
                    if(endNode):
                        endNode = False
                    elif numOfEnd <= 0:
                        endNode = True 

                        obsticle = False
                        clear = False
                        startNode = False
                    
                
                if (event.key == pygame.K_BACKSPACE):  #clear the grid
                    window.fill(WHITE)
                    listOfNode = drawGridNodes(colAndRow,space)
                    numOfStart = numOfEnd = 0
                    

                        
            
         
            
            #try:
            if (pygame.mouse.get_pressed()[0]):  #grid interaction
                x,y = getMousePos()
                if x <= width:
                    thisNode = findNode(x,y,space,listOfNode)
                    if (obsticle):

                        if (thisNode.color == YELLOW):
                            numOfEnd = 0
                        elif (thisNode.color == BLUE):
                            numOfStart = 0

                        thisNode.setObsticle()
                        
                    elif (clear):
                        if (thisNode.color == YELLOW):
                            numOfEnd = 0
                        elif (thisNode.color == BLUE):
                            numOfStart = 0
                                
                        thisNode.clear()

                    elif(((startNode) and (numOfStart == 0)) and (thisNode.color != YELLOW)):
                        thisNode.setStart()
                        theStartNode = thisNode
                        numOfStart = 1

                    elif(((endNode)and (numOfEnd == 0))and (thisNode.color != BLUE)):
                        thisNode.setEnd()
                        theEndNode = thisNode
                        numOfEnd = 1
            #except:
                #print()

                


        drawGridLine(window,colAndRow,width)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

runCode()









