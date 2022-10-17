
# Tomado y modificado de: https://realpython.com/pygame-a-primer/

# Librerias
import numpy as np
## Import the pygame module
import pygame
## Import random for random numbers
import random

## Constantes
velocidadBaja=2
velocidadAlta=60
maxCarPosition=255


## Variable cambiar dirección
cambiarDireccion=True

## Define constants for the screen width and height

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Funciones

def maxDistance(index,size):
    # Halla la máxima distancia desde un punto hasta los bordes de un cuadro
    n=size[0]-1
    m=size[1]-1
    miMax=0

    # Recorrido superior e inferior
    for j in range(m):
        distanceTop=((index[0]-0)**2+(index[1]-j)**2)**0.5
        distanceBottom=((index[0]-n)**2+(index[1]-j)**2)**0.5
        if(max(distanceTop,distanceBottom)>miMax):
            miMax=max(distanceTop,distanceBottom)

    # Recorridos laterales

    for i in range(n):
        distanceLeft=((index[0]-i)**2+(index[1]-0)**2)**0.5
        distanceRight=((index[0]-i)**2+(index[1]-m)**2)**0.5
        if(max(distanceLeft,distanceRight)>miMax):
            miMax=max(distanceLeft,distanceRight)

    return miMax



def colorImage(index,miMax,image):
    n=image.shape[0]
    m=image.shape[1]

    for i in range(n):
        for j in range(m):
            distance=np.linalg.norm([index[0]-i,index[1]-j],2)
            image[i,j,0:2]=np.floor(255-255*distance/miMax)
    
    return image


# Import pygame.locals for easier access to key coordinates

# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame

# Define a Player object by extending pygame.sprite.Sprite

# The surface drawn on the screen is now an attribute of 'player'

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Player, self).__init__()
        image = pygame.transform.scale(pygame.image.load("./figs/jet.png"),(140,40))
        self.surf = image.convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, np.floor(SCREEN_WIDTH/3)),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        
        self.speed = 5

        

    # Move the sprite based on user keypresses

    def update(self,cambiarDireccion):


        # Keep player on the screen

        if self.rect.left <= 0:
            self.rect.left = 0
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(0, np.floor(SCREEN_WIDTH/3)),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT



        if cambiarDireccion:
            self.rect.move_ip(self.speed, 0)
        else:
            self.rect.move_ip(-self.speed, 0)

pygame.init()

# Create the screen object

# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Hacer Imagen

index=[random.randint(np.floor(SCREEN_WIDTH*2/3), SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT)]
background =np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT,3),np.uint8)
miMax=maxDistance(index,background.shape[0:2])
background_int=colorImage(index,miMax,background)
background = pygame.surfarray.make_surface(background_int)


# Instantiate player. Right now, this is just a rectangle.
player = Player()


all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # Look at every event in the queue

    for event in pygame.event.get():

        # Did the user hit a key?
        if event.type == KEYDOWN:

            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
    

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    
    if player.rect.right >= SCREEN_WIDTH:
        cambiarDireccion=False
    elif player.rect.left <= 0:
        cambiarDireccion=True


    # Update the player sprite based on user keypresses
    player.update(cambiarDireccion)
    
    # Se actualiza el fondo
    screen.blit(background,(0,0))
    
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Without the call to .flip(), nothing is shown.
    pygame.display.flip()

    # Según la cernanía de la fuente, este se desplaza
    carPosition=background_int[player.rect.center[0],player.rect.center[1],0]
    clock_velocity= np.ceil((velocidadAlta-velocidadBaja)*carPosition/maxCarPosition+velocidadBaja)
    
    print(f'V:{clock_velocity}')
    clock.tick(clock_velocity)

    