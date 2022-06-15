import sys
from src.Settings import *
from Stats import *
from ClickArea import *
from MessageBoard import *

def run_game():
    pygame.init()
    clock = pygame.time.Clock()
    g_set = Settings(boardwidth=300, boardheight=600, message_board_height=50)
    g_stats = Stats(g_set)
    game_screen = pygame.display.set_mode((g_set.game_screen_width,
                                           g_set.game_screen_height + g_set.message_board_height))
    messageBoard = MessageBoard(game_screen, g_set, g_stats)
    areasList = createClickAreas(game_screen, g_set, g_stats)
    updateScreen(game_screen, g_set, g_stats, areasList, messageBoard)
    while True:
        clock.tick(120)
        if g_stats.waiting_game_input and not g_stats.drawing_click_area:
            checkEvents(game_screen, g_set, g_stats, areasList, messageBoard)
        elif not g_stats.waiting_game_input and g_stats.drawing_click_area:
            updateScreen(game_screen, g_set, g_stats, areasList, messageBoard)
        elif not g_stats.waiting_game_input and not g_stats.drawing_click_area:
            # This code comes into play once animation for X or O is done.
            # Checking the board to winner and turning event checker back ON!
            if checkBoard(g_stats, areasList) == False:
                g_stats.switch_turns()
                messageBoard.assignTurnMessage()
            pygame.event.clear()
            g_stats.waiting_game_input = True
            updateScreen(game_screen, g_set, g_stats, areasList, messageBoard)

def checkEvents(game_screen, g_set, g_stats, areasList, mBoard):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            checkClickedArea(game_screen, g_stats, areasList, (mouse_x, mouse_y), mBoard)
            updateScreen(game_screen, g_set, g_stats, areasList, mBoard)


def checkClickedArea(game_screen, g_stats, areasList, mouseLocation, mBoard):
    if not g_stats.game_over:
        for area in areasList:
            if area.rect.collidepoint(mouseLocation):
                if area.state == 'b':
                    area.mouseClickLocationx = mouseLocation[0]
                    area.mouseClickLocationy = mouseLocation[1]
                    area.generateAdjustedXCoor()
                    area.state = 'd'
                    g_stats.drawing_click_area = True
                    g_stats.waiting_game_input = False
    elif g_stats.game_over:
        if game_screen.get_rect().collidepoint(mouseLocation):
            resetGame(g_stats, areasList, mBoard)


def updateScreen(game_screen, g_set, g_stats, areasList, mBoard):
    drawClickAreas(game_screen, g_set, g_stats, areasList)
    drawHashtag(game_screen, g_set)
    drawWinningLine(game_screen, g_set, g_stats, mBoard)
    drawMessageBoard(mBoard)
    pygame.display.flip()

def drawMessageBoard(mBoard):
    mBoard.draw_message()

def resetClickArea(areasList):
    for area in areasList:
        area.clickAreaReset()

def resetGame(g_stats, areasList, mBoard):
    g_stats.reset_stats()
    mBoard.assignTurnMessage()
    resetClickArea(areasList)

def isAllAreasUsed(areasList):
    for area in areasList:
        if area.state == 'b':
            return False
    return True

def checkBoard(g_stats, areasList):
    if checkBoardLine(areasList[0], areasList[1], areasList[2]):
        g_stats.winningLine = 'vl1'
    elif checkBoardLine(areasList[3], areasList[4], areasList[5]):
        g_stats.winningLine = 'vl2'
    elif checkBoardLine(areasList[6], areasList[7], areasList[8]):
        g_stats.winningLine = 'vl3'
    elif checkBoardLine(areasList[0], areasList[3], areasList[6]):
        g_stats.winningLine = 'hl1'
    elif checkBoardLine(areasList[1], areasList[4], areasList[7]):
        g_stats.winningLine = 'hl2'
    elif checkBoardLine(areasList[2], areasList[5], areasList[8]):
        g_stats.winningLine = 'hl3'
    elif checkBoardLine(areasList[0], areasList[4], areasList[8]):
        g_stats.winningLine = 'cr1'
    elif checkBoardLine(areasList[2], areasList[4], areasList[6]):
        g_stats.winningLine = 'cr2'
    elif isAllAreasUsed(areasList):
        #marker for all area used with no winner outcome
        g_stats.winningLine = 'None'
    else:
        return False
    return True

def checkBoardLine(area1, area2, area3):
    if (area1.state == area2.state == area3.state == 'x') \
            or (area1.state == area2.state == area3.state == 'o'):
        return True
    return False

def createClickAreas(game_screen, g_set, g_stats):
    areasList = []
    for horizontal in range(3):
        for vertical in range(3):
            #creating 9 ClickAreas based on RELATIVE coordinates (corelated to the whole board)
            areasList.append(ClickArea((horizontal * g_set.x1, vertical * g_set.y1), game_screen, g_set, g_stats))
    return areasList

def drawClickAreas(screen, g_set, g_stats, areasList):
    for area in [al_blank for al_blank in areasList if al_blank.state == 'b']:
        area.draw_click_area()
    for area in [al_blank for al_blank in areasList if al_blank.state == 'x'
                                                       or al_blank.state == 'o']:
        area.draw_click_area()
    for area in [al for al in areasList if al.state == 'd']:
        area.draw_click_area()

def drawWinningLine(game_screen, g_set, g_stats, mBoard):
    if g_stats.winningLine and not g_stats.game_over:
        if g_stats.winningLine == 'None':
            g_stats.game_over = True
            mBoard.gameOverNoWinnerMessage()
        else:
            g_stats.game_over = True
            mBoard.gameOverMessage()
            g_stats.setWinningLine()
            pygame.draw.line(game_screen, (255, 0, 0), (g_stats.winLinex1, g_stats.winLiney1),
                             (g_stats.winLinex2, g_stats.winLiney2), 3)
    elif g_stats.winningLine and g_stats.game_over:
        pygame.draw.line(game_screen, (255, 0, 0), (g_stats.winLinex1, g_stats.winLiney1),
                         (g_stats.winLinex2, g_stats.winLiney2), 3)

def drawHashtag(game_screen, g_set):
    pygame.draw.line(game_screen, (0, 0, 255), (g_set.x1, 10), (g_set.x1, g_set.game_screen_height - 10))
    pygame.draw.line(game_screen, (0, 0, 255), (g_set.x2, 10), (g_set.x2, g_set.game_screen_height - 10))
    pygame.draw.line(game_screen, (0, 0, 255), (10, g_set.y1), (g_set.game_screen_width - 10, g_set.y1))
    pygame.draw.line(game_screen, (0, 0, 255), (10, g_set.y2), (g_set.game_screen_width - 10, g_set.y2))
    # Also drawing 3 lines separator for board message
    pygame.draw.line(game_screen, (0, 0, 255), (0, g_set.game_screen_height - 2),
                     (g_set.game_screen_width, g_set.game_screen_height - 2))
    pygame.draw.line(game_screen, (0, 0, 255), (0, g_set.game_screen_height),
                     (g_set.game_screen_width, g_set.game_screen_height))
    pygame.draw.line(game_screen, (0, 0, 255), (0, g_set.game_screen_height + 2),
                     (g_set.game_screen_width, g_set.game_screen_height + 2))

if __name__ == '__main__':
    run_game()
