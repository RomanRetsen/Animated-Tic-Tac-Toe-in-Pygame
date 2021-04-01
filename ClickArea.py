import bisect
import random
import pygame
import math

class ClickArea:

    def __init__(self, position, screen, g_set, g_stats):
        self.x, self.y = position
        self.screen = screen
        self.g_stats = g_stats
        self.g_set = g_set
        self.screen_rect = screen.get_rect()
        self.width = g_set.click_area_width
        self.height = g_set.click_area_height
        #center of the cell and defaulf mouse click are the same
        self.centerx = self.mouseClickLocationx = position[0] + int(g_set.click_area_width / 2)
        self.centery = self.mouseClickLocationy = position[1] + int(g_set.click_area_height /  2)

        # sign "x" is not drawn from the edges of area(square). Space offset is set here
        self.signOffSetx = int(self.width * 0.1)
        self.signOffSety = int(self.height * 0.1)
        self.backgroundcolor = (255, 255, 255)
        self.linecolor = (0, 0, 255)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        #list of functions of drawing sign "O"  to random pick from.
        self.oFunc = [self.drawing_click_area_o, self.drawing_click_area_o2, self.drawing_click_area_o3,
                      self.drawing_click_area_o4, self.drawing_click_area_o5, self.drawing_click_area_o6,
                      self.drawing_click_area_o7, self.drawing_click_area_o8, self.drawing_click_area_o9,
                      self.drawing_click_area_o10, self.drawing_click_area_o11]

        #list of functions of drawing sign "X"  to random pick from.
        self.xFunc = [self.drawing_click_area_x, self.drawing_click_area_x2, self.drawing_click_area_x3,
                      self.drawing_click_area_x4, self.drawing_click_area_x5, self.drawing_click_area_x6,
                      self.drawing_click_area_x7]

        self.clickAreaReset()

    def clickAreaReset(self):
        self.state = 'b'
        self.calculateCrossCoord()
        self.calculateEllipseCoord()
        self.randomChooseXFunc()
        self.randomChooseOFunc()

    def calculateCrossCoord(self):
        #line 1 . It's 2 points - top left and bottom right
        self.x1_1 = self.x + self.signOffSetx
        self.y1_1 = self.y + self.signOffSety
        self.x1_2 = self.x + self.width - self.signOffSetx
        self.y1_2 = self.y + self.height - self.signOffSety
        self.length_of_line = int(math.sqrt((self.x1_1 - self.x1_2)**2 + (self.y1_1 - self.y1_2)**2))
        self.half_length_line = int(self.length_of_line / 2)
        # line 2. 2 points - top right and bottom left
        self.x2_1 = self.x + self.width - self.signOffSetx
        self.y2_1 = self.y + self.signOffSety
        self.x2_2 = self.x + self.signOffSetx
        self.y2_2 = self.y + self.height - self.signOffSety
        # cross point
        self.x_half = self.mouseClickLocationx = self.x + int(self.width / 2 )
        self.y_half = self.mouseClickLocationy = self.y + int(self.height / 2 )
        self.growingx = 0
        self.growingy = 0
        # slope and b info needed for line formula
        self.slope1 =  (self.y1_2 - self.y1_1) / (self.x1_2 - self.x1_1)
        self.b1 = self.y1_2 - self.slope1 * self.x1_2
        self.slope2 =  (self.y2_2 - self.y2_1) / (self.x2_2 - self.x2_1)
        self.b2 = self.y2_2 - self.slope2 * self.x2_2
        # Two stages for drawing X
        self.stage1_x_done = False
        self.stage2_x_done = False

    #For drawing "O" different approach was chosen. All coord. of dots of the ellipse put in list
    def calculateEllipseCoord(self):
        self.ellipseAnimationSlice = 0
        self.t = 0.1
        minorRadius = int((self.width - self.signOffSetx * 4) / 2)
        majorRadius = int((self.height - self.signOffSety * 2) / 2)
        self.ellipseDotsBlip = []
        #generating list of dots for drawing ellipse
        #formula is adjusted on half of width and height of cell
        # to place ellipse in the middle of cell
        self.ellipseDots = []
        self.ellipseDotsScattered = []
        self.ellipseDotsScatteredQuadrated = []
        index = 0
        while self.t < 2 * math.pi:
            tempx = int(self.x + minorRadius * math.cos(self.t) + int(self.width / 2))
            tempy = int(self.y + majorRadius * math.sin(self.t) + int(self.height / 2))
            self.ellipseDots.append([index, tuple((tempx, tempy))])
            self.ellipseDotsScattered.append([index, list([tempx, tempy]),
                                              list([random.randint(self.x, self.x + self.width),
                                                    random.randint(self.y, self.y + self.height)]), 0])
            self.generatedEllipseDotsSQ(index, tempx, tempy)
            self.t += 0.05
            index += 1

    #generating scattered dots in either of 4 areas depending on final location of dot in the circle
    def generatedEllipseDotsSQ(self, index, destinationx, destinationy):
        if destinationx <= self.centerx and destinationy <= self.centery:
            self.ellipseDotsScatteredQuadrated.append([index, list([destinationx, destinationy]),
                                              list([random.randint(self.x, destinationx),
                                                    random.randint(self.y, destinationy)])])
        elif destinationx >= self.centerx and destinationy >= self.centery:
            self.ellipseDotsScatteredQuadrated.append([index, list([destinationx, destinationy]),
                                                       list([random.randint(destinationx, self.x + self.width),
                                                             random.randint(destinationy, self.y + self.height)])])
        elif destinationx < self.centerx and destinationy > self.centery:
            self.ellipseDotsScatteredQuadrated.append([index, list([destinationx, destinationy]),
                                                       list([random.randint(self.x, destinationx),
                                                             random.randint(destinationy, self.y + self.height)])])
        elif destinationx > self.centerx and destinationy < self.centery:
            self.ellipseDotsScatteredQuadrated.append([index, list([destinationx, destinationy]),
                                                       list([random.randint(destinationx, self.x + self.width),
                                                             random.randint(self.y, destinationy)])])

    def relocate_dots_center_cell(self, ellipseDotsScattered):
        for index in range(len(ellipseDotsScattered)):
            ellipseDotsScattered[index][2][0]  = self.centerx
            ellipseDotsScattered[index][2][1] = self.centery

    ################################################################
    #states b-blank; d-drawing animation; x - it's X; o - it's O
    def draw_click_area(self):
        if (self.state == 'b'):
            self.draw_click_area_blank()
        elif self.state == 'd':
            if self.g_stats.gamer_turn == 'x':
                self.chosenXFunc()
            elif self.g_stats.gamer_turn == 'o':
                self.chosenOFunc()
        elif self.state == 'x':
            #old code. none animation drawing of x
            self.draw_click_area_x()
        elif self.state == 'o':
            #old code. none animation drawing of o
            self.draw_click_area_o()

    def draw_click_area_blank(self):
        self.screen.fill(self.backgroundcolor, self.rect)

    def draw_click_area_x(self):
        self.draw_click_area_blank()
        pygame.draw.line(self.screen, self.linecolor, (self.x1_1, self.y1_1), (self.x1_2, self.y1_2))
        pygame.draw.line(self.screen, self.linecolor, (self.x2_1, self.y2_1), (self.x2_2, self.y2_2))

    def draw_click_area_o(self):
        self.draw_click_area_blank()
        self.screen.fill(self.backgroundcolor, self.rect)
        pygame.draw.ellipse(self.screen, self.linecolor,
                            (self.x + (self.signOffSetx * 2), self.y + self.signOffSety,
                             self.width - (self.signOffSetx * 4), self.height - (self.signOffSety * 2)), 1)

    def randomChooseOFunc(self):
        self.chosenOFunc = self.oFunc[random.randint(0, len(self.oFunc) - 1)]
        # self.chosenOFunc = self.oFunc[10]
        if self.chosenOFunc.__name__ == 'drawing_click_area_o3':
            random.shuffle(self.ellipseDots)
        elif self.chosenOFunc.__name__ == 'drawing_click_area_o11':
            self.relocate_dots_center_cell(self.ellipseDotsScattered)

    def randomChooseXFunc(self):
        self.chosenXFunc = self.xFunc[random.randint(0, len(self.xFunc) - 1)]
        # self.chosenXFunc = self.xFunc[6]
        if self.chosenXFunc.__name__ == 'drawing_click_area_x7':
            self.generateInitialXCoor_x7()

    #Function for drawing X
    def calculatey(self, x, slope, b):
        return int((x * slope) + b)

    def calculatex(self, y, slope, b):
        return int((y - b) / slope)

    def drawing_click_area_x(self):
        if self.x1_1 + self.growingx <= self.x1_2:
            pygame.draw.line(self.screen, self.linecolor, (self.x1_1, self.y1_1),
                             (self.x1_1 + self.growingx,
                              self.calculatey(self.x1_1 + self.growingx, self.slope1, self.b1)))
            pygame.draw.line(self.screen, self.linecolor, (self.x2_1, self.y2_1),
                             (self.x2_1 - self.growingx,
                              self.calculatey(self.x2_1 - self.growingx, self.slope2, self.b2)))
            self.growingx += 1
        else:
            self.state = 'x'
            self.g_stats.drawing_click_area = False

    def drawing_click_area_x2(self):
        if self.x1_1 + self.growingx <= self.x_half:
            pygame.draw.line(self.screen, self.linecolor, (self.x1_1, self.y1_1),
                             (self.x1_1 + self.growingx,
                              self.calculatey(self.x1_1 + self.growingx, self.slope1, self.b1)))
            pygame.draw.line(self.screen, self.linecolor, (self.x1_2, self.y1_2),
                             (self.x1_2 - self.growingx,
                              self.calculatey(self.x1_2 - self.growingx, self.slope1, self.b1)))
            pygame.draw.line(self.screen, self.linecolor, (self.x2_1, self.y2_1),
                             (self.x2_1 - self.growingx,
                              self.calculatey(self.x2_1 - self.growingx, self.slope2, self.b2)))
            pygame.draw.line(self.screen, self.linecolor, (self.x2_2, self.y2_2),
                             (self.x2_2 + self.growingx,
                              self.calculatey(self.x2_2 + self.growingx, self.slope2, self.b2)))
            self.growingx += 1
        else:
            self.state = 'x'
            self.g_stats.drawing_click_area = False

    def drawing_click_area_x3(self):
        if self.x1_1 <= self.x_half - self.growingx:
            pygame.draw.line(self.screen, self.linecolor, (self.x_half, self.y_half),
                             (self.x_half - self.growingx,
                              self.calculatey(self.x_half - self.growingx, self.slope1, self.b1)))
            pygame.draw.line(self.screen, self.linecolor, (self.x_half, self.y_half),
                             (self.x_half - self.growingx,
                              self.calculatey(self.x_half - self.growingx, self.slope2, self.b2)))
            pygame.draw.line(self.screen, self.linecolor, (self.x_half, self.y_half),
                             (self.x_half + self.growingx,
                              self.calculatey(self.x_half + self.growingx, self.slope1, self.b1)))
            pygame.draw.line(self.screen, self.linecolor, (self.x_half, self.y_half),
                             (self.x_half + self.growingx,
                              self.calculatey(self.x_half + self.growingx, self.slope2, self.b2)))
            self.growingx += 1
        else:
            self.state = 'x'
            self.g_stats.drawing_click_area = False

    def drawing_click_area_x4(self):
        self.draw_click_area_blank()
        if self.x + self.growingx <= self.x + self.width:
            pygame.draw.line(self.screen, self.linecolor, (self.x + self.growingx, self.y),
                             (self.x + self.growingx, self.y + self.height))
            if self.x + self.growingx >= self.x1_1:
                animatedx = self.x + self.growingx
                if self.x + self.growingx > self.x1_2:
                    animatedx = self.x1_2
                pygame.draw.line(self.screen, self.linecolor,
                                 (self.x1_1, self.y1_1),
                                 (animatedx,
                                  self.calculatey(animatedx, self.slope1, self.b1)))
                pygame.draw.line(self.screen, self.linecolor,
                                 (self.x2_2, self.y2_2),
                                 (animatedx,
                                  self.calculatey(animatedx, self.slope2, self.b2)))
            self.growingx += 1
        else:
            pygame.draw.line(self.screen, self.linecolor,
                             (self.x1_1, self.y1_1),
                             (self.x1_2, self.y1_2))
            pygame.draw.line(self.screen, self.linecolor,
                             (self.x2_2, self.y2_2),
                             (self.x2_1, self.y2_1))
            self.state = 'x'
            self.g_stats.drawing_click_area = False

    def drawing_click_area_x5(self):
        self.draw_click_area_blank()
        if self.y + self.growingy <= self.y + self.height:
            pygame.draw.line(self.screen, self.linecolor, (self.x, self.y + self.growingy),
                             (self.x + self.width, self.y + self.growingy))
            if self.y + self.growingy >= self.y1_1:
                animatedy = self.y + self.growingy
                if self.y + self.growingy >= self.y1_2:
                    animatedy = self.y1_2
                pygame.draw.line(self.screen, self.linecolor, (self.x1_1, self.y1_1),
                                 (self.calculatex(animatedy, self.slope1, self.b1),
                                  animatedy))
                pygame.draw.line(self.screen, self.linecolor, (self.x2_1, self.y2_1),
                                 (self.calculatex(animatedy, self.slope2, self.b2),
                                  animatedy))
            self.growingy += 1
        else:
            pygame.draw.line(self.screen, self.linecolor,
                             (self.x1_1, self.y1_1),
                             (self.x1_2, self.y1_2))
            pygame.draw.line(self.screen, self.linecolor,
                             (self.x2_1, self.y2_1),
                             (self.x2_2, self.y2_2))
            self.state = 'x'
            self.g_stats.drawing_click_area = False

    def drawing_click_area_x6(self):
        if not self.stage1_x_done:
            #initial generateAdjustedXCoor call happens in ckeckClickedArea in my_game.py
            #It's done there to adjust properly based on mouse clicked coordinates
            if self.x1_1_adj <= self.mouseClickLocationx - self.growingx:
                self.drawing_adjusted_x()
                self.growingx += 1
            else:
                self.stage1_x_done = True
        elif self.stage1_x_done and not self.stage2_x_done:
            if self.mouseClickLocationx != self.centerx or self.mouseClickLocationy != self.centery:
                self.draw_click_area_blank()
                self.approachXToCenter()
                self.generateAdjustedXCoor()
                self.drawing_adjusted_x()
            else:
                self.stage2_x_done = True
        elif self.stage1_x_done and self.stage2_x_done:
            self.state = 'x'
            self.g_stats.drawing_click_area = False

    def drawing_adjusted_x(self):
        pygame.draw.line(self.screen, self.linecolor, (self.mouseClickLocationx, self.mouseClickLocationy),
                         (self.mouseClickLocationx - self.growingx,
                          self.calculatey(self.mouseClickLocationx - self.growingx, self.slope1, self.b1_adj)))
        pygame.draw.line(self.screen, self.linecolor, (self.mouseClickLocationx, self.mouseClickLocationy),
                         (self.mouseClickLocationx - self.growingx,
                          self.calculatey(self.mouseClickLocationx - self.growingx, self.slope2, self.b2_adj)))
        pygame.draw.line(self.screen, self.linecolor, (self.mouseClickLocationx, self.mouseClickLocationy),
                         (self.mouseClickLocationx + self.growingx,
                          self.calculatey(self.mouseClickLocationx + self.growingx, self.slope1, self.b1_adj)))
        pygame.draw.line(self.screen, self.linecolor, (self.mouseClickLocationx, self.mouseClickLocationy),
                         (self.mouseClickLocationx + self.growingx,
                          self.calculatey(self.mouseClickLocationx + self.growingx, self.slope2, self.b2_adj)))

    def generateAdjustedXCoor(self):
        self.correctionx = self.mouseClickLocationx - self.centerx
        self.correctiony = self.mouseClickLocationy - self.centery
        self.x1_1_adj = self.x1_1 + self.correctionx
        self.x1_2_adj = self.x1_2 + self.correctionx
        self.y1_2_adj = self.y1_2 + self.correctiony
        self.x2_1_adj = self.x2_1 + self.correctionx
        self.x2_2_adj = self.x2_2 + self.correctionx
        self.y2_2_adj = self.y2_2 + self.correctiony

        self.b1_adj = self.y1_2_adj - self.slope1 * self.x1_2_adj
        self.b2_adj = self.y2_2_adj - self.slope2 * self.x2_2_adj

    def approachXToCenter(self):
        #increment x param if needed
        if self.mouseClickLocationx > self.centerx:
            self.mouseClickLocationx -= 1
        elif self.mouseClickLocationx < self.centerx:
            self.mouseClickLocationx += 1
        else:
            pass
        #increment y param if needed
        if self.mouseClickLocationy > self.centery:
            self.mouseClickLocationy -= 1
        elif self.mouseClickLocationy < self.centery:
            self.mouseClickLocationy += 1
        else:
            pass


    def drawing_click_area_x7(self):
        if not self.stage1_x_done:
            if abs(self.centerx1_adj - self.centerx) > (self.slope1CorrectionParam * 100) \
                    or abs(self.centery1_adj - self.centery) > (self.slope1CorrectionParam * 100) \
                    or abs(self.centerx2_adj - self.centerx) > (self.slope2CorrectionParam * 100) \
                    or abs(self.centery2_adj - self.centery) > (self.slope2CorrectionParam * 100):
                self.draw_click_area_blank()
                self.approachX1ToCenter_x7()
                self.approachX2ToCenter_x7()
                self.generateAdjustedXCoor_x7()
                self.drawing_adjusted_x7()
            else:
                self.centerx1_adj = self.centerx2_adj = self.centerx
                self.centery1_adj = self.centery2_adj = self.centery
                self.stage1_x_done = True

        elif self.stage1_x_done and not self.stage2_x_done:
            if round(self.slope1_adj, 1) != round(self.slope1, 1) or round(self.slope2_adj, 1) != round(self.slope2, 1):
                self.draw_click_area_blank()
                self.generateAdjustedXCoor_x7()
                self.drawing_adjusted_x7()
                pass
            else:
                self.stage2_x_done = True
        elif self.stage1_x_done and self.stage2_x_done:
            self.state = 'x'
            self.g_stats.drawing_click_area = False

    def approachX1ToCenter_x7(self):
        #increment x param if needed
        if self.centerx1_adj > self.centerx \
                and abs(self.centerx1_adj - self.centerx) > int(self.slope1CorrectionParam * 100):
            self.centerx1_adj -= int(self.slope1CorrectionParam * 100)
        elif self.centerx1_adj < self.centerx \
                and abs(self.centerx1_adj - self.centerx) > int(self.slope1CorrectionParam * 100):
            self.centerx1_adj += int(self.slope1CorrectionParam * 100)
        else:
            pass
        #increment y param if needed
        if self.centery1_adj > self.centery \
                and abs(self.centery1_adj - self.centery) > int(self.slope1CorrectionParam * 100):
            self.centery1_adj -= int(self.slope1CorrectionParam * 100)
        elif self.centery1_adj < self.centery \
                and abs(self.centery1_adj - self.centery) > int(self.slope1CorrectionParam * 100):
            self.centery1_adj += int(self.slope1CorrectionParam * 100)
        else:
            pass

    def approachX2ToCenter_x7(self):
        #increment x param if needed
        if self.centerx2_adj > self.centerx \
                and abs(self.centerx2_adj - self.centerx) > int(self.slope2CorrectionParam * 100):
            self.centerx2_adj -= int(self.slope2CorrectionParam * 100)
        elif self.centerx2_adj < self.centerx \
                and abs(self.centerx2_adj - self.centerx) > int(self.slope2CorrectionParam * 100):
            self.centerx2_adj += int(self.slope2CorrectionParam * 100)
        else:
            pass
        #increment y param if needed
        if self.centery2_adj > self.centery \
                and abs(self.centery2_adj - self.centery) > int(self.slope2CorrectionParam):
            self.centery2_adj -= int(self.slope2CorrectionParam * 100)
        elif self.centery2_adj < self.centery \
                and abs(self.centery2_adj - self.centery)  > int(self.slope2CorrectionParam):
            self.centery2_adj += int(self.slope2CorrectionParam * 100)
        else:
            pass

    def generateAdjustedXCoor_x7(self):
        self.pivotX1_x7()
        self.pivotX2_x7()
        self.x1_1_adj = self.centerx1_adj + self.half_length_line * math.sqrt(1 / (1 + self.slope1_adj ** 2))
        self.x1_2_adj = self.centerx1_adj - self.half_length_line * math.sqrt(1 / (1 + self.slope1_adj ** 2))
        self.y1_1_adj = self.centery1_adj + self.slope1_adj * self.half_length_line * math.sqrt(1 / (1 + self.slope1_adj ** 2))
        self.y1_2_adj = self.centery1_adj - self.slope1_adj * self.half_length_line * math.sqrt(1 / (1 + self.slope1_adj ** 2))

        self.x2_1_adj = self.centerx2_adj + self.half_length_line * math.sqrt(1 / (1 + self.slope2_adj ** 2))
        self.x2_2_adj = self.centerx2_adj - self.half_length_line * math.sqrt(1 / (1 + self.slope2_adj ** 2))
        self.y2_1_adj = self.centery2_adj + self.slope2_adj * self.half_length_line * math.sqrt(1 / (1 + self.slope2_adj ** 2))
        self.y2_2_adj = self.centery2_adj - self.slope2_adj * self.half_length_line * math.sqrt(1 / (1 + self.slope2_adj ** 2))

    def pivotX1_x7(self):
        #stage 1 (approaching to center of cell) - constant pivoting
        #once stage 1 is done, stop pivoting at proper line slope
        if self.stage1_x_done:
            if abs(round(self.slope1_adj, 1))  < 2:
                omega = self.slope1CorrectionParam
            elif abs(round(self.slope1_adj, 1)) >=2 \
                and abs(round(self.slope1_adj, 1)) < 10:
                omega = self.slope1CorrectionParam * 10
            elif abs(round(self.slope1_adj, 1)) >= 10 \
                and abs(round(self.slope1_adj, 1)) < 50:
                omega = self.slope1CorrectionParam * 50
            elif abs(round(self.slope1_adj, 1)) >= 50 \
                    and abs(round(self.slope1_adj, 1)) < 150:
                omega = self.slope1CorrectionParam * 150
            elif abs(round(self.slope1_adj, 1)) >= 150:
                omega = self.slope1CorrectionParam * 1000

            if abs(round(self.slope1_adj, 1) - round(self.slope1, 1)) <= abs(omega):
                self.slope1_adj = self.slope1
            else:
                self.pivotnocheckX1_x7()
        else:
            self.pivotnocheckX1_x7()

    def pivotnocheckX1_x7(self):
        # print(f'slop1_adj  {self.slope1_adj}')
        if round(self.slope1_adj) >= self.length_of_line - 2.5:
            self.slope1_adj = (self.slope1_adj - 1) * (-1)
        elif round(self.slope1_adj) >= 0 and round(self.slope1_adj) < 2:
            self.slope1_adj += self.slope1CorrectionParam
        elif round(self.slope1_adj) >= 2 and round(self.slope1_adj) < 10:
            self.slope1_adj += self.slope1CorrectionParam * 10
        elif round(self.slope1_adj) >= 10 and round(self.slope1_adj) < 50:
            self.slope1_adj += self.slope1CorrectionParam * 50
        elif round(self.slope1_adj) >= 50 and round(self.slope1_adj) < 150:
            self.slope1_adj += self.slope1CorrectionParam * 150
        elif round(self.slope1_adj) >= 150:
            self.slope1_adj += self.slope1CorrectionParam * 1000

        elif round(self.slope1_adj) < 0 and round(self.slope1_adj) > -2:
            self.slope1_adj += self.slope1CorrectionParam
        elif round(self.slope1_adj) <= -2 and round(self.slope1_adj) > -10:
            self.slope1_adj += self.slope1CorrectionParam * 10
        elif round(self.slope1_adj) <= -10 and round(self.slope1_adj) > -50:
            self.slope1_adj += self.slope1CorrectionParam * 50
        elif round(self.slope1_adj) <= -50 and round(self.slope1_adj) > -150:
            self.slope1_adj += self.slope1CorrectionParam * 150
        elif round(self.slope1_adj) <= -150:
            self.slope1_adj += self.slope1CorrectionParam * 1000


    def pivotX2_x7(self):
        if self.stage1_x_done:
            if abs(round(self.slope2_adj, 1))  < 2:
                omega = self.slope2CorrectionParam
            elif abs(round(self.slope2_adj, 1)) >=2 \
                    and abs(round(self.slope2_adj, 1)) < 10:
                omega = self.slope2CorrectionParam * 10
            elif abs(round(self.slope2_adj, 1)) >= 10 \
                    and abs(round(self.slope2_adj, 1)) < 50:
                omega = self.slope2CorrectionParam * 50
            elif abs(round(self.slope2_adj, 1)) >= 50 \
                    and abs(round(self.slope2_adj, 1)) < 150:
                omega = self.slope2CorrectionParam * 150
            elif abs(round(self.slope2_adj, 1)) >= 150:
                omega = self.slope2CorrectionParam * 1000

            if abs(round(self.slope2_adj, 1) - round(self.slope2, 1)) <= abs(omega):
                self.slope2_adj = self.slope2
            else:
                self.pivotnocheckX2_x7()
        else:
            self.pivotnocheckX2_x7()

    def pivotnocheckX2_x7(self):

        if round(self.slope2_adj) <= -(self.length_of_line - 2.5):
            self.slope2_adj = (self.slope2_adj) * (-1)
        elif round(self.slope2_adj) >= 0 and round(self.slope2_adj) < 2:
            self.slope2_adj -= self.slope2CorrectionParam
        elif round(self.slope2_adj) >= 2 and round(self.slope2_adj) < 10:
            self.slope2_adj -= self.slope2CorrectionParam * 10
        elif round(self.slope2_adj) >= 10 and round(self.slope2_adj) < 50:
            self.slope2_adj -= self.slope2CorrectionParam * 50
        elif round(self.slope2_adj) >= 50 and round(self.slope2_adj) < 150:
            self.slope2_adj -= self.slope2CorrectionParam * 150
        elif round(self.slope2_adj) >= 150:
            self.slope2_adj -= self.slope2CorrectionParam * 1000

        elif round(self.slope2_adj) < 0 and round(self.slope2_adj) > -2:
            self.slope2_adj -= self.slope2CorrectionParam
        elif round(self.slope2_adj) <= -2 and round(self.slope2_adj) > -10:
            self.slope2_adj -= self.slope2CorrectionParam * 10
        elif round(self.slope2_adj) <= -10 and round(self.slope2_adj) > -50:
            self.slope2_adj -= self.slope2CorrectionParam * 50
        elif round(self.slope2_adj) <= -50 and round(self.slope2_adj) > -150:
            self.slope2_adj -= self.slope2CorrectionParam * 150
        elif round(self.slope2_adj) <= -150:
            self.slope2_adj -= self.slope2CorrectionParam * 1000

    def drawing_adjusted_x7(self):
        pygame.draw.line(self.screen, self.linecolor, (self.x1_1_adj, self.y1_1_adj), (self.x1_2_adj, self.y1_2_adj))
        pygame.draw.line(self.screen, self.linecolor, (self.x2_1_adj, self.y2_1_adj), (self.x2_2_adj, self.y2_2_adj))

    def generateInitialXCoor_x7(self):
        self.centerx1_adj = self.half_length_line
        self.centery1_adj = self.centery2_adj = self.g_set.game_screen_height
        self.centerx2_adj = self.g_set.game_screen_width - self.half_length_line
        self.slope1_adj = 0
        self.slope2_adj = 0
        slopeCorrectionParamOption = [0.01, 0.02, 0.03]
        self.slope1CorrectionParam = random.choice(slopeCorrectionParamOption)
        slopeCorrectionParamOption.remove(self.slope1CorrectionParam)
        self.slope2CorrectionParam = random.choice(slopeCorrectionParamOption)
        # self.slope1CorrectionParam = 0.01
        # self.slope2CorrectionParam = 0.01
        self.g_stats.drawing_stage1_x = True

    # Function for drawing O
    def drawing_click_area_o(self):
        if self.ellipseAnimationSlice < len(self.ellipseDots) - 1:
            pygame.draw.line(self.screen, self.linecolor, (self.ellipseDots[self.ellipseAnimationSlice][1]),
                             (self.ellipseDots[self.ellipseAnimationSlice + 1][1]))
            self.ellipseAnimationSlice += 1
        else:
            pygame.draw.line(self.screen, self.linecolor, (self.ellipseDots[0][1]), (self.ellipseDots[-1][1]), 1)
            self.state = 'o'
            self.g_stats.drawing_click_area = False

    def drawing_click_area_o2(self):
        if self.ellipseAnimationSlice < len(self.ellipseDots) - 1:
            pygame.draw.line(self.screen, self.linecolor, (self.ellipseDots[self.ellipseAnimationSlice][1]),
                             (self.ellipseDots[self.ellipseAnimationSlice][1]))
            self.ellipseAnimationSlice += 1
        else:
            for item in range(len(self.ellipseDots) - 1):
                pygame.draw.line(self.screen, self.linecolor, (self.ellipseDots[item][1]),
                                 (self.ellipseDots[item + 1][1]))
            pygame.draw.line(self.screen, self.linecolor, (self.ellipseDots[0][1]),
                             (self.ellipseDots[-1][1]))
            self.state = 'o'
            self.g_stats.drawing_click_area = False

    def drawing_click_area_o3(self):
        if self.ellipseAnimationSlice < len(self.ellipseDots) - 1:
            pygame.draw.line(self.screen, self.linecolor, (self.ellipseDots[self.ellipseAnimationSlice][1]),
                             (self.ellipseDots[self.ellipseAnimationSlice][1]))
            self.ellipseAnimationSlice += 1
        else:
            self.ellipseDots.sort(key=lambda x: x[0])
            for item in range(len(self.ellipseDots) - 1):
                pygame.draw.line(self.screen, self.linecolor, (self.ellipseDots[item][1]),
                                 (self.ellipseDots[item + 1][1]))
            pygame.draw.line(self.screen, self.linecolor, (self.ellipseDots[0][1]),
                             (self.ellipseDots[-1][1]))
            self.state = 'o'
            self.g_stats.drawing_click_area = False

    def drawing_click_area_o4(self):
        self.draw_click_area_blank()

        if self.x + self.growingx <= self.x + self.width:
            pygame.draw.line(self.screen, self.linecolor, (self.x + self.growingx, self.y),
                             (self.x + self.growingx, self.y + self.height))
            #adding ellipses dots that have same x param
            for dot in self.ellipseDots:
                if dot[1][0] == self.x + self.growingx:
                    bisect.insort(self.ellipseDotsBlip, dot)
                else:
                    if len(self.ellipseDotsBlip) > 1:
                        pygame.draw.line(self.screen, self.linecolor, (self.ellipseDotsBlip[0][1]),
                                         (self.ellipseDotsBlip[-1][1]))
            #drawing ellipses dots that were bypassed by scanning line

            for index in range(len(self.ellipseDotsBlip) - 1):
                pygame.draw.line(self.screen, self.linecolor, (self.ellipseDotsBlip[index][1]),
                                 (self.ellipseDotsBlip[index + 1][1]))

            self.growingx += 1
        else:
            for index in range(len(self.ellipseDotsBlip) - 1):
                pygame.draw.line(self.screen, self.linecolor, (self.ellipseDotsBlip[index][1]),
                                 (self.ellipseDotsBlip[index + 1][1]))
            pygame.draw.line(self.screen, self.linecolor, (self.ellipseDotsBlip[0][1]),
                             (self.ellipseDotsBlip[-1][1]))
            self.state = 'o'
            self.g_stats.drawing_click_area = False

    def drawing_click_area_o5(self):
        self.draw_click_area_blank()

        if self.y + self.growingy <= self.y + self.height:
            pygame.draw.line(self.screen, self.linecolor, (self.x, self.y + self.growingy),
                             (self.x + self.width, self.y + self.growingy))
            #adding ellipses dots that have same y param
            for dot in self.ellipseDots:
                if dot[1][1] == self.y + self.growingy:
                    bisect.insort(self.ellipseDotsBlip, dot)
                else:
                    if len(self.ellipseDotsBlip) > 1:
                        pygame.draw.line(self.screen, self.linecolor, (self.ellipseDotsBlip[0][1]),
                                         (self.ellipseDotsBlip[-1][1]))
            #drawing ellipses dots that were bypassed by scanning line

            for index in range(len(self.ellipseDotsBlip) - 1):
                pygame.draw.line(self.screen, self.linecolor, (self.ellipseDotsBlip[index][1]),
                                 (self.ellipseDotsBlip[index + 1][1]))

            self.growingy += 1
        else:
            for index in range(len(self.ellipseDotsBlip) - 1):
                pygame.draw.line(self.screen, self.linecolor, (self.ellipseDotsBlip[index][1]),
                                 (self.ellipseDotsBlip[index + 1][1]))
            pygame.draw.line(self.screen, self.linecolor, (self.ellipseDotsBlip[0][1]),
                             (self.ellipseDotsBlip[-1][1]))
            self.state = 'o'
            self.g_stats.drawing_click_area = False


    def drawing_click_area_o6(self):
        self.draw_click_area_blank()

        scattered_dots_arranged = True
        for index in range(len(self.ellipseDotsScattered) ):
            if ((self.ellipseDotsScattered[index][1][0] != self.ellipseDotsScattered[index][2][0]) or
                    (self.ellipseDotsScattered[index][1][1] != self.ellipseDotsScattered[index][2][1])):
                self.approachToLocation(index, self.ellipseDotsScattered)
                scattered_dots_arranged = False

        if not scattered_dots_arranged:
            for index in range(len(self.ellipseDotsScattered) ):
                pygame.draw.line(self.screen, self.linecolor,
                                 (self.ellipseDotsScattered[index][2]), (self.ellipseDotsScattered[index][2]))
        else:
            for index in range(len(self.ellipseDotsScattered) -1 ):
                pygame.draw.line(self.screen, self.linecolor,
                                 (self.ellipseDotsScattered[index][2]), (self.ellipseDotsScattered[index + 1][2]))
            pygame.draw.line(self.screen, self.linecolor,
                             self.ellipseDotsScattered[0][2], self.ellipseDotsScattered[-1][2])
            self.state = 'o'
            self.g_stats.drawing_click_area = False


    def drawing_click_area_o7(self):
        self.draw_click_area_blank()
        scattered_dots_arranged = True
        for index in range(len(self.ellipseDotsScatteredQuadrated) ):
            if ((self.ellipseDotsScatteredQuadrated[index][1][0] != self.ellipseDotsScatteredQuadrated[index][2][0]) or
                    (self.ellipseDotsScatteredQuadrated[index][1][1] != self.ellipseDotsScatteredQuadrated[index][2][1])):
                self.approachToLocation(index, self.ellipseDotsScatteredQuadrated)
                scattered_dots_arranged = False

        if not scattered_dots_arranged:
            for index in range(len(self.ellipseDotsScatteredQuadrated) ):
                pygame.draw.line(self.screen, self.linecolor,
                                 (self.ellipseDotsScatteredQuadrated[index][2]),
                                 (self.ellipseDotsScatteredQuadrated[index][2]))
        else:
            for index in range(len(self.ellipseDotsScatteredQuadrated) -1 ):
                pygame.draw.line(self.screen, self.linecolor,
                                 (self.ellipseDotsScatteredQuadrated[index][2]),
                                 (self.ellipseDotsScatteredQuadrated[index + 1][2]))
            pygame.draw.line(self.screen, self.linecolor,
                             self.ellipseDotsScatteredQuadrated[0][2],
                             self.ellipseDotsScatteredQuadrated[-1][2])
            self.state = 'o'
            self.g_stats.drawing_click_area = False


    def drawing_click_area_o8(self):
        scattered_dots_arranged = True
        for index in range(len(self.ellipseDotsScattered) ):
            if ((self.ellipseDotsScattered[index][1][0] != self.ellipseDotsScattered[index][2][0]) or
                    (self.ellipseDotsScattered[index][1][1] != self.ellipseDotsScattered[index][2][1])):
                self.approachToLocation(index, self.ellipseDotsScattered)
                scattered_dots_arranged = False

        if not scattered_dots_arranged:
            for index in range(len(self.ellipseDotsScattered) ):
                pygame.draw.line(self.screen, self.linecolor,
                                 (self.ellipseDotsScattered[index][2]), (self.ellipseDotsScattered[index][2]))
        else:
            self.draw_click_area_blank()
            for index in range(len(self.ellipseDotsScattered) -1 ):
                pygame.draw.line(self.screen, self.linecolor,
                                 (self.ellipseDotsScattered[index][2]), (self.ellipseDotsScattered[index + 1][2]))
            pygame.draw.line(self.screen, self.linecolor,
                             self.ellipseDotsScattered[0][2], self.ellipseDotsScattered[-1][2])
            self.state = 'o'
            self.g_stats.drawing_click_area = False


    def drawing_click_area_o9(self):
        scattered_dots_arranged = True
        for index in range(len(self.ellipseDotsScatteredQuadrated) ):
            if ((self.ellipseDotsScatteredQuadrated[index][1][0] != self.ellipseDotsScatteredQuadrated[index][2][0]) or
                    (self.ellipseDotsScatteredQuadrated[index][1][1] != self.ellipseDotsScatteredQuadrated[index][2][1])):
                self.approachToLocation(index, self.ellipseDotsScatteredQuadrated)
                scattered_dots_arranged = False

        if not scattered_dots_arranged:
            for index in range(len(self.ellipseDotsScatteredQuadrated) ):
                pygame.draw.line(self.screen, self.linecolor,
                                 (self.ellipseDotsScatteredQuadrated[index][2]),
                                 (self.ellipseDotsScatteredQuadrated[index][2]))
        else:
            self.draw_click_area_blank()
            for index in range(len(self.ellipseDotsScatteredQuadrated) -1 ):
                pygame.draw.line(self.screen, self.linecolor,
                                 (self.ellipseDotsScatteredQuadrated[index][2]),
                                 (self.ellipseDotsScatteredQuadrated[index + 1][2]))
            pygame.draw.line(self.screen, self.linecolor,
                             self.ellipseDotsScatteredQuadrated[0][2],
                             self.ellipseDotsScatteredQuadrated[-1][2])
            self.state = 'o'
            self.g_stats.drawing_click_area = False

    def drawing_click_area_o10(self):
        # self.draw_click_area_blank()

        scattered_dots_arranged = True
        for index in range(len(self.ellipseDotsScattered) ):
            if self.ellipseDotsScattered[index][3] == 0:
                self.generateOrbitTrajectory(index, self.ellipseDotsScattered)
                scattered_dots_arranged = False
            elif self.ellipseDotsScattered[index][3] == 1:
                self.continueOrbitTrajectory(index, self.ellipseDotsScattered)
                scattered_dots_arranged = False
            elif self.ellipseDotsScattered[index][3] == 2:
                if ((self.ellipseDotsScattered[index][1][0] != self.ellipseDotsScattered[index][2][0]) or
                        (self.ellipseDotsScattered[index][1][1] != self.ellipseDotsScattered[index][2][1])):
                    self.approachToLocation(index, self.ellipseDotsScattered)
                    scattered_dots_arranged = False

        if not scattered_dots_arranged:
            for index in range(len(self.ellipseDotsScattered) ):
                pygame.draw.line(self.screen, self.linecolor,
                                 (self.ellipseDotsScattered[index][2]), (self.ellipseDotsScattered[index][2]))
        else:
            for index in range(len(self.ellipseDotsScattered) -1 ):
                pygame.draw.line(self.screen, self.linecolor,
                                 (self.ellipseDotsScattered[index][2]), (self.ellipseDotsScattered[index + 1][2]))
            pygame.draw.line(self.screen, self.linecolor,
                             self.ellipseDotsScattered[0][2], self.ellipseDotsScattered[-1][2])
            self.state = 'o'
            self.g_stats.drawing_click_area = False

    def drawing_click_area_o11(self):
        self.drawing_click_area_o6()

    # ellipseDotsScattered
    # 0 - index in the final sequence
    # 1 - final location coord
    # 2 - current location coord
    # 3 - state of animation (for function 10, there are 3 stages)
    # 4 theta parameter (angular parameter 0 * 2PI or 360degree)
    # 5 radius of orbital animation. Distance from random placement and center of the cell
    # 6 speed of orbital animation.
    # 7 counter of dots for orbital trajectory

    def generateOrbitTrajectory(self, index, ellipseDotsScattered):
        theta = math.atan2(self.centery - self.ellipseDotsScattered[index][2][1],
                           self.centerx - self.ellipseDotsScattered[index][2][0])
        orbital_radius = math.sqrt(((self.centerx - ellipseDotsScattered[index][2][0]) ** 2) +
                                   ((self.centery - ellipseDotsScattered[index][2][1]) ** 2))
        #start and finish theta
        ellipseDotsScattered[index].append(round(theta, 1))
        ellipseDotsScattered[index].append(round(orbital_radius))
        orbitTrajectorySpeedOptions = {0.01: 628, 0.02: 314, 0.03: 209, 0.04: 157, 0.05: 125, 0.1: 62}
        orbitTrajectorySpeed = random.choice(list(orbitTrajectorySpeedOptions.keys()))
        ellipseDotsScattered[index].append(orbitTrajectorySpeed)

        #theta counter -  - full circle
        ellipseDotsScattered[index].append(orbitTrajectorySpeedOptions[orbitTrajectorySpeed])
        ellipseDotsScattered[index][3] = 1

    def continueOrbitTrajectory(self, index, ellipseDotsScattered):
        if ellipseDotsScattered[index][7] > 0:
            #trajactory angle + trajectory speed
            if ellipseDotsScattered[index][4] + ellipseDotsScattered[index][6] >= 3.14:
                ellipseDotsScattered[index][4]  = -3.14
                ellipseDotsScattered[index][7] -= 1
            else:
                ellipseDotsScattered[index][4] += ellipseDotsScattered[index][6]
                ellipseDotsScattered[index][7] -= 1

            tempx = int(self.x + ellipseDotsScattered[index][5] *
                        math.cos(ellipseDotsScattered[index][4]) + int(self.width / 2))
            tempy = int(self.y + ellipseDotsScattered[index][5] *
                        math.sin(ellipseDotsScattered[index][4]) + int(self.height / 2))
            ellipseDotsScattered[index][2][0] = tempx
            ellipseDotsScattered[index][2][1] = tempy

        else:
            ellipseDotsScattered[index][3] = 2

    def approachToLocation(self, index, ellipseDotsScattered):
        #increment x param if needed
        if ellipseDotsScattered[index][2][0] > ellipseDotsScattered[index][1][0]:
            ellipseDotsScattered[index][2][0] -= 1
        elif ellipseDotsScattered[index][2][0] < ellipseDotsScattered[index][1][0]:
            ellipseDotsScattered[index][2][0] += 1
        else:
            pass
        #increment y param if needed
        if ellipseDotsScattered[index][2][1] > ellipseDotsScattered[index][1][1]:
            ellipseDotsScattered[index][2][1] -= 1
        elif ellipseDotsScattered[index][2][1] < ellipseDotsScattered[index][1][1]:
            ellipseDotsScattered[index][2][1] += 1
        else:
            pass











