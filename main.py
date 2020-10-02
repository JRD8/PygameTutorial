# Pygame General Tutorial
import pygame

WIN_WIDTH = 500
WIN_HEIGHT = 480

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # Set screen size parameters

pygame.display.set_caption("JRD Tutorial") # Set window caption

# Load sprite images (into lists where needed)
walkRight = [pygame.image.load("assets/R1.png"), pygame.image.load('assets/R2.png'), pygame.image.load('assets/R3.png'), pygame.image.load('assets/R4.png'), pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'), pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'), pygame.image.load('assets/R9.png')]
walkLeft = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), pygame.image.load('assets/L3.png'), pygame.image.load('assets/L4.png'), pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'), pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), pygame.image.load('assets/L9.png')]
bg = pygame.image.load("assets/bg.jpg")
char = pygame.image.load('assets/standing.png')

clock = pygame.time.Clock()


class player(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = 10 # Velocity, set how fast the character moves
		self.isJump = False # Jump action flag
		self.jumpCount = 10 # Jump action counter
		self.left = False # Left walk action flag
		self.right = False # Right walk action flag
		self.walkCount = 0 # Walk action counter
		return

	def draw(self, win):
		if self.walkCount + 1 >= 27:
			self.walkCount = 0

		if self.left: # If we are walking left, ie left = True
			win.blit(walkLeft[self.walkCount//3], (self.x, self.y)) # Index to the correct frame, using integer division
			self.walkCount += 1
		elif self.right: # If we are walking right, ie right = True
			win.blit(walkRight[self.walkCount//3], (self.x, self.y)) # Index to the correct frame, using integer division
			self.walkCount += 1
		else: # If we are standing still or jumping
			win.blit(char, (self.x, self.y)) # In that case, show the standing character
		return


def redrawGameWindow():
	win.blit(bg, (0,0))
	man.draw(win)
	pygame.display.update() # Have to update the display to draw the object
	return

# Main loop
man = player(50, 400, 64, 64) # Instantiate the player with default/init values, 64 x 64 = dimensions of the sprite
run = True

while run:

	clock.tick(27) # Set FPS

	for event in pygame.event.get(): # Check pygame for any events/anything that happens from the user
		if event.type == pygame.QUIT: # If quit event, quit the loop
			run = False

	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT] and man.x > 0: # Have to constrain the edges...
		man.x -= man.vel
		man.left = True # Toggle the directional flags
		man.right = False # Toggle the directional flags
	
	elif keys[pygame.K_RIGHT] and man.x < (WIN_WIDTH - man.width): # Have to constrain the edges...
		man.x += man.vel
		man.left = False # Toggle the directional flags
		man.right = True # Toggle the directional flags
	
	else:
		man.left = False
		man.right = False
		man.walkCount = 0
	

	if not (man.isJump): # Constrain up/down/additional jumps during jumps
		if keys[pygame.K_SPACE]: # Jump key
			man.isJump = True # Toggle jump action flag
			man.left = False
			man.right = False
			man.walkCount = 0
	else:
		neg = 1
		if man.jumpCount >= -10:
			if man.jumpCount < 0:
				neg = -1
			man.y -= (man.jumpCount ** 2) * 0.5 * neg
			man.jumpCount -= 1
		else:
			man.isJump = False # Reset jump action flag
			man.jumpCount = 10 # Reinitialize the jump counter

	redrawGameWindow()

pygame.quit()