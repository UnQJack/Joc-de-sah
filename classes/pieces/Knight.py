import pygame
import sys

sys.path.append('D:/data/classes/')
from Piece import Piece

class Knight(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		if color == 'black':
			img_path = 'D:/data/imgs/b_knight.png'
		else:
			img_path = 'D:/data/imgs/w_knight.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

		self.notation = 'N'


	def get_possible_moves(self, board):
		output = []
		moves = [
			(1, -2),
			(2, -1),
			(2, 1),
			(1, 2),
			(-1, 2),
			(-2, 1),
			(-2, -1),
			(-1, -2)
		]

		for move in moves:
			new_pos = (self.x + move[0], self.y + move[1])
			if (
				new_pos[0] < 8 and
				new_pos[0] >= 0 and 
				new_pos[1] < 8 and 
				new_pos[1] >= 0
			):
				output.append([
					board.get_square_from_pos(
						new_pos
					)
				])

		return output