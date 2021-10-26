import pygame,sys
import random

pygame.init()
SCREEN_WIDTH,SCREEN_HEIGHT = 800,600
screen  =pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("Memory Squares")
FPS = 60

clock = pygame.time.Clock()

BLUE = (0,0,255)
WHITE = (255,) * 3
BLACK = (0,) * 3
LIGHTBLUE = (173,216,230)

class Square(pygame.sprite.Sprite):


    def __init__(self,x,y,size):
        super().__init__()



        self.size = size
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.flashed = False
        self.image.fill(BLUE)
    

    def set_flash(self):
        self.flashed = True
        self.image.fill(LIGHTBLUE)

    def draw(self):


        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen,BLACK,(*self.rect.topleft,self.size,self.size),2)











class Game:
    
    
    FONT = pygame.font.SysFont("calibri",40,bold=True)

    def __init__(self,rows=20,cols=20,size=25):
        self.rows = rows
        self.cols = cols


        self.side_gap = (SCREEN_WIDTH - rows *size)//2
        self.top_gap = (SCREEN_HEIGHT - cols * size)//2

        
        self.squares = pygame.sprite.Group()
        self.click_text = self.FONT.render("Click on New Square Added",True,BLACK)
        self.click_text_rect = self.click_text.get_rect(center=(SCREEN_WIDTH//2,10 + self.click_text.get_height()//2))


        
        self.grid = []
        self.row_cols = []
        for row in range(self.rows):
            new_row = []
            for col in range(self.cols):
                square = Square(self.side_gap + col * size,self.top_gap + row * size,size)
                self.squares.add(square)
                new_row.append(square)
                self.row_cols.append((row,col))
            self.grid.append(new_row)

        
        
        first_row,first_col = random.choice(self.row_cols)
        self.row_cols.remove((first_row,first_col))
        self.grid[first_row][first_col].set_flash()

    





    def _play(self):


        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass

             
            screen.fill(WHITE)
            for square in self.squares:
                square.draw()
            screen.blit(self.click_text,self.click_text_rect)
            pygame.display.update()
            clock.tick(FPS)
    

    def __call__(self):
        self._play()



game = Game()

game()






