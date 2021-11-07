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
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)

class Square(pygame.sprite.Sprite):


    def __init__(self,x,y,size):
        super().__init__()



        self.size = size
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.flashed = False
        self.image.fill(BLUE)
    

    def set_red(self):
        self.image.fill(RED)

    def set_flash(self):
        self.flashed = True
        self.image.fill(LIGHTBLUE)
    
    def reset(self):
        self.flashed = False
        self.image.fill(BLUE)
    def draw(self):


        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen,BLACK,(*self.rect.topleft,self.size,self.size),2)












class Game:
    
    
    FONT = pygame.font.SysFont("calibri",40,bold=True)
    START_SOUND = pygame.mixer.Sound("racestart.wav")
    BUZZER_SOUND = pygame.mixer.Sound("buzzer.ogg")
    CLICK_SOUND = pygame.mixer.Sound("match1.wav")
    def __init__(self,rows=20,cols=20,size=25):
        self.rows = rows
        self.cols = cols


        self.size = size
        self.side_gap = (SCREEN_WIDTH - rows *size)//2
        self.top_gap = (SCREEN_HEIGHT - cols * size)//2
        self.score = 0
        self.score_text = self.FONT.render("0",True,WHITE)
        self.board_width = size *cols
        self.board_height = size * rows
        self.game_over = True
        self.enter_text = self.FONT.render("Hit Enter to Play Again",True,WHITE)
        self.enter_text_rect = self.enter_text.get_rect(center=(SCREEN_WIDTH//2,10 + self.enter_text.get_height()//2))
        self.first_time = True
        self.first_time_text = self.FONT.render("Hit Enter to PLAY!",True,WHITE)
        self.first_time_rect = self.first_time_text.get_rect(center=(SCREEN_WIDTH//2,10 + self.first_time_text.get_height()//2))
        

        self.game_end_transparent_background = pygame.Surface((self.board_width,self.board_height),flags=pygame.SRCALPHA)
        self.game_end_transparent_background.fill((255,255,255,100))
        

        
        text = self.FONT.render("GAME OVER",True,RED)
        text_rect = text.get_rect(center=(self.game_end_transparent_background.get_width()//2,self.game_end_transparent_background.get_height()//2))
        self.game_end_transparent_background.blit(text,text_rect)
        
        

        self.squares = pygame.sprite.Group()
        self._set_click_text()


        
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

        
    def _set_click_text(self): 
        self.click_text = self.FONT.render("Click on New Square Added",True,WHITE)
        self.click_text_rect = self.click_text.get_rect(center=(SCREEN_WIDTH//2,10 + self.click_text.get_height()//2))



    
    def _check_if_high_score_and_write(self,score):


        with open("high_scores.txt",'r') as f:
            scores = list(map(int,f.readlines()))


        if score > scores[-1]:
            scores.pop()
            scores.append(score)

        scores.sort()


        with open("high_scores.txt",'w') as f:
            for score in scores:
                f.write(f"{score}\n")


    
    def _start_timer(self):


        messages = ['READY','SET','GO']
        colors = [RED,YELLOW,GREEN]


        texts = [self.FONT.render(message,True,color) for message,color in zip(messages,colors)]
        text_index = 0
        current_text = texts[0]


        SECOND_EVENT = pygame.USEREVENT + 1


        pygame.time.set_timer(SECOND_EVENT,1000)
        self.START_SOUND.play()


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == SECOND_EVENT:
                    text_index += 1
                    if text_index == len(texts):
                        return

                    current_text = texts[text_index]


            
            screen.fill(BLACK)
            self._draw_board()
            screen.blit(current_text,(SCREEN_WIDTH//2 - current_text.get_width()//2,0))
            screen.blit(self.score_text,(0,0))
            pygame.display.update()

    

    def _set_new_square_flash(self):
        row,col = random.choice(self.row_cols)
        self.row_cols.remove((row,col))
        self.flash_row = row
        self.flash_col = col
        self.grid[row][col].set_flash()

    def _draw_board(self):


        for square in self.squares:
            square.draw()
    

    def _check_row_and_column_pressed(self,x,y): 



        if self.side_gap < x < self.side_gap + self.board_width and self.top_gap < y < self.top_gap + self.board_height:
            x -= self.side_gap
            y -= self.top_gap
            row_pressed,col_pressed = y // self.size,x//self.size

            if row_pressed == self.flash_row and col_pressed == self.flash_col:
                self.CLICK_SOUND.play()
                return True
            
            
            if self.grid[row_pressed][col_pressed].flashed == True:
                self.game_over = True
                self.grid[self.flash_row][self.flash_col].set_red()
                self.BUZZER_SOUND.play()
                self._check_if_high_score_and_write(self.score)


        return False


    
    def _reset_board(self):


        for square in self.squares:
            if square.flashed:
                square.reset()

        self.score = 0
        self.score_text = self.FONT.render("0",True,WHITE)
        self._start_timer()
        self._set_new_square_flash()
        self.game_over = False
    
    def _draw(self):
        screen.fill(BLACK)
        for square in self.squares:
            square.draw()
        if not self.game_over:
            if not self.first_time:
                screen.blit(self.click_text,self.click_text_rect)
        else:
            if not self.first_time:
                screen.blit(self.game_end_transparent_background,(self.side_gap,self.top_gap))
                screen.blit(self.enter_text,self.enter_text_rect)
            else:
                screen.blit(self.first_time_text,self.first_time_rect)
        screen.blit(self.score_text,(0,0))
        pygame.display.update()
        clock.tick(FPS)
    
    def _play(self):
        

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()

                    guessed_correct = self._check_row_and_column_pressed(x,y)
                    if guessed_correct:
                        self.score += 1
                        self.score_text = self.FONT.render(f"{self.score}",True,WHITE)
                        self._set_new_square_flash()
                if  event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.first_time:
                            self.first_time = False
                            self.game_over = False
                            self._start_timer()
                            self._set_new_square_flash()
                        elif self.game_over:
                            self._reset_board()







             
            screen.fill(BLACK)
            for square in self.squares:
                square.draw()
            if not self.game_over:
                if not self.first_time:
                    screen.blit(self.click_text,self.click_text_rect)
            else:
                if not self.first_time:
                    screen.blit(self.game_end_transparent_background,(self.side_gap,self.top_gap))
                    screen.blit(self.enter_text,self.enter_text_rect)
                else:
                    screen.blit(self.first_time_text,self.first_time_rect)
            screen.blit(self.score_text,(0,0))
            pygame.display.update()
            clock.tick(FPS)
    

    def __call__(self):
        self._play()

class Game2(Game):

    
    def _set_click_text(self):
        self.click_text = self.FONT.render("Click on New Square Added",True,WHITE)
        self.click_text_rect = self.click_text.get_rect(center=(SCREEN_WIDTH//2,10 + self.click_text.get_height()//2))

    def _flash_square(self,row,col): 
        self.grid[row][col].set_flash()

    



    def _set_new_square_flash(self):
        row,col = random.randint(0,self.rows - 1),random.randint(0,self.cols -1)
        

        def flashes_helper(row,col,length):
            
            self._flash_square(row,col)

            if length == 0:
                return True
            if random.randint(1,2) == 1:
                return False

            for row_diff in (-1,0,1):
                for col_diff in (-1,0,1):
                    if row_diff ==0 and col_diff == 0:
                        continue

                    new_row =row + row_diff
                    new_col = col + col_diff

                    if self.grid[new_row][new_col].flashed == False:
                        result = flashes_helper(new_row,new_col,length -1)
                        if result:
                            return True

            return False

        length = 3
        flashes_helper(row,col,length)
        

game = Game()

game()






