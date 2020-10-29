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
        # sign "x" is not drawn from the edges of area(square). Buffer offset is set here
        self.signOffSetx = int(self.width * 0.1)
        self.signOffSety = int(self.height * 0.1)
        self.backgroundcolor = (255, 255, 255)
        self.linecolor = (0, 0, 255)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.state = 'b'

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
                self.ellipseDots.sort(key=lambda x: x[0])
                for item in range(len(self.ellipseDots) - 1):
                    pygame.draw.line(self.screen, self.linecolor, (self.ellipseDots[item][1]),
                                     (self.ellipseDots[item + 1][1]))
                self.state = 'o'
                self.g_stats.drawing_click_area = False

        #list of functions of drawing sign "O"  to random pick from.
        self.oFunc = [drawing_click_area_o, drawing_click_area_o2]
        self.calculateCrossCoord()
        self.ellipseAnimationSlice = 0
        self.calculateEllipseCoord()
        self.randomChooseOFunc()

    def clickAreaReset(self):
        self.state = 'b'
        self.currentx1 = self.x1_1
        self.currentx2 = self.x2_1
        self.ellipseAnimationSlice = 0

    def calculateCrossCoord(self):
        self.currentx1 = self.x1_1 = self.x + self.signOffSetx
        self.y1_1 = self.y + self.signOffSety
        self.x1_2 = self.x + self.width - self.signOffSetx
        self.y1_2 = self.y + self.height - self.signOffSety
        self.currentx2 = self.x2_1 = self.x + self.width - self.signOffSetx
        self.y2_1 = self.y + self.signOffSety
        self.x2_2 = self.x + self.signOffSetx
        self.y2_2 = self.y + self.height - self.signOffSety
        self.slope1 =  (self.y1_2 - self.y1_1) / (self.x1_2 - self.x1_1)
        self.b1 = self.y1_2 - self.slope1 * self.x1_2
        self.slope2 =  (self.y2_2 - self.y2_1) / (self.x2_2 - self.x2_1)
        self.b2 = self.y2_2 - self.slope2 * self.x2_2

    #For drawing "O" different approach was chosen. All coord. of ellipse put in list
    def calculateEllipseCoord(self):
        self.t = 0.0
        minorRadius = int((self.width - self.signOffSetx * 4) / 2)
        majorRadius = int((self.height - self.signOffSety * 2) / 2)

        self.ellipseDots = []
        index = 0
        while self.t < 2 * math.pi:
            tempx = int(self.x + minorRadius * math.cos(self.t) + int(self.width / 2))
            tempy = int(self.y + majorRadius * math.sin(self.t) + int(self.height / 2))
            self.ellipseDots.append([index, tuple((tempx, tempy))])
            self.t += 0.05
            index += 1

        print(self.ellipseDots)

    #states b-blank; d-drawing animation; x - it's X; o - it's O
    def draw_click_area(self):
        if self.state == 'b':
            self.draw_click_area_blank()
        elif self.state == 'd':
            if self.g_stats.gamer_turn == 'x':
                self.drawing_click_area_x()
            elif self.g_stats.gamer_turn == 'o':
                self.chosenOFunc(self)
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

    def drawing_click_area_x(self):
        if self.currentx1 <= self.x1_2:
            pygame.draw.line(self.screen, self.linecolor, (self.x1_1, self.y1_1),
                             (self.currentx1, self.calculatey(self.currentx1, self.slope1, self.b1)))
            pygame.draw.line(self.screen, self.linecolor, (self.x2_1, self.y2_1),
                             (self.currentx2, self.calculatey(self.currentx2, self.slope2, self.b2)))
            self.currentx1 += 1
            self.currentx2 -= 1
        else:
            self.state = 'x'
            self.g_stats.drawing_click_area = False

    def calculatey(self, x, slope, b):
        return int((x * slope) + b)

    def draw_click_area_o(self):
        self.screen.fill(self.backgroundcolor, self.rect)
        pygame.draw.ellipse(self.screen, self.linecolor,
                            (self.x + (self.signOffSetx * 2), self.y + self.signOffSety,
                             self.width - (self.signOffSetx * 4), self.height - (self.signOffSety * 2)), 1)

    def randomChooseOFunc(self):
        self.chosenOFunc = self.oFunc[random.randint(0, len(self.oFunc) - 1)]
        if self.chosenOFunc == 'drawing_click_area_o':
            pass
        elif self.chosenOFunc == 'drawing_click_area_o2':
            random.shuffle(self.ellipseDots)