import pygame

pygame.font.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

class Square:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.abs_x = x * width
		self.abs_y = y * height
		self.abs_pos = (self.abs_x, self.abs_y)
		self.pos = (x, y)
		self.color = 'light' if (x + y) % 2 == 0 else 'dark'
		self.draw_color = (220, 189, 194) if self.color == 'light' else (53, 53, 53)
		self.highlight_color = (100, 249, 83) if self.color == 'light' else (0, 228, 10)
		self.occupying_piece = None
		self.coord = self.get_coord()
		self.highlight = False

		self.rect = pygame.Rect(
			self.abs_x,
			self.abs_y,
			self.width,
			self.height
		)


	def get_coord(self):
		columns = 'abcdefgh'
		return columns[self.x] + str(self.y + 1)


	def draw(self, display):
		color = 'dark gray'
		if (self.x + self.y) % 2 == 0:
			color = 'light gray'

		if self.highlight:
			color = (186, 151, 200)

		x_coord = self.x * self.width
		y_coord = self.y * self.height
		rect_width = self.width
		rect_height = self.height	

		pygame.draw.rect(display, color, (x_coord, y_coord, rect_width, rect_height))

		pygame.draw.line(display, 'black', (x_coord, y_coord), (x_coord + rect_width, y_coord), 2)
		pygame.draw.line(display, 'black', (x_coord + rect_width, y_coord), (x_coord + rect_width, y_coord + rect_height), 2)
		pygame.draw.line(display, 'black', (x_coord, y_coord + rect_height), (x_coord + rect_width, y_coord + rect_height), 2)
		pygame.draw.line(display, 'black', (x_coord, y_coord), (x_coord, y_coord + rect_height), 2)


		if self.occupying_piece != None:
			centering_rect = self.occupying_piece.img.get_rect()
			centering_rect.center = self.rect.center
			display.blit(self.occupying_piece.img, centering_rect.topleft)
