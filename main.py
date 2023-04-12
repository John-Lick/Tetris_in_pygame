import sys
from tetris import Tetris, Text
import pathlib
from Settings import *

#Highest level of the program, handles app clock, rendering that sort of stuff
class App:
    #initialization
    def __init__(self):
        #Initialize pygame and audio mixer
        pg.init()
        mixer.init(48000, -16, 1, 1024)
        pg.display.set_caption("Tertris")
        self.screen = pg.display.set_mode(GAME_RES)
        self.clock = pg.time.Clock()
        #Create the tetris game
        self.tetris = Tetris(self)
        self.set_timer()
        #Creates the text for the hud
        self.text = Text(self)
        #Starts the iconic tune
        self.tetris.song.play(self.tetris.theme, -1)  
    #allows controlling time based events such as block falling and player movement
    def set_timer(self):
        #Sets ids and initializes timer related variables
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        #Set time interval for game events, interval scales with level
        pg.time.set_timer(self.user_event, DIFFICULTY_MAP[self.tetris.level])
        pg.time.set_timer(self.fast_user_event, FAST_TIME)
    #update the clock at our regular framerate
    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)
    #renders everything
    def draw(self):
        self.screen.fill(BGC)
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()
    #Event handler
    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            #if the quit button is hit, quit
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            #if a key is down we run the control function in the game
            if event.type == KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            # if we're on cycle for the game to push down, we push down at the intended rate
            if event.type == self.user_event:
                self.anim_trigger = True
            if event.type == self.fast_user_event:
                self.fast_anim_trigger = True
    #main loop
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
#if we're running the main file it starts, this is so if we're importing this file it won't start a game on its own
if __name__ == '__main__':
    app = App()
    app.run()
