import bisect
import random
import pygame
import math

class ClickArea:

    def __init__(self, position, screen, g_set, g_stats):
        self.x, self.y = position
        self.screen = screen
        self.g_stats = g_stats
        self.screen_rect = screen.get_rect()
        self.width = g_set.click_area_width
        self.height = g_set.click_area_height
        self.centerx = position[0] + int(g_set.click_area_width / 2)
        self.centery = position[1] + int(g_set.click_area_height /  2)

        # sign "x" is not drawn from the edges of area(square). Space offset is set here
        self.signOffSetx = int(self.width * 0.1)
        self.signOffSety = int(self.height * 0.1)
        self.backgroundcolor = (255, 255, 255)
        self.linecolor = (0, 0, 255)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        #list of functions of drawing sign "O"  to random pick from.
        self.oFunc = [self.drawing_click_area_o, self.drawing_click_area_o2, self.drawing_click_area_o3,
                      self.drawing_click_area_o4, self.drawing_click_area_o5, self.drawing_click_area_o6,
                      self.drawing_click_area_o7, self.drawing_click_area_o8, self.drawing_click_area_o9]

        #list of functions of drawing sign "X"  to random pick from.
        self.xFunc = [self.drawing_click_area_x, self.drawing_click_area_x2, self.drawing_click_area_x3,
                      self.drawing_click_area_x4, self.drawing_click_area_x5]

        self.clickAreaReset()

    def clickAreaReset(self):
        self.state = 'b'
        self.calculateCrossCoord()
        self.calculateEllipseCoord()
        self.randomChooseXFunc()
        self.randomChooseOFunc()

    def calculateCrossCoord(self):
        #line 1 . It's 2 points - top left and bottom right
        self.currentx1 = self.x1_1 = self.x + self.signOffSetx
        self.y1_1 = self.y + self.signOffSety
        self.x1_2 = self.x + self.width - self.signOffSetx
        self.y1_2 = self.y + self.height - self.signOffSety
        # line 2. 2 points - top right and bottom left
        self.currentx2 = self.x2_1 = self.x + self.width - self.signOffSetx
        self.y2_1 = self.y + self.signOffSety
        self.x2_2 = self.x + self.signOffSetx
        self.y2_2 = self.y + self.height - self.signOffSety
        # cross point
        self.x_half = self.x + int(self.width /2 )
        self.y_half = self.y + int(self.height /2 )
        self.growingx = 0
        self.growingy = 0
        # slope and b info needed for line formula
        self.slope1 =  (self.y1_2 - self.y1_1) / (self.x1_2 - self.x1_1)
        self.b1 = self.y1_2 - self.slope1 * self.x1_2
        self.slope2 =  (self.y2_2 - self.y2_1) / (self.x2_2 - self.x2_1)
        self.b2 = self.y2_2 - self.slope2 * self.x2_2

    #For drawing "O" different approach was chosen. All coord. of ellipse put in list
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
                                                    random.randint(self.y, self.y + self.height)])])
            self.generatedEllipseDotsSQ(index, tempx, tempy)
            self.t += 0.05
            index += 1

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

    ################################################################
    #states b-blank; d-drawing animation; x - it's X; o - it's O
    def draw_click_area(self):
        if self.state == 'b':
            self.draw_click_area_blank()
        elif self.state == 'd':
            if self.g_stats.gamer_turn == 'x':
                self.chosenXFunc()
            elif self.g_stats.gamer_turn == 'o':
                print(self.chosenOFunc.__name__)
                self.chosenOFunc()
        elif self.state == 'x':
            pass
            #old code. none animation drawing of x
            #self.draw_click_area_x()
        elif self.state == 'o':
            pass
            #old code. none animation drawing of o
            #self.draw_click_area_o()

    def draw_click_area_blank(self):
        self.screen.fill(self.backgroundcolor, self.rect)

    def draw_click_area_x(self):
        pygame.draw.line(self.screen, self.linecolor, (self.x1_1, self.y1_1), (self.x1_2, self.y1_2))
        pygame.draw.line(self.screen, self.linecolor, (self.x2_1, self.y2_1), (self.x2_2, self.y2_2))

    def draw_click_area_o(self):
        self.screen.fill(self.backgroundcolor, self.rect)
        pygame.draw.ellipse(self.screen, self.linecolor,
                            (self.x + (self.signOffSetx * 2), self.y + self.signOffSety,
                             self.width - (self.signOffSetx * 4), self.height - (self.signOffSety * 2)), 1)

    def calculatey(self, x, slope, b):
        return int((x * slope) + b)

    def calculatex(self, y, slope, b):
        return int((y - b) / slope)

    def randomChooseOFunc(self):
        # self.chosenOFunc = self.oFunc[random.randint(0, len(self.oFunc) - 1)]
        self.chosenOFunc = self.oFunc[5]
        if self.chosenOFunc.__name__ == 'drawing_click_area_o':
            pass
        elif self.chosenOFunc.__name__ == 'drawing_click_area_o2':
            pass
        elif self.chosenOFunc.__name__ == 'drawing_click_area_o3':
            random.shuffle(self.ellipseDots)

    def randomChooseXFunc(self):
        self.chosenXFunc = self.xFunc[random.randint(0, len(self.xFunc) - 1)]
        # self.chosenXFunc = self.xFunc[4]

    #Function for drawing X
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
        print(self.growingx)
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







