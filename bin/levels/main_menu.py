import os
import sys
import time

from ..classes.level import Level
from bin.colours import *
from ..classes.buttons import ButtonRect

gameOn = False


class MainMenu(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.f_regular_small = pg.font.Font(os.getcwd() + "/resources/Herculanum-Regular.ttf", 40)
        self.f_regular = pg.font.Font(os.getcwd() + "/resources/Herculanum-Regular.ttf", 50)
        self.f_regular_big = pg.font.Font(os.getcwd() + "/resources/Herculanum-Regular.ttf", 100)
        # Create Button Class
        self.b_play_game = ButtonRect(self.text_canvas, 100, 400, 650, 150, cw_blue, "Play Game", self.f_regular_big, white)
        self.b_options = ButtonRect(self.text_canvas, 100, 600, 300, 100, cw_blue, "Options", self.f_regular, white)
        self.b_help = ButtonRect(self.text_canvas, 450, 600, 300, 100, cw_blue, "How to Play", self.f_regular_small, white)
        self.b_credits = ButtonRect(self.text_canvas, 100, 750, 300, 100, cw_blue, "Credits", self.f_regular, white)
        self.b_quit = ButtonRect(self.text_canvas, 450, 750, 300, 100, cw_blue, "Quit", self.f_regular, white)
        self.buttons = [self.b_play_game, self.b_options, self.b_help, self.b_credits, self.b_quit]
        self.background = pg.image.load(os.getcwd() + "/resources/menus/01_main_menu.png").convert()

    def run(self):
        while True:
            # Framerate Independence
            dt = time.time() - self.last_time
            dt *= 60  # Delta time - 60fps physics
            self.last_time = time.time()
            self.click = False
            mx, my = pg.mouse.get_pos()  # Get mouse position
            # ----------------------------------------------------------------------------------------------------------
            for event in pg.event.get():
                pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
                if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:  # When Mouse Button Clicked
                    if event.button == 1:  # Left Mouse Button
                        self.click = True
            # ------------------------------------------------------------------------------------------------------------------
            if not self.fade_out and not self.freeze:
                self.transition_in("game", self.game_canvas, dt)
            elif self.freeze:  # To prevent the transition from happening offscreen
                self.freeze = False
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens()
            # ------------------------------------------------------------------------------------------------------------------
            self.game_canvas.fill(white)
            pg.draw.rect(self.game_canvas, (pg.Color("#171717")), pg.Rect(0, 0, self.width, 375))
            self.game_canvas.blit(self.background, (0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            for i in self.buttons:
                i.draw_button(mx, my)
            # --------------------------------------------------------------------------------------------------------------
            if self.b_play_game.check_click(mx, my, self.click):
                self.next_level = 2
                self.fade_out = True
            # --------------------------------------------------------------------------------------------------------------
            if self.b_options.check_click(mx, my, self.click):
                self.next_level = 4
                self.fade_out = True
            # --------------------------------------------------------------------------------------------------------------
            if self.b_help.check_click(mx, my, self.click):
                self.next_level = 5
                self.fade_out = True
            # --------------------------------------------------------------------------------------------------------------
            if self.b_credits.check_click(mx, my, self.click):
                self.next_level = 6
                self.fade_out = True
            # --------------------------------------------------------------------------------------------------------------
            if self.b_quit.check_click(mx, my, self.click):
                self.next_level = 7
                self.fade_out = True
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            # print(self.clock.get_fps())
            pg.display.update()
