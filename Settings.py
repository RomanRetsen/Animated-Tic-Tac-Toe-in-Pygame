class Settings:
    def __init__(self, s_width, s_height, message_board_height):
        self.game_screen_width = s_width
        self.game_screen_height = s_height
        self.message_board_height = message_board_height
        self.x1, self.x2, self.y1, self.y2 = self.calculateHashMarks()
        self.click_area_width = self.x1
        self.click_area_height = self.y1
        print(self.click_area_width / 2, self.game_screen_width / 6)

    def calculateHashMarks(self):
        x1 = self.game_screen_width / 3
        x2 = (self.game_screen_width / 3) * 2
        y1 = self.game_screen_height / 3
        y2 = (self.game_screen_height / 3) * 2
        return (int(x1), int(x2), int(y1), int(y2))