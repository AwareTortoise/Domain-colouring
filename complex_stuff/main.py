import pygame
import math
import colorsys

height = 1024
width = 1024
scaleFactor = 1

def normalize (color):
    return color[0] / 255.0, color[1] / 255.0, color[2] / 255.0

def reformat (color):
    return int (round (color[0] * 255)), \
           int (round (color[1] * 255)), \
           int (round (color[2] * 255))

def colour(x,y):
    (x2,y2) = pixelToCoord(x,y)
    if x2 == 0:
        hsv = (0,1.0, min(math.sqrt(x2*x2 + y2*y2)/150,1))
    else:
        hsv = (abs(math.atan(abs(y2)/abs(x2))/(math.pi/2)),1.0, max(min(math.sqrt(x2*x2 + y2*y2)/200 -0.1, 1), 0))
    return reformat (colorsys.hsv_to_rgb (*hsv))

def cubicTransfrom(xCoord,yCoord):
    z = complex(*pixelToCoord(xCoord,yCoord))
    point = 4*z*z*z+ 300*z*z - 200*z + 100000
    return coordToPixel(point.real, point.imag)


def quadraticTransform(xCoord,yCoord):
    z = complex(*pixelToCoord(xCoord,yCoord))
    point = z*z - 200*z + 100000
    return coordToPixel(point.real, point.imag)

def blankTransform(x,y):
    return(x,y)


def pixelToCoord(x,y):
    return (x-round((scaleFactor*width)/2), y-round((scaleFactor*height)/2))

def coordToPixel(x,y):
    x2 = math.floor(x)
    y2 = math.floor(y)
    x2 += round((scaleFactor*width)/2)
    y2 += round((scaleFactor*height)/2)
    # while x2 >= width:
    #     x2 -= width
    # while y2 >= height:
    #     y2 -= height
    # while x2 < 0:
    #     x2 += width
    # while y2 < 0:
    #     y2 += height
    return (x2,y2)

screen = pygame.display.set_mode(((height), (width)))

pygame.display.set_caption('Colours')

def genrateGraph(transform):
    global screen
    grid = []
    for y in range(round(scaleFactor*width)):
        grid.append([])
        for x in range(round(scaleFactor*width)):
            (x2,y2) = transform(x,y)
            screen.set_at((x,y), colour(x2,y2))

    for x in range(height):
        screen.set_at((x,math.floor(width/2)), (0,0,0))

    for y in range(height):
        screen.set_at((math.floor(height/2),y), (0,0,0))
    pygame.display.flip()
    print("loaded graph")


genrateGraph(blankTransform)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 49:
                genrateGraph(blankTransform)
            if event.key == 50:
                genrateGraph(quadraticTransform)
            if event.key == 51:
                genrateGraph(cubicTransfrom)
