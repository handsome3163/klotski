#!/usr/bin/env python

import pygame, sys
from pygame.locals import *

# The starting state of the board
import start
from start import *

pygame.init()
fpsClock = pygame.time.Clock()

# set up the window
DS = pygame.display.set_mode((700, 600), 0, 32)
pygame.display.set_caption("CIS 27 Spring 2014 Scott Kinney Final")

def drawText(moveCount, moveableTiles):
    fontObj = pygame.font.Font('freesansbold.ttf', 24)
    movesSurfaceObj = fontObj.render('Moves: ' + str(moveCount), True, LGREEN, BLACK)
    movesRectObj = movesSurfaceObj.get_rect()
    movesRectObj.center = (75,575)

    fontObj = pygame.font.Font('freesansbold.ttf', 14)
    moveableSurfaceObj = fontObj.render('moveableTiles ' + \
                                            str(len(moveableTiles)), True, LGREEN, BLACK)

    moveableRectObj = moveableSurfaceObj.get_rect()
    moveableRectObj.center = (550,50)

    # draw the text to the display surface (DS)
    DS.blit(movesSurfaceObj, movesRectObj)
    DS.blit(moveableSurfaceObj, moveableRectObj)

def drawBoard():
    pygame.draw.rect(DS, GREY, (49, 0, 402, 502))
    for i in tiles:
        pygame.draw.rect(DS, YELLOW, i, 2)
    for i in emptyTiles:
        pygame.draw.rect(DS, BLACK, i)
        
def getEmptyTileState():
    if abs(emptyTiles[0].centerx - emptyTiles[1].centerx) == 100 and \
            emptyTiles[0].centery == emptyTiles[1].centery:
        return TOGETHER_HORZ
    elif abs(emptyTiles[0].centery - emptyTiles[1].centery) == 100 and \
            emptyTiles[0].centerx == emptyTiles[1].centerx:
        return TOGETHER_VERT
    else:
        return APART


def buildMoveableTileList(moveableTiles):

    for i in tiles:

        if i.midleft == emptyTiles[0].midright or i.midleft ==  emptyTiles[1].midright:
            moveableTiles.append(i)

        elif i.midright == emptyTiles[0].midleft or i.midright == emptyTiles[1].midleft:
            moveableTiles.append(i)

        elif i.midbottom == emptyTiles[0].midtop or i.midbottom ==  emptyTiles[1].midtop:
            moveableTiles.append(i)

        elif i.midtop == emptyTiles[0].midbottom or i.midtop == emptyTiles[1].midbottom:
            moveableTiles.append(i)

    empState = getEmptyTileState()
    
    if empState == TOGETHER_HORZ:
        for i in tiles:

            # wide tile on top empties on bottom
            if i.bottomright == emptyTiles[0].topright and i.bottomleft == emptyTiles[1].topleft:
                moveableTiles.append(i)
            elif i.bottomright == emptyTiles[1].topright and i.bottomleft == emptyTiles[0].topleft:
                moveableTiles.append(i)

            # wide tile on bottom empties on top
            if i.topright == emptyTiles[0].bottomright and i.topleft == emptyTiles[1].bottomleft:
                moveableTiles.append(i)
            elif i.topright == emptyTiles[1].bottomright and i.topleft == emptyTiles[0].bottomleft:
                moveableTiles.append(i)

    if empState == TOGETHER_VERT:
        for i in tiles:
            
            # Tall tile verticaly right of stacked empties
            if i.bottomleft == emptyTiles[0].bottomright and i.topleft == emptyTiles[1].topright:
                moveableTiles.append(i)
            elif i.bottomleft == emptyTiles[1].bottomright and i.topleft == emptyTiles[0].topright:
                moveableTiles.append(i)

            # Tall tile vertically left of stacked empties 
            if i.bottomright == emptyTiles[0].bottomleft and i.topright == emptyTiles[1].topleft:
                moveableTiles.append(i)
            elif i.bottomright == emptyTiles[1].bottomleft and i.topright == emptyTiles[0].topleft:
                moveableTiles.append(i)


def getNextMoveableTile(moveableTiles, curTile):
    i = moveableTiles.index(curTile)
    if i == len(moveableTiles) - 1:
        return moveableTiles[0]
    else:
        return moveableTiles[i + 1]

def findEmptyTileToSwap(tile, direction):
    if direction == K_DOWN:
        for i in emptyTiles:
            if i.midtop == tile.midbottom:
                return emptyTiles.index(i)
    elif direction == K_UP:
        for i in emptyTiles:
            if i.midbottom == tile.midtop:
                return emptyTiles.index(i)
    elif direction == K_RIGHT:
        for i in emptyTiles:
            if i.midleft == tile.midright:
                return emptyTiles.index(i)
    elif direction == K_LEFT:
        for i in emptyTiles:
            if i.midright == tile.midleft:
                return emptyTiles.index(i)
    else:
        return None
    
def move(tile, direction, moveCount, f):
    tileIndex = tiles.index(tile)
    emptyTileIndex = findEmptyTileToSwap(tile, direction)

    if emptyTileIndex == None:
        return None

    if direction == K_DOWN:

        if tiles[tileIndex].width == NARROW:
            f.write("narrow tile down from " + str(tiles[tileIndex]) + NEW_LINE)
            tiles[tileIndex].bottom = emptyTiles[emptyTileIndex].bottom
            emptyTiles[emptyTileIndex].bottom = tiles[tileIndex].top
            f.write("narrow tile to " + str(tiles[tileIndex]) + NEW_LINE)

        # MOVE THE HORIZONTAL TILE DOWN DOESN'T WORK
        elif tiles[tileIndex].width == WIDE:
            f.write("horz tile" + str(tiles[tileIndex]) + NEW_LINE)
            emptyTiles[0].centery = tiles[tileIndex].centery
            emptyTiles[1].centery = tiles[tileIndex].centery
            tiles[tileIndex].bottom = emptyTiles[0].bottom
        else:
            return None

    elif tiles[tileIndex].width == NARROW and direction == K_UP:
        tiles[tileIndex].top = emptyTiles[emptyTileIndex].top
        emptyTiles[emptyTileIndex].top = tiles[tileIndex].bottom

    elif tiles[tileIndex].height == SHORT and direction == K_RIGHT:
        tiles[tileIndex].right = emptyTiles[emptyTileIndex].right
        emptyTiles[emptyTileIndex].right = tiles[tileIndex].left

    elif tiles[tileIndex].height == SHORT and direction == K_LEFT:
        tiles[tileIndex].left = emptyTiles[emptyTileIndex].left
        emptyTiles[emptyTileIndex].left = tiles[tileIndex].right
    
    moveCount += 1
    drawBoard()
    pygame.display.update()
    fpsClock.tick(FPS)
    return moveCount

def main():
    moveCount = 0
    DS.fill(BGCOLOR)
    drawBoard()

    moveableTiles = list()
    buildMoveableTileList(moveableTiles)
    drawText(moveCount, moveableTiles)
    curTile = tiles[8]  # bottom left tile seems like a good starting selection
    prevTile = tiles[8]
    f = open('klotski.log', 'a')

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_TAB:
                    curTile = getNextMoveableTile(moveableTiles, curTile)
                    pygame.draw.rect(DS, YELLOW, prevTile, 2)
                    pygame.draw.rect(DS, RED, curTile, 2)
                    prevTile = curTile
                if event.key in (K_UP, K_DOWN, K_RIGHT, K_LEFT):
                    tempCount = move(curTile, event.key, moveCount, f)
                    if tempCount == None:
                        continue

                    moveCount = tempCount
                    del moveableTiles[:]
                    buildMoveableTileList(moveableTiles)
                    drawText(moveCount, moveableTiles)

        pygame.display.update()
        fpsClock.tick(FPS)
    f.close()

if __name__ == '__main__':
    main()
