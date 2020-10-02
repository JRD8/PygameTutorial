# Pygame General Tutorial
import pygame
pygame.init() # essential after import to initiate the module


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


# Attributes for the initial rectangle character
x = 50
y = 400	
width = 64 # Use the width dimension of the sprite
height = 64 # Use the height dimension of the sprite
vel = 10 # Velocity, set how fast the character moves
isJump = False # Jump action flag
jumpCount = 10 # Jump action counter
left = False # Left walk action flag
right = False # Right walk action flag
walkCount = 0 # Walk action counter


def redrawGameWindow():
	#win.fill((0,0,0)) # Fill the screen all black to refresh & not have residual char lines
	global walkCount
	win.blit(bg, (0,0))

	# pygame.draw.rect(win, (255,0,0), (x, y, width, height)) # Define/redefine red obj to be drawn
	
	if walkCount + 1 >= 27:
		walkCount = 0

	# Draw sprites routine
	if left: # If we are walking left, ie left = True
		win.blit(walkLeft[walkCount//3], (x,y)) # Index to the correct frame, using integer division
		walkCount += 1
	elif right: # If we are walking right, ie right = True
		win.blit(walkRight[walkCount//3], (x,y)) # Index to the correct frame, using integer division
		walkCount += 1
	else: # If we are standing still or jumping
		win.blit(char, (x,y)) # In that case, show the standing character


	pygame.display.update() # Have to update the display to draw the object 

# Main loop
run = True
while run:
	#pygame.time.delay(50) # A small timedelay in milliseconds.  So, doesn't run too fast
	clock.tick(27) # Set FPS

	# TODO: RESEARCH PYGAME EVENTS
	for event in pygame.event.get(): # Check pygame for any events/anything that happens from the user
		if event.type == pygame.QUIT: # If quit event, quit the loop
			run = False

	keys = pygame.key.get_pressed()

	# TODO: RESEARCH PYGAME KEYS
	if keys[pygame.K_LEFT] and x > 0: # Have to constrain the edges...
		x -= vel
		left = True # Toggle the directional flags
		right = False # Toggle the directional flags
	
	elif keys[pygame.K_RIGHT] and x < (WIN_WIDTH - width): # Have to constrain the edges...
		x += vel
		left = False # Toggle the directional flags
		right = True # Toggle the directional flags
	
	else:
		left = False
		right = False
		walkCount = 0
	

	if not (isJump): # Constrain up/down/additional jumps during jumps
		# Up/Down functionality removed in Tutorial #3 in order to animate cg
			# if keys[pygame.K_UP] and y > 0: # Have to constrain the edges...
			# 	y -= vel
			# if keys[pygame.K_DOWN] and y < (WIN_HEIGHT - height): # Have to constrain the edges...
			# 	y += vel
		if keys[pygame.K_SPACE]: # Jump key
			isJump = True # Toggle jump action flag
			left = False
			right = False
			walkCount = 0
	else:
		neg = 1
		if jumpCount >= -10:
			if jumpCount < 0:
				neg = -1
			y -= (jumpCount ** 2) * 0.5 * neg
			jumpCount -= 1
		else:
			isJump = False # Reset jump action flag
			jumpCount = 10 # Reinitialize the jump counter



	# TODO: RESEARCH PYGAME SHAPES IN LIBRARY
	# Code has been moved outside of main loop and refactored into a def redrawGameWindow() function
		# win.fill((0,0,0)) # Fill the screen all black to refresh & not have residual char lines
		# pygame.draw.rect(win, (255,0,0), (x, y, width, height)) # Define/redefine red obj to be drawn
		# pygame.display.update() # Have to update the display to draw the object 
	redrawGameWindow()

pygame.quit()