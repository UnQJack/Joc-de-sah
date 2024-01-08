import pygame
import sys

pygame.font.init()

sys.path.append('D:/data/classes/')
from Board import Board

pygame.display.set_caption('Two-Player Pygame Chess!')

WINDOW_SIZE = (800, 650) 
screen = pygame.display.set_mode(WINDOW_SIZE)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
timer = pygame.time.Clock()
fps = 60

board = Board(WINDOW_SIZE[0]-200, WINDOW_SIZE[1]-50) 

status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
               'Black: Select a Piece to Move!', 'Black: Select a Destination!']
current_status = 0  

def draw(display):
    display.fill('dark gray')
    board.draw(display)
    
    #pygame.draw.rect(display, 'dark gray', (WINDOW_SIZE[0] - 200, 0, 200, WINDOW_SIZE[1]))
    #pygame.draw.rect(display, 'dark gray', (0, WINDOW_SIZE[1] - 50, WINDOW_SIZE[0], 50))
    font = pygame.font.Font(None, 36)
    text = font.render(status_text[current_status], True, (0, 0, 0))
    display.blit(text, (10, WINDOW_SIZE[1] - 50))
    screen.blit(medium_font.render('FORFEIT', True, 'black'), (610, 600))
    pygame.display.update()
        
        
def draw_scores():
    font = pygame.font.Font(None, 36)
    white_score_text = font.render(f'White Score: {white_score}', True, (255, 255, 255))
    black_score_text = font.render(f'Black Score: {black_score}', True, (255, 255, 255))
    screen.blit(white_score_text, (10, 10))
    screen.blit(black_score_text, (10, 60))

white_score = 0
black_score = 0

if __name__ == '__main__':
    running = True
    while running:
        timer.tick(fps)
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1:
                    board.handle_click(mx, my)
                    current_status = (current_status + 1) % len(status_text)
                    
        if board.is_in_checkmate('black'):
            print('White wins!')
            white_score += 1
            running = False
        elif board.is_in_checkmate('white'):
            print('Black wins!')
            black_score += 1
            running = False
        
        draw(screen)
