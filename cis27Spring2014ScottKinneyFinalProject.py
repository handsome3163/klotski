#!/usr/bin/env python
'''
Program Name: cis27Spring2014ScottKinneyFinalProject.py
Written By:   Scott Kinney
Date:         Tue May 20 19:33:30 PDT 2014
'''

import sys, os
import pygame
from pygame.locals import *

# The starting state of the board
import start
from start import *

pygame.init()
fpsClock = pygame.time.Clock()

# set up the window
DS = pygame.display.set_mode((500, 600), 0, 32)
pygame.display.set_caption\
    ("CIS 27 Spring 2014 Scott Kinney Final ~ Klotski Puzzle")

def drawText(moveCount, moveableTiles):
    fontObj = pygame.font.Font('freesansbold.ttf', 24)
    movesSurfaceObj = fontObj.render('Moves: ' + str(moveCount), \
                                         True, LGREEN, BLACK)
    movesRectObj = movesSurfaceObj.get_rect()
    movesRectObj.center = (75,575)

    fontObj = pygame.font.Font('freesansbold.ttf', 14)
    instrucSurfaceObj = fontObj.render\
        ("Tab thru moveable tiles and use arrow to move", True, LGREEN, BLACK)

    instrucRectObj = instrucSurfaceObj.get_rect()
    instrucRectObj.center = (175,535)

    # draw the text to the display surface (DS)
    DS.blit(movesSurfaceObj, movesRectObj)
    DS.blit(instrucSurfaceObj, instrucRectObj)

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
        if i.midleft == emptyTiles[0].midright or i.midleft ==  \
                emptyTiles[1].midright:
            moveableTiles.append(i)

        elif i.midright == emptyTiles[0].midleft or i.midright == \
                emptyTiles[1].midleft:
            moveableTiles.append(i)

        elif i.midbottom == emptyTiles[0].midtop or i.midbottom == \
                emptyTiles[1].midtop:
            moveableTiles.append(i)

        elif i.midtop == emptyTiles[0].midbottom or i.midtop == \
                emptyTiles[1].midbottom:
            moveableTiles.append(i)

    empState = getEmptyTileState()
    
    if empState == TOGETHER_HORZ:
        for i in tiles:

            # wide tile on top empties on bottom
            if i.bottomright == emptyTiles[0].topright and i.bottomleft == \
                    emptyTiles[1].topleft:
                moveableTiles.append(i)
            elif i.bottomright == emptyTiles[1].topright and i.bottomleft == \
                    emptyTiles[0].topleft:
                moveableTiles.append(i)

            # wide tile on bottom empties on top
            if i.topright == emptyTiles[0].bottomright and i.topleft == \
                    emptyTiles[1].bottomleft:
                moveableTiles.append(i)
            elif i.topright == emptyTiles[1].bottomright and i.topleft == \
                    emptyTiles[0].bottomleft:
                moveableTiles.append(i)

    if empState == TOGETHER_VERT:
        for i in tiles:
            
            # Tall tile verticaly right of stacked empties
            if i.bottomleft == emptyTiles[0].bottomright and i.topleft == \
                    emptyTiles[1].topright:
                moveableTiles.append(i)
            elif i.bottomleft == emptyTiles[1].bottomright and i.topleft == \
                    emptyTiles[0].topright:
                moveableTiles.append(i)

            # Tall tile vertically left of stacked empties 
            if i.bottomright == emptyTiles[0].bottomleft and i.topright == \
                    emptyTiles[1].topleft:
                moveableTiles.append(i)
            elif i.bottomright == emptyTiles[1].bottomleft and i.topright == \
                    emptyTiles[0].topleft:
                moveableTiles.append(i)


def getNextMoveableTile(moveableTiles, curTile):
    i = moveableTiles.index(curTile)
    if i == len(moveableTiles) - 1:
        return moveableTiles[0]
    else:
        return moveableTiles[i + 1]

def isValidMove(tile, direction):
    bool = False
    empState = getEmptyTileState()
    
    if empState == TOGETHER_HORZ and direction == K_DOWN:
            # wide tile on top empties on bottom
            if tile.bottomright == emptyTiles[0].topright and tile.bottomleft == \
                    emptyTiles[1].topleft:
                bool = True
            elif tile.bottomright == emptyTiles[1].topright and tile.bottomleft == \
                    emptyTiles[0].topleft:
                bool = True
    elif empState == TOGETHER_HORZ and direction == K_UP:
            # wide tile on bottom empties on top
            if tile.topright == emptyTiles[0].bottomright and tile.topleft == \
                    emptyTiles[1].bottomleft:
                bool = True
            elif tile.topright == emptyTiles[1].bottomright and tile.topleft == \
                    emptyTiles[0].bottomleft:
                bool = True

    elif empState == TOGETHER_VERT and direction == K_LEFT:
            
            # Tall tile verticaly right of stacked empties
            if tile.bottomleft == emptyTiles[0].bottomright and tile.topleft == \
                    emptyTiles[1].topright:
                bool = True
            elif tile.bottomleft == emptyTiles[1].bottomright and tile.topleft == \
                    emptyTiles[0].topright:
                bool = True

    elif empState == TOGETHER_VERT and direction == K_RIGHT:
            # Tall tile vertically left of stacked empties 
            if tile.bottomright == emptyTiles[0].bottomleft and tile.topright == \
                    emptyTiles[1].topleft:
                bool = True
            elif tile.bottomright == emptyTiles[1].bottomleft and tile.topright == \
                    emptyTiles[0].topleft:
                bool = True
    else:
        bool = False
    return bool
    

def findEmptyTileToSwap(tile, direction):
    index = None

    if tile.width == NARROW or tile.height == SHORT:
        if direction == K_DOWN:
            for i in emptyTiles:
                if i.midtop == tile.midbottom:
                    index = emptyTiles.index(i)

        elif direction == K_UP:
            for i in emptyTiles:
                if i.midbottom == tile.midtop:
                    index = emptyTiles.index(i)

        if direction == K_RIGHT:
            for i in emptyTiles:
                if i.midleft == tile.midright:
                    index = emptyTiles.index(i)
                    
        elif direction == K_LEFT:
            for i in emptyTiles:
                if i.midright == tile.midleft:
                    index = emptyTiles.index(i)
    return index
    
def move(tile, direction, moveCount, f):
    tileIndex = tiles.index(tile)
    if tileIndex == None:
        return None

    emptyTileIndex = findEmptyTileToSwap(tile, direction)
    
    if direction == K_DOWN:
        if tiles[tileIndex].width == NARROW and emptyTileIndex != None:
            tiles[tileIndex].bottom = emptyTiles[emptyTileIndex].bottom
            emptyTiles[emptyTileIndex].bottom = tiles[tileIndex].top
            moveCount += 1
    
        elif tiles[tileIndex].width == WIDE and isValidMove(tile, direction):
            tiles[tileIndex].bottom = emptyTiles[0].bottom
            emptyTiles[0].bottom = tiles[tileIndex].top
            emptyTiles[1].bottom = tiles[tileIndex].top
            moveCount += 1

    elif direction == K_UP:
        if tiles[tileIndex].width == NARROW and emptyTileIndex != None:
            tiles[tileIndex].top = emptyTiles[emptyTileIndex].top
            emptyTiles[emptyTileIndex].top = tiles[tileIndex].bottom
            moveCount += 1

        elif tiles[tileIndex].width == WIDE and isValidMove(tile, direction):
            tiles[tileIndex].top = emptyTiles[0].top
            emptyTiles[0].top = tiles[tileIndex].bottom
            emptyTiles[1].top = tiles[tileIndex].bottom
            moveCount += 1

    elif direction == K_RIGHT:
        if tiles[tileIndex].height == SHORT and emptyTileIndex != None:
            tiles[tileIndex].right = emptyTiles[emptyTileIndex].right
            emptyTiles[emptyTileIndex].right = tiles[tileIndex].left
            moveCount += 1
    
        elif tiles[tileIndex].height == TALL and isValidMove(tile, direction):
            tiles[tileIndex].right = emptyTiles[0].right
            emptyTiles[0].right = tiles[tileIndex].left
            emptyTiles[1].right = tiles[tileIndex].left
            moveCount += 1

    elif direction == K_LEFT:
        if tiles[tileIndex].height == SHORT and emptyTileIndex != None:
            tiles[tileIndex].left = emptyTiles[emptyTileIndex].left
            emptyTiles[emptyTileIndex].left = tiles[tileIndex].right
            moveCount += 1

        elif tiles[tileIndex].height == TALL and isValidMove(tile, direction):
            tiles[tileIndex].left = emptyTiles[0].left
            emptyTiles[0].left = tiles[tileIndex].right
            emptyTiles[1].left = tiles[tileIndex].right
            moveCount += 1
    else:
        return None

    drawBoard()
    pygame.display.update()
    fpsClock.tick(FPS)
    return moveCount

def isSolved(tile):
    if tile.size == (200,200) and tile.midbottom == (250,500):
        return True
    else:
        return False

def terminate():
     pygame.quit()
     sys.exit()

def solvedMessage(DS):
    fontObj = pygame.font.Font('freesansbold.ttf', 24)
    solvedSurfaceObj = fontObj.render('Solved', True, LGREEN, GREY)

    solvedRectObj = solvedSurfaceObj.get_rect()
    solvedRectObj.center = (250, 450)

    DS.blit(solvedSurfaceObj, solvedRectObj)
    DS.blit(solvedSurfaceObj, solvedRectObj)
    
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
    f.write(NEW_LINE + "** New game **" + NEW_LINE)

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if isSolved(curTile):
                solvedMessage(DS)
                break
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

if __name__ == '__main__':
    main()
