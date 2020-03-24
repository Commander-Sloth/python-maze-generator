import pygame
import time, sys, random
from mazeGenerator import generateMaze

pygame.init()

#Define game variables.
SIZE = 4 # >3
WIN_WIDTH = (SIZE*30)+30
WIN_HEIGHT = (SIZE*30)+30
ROWS = SIZE
COLS = SIZE
backgroudColour = (0,0,0)

mazeArray = generateMaze(4)

cursorEvent = pygame.event.poll()

timeElapsed = 0
clock = pygame.time.Clock()

notRunning = False

#Set up the Pygame window.
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Maze')

screen.fill(backgroudColour)

# Reusable function to return desired text object, which can be displayed.
def drawText(labelText, xPos, yPos):
	font = pygame.font.Font('freesansbold.ttf', 16)
	text = font.render(labelText, True, (255, 0, 255))
	textRect = text.get_rect()
	textRect.center = (xPos, yPos)
	return screen.blit(text, textRect)


def print_array():
	global mazeArray
	for i in range(ROWS):
		print(mazeArray[i])


def positionInArray(coordinates): # [c, r]
	colPos = coordinates[0]
	rowPos = coordinates[1]

	if colPos >= 0 and colPos <= COLS-1 and rowPos >= 0 and rowPos <= ROWS-1:
		return True
	else: return False


def drawFixers():
	lineSize = 3

	lineMarg = 15
	for row in range(ROWS):
		for col in range(COLS):
			UP = getNewCoords([col, row], [0, -1])
			LEFT = getNewCoords([col, row], [-1, 0])
			DOWN = getNewCoords([col, row], [0, 1])
			RIGHT = getNewCoords([col, row], [1, 0])

			if positionInArray([col+1, row+1]) and positionInArray(RIGHT) and positionInArray(DOWN):
				if mazeArray[row+1][col+1] == mazeArray[row][col]:
					if (mazeArray[DOWN[1]][DOWN[0]] == mazeArray[row][col] + 1 or mazeArray[DOWN[1]][DOWN[0]] == mazeArray[row][col] -1) and (mazeArray[RIGHT[1]][RIGHT[0]] == mazeArray[row][col] + 1 or mazeArray[RIGHT[1]][RIGHT[0]] == mazeArray[row][col] -1):
						pygame.draw.line(screen, (255, 255, 255), (col*30 + 30 - lineMarg, row*30 + 30 + lineMarg), (col*30 + 30 + lineMarg, row*30 + 30 + lineMarg), lineSize)
					# OR RIGHT

			if positionInArray([col-1, row+1]) and positionInArray(LEFT) and positionInArray(DOWN):
				if mazeArray[row+1][col-1] == mazeArray[row][col]:
					if (mazeArray[DOWN[1]][DOWN[0]] == mazeArray[row][col] + 1 or mazeArray[DOWN[1]][DOWN[0]] == mazeArray[row][col] -1) and (mazeArray[LEFT[1]][LEFT[0]] == mazeArray[row][col] + 1 or mazeArray[LEFT[1]][LEFT[0]] == mazeArray[row][col] -1):
						pygame.draw.line(screen, (255, 255, 255), (col*30 + 30 - lineMarg, row*30 + 30 + lineMarg), (col*30 + 30 + lineMarg, row*30 + 30 + lineMarg), lineSize)
					# OR RIGHT


def getNewCoords(coordinates, direction):
	newC = coordinates[0] + direction[0]
	newR = coordinates[1] + direction[1]
	newCoords = [newC, newR]

	return newCoords


def displayStuff():
	lineSize = 3
	lineMarg = 15
	for row in range(ROWS):
		for col in range(COLS):
			UP = getNewCoords([col, row], [0, -1])
			LEFT = getNewCoords([col, row], [-1, 0])
			DOWN = getNewCoords([col, row], [0, 1])
			RIGHT = getNewCoords([col, row], [1, 0])

			if positionInArray(UP):
				if mazeArray[UP[1]][UP[0]] != mazeArray[row][col] + 1 and mazeArray[UP[1]][UP[0]] != mazeArray[row][col] -1:
					pygame.draw.line(screen, (255,255,255), (col*30 + 30 - lineMarg, row*30 + 30 - lineMarg), (col*30 + 30 + lineMarg, row*30 + 30 - lineMarg), lineSize)
			
			if positionInArray(DOWN):
				if mazeArray[DOWN[1]][DOWN[0]] != mazeArray[row][col] + 1 and mazeArray[DOWN[1]][DOWN[0]] != mazeArray[row][col] -1:
					pygame.draw.line(screen, (255,255,255), (col*30 + 30 - lineMarg, row*30 + 30 + lineMarg), (col*30 + 30 + lineMarg, row*30 + 30 + lineMarg), lineSize)

			if positionInArray(LEFT):
				if mazeArray[LEFT[1]][LEFT[0]] != mazeArray[row][col] + 1 and mazeArray[LEFT[1]][LEFT[0]] != mazeArray[row][col] -1:
					pygame.draw.line(screen, (255,255,255), (col*30 + 30 - lineMarg, row*30 + 30 - lineMarg), (col*30 + 30 - lineMarg, row*30 + 30 + lineMarg), lineSize)

			if positionInArray(RIGHT):
				if mazeArray[RIGHT[1]][RIGHT[0]] != mazeArray[row][col] + 1 and mazeArray[RIGHT[1]][RIGHT[0]] != mazeArray[row][col] -1:
					pygame.draw.line(screen, (255,255,255), (col*30 + 30 + lineMarg, row*30 + 30 - lineMarg), (col*30 + 30 + lineMarg, row*30 + 30 + lineMarg), lineSize)

			pygame.draw.rect(screen, (255, 255, 255), (col*30 + 30 - lineMarg, row*30 + 30 - lineMarg, lineSize-1, lineSize-1))

			pygame.draw.rect(screen, (255, 255, 255), (15, 15, WIN_WIDTH-30 , WIN_HEIGHT-30), lineSize)
			#drawText(str(mazeArray[row][col]), col*30 + 30, row*30 + 30)


# Main loop to update and draw the game in screen.
def displayLoop():
	global notRunning
	timeTracker = 0

	while not notRunning:
		timeTracker += 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()

		# Do not update the images every single frame, however, key events are detected every frame.
		if timeTracker % 10 == 0:
			screen.fill(backgroudColour)
			displayStuff()
			drawFixers()

		pygame.display.flip()	
		clock.tick(60)

	#Stop processing coverField, wait for user to restart the game.
	while notRunning: 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					startGame()
			
		screen.fill(backgroudColour)

		#displayStuff()
		drawText("Press space to restart.", 175, 175)

		pygame.display.flip()

		clock.tick(60)

displayLoop()