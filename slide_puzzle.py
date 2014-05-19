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
        
def buildMoveableTileList(moveableTiles):
    for i in tiles:

        if i.midleft == emptyTiles[0].midright or i.midleft ==  emptyTiles[1].midright:
            moveableTiles.append(i)

        if i.midright == emptyTiles[0].midleft or i.midright == emptyTiles[1].midleft:
            moveableTiles.append(i)

        if i.midbottom == emptyTiles[0].midtop or i.midbottom ==  emptyTiles[1].midtop:
            moveableTiles.append(i)

        if i.midtop == emptyTiles[0].midbottom or i.midbottom == emptyTiles[1].midbottom:
            moveableTiles.append(i)
        
        if i.midbottom == emptyTiles[0].topright and emptyTiles[1].topleft == i.midbottom:
            moveableTiles.append(i)
        if i.midbottom == emptyTiles[1].topright and emptyTiles[0].topleft == i.midbottom:
            moveableTiles.append(i)

        if i.midtop == emptyTiles[0].bottomright and emptyTiles[1].bottomleft == i.midtop:
            moveableTiles.append(i)
        if i.midtop == emptyTiles[1].bottomright and emptyTiles[0].bottomleft == i.midtop:
            moveableTiles.append(i)
        
        if i.midleft == emptyTiles[0].topright and emptyTiles[1].bottomright == i.midleft:
            moveableTiles.append(i)
        if i.midleft == emptyTiles[1].topright and emptyTiles[0].bottomright == i.midleft:
            moveableTiles.append(i)
            
        if i.midright == emptyTiles[0].topleft and emptyTiles[1].bottomleft == i.midright:
            moveableTiles.append(i)
        if i.midright == emptyTiles[1].topleft and emptyTiles[0].bottomleft == i.midright:
            moveableTiles.append(i)


def getNextMoveableTile(moveableTiles, curTile):
    if moveableTiles.index(curTile) == len(moveableTiles) - 1:
        return moveableTiles[0]
    else:
        return moveableTiles[moveableTiles.index(curTile) + 1]

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
    
def move(tile, direction, moveCount):
    tileIndex = tiles.index(tile)
    emptyTileIndex = findEmptyTileToSwap(tile, direction)

    if emptyTileIndex == None:
        return None

    if tiles[tileIndex].width == 100 and direction == K_DOWN:
        temp = tile.top
        tiles[tileIndex].bottom = emptyTiles[emptyTileIndex].bottom
        emptyTiles[emptyTileIndex].top = temp

    elif tiles[tileIndex].width == 100 and direction == K_UP:
        temp = tile.bottom
        tiles[tileIndex].top = emptyTiles[emptyTileIndex].top
        emptyTiles[emptyTileIndex].bottom = temp

    elif tiles[tileIndex].height == 100 and direction == K_RIGHT:
        temp = tile.left
        tiles[tileIndex].right = emptyTiles[emptyTileIndex].right
        emptyTiles[emptyTileIndex].left = temp

    elif tiles[tileIndex].height == 100 and direction == K_LEFT:
        temp = tile.right
        tiles[tileIndex].left = emptyTiles[emptyTileIndex].left
        emptyTiles[emptyTileIndex].right = temp

    elif tiles[tileIndex].width == 200 and direction == K_DOWN:
        temp = tile.top
        tiles[tileIndex].bottom = emptyTiles[0].bottom
        emptyTiles[0].top = temp
        emptyTiles[1].top = temp
    else:
        return None
    
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
    curTile = tiles[8]
    prevTile = tiles[8]

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
                    tempCount = move(curTile, event.key, moveCount)
                    if tempCount == None:
                        continue
                    moveCount = tempCount
                    drawText(moveCount, moveableTiles)    
                    del moveableTiles[:]
                    buildMoveableTileList(moveableTiles)

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
