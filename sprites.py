#!/usr/bin/python
# -*- coding: latin-1 -*-

# Reggie! - New Super Mario Bros. U Level Editor
# Version v0.3 ALPHA
# Copyright (C) 2009-2015 Treeki, Tempus, angelsl, JasonP27, Kamek64,
# MalStar1000, RoadrunnerWMC, MrRean

# This file is part of Reggie!.

# Reggie! is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Reggie! is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Reggie!.  If not, see <http://www.gnu.org/licenses/>.



# sprites.py
# Contains code to render NSMBU sprite images
# not even close to done...need to do quite a few


################################################################
################################################################

# Imports

from PyQt5 import QtCore, QtGui
Qt = QtCore.Qt


import spritelib as SLib
ImageCache = SLib.ImageCache


################################################################
################################################################

# GETTING SPRITEDATA:
# You can get the spritedata that is set on a sprite to alter
# the image that is shown. To do this, add a datachanged method,
# with the parameter self. In this method, you can access the
# spritedata through self.parent.spritedata[n], which returns
# the (n+1)th byte of the spritedata. To find the n for nybble
# x, use this formula:
# n = (x/2) - 1
#
# If the nybble you want is the upper 4 bits of n (odd), you
# can get the value of x like this:
# val_x = n >> 4

class SpriteImage_Block(SLib.SpriteImage): # 59, 60
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.spritebox.shown = False
        self.contentsOverride = None

        self.tilenum = 1315
        self.tileheight = 1
        self.tilewidth = 1
        self.yOffset = 0
        self.xOffset = 0
        self.invisiblock = False

    def dataChanged(self):
        super().dataChanged()

        if self.contentsOverride is not None:
            self.image = ImageCache['Items'][self.contentsOverride]
        else:
            contents = self.parent.spritedata[9] & 0xF
            acorn = (self.parent.spritedata[6] >> 4) & 1

            if acorn:
                self.image = ImageCache['Items'][15]
            elif contents != 0:
                self.image = ImageCache['Items'][contents-1]
            else:  # load a coin if a stupid value is entered. Also, 0.
                self.image = ImageCache['Items'][0]

    def paint(self, painter):
        super().paint(painter)

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        if self.tilenum < len(SLib.Tiles):
            if self.invisiblock:
                painter.drawPixmap(0, 0, ImageCache['InvisiBlock'])
            else:
                painter.drawPixmap(self.yOffset, self.xOffset, self.tilewidth*60, self.tileheight*60, SLib.Tiles[self.tilenum].main)
        painter.drawPixmap(0, 0, self.image)

class SpriteImage_Goomba(SLib.SpriteImage_Static): # 0
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['Goomba'],
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Goomba', 'goomba.png')

# Unused/sprite image doesn't exist
#class SpriteImage_PipePiranhaUp(SLib.SpriteImage_Static): # 2
#    def __init__(self, parent):
#        super().__init__(
#            parent,
#            4.75,
#            ImageCache['PipePiranhaUp'],
#            )
#
#    @staticmethod
#    def loadImages():
#        SLib.loadIfNotInImageCache('PipePiranhaUp', 'piranha_pipe_up.png')        

# Image needs to be improved
class SpriteImage_KoopaTroopa(SLib.SpriteImage_StaticMultiple): # 19
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ) #What image to load is taken care of later

        self.yOffset = -2
        self.xOffset = -1

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('KoopaG', 'koopa_green.png')
        SLib.loadIfNotInImageCache('KoopaR', 'koopa_red.png')

    def dataChanged(self):

        # shiz
        shellcolor = self.parent.spritedata[5] & 1 # just 2 values, so throw this

        if shellcolor == 0:
            self.image = ImageCache['KoopaG']
        else:
            self.image = ImageCache['KoopaR']
            
        super().dataChanged()

# Image doesn't exist
#class SpriteImage_StarCoin(SLib.SpriteImage_Static): # 45
#    def __init__(self, parent):
#        super().__init__(
#            parent,
#            3.75,
#            ImageCache['StarCoin'],
#            )
#
#    @staticmethod
#    def loadImages():
#        SLib.loadIfNotInImageCache('StarCoin', 'starcoin.png')

# Image doesn't exist
#class SpriteImage_MovementControlledStarCoin(SLib.SpriteImage_Static): # 48
#    def __init__(self, parent):
#        super().__init__(
#            parent,
#            3.75,
#            ImageCache['MCStarCoin'],
#            )
#
#    @staticmethod
#    def loadImages():
#        SLib.loadIfNotInImageCache('MCStarCoin', 'starcoin.png')               

class SpriteImage_QBlock(SpriteImage_Block): # 59
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            )
        self.tilenum = 49

class SpriteImage_BrickBlock(SpriteImage_Block): # 60
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            )
        self.tilenum = 48

class SpriteImage_InvisiBlock(SpriteImage_Block): # 61
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            )
        self.invisiblock = True

class SpriteImage_Coin(SLib.SpriteImage_Static): # 65
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['Coin'],
            )

class SpriteImage_MovementControllerTwoWay(SLib.SpriteImage): # 70
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            )

        width = ((self.parent.spritedata[7] & 0xF) + 1) << 4
        distance = self.parent.spritedata[5] >> 4
        self.aux.append(SLib.AuxiliaryTrackObject(parent, width, distance + 60, SLib.AuxiliaryTrackObject.Vertical))


    def dataChanged(self):
        super().dataChanged()

        distance = self.parent.spritedata[5] >> 4
        width = ((self.parent.spritedata[7] & 0xF) + 1) << 4
        self.aux[0].setSize(width, distance + 60)
        self.aux[0].setPos(0, 0)
        self.aux[0].update()        

class SpriteImage_MovingCoin(SLib.SpriteImage_Static): # 87
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['Coin'],
            )

class SpriteImage_QuestionSwitch(SLib.SpriteImage_Static): # 104
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['QSwitch'],
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('QSwitch', 'q_switch.png')

class SpriteImage_PSwitch(SLib.SpriteImage_Static): # 105
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['PSwitch'],
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('PSwitch', 'p_switch.png')        

class SpriteImage_PipeUp(SLib.SpriteImage): # 139
    def __init__(self, parent, scale=3.75):
        super().__init__(parent, scale)
        self.spritebox.shown = False
        self.parent.setZValue(24999)
        self.width = 32
        self.pipeHeight = 60
        self.hasTop = True
        self.colour = 0
        self.colours = ('Green', 'Red', 'Yellow', 'Blue')

    @staticmethod
    def loadImages():
        if 'PipeTopGreen' not in ImageCache:
            for colour in ('Green', 'Red', 'Yellow', 'Blue'):
                ImageCache['PipeTop%s' % colour] = SLib.GetImg('pipe_%s_top.png' % colour.lower())
                ImageCache['PipeMiddleV%s' % colour] = SLib.GetImg('pipe_%s_middle.png' % colour.lower())

    def dataChanged(self):
        super().dataChanged()

        rawheight = (self.parent.spritedata[5] & 0x0F) + 1
        rawtop = self.parent.spritedata[2] >> 4
        rawcolour = self.parent.spritedata[5] >> 4

        if rawtop == 0:
            self.hasTop = True
            self.pipeHeight = rawheight
        elif rawtop == 1:
            self.hasTop = True
            self.pipeHeight = rawheight + 1
        elif rawtop == 3:
            self.hasTop = False
            self.pipeHeight = rawheight
        else:
            self.hasTop = True
            self.pipeHeight = rawheight

        self.height = self.pipeHeight * 16
        self.yOffset = 16 - self.height
        self.colour = self.colours[rawcolour]

    def paint(self, painter):
        super().paint(painter)

        if self.hasTop:
            painter.drawPixmap(0, 0, ImageCache['PipeTop%s' % self.colour])
            painter.drawTiledPixmap(0, 60, 120, self.pipeHeight * 60 - 60, ImageCache['PipeMiddleV%s' % self.colour])
        else:
            painter.drawTiledPixmap(0, 0, 120, self.pipeHeight * 60, ImageCache['PipeMiddleV%s' % self.colour])

class SpriteImage_BubbleYoshi(SLib.SpriteImage_Static): # 143, 243
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['BubbleYoshi'],
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BubbleYoshi', 'babyyoshibubble.png')
       
class SpriteImage_POWBlock(SLib.SpriteImage_Static): # 152
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['POWBlock'],
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('POWBlock', 'block_pow.png')  

class SpriteImage_CoinOutline(SLib.SpriteImage_StaticMultiple): # 158
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75, # native res (3.75*16=60)
            ImageCache['CoinOutlineMultiplayer'],
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('CoinOutline', 'coin_outline.png')
        SLib.loadIfNotInImageCache('CoinOutlineMultiplayer', 'coin_outline_multiplayer.png')

    def dataChanged(self):
        multi = (self.parent.spritedata[2] >> 4) & 1
        self.image = ImageCache['CoinOutline' + ('Multiplayer' if multi else '')]
        super().dataChanged()

class SpriteImage_Springboard(SLib.SpriteImage_Static): # 215
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['Springboard'],
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Springboard', 'springboard.png')         

class SpriteImage_BalloonYoshi(SLib.SpriteImage_Static): # 224
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['BalloonYoshi'],
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BalloonYoshi', 'balloonbabyyoshi.png')

class SpriteImage_TileGod(SLib.SpriteImage): # 237
    def __init__(self, parent):
        super().__init__(parent, 3.75)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 0, 0))

    def dataChanged(self):
        super().dataChanged()

        width = self.parent.spritedata[8] & 0xF
        height = self.parent.spritedata[5] >> 4
        if width == 0: width = 1
        if height == 0: height = 1
        if width == 1 and height == 1:
            self.aux[0].setSize(0,0)
            return
        self.aux[0].setSize(width * 60, height * 60)

class SpriteImage_Muncher(SLib.SpriteImage_StaticMultiple): # 259
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ) 

        #self.yOffset = -2
        #self.xOffset = -1

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('MuncherReg', 'muncher.png')
        SLib.loadIfNotInImageCache('MuncherFr', 'muncher_frozen.png')

    def dataChanged(self):

        # shiz
        shellcolor = self.parent.spritedata[5] & 1 # just 2 values, so throw this

        if shellcolor == 0:
            self.image = ImageCache['MuncherReg']
        else:
            self.image = ImageCache['MuncherFr']
            
        super().dataChanged()        

class SpriteImage_Parabeetle(SLib.SpriteImage_Static): # 261
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['Parabeetle'],
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Parabeetle', 'parabeetle.png')

class SpriteImage_RotationControlledCoin(SLib.SpriteImage_Static): # 325
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['Coin'],
            )

class SpriteImage_MovementControlledCoin(SLib.SpriteImage_Static): # 326
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['Coin'],
            )

class SpriteImage_BoltControlledCoin(SLib.SpriteImage_Static): # 328
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['Coin'],
            )

class SpriteImage_WoodenBox(SLib.SpriteImage_StaticMultiple): # 338
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Reg2x2', 'reg_box_2x2.png')
        SLib.loadIfNotInImageCache('Reg4x2', 'reg_box_4x2.png')
        SLib.loadIfNotInImageCache('Reg2x4', 'reg_box_2x4.png')
        SLib.loadIfNotInImageCache('Reg4x4', 'reg_box_4x4.png')                
        SLib.loadIfNotInImageCache('Inv2x2', 'inv_box_2x2.png')
        SLib.loadIfNotInImageCache('Inv4x2', 'inv_box_4x2.png')
        SLib.loadIfNotInImageCache('Inv2x4', 'inv_box_2x4.png')
        SLib.loadIfNotInImageCache('Inv4x4', 'inv_box_4x4.png')        

    def dataChanged(self):          
        
        boxcolor = self.parent.spritedata[4]
        boxsize = self.parent.spritedata[5] >> 4
        
        if boxsize == 0 and boxcolor == 0:
            self.image = ImageCache['Reg2x2']
        elif boxsize == 1 and boxcolor == 0:
            self.image = ImageCache['Reg2x4']
        elif boxsize == 2 and boxcolor == 0:
            self.image = ImageCache['Reg4x2']
        elif boxsize == 3 and boxcolor == 0:
            self.image = ImageCache['Reg4x4']
        elif boxsize == 0 and boxcolor == 2:
            self.image = ImageCache['Inv2x2']
        elif boxsize == 1 and boxcolor == 2:
            self.image = ImageCache['Inv2x4']
        elif boxsize == 2 and boxcolor == 2:
            self.image = ImageCache['Inv4x2']
        elif boxsize == 3 and boxcolor == 2:
            self.image = ImageCache['Inv4x4']
        else:
            self.image = ImageCache['Reg2x2'] # let's not make some nonsense out of this
            
        super().dataChanged()
   
class SpriteImage_SuperGuide(SLib.SpriteImage_Static): # 348
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['SuperGuide'],
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('SuperGuide', 'guide_block.png')          

class SpriteImage_GoldenYoshi(SLib.SpriteImage_Static): # 365
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['GoldenYoshi'],
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('GoldenYoshi', 'babyyoshiglowing.png')

# Unfinished
#class SpriteImage_BigBrickBlock(SpriteImage_Block): # 422
#    def __init__(self, parent):
#        super().__init__(
#            parent,
#            3.75,
#            )
#        self.tilenum = 128
#        self.tileheight = 2
#        self.tilewidth = 2

class SpriteImage_BonyBeetle(SLib.SpriteImage_Static): # 443
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['BonyBeetle'],
            )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BonyBeetle', 'bony_beetle.png')

# Unfinished
#class SpriteImage_BigQBlock(SpriteImage_Block): # 475
#    def __init__(self, parent):
#        super().__init__(
#            parent,
#            3.75,
#            )
#        self.tilenum = 130
#        self.tileheight = 2
#        self.tilewidth = 2

class SpriteImage_WaddleWing(SLib.SpriteImage_StaticMultiple): # 481
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ) #What image to load is taken care of later

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('WaddlewingL', 'waddlewing_l.png')
        SLib.loadIfNotInImageCache('WaddlewingR', 'waddlewing_r.png')

    def dataChanged(self):

        # shiz
        rawdir = self.parent.spritedata[5]

        if rawdir == 2:
            self.image = ImageCache['WaddlewingR']
        else:
            self.image = ImageCache['WaddlewingL']
            
        super().dataChanged()

class SpriteImage_BoltControlledMovingCoin(SLib.SpriteImage_Static): # 496
    def __init__(self, parent):
        super().__init__(
            parent,
            3.75,
            ImageCache['Coin'],
            )

class SpriteImage_MovingGrassPlatform(SLib.SpriteImage): # 499
    def __init__(self, parent):
        super().__init__(parent, 3.75)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 0, 0))

    def dataChanged(self):
        super().dataChanged()

        width = self.parent.spritedata[8] & 0xF
        height = self.parent.spritedata[9] & 0xF
        if width == 0: width = 1
        if height == 0: height = 1
        if width == 1 and height == 1:
            self.aux[0].setSize(0,0)
            return
        self.aux[0].setSize(width * 60, height * 60)        

################################################################
################################################################


ImageClasses = {
    0: SpriteImage_Goomba,
    19: SpriteImage_KoopaTroopa,
    59: SpriteImage_QBlock,
    60: SpriteImage_BrickBlock,
    61: SpriteImage_InvisiBlock,
    65: SpriteImage_Coin,
#    70: SpriteImage_MovementControllerTwoWay,
    87: SpriteImage_MovingCoin,
    104: SpriteImage_QuestionSwitch,
    105: SpriteImage_PSwitch,
    139: SpriteImage_PipeUp,
    143: SpriteImage_BubbleYoshi,
    152: SpriteImage_POWBlock,
    158: SpriteImage_CoinOutline,
    215: SpriteImage_Springboard,
    224: SpriteImage_BalloonYoshi,
    237: SpriteImage_TileGod,
    243: SpriteImage_BubbleYoshi,
    259: SpriteImage_Muncher,
    261: SpriteImage_Parabeetle,
    325: SpriteImage_RotationControlledCoin,
    326: SpriteImage_MovementControlledCoin,
    328: SpriteImage_BoltControlledCoin,
    338: SpriteImage_WoodenBox,    
    348: SpriteImage_SuperGuide,
    365: SpriteImage_GoldenYoshi,
#    422: SpriteImage_BigBrickBlock,
    443: SpriteImage_BonyBeetle,
#    475: SpriteImage_BigQBlock,
    481: SpriteImage_WaddleWing,
    496: SpriteImage_BoltControlledMovingCoin,
    499: SpriteImage_MovingGrassPlatform,
    }
