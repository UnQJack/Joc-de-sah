import pygame
import sys

sys.path.append('D:/data/classes/')
from Square import Square
sys.path.append('D:/data/classes/pieces')
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from King import King
from Pawn import Pawn

class Board:
	def __init__(self, width, height): 
		self.width = width
		self.height = height
		self.tile_width = width // 8
		self.tile_height = height // 8
		self.selected_piece = None
		self.turn = 'white'
		self.captured_pieces_white = []
		self.captured_pieces_black = []

		self.config = [
			['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
			['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
			['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
		]

		self.squares = self.generate_squares()

		self.setup_board()


	def generate_squares(self): #Creează o listă de obiecte Square pentru reprezentarea pătratelor pe tabla de șah.
		output = []
		for y in range(8):
			for x in range(8):
				output.append(
					Square(x,  y, self.tile_width, self.tile_height)
				)
		return output


	def get_square_from_pos(self, pos): #Returnează obiectul square corespunzător unei anumite poziții pe tabla de șah.
		for square in self.squares:
			if (square.x, square.y) == (pos[0], pos[1]):
				return square


	def get_piece_from_pos(self, pos): #Returnează piesa de șah de pe un anumit pătrat al tablei.
		return self.get_square_from_pos(pos).occupying_piece


	def setup_board(self): #Inițializează tabla de șah cu piese, în funcție de configurația dată în self.config.
		for y, row in enumerate(self.config):
			for x, piece in enumerate(row):
				if piece != '':
					square = self.get_square_from_pos((x, y))
					if piece[1] == 'R':
						square.occupying_piece = Rook(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					elif piece[1] == 'N':
						square.occupying_piece = Knight(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					elif piece[1] == 'B':
						square.occupying_piece = Bishop(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					elif piece[1] == 'Q':
						square.occupying_piece = Queen(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					elif piece[1] == 'K':
						square.occupying_piece = King(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					elif piece[1] == 'P':
						square.occupying_piece = Pawn(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)


	def handle_click(self, mx, my): #Gestionează evenimentul de click pe tabla de șah, determinând acțiunile corespunzătoare, cum ar fi selectarea unei piese sau mutarea acesteia.
		x = mx // self.tile_width
		y = my // self.tile_height
		clicked_square = self.get_square_from_pos((x, y))

		if self.selected_piece is None:
			if clicked_square.occupying_piece is not None:
				if clicked_square.occupying_piece.color == self.turn:
					self.selected_piece = clicked_square.occupying_piece

		elif self.selected_piece.move(self, clicked_square):
			self.turn = 'white' if self.turn == 'black' else 'black'

		elif clicked_square.occupying_piece is not None:
			if clicked_square.occupying_piece.color == self.turn:
				self.selected_piece = clicked_square.occupying_piece


	def is_in_check(self, color, board_change=None): #Verifică dacă un rege de anumită culoare este în șah. Parametrul board_change este utilizat pentru a simula o mutare temporară pe tabla de șah.
		output = False
		king_pos = None

		changing_piece = None
		old_square = None
		new_square = None
		new_square_old_piece = None

		if board_change is not None:
			for square in self.squares:
				if square.pos == board_change[0]:
					changing_piece = square.occupying_piece
					old_square = square
					old_square.occupying_piece = None
			for square in self.squares:
				if square.pos == board_change[1]:
					new_square = square
					new_square_old_piece = new_square.occupying_piece
					new_square.occupying_piece = changing_piece

		pieces = [
			i.occupying_piece for i in self.squares if i.occupying_piece is not None
		]

		if changing_piece is not None:
			if changing_piece.notation == 'K':
				king_pos = new_square.pos
		if king_pos == None:
			for piece in pieces:
				if piece.notation == 'K' and piece.color == color:
						king_pos = piece.pos
		for piece in pieces:
			if piece.color != color:
				for square in piece.attacking_squares(self):
					if square.pos == king_pos:
						output = True

		if board_change is not None:
			old_square.occupying_piece = changing_piece
			new_square.occupying_piece = new_square_old_piece
						
		return output


	def is_in_checkmate(self, color): #Verifică dacă o anumită culoare este în șah și în mat. Este folosită pentru a determina sfârșitul jocului.
		output = False

		for piece in [i.occupying_piece for i in self.squares]:
			if piece != None:
				if piece.notation == 'K' and piece.color == color:
					king = piece

		if king.get_valid_moves(self) == []:
			if self.is_in_check(color):
				output = True

		return output


	def draw(self, display): #Desenează tabla de șah pe fereastra Pygame, evidențiind pătratele selectate și mișcările valide ale piesei selectate. Această implementare include și clase pentru diverse tipuri de piese de șah (Rook, Bishop, Knight, Queen, King, Pawn), dar codul acestora nu este furnizat aici. Funcționalitatea acestora este evidentă în metoda setup_board, unde sunt create și plasate pe tabla de șah în funcție de configurație.
		if self.selected_piece is not None:
			self.get_square_from_pos(self.selected_piece.pos).highlight = True
			for square in self.selected_piece.get_valid_moves(self):
				square.highlight = True

		for square in self.squares:
			square.draw(display)

