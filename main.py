# Pygame General Tutorial
import pygame

WIN_WIDTH = 500
WIN_HEIGHT = 480
pygame.mixer.init()
pygame.font.init()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # Set screen size parameters

pygame.display.set_caption("JRD Tutorial") # Set window caption

# Load sprite images (into lists where needed)
walkRight = [pygame.image.load("assets/R1.png"), pygame.image.load('assets/R2.png'), pygame.image.load('assets/R3.png'), pygame.image.load('assets/R4.png'), pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'), pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'), pygame.image.load('assets/R9.png')]
walkLeft = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), pygame.image.load('assets/L3.png'), pygame.image.load('assets/L4.png'), pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'), pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), pygame.image.load('assets/L9.png')]
bg = pygame.image.load("assets/bg.jpg")
char = pygame.image.load('assets/standing.png')

# Load SFX and play music
bulletSound = pygame.mixer.Sound("assets/bullet.wav")
hitSound = pygame.mixer.Sound("assets/hit.wav")
music = pygame.mixer.music.load("assets/music.wav")
pygame.mixer.music.set_volume(0.6) 
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

score = 0

class enemy(object):
	walkRight = [pygame.image.load("assets/R1E.png"), pygame.image.load('assets/R2E.png'), pygame.image.load('assets/R3E.png'), pygame.image.load('assets/R4E.png'), pygame.image.load('assets/R5E.png'), pygame.image.load('assets/R6E.png'), pygame.image.load('assets/R7E.png'), pygame.image.load('assets/R8E.png'), pygame.image.load('assets/R9E.png'), pygame.image.load('assets/R10E.png'), pygame.image.load('assets/R11E.png')]
	walkLeft = [pygame.image.load('assets/L1E.png'), pygame.image.load('assets/L2E.png'), pygame.image.load('assets/L3E.png'), pygame.image.load('assets/L4E.png'), pygame.image.load('assets/L5E.png'), pygame.image.load('assets/L6E.png'), pygame.image.load('assets/L7E.png'), pygame.image.load('assets/L8E.png'), pygame.image.load('assets/L9E.png'), pygame.image.load('assets/L10E.png'), pygame.image.load('assets/L11E.png')]

	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.end = end
		self.walkCount = 0 # Walk action counter
		self.vel = 3
		self.path = [self.x, self.end] # X Coordinates of where enemy starts and where ends
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)
		self.health = 10
		self.visible = True

	def draw(self, win):
		self.move()

		if self.visible: # Only draw enemy if flagges as visible (i.e., Health > 0)

			if self.walkCount + 1 >= 33: # 33 = 3 x 11 enemy sprite frames
				self.walkCount = 0

			if self.vel > 0: # If vel is positive, enemy is moving right
				win.blit(self.walkRight[self.walkCount//3], (self.x, self.y)) # Index to the correct frame, using integer division
				self.walkCount += 1
			else: # If vel is negative, enemy is moving left
				win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y)) # Index to the correct frame, using integer division
				self.walkCount += 1
			
			# Health Bar/Blend
			pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) # Red Bar
			pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10)) # Green Bar

			self.hitbox = (self.x + 17, self.y + 2, 31, 57)
			# pygame.draw.rect(win, (255,0,0), (self.hitbox), 2)


	def move(self):
		if self.vel > 0: # If vel is positive, enemy is moving right
			if self.x + self.vel < self.path[1]: # If before the end of path
				self.x += self.vel
			else: # At end of path, flip and switch direction
				self.vel = self.vel * -1
				self.walkCount = 0
		else: # If vel is negative, enemy is moving left
			if self.x - self.vel > self.path[0]: # If before the beginning of path
				self.x += self.vel
			else: # At end of path, flip and switch direction
				self.vel = self.vel * -1
				self.walkCount = 0

	def hit(self):
		if self.health > 0:
			self.health -= 1 # Decrement health
		else: # If health down to 0. then flag enemy as invisible
			self.visible = False


class projectile(object):
	def __init__(self, x, y, radius, color, facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.vel = 8 * facing # Arbitrary value for vel
	
	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class player(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = 4 # Velocity, set how fast the character moves
		self.isJump = False # Jump action flag
		self.jumpCount = 10 # Jump action counter
		self.left = False # Left walk action flag
		self.right = False # Right walk action flag
		self.walkCount = 0 # Walk action counter
		self.standing = True # Standing or moving flag
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)


	def draw(self, win):
		if self.walkCount + 1 >= 27: # 27 = 3 x 9 player sprite frames
			self.walkCount = 0

		if not (self.standing): # If moving...
			if self.left: # If we are walking left, ie left = True
				win.blit(walkLeft[self.walkCount//3], (self.x, self.y)) # Index to the correct frame, using integer division
				self.walkCount += 1
			elif self.right: # If we are walking right, ie right = True
				win.blit(walkRight[self.walkCount//3], (self.x, self.y)) # Index to the correct frame, using integer division
				self.walkCount += 1
		else: # If we are standing still or jumping
			# win.blit(char, (self.x, self.y)) # In that case, show the standing character
			if self.right:
				win.blit(walkRight[0], (self.x, self.y))
			else:
				win.blit(walkLeft[0], (self.x, self.y))
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)
		# pygame.draw.rect(win, (255,0,0), (self.hitbox), 2)

	def hit(self):
		self.isJump = False
		self.jumpCount = 10
		self.x = 10
		self.y = 400
		self.walkCount = 0
		font1 = pygame.font.SysFont("comicsans", 100)
		text = font1.render("-5", 1, (255, 0, 0)) # Feedback to player the collision -5
		win.blit(text, (250 - (text.get_width()/2), 200))
		pygame.display.update()
		i = 0
		while i < 150: # Need a delay or score penalty alertFui wont stay on screen
			pygame.time.delay(10)
			i += 1
			for event in pygame.event.get(): # Check pygame for any events/anything that happens from the user
				if event.type == pygame.QUIT: # If quit event, quit the loop
					i = 301
					pygame.quit()


def redrawGameWindow():
	win.blit(bg, (0,0)) # Draw the background

	text = font.render("Score: " + str(score), 1, (0,0,0)) # Draw the score
	win.blit(text, (360, 10))

	man.draw(win) # Draw the player
	goblin.draw(win) # Draw the enemy
	for bullet in bullets: # Draw the bullets
		bullet.draw(win)

	pygame.display.update() # Have to update the display the objects that are "blitted"

# Main loop
font = pygame.font.SysFont("comicsans", 30, True)
man = player(250, 400, 64, 64) # Instantiate the player with default/init values, 64 x 64 = dimensions of the sprite
goblin = enemy(30, 400, 64, 64, 400) # Instantiate the enemy with default/init values, 64 x 64 = dimensions of the sprite
shootLoop = 0 # Reduce bullet spamming var
bullets = [] # This list is way to implement multiple bullets.
run = True

while run:

	clock.tick(27) # Set FPS

	# Check player/goblin collison
	if goblin.visible:
		if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]: # Check within Y coords
			if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]: # Check within x coords
				man.hit()
				score -= 5 # Decrease player score -5

	# Basic shootLoop timer to delay each additional bullet
	if shootLoop > 0:
		shootLoop += 1
	if shootLoop > 3:
		shootLoop = 0

	for event in pygame.event.get(): # Check pygame for any events/anything that happens from the user
		if event.type == pygame.QUIT: # If quit event, quit the loop
			run = False

	for bullet in bullets: # Multple bullet handling routing

		# Bullet collision check
		if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]: # Check within Y coords
			if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]: # Check within x coords
				hitSound.play()
				goblin.hit()
				score += 1 # Increment the player score
				bullets.pop(bullets.index(bullet)) # Make bullet disappear

		if bullet.x < WIN_WIDTH and bullet.x > 0: # If bullet is on the screen, move it
			bullet.x += bullet.vel
		else: # If bullet is not on the screen, pop it from the list and remove it
			bullets.pop(bullets.index(bullet)) # Make bullet disappear
			

	keys = pygame.key.get_pressed()

	if keys[pygame.K_SPACE] and shootLoop == 0: # Shoot Action Key, constrain the number of bullets using shootLoop
		bulletSound.play()
		if man.left: # If man is facing left...
			facing  = -1
		else:
			facing = 1 # Or else man is facing right...
		if len(bullets) < 5: # This is the max amount of bullets that shooter can have on screen at once, can't spam bullets
			bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height //2), 6, (0,0,0), facing)) # Append the bullets list with a newly created/instantiated projectile

		shootLoop = 1

	if keys[pygame.K_LEFT] and man.x > 0: # Have to constrain the edges...
		man.x -= man.vel
		man.left = True # Toggle the directional flags
		man.right = False # Toggle the directional flags
		man.standing = False
	
	elif keys[pygame.K_RIGHT] and man.x < (WIN_WIDTH - man.width): # Have to constrain the edges...
		man.x += man.vel
		man.left = False # Toggle the directional flags
		man.right = True # Toggle the directional flags
		man.standing = False
	
	else:
		man.standing = True
		man.walkCount = 0
	

	if not (man.isJump): # Constrain up/down/additional jumps during jumps
		if keys[pygame.K_UP]: # Jump Acton Key
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