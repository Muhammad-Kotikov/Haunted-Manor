

import pygame
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((600, 600))


image_sprite = [pygame.image.load("rsc/sprites/Mc_walking/MC_walking_-1.png"),
				pygame.image.load("rsc/sprites/Mc_walking/MC_walking_-1.png"),
				pygame.image.load("rsc/sprites/Mc_walking/MC_walking_-2.png"),
                pygame.image.load("rsc/sprites/Mc_walking/MC_walking_-2.png"),
				pygame.image.load("rsc/sprites/Mc_walking/MC_walking_-3.png"),  #für mich: er erkennt die Bilder juhu
                pygame.image.load("rsc/sprites/Mc_walking/MC_walking_-3.png"),
				pygame.image.load("rsc/sprites/Mc_walking/MC_walking_-4.png"),
                pygame.image.load("rsc/sprites/Mc_walking/MC_walking_-4.png")]


clock = pygame.time.Clock()

# Creating a new variable
# We will use this variable to
# iterate over the sprite list
value = 0

# Creating a boolean variable that
# we will use to run the while loop
run = True

# Creating a boolean variable to
# check if the character is moving
# or not
moving = False

# Creating a variable to store
# the velocity
velocity = 12

# Starting coordinates of the sprite
x = 100
y = 150

# Creating an infinite loop
# to run our game
while run:

	# Setting the framerate to 10fps just
	# to see the result properly
	clock.tick(8)

	# iterate over the list of Event objects
	# that was returned by pygame.event.get() method.
	for event in pygame.event.get():

		# Closing the window and program if the
		# type of the event is QUIT
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()
			quit()

		# Checking event key if the type
		# of the event is KEYUP i.e.
		# keyboard button is released
		if event.type == pygame.KEYUP:

			# Setting the value of moving to False
			# and the value f value variable to 0
			# if the button released is
			# Left arrow key or right arrow key
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				moving = False
				value = 0

	# Storing the key pressed in a
	# new variable using key.get_pressed()
	# method
	key_pressed_is = pygame.key.get_pressed()

	# Changing the x coordinate
	# of the player and setting moving
	# variable to True
	if key_pressed_is[K_LEFT]:
		x -= 8
		moving = True
	if key_pressed_is[K_RIGHT]:
		x += 8
		moving = True

	# If moving variable is True
	# then increasing the value of
	# value variable by 1
	if moving:
		value += 1

	# Setting 0 in value variable if its
	# value is greater than the length
	# of our sprite list
	if value >= len(image_sprite):
		value = 0

	# Storing the sprite image in an
	# image variable
	image = image_sprite[value]

	# Scaling the image
	image = pygame.transform.scale(image, (23, 36))

	# Displaying the image in our game window
	window.blit(image, (x, y))

	# Updating the display surface
	pygame.display.update()

	# Filling the window with black color
	window.fill((0, 0, 0))
