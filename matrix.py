import pygame
from random import randint, choice
from pygame.locals import *
import string

max_lines = 100

class textblock():
    """ A block including one character """
    def __init__(self,character, font, background, fadetime, x_pos, y_pos):
        # Draw our character to the screen
        self.last_update = pygame.time.get_ticks()
        self.character = character
        self.font = font
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.cur_color = 0
        self.rect = None
        self.color_prog = [(250,250,250),  
                           (150,150,169),
                           (125,250,125),
                           (0,250,0), 
                           (0,250,0), 
                           (0,250,0), 
                           (0,250,0), 
                           (0,125,0), 
                           (0,100,0), 
                           (0,0,0)]

        self.fade_interval = (fadetime * 1000)/len(self.color_prog)
        self.update(background)

    def update(self, background):
        # Update the character and redraw
        # When faded we return False, otherwise return True
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_update) > self.fade_interval:
            self.last_update = current_time
            self.cur_color = self.cur_color + 1
            if randint(0,10000) == 1:
                background.fill(pygame.Color("black"), self.rect)
                self.character = choice(string.ascii_lowercase)

        if self.cur_color >= len(self.color_prog):
            background.fill(pygame.Color("black"), self.rect)
            return False

        text = self.font.render(self.character, 1, self.color_prog[self.cur_color])
        textpos = text.get_rect()
        textpos.x = self.x_pos
        textpos.y = self.y_pos
        background.blit(text, textpos)
        self.rect = textpos
        if randint(0,100) == 1:
            self.character = choice(string.ascii_lowercase)
        return True


class textline():
    """ A line of text travelling """
    def __init__(self, font, background, x_pos, speed):
        self.last_update = pygame.time.get_ticks()
        self.x_pos = x_pos
        self.head_y_pos = 0
        self.chars = []
        self.font = font
        self.font_height = font.get_height()
        self.speed = speed

    def update(self,background):
        to_remove = []
        for i in range(0,len(self.chars)):
            response = self.chars[i].update(background)
            if not response:
                to_remove.append(i)

        for i in sorted(to_remove, reverse=True):  # sorted so we don't try to delete keys already removed
            del(self.chars[i])

        current_time = pygame.time.get_ticks()
        if (current_time - self.last_update) > self.speed:
            self.last_update = current_time
  
            if self.head_y_pos < 600:
                new_char = choice(string.ascii_lowercase)
                self.head_y_pos = self.head_y_pos + self.font_height
                self.chars.append(textblock(new_char,self.font,background,2,self.x_pos, self.head_y_pos))             
                return True

            if len(self.chars) == 0:
                return False
        return True


def main():
   
	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((1200, 600))
	pygame.display.set_caption('Falling Text')

	# Fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

        # Draw our lines
	font = pygame.font.Font("resources/fonts/matrix.ttf", 16)

        matrix_lines = list()
        for i in range(5):
            matrix_lines.append(textline(font,background,randint(0,120)*10,randint(30,150)))

	# Blit everything to the screen
	screen.blit(background, (0, 0))
	pygame.display.flip()

	# Event loop
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

                to_remove = []
                for i in range(0,len(matrix_lines)):
                    response = matrix_lines[i].update(background)
                    if not response:
                        to_remove.append(i)

                for i in to_remove:
                    del(matrix_lines[i])
                    matrix_lines.append(textline(font,background,randint(0,120)*10,randint(30,150)))

                if len(matrix_lines) < max_lines:
                    if randint(0,10) > 8:
                        matrix_lines.append(textline(font,background,randint(0,120)*10,randint(30,150)))

		screen.blit(background, (0, 0))
		pygame.display.flip()


if __name__ == '__main__': main()
