import pygame
import random
import sys
from pygame.math import Vector2

pygame.init()

# Inisialisasi variabel dan konstanta
cell_size = 35
cell_number = 20
width, height = cell_number * cell_size, cell_number * cell_size
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
apel = pygame.image.load("Apple.png").convert_alpha()
game_font = pygame.font.Font(None, 36)
icon = pygame.image.load("Logo game.ico")
pygame.display.set_icon(icon)
# Load sounds
eat_sound = pygame.mixer.Sound("Sound/sound Makan.mp3")
menu_sound = pygame.mixer.Sound("Sound/main menu sound.wav")
death_sound = pygame.mixer.Sound("Sound/dead notification.mp3")

SCREEN_UPDATE = pygame.USEREVENT
pygame.display.set_caption("SERPENTES")
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Definisi kelas SNAKE, FRUIT, dan MAIN
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)

            # Draw snake body with stroke
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 0), block_rect)  # Black stroke
            pygame.draw.rect(screen, (255, 255, 255), block_rect.inflate(-4, -4))  # White fill

            # Draw eyes on the head of the snake
            if block == self.body[0]:
                eye_size = int(cell_size * 0.2)
                eye_offset_x = int(cell_size * 0.2)
                eye_offset_y = int(cell_size * 0.2)
                left_eye_rect = pygame.Rect(x_pos + eye_offset_x, y_pos + eye_offset_y, eye_size, eye_size)
                right_eye_rect = pygame.Rect(x_pos + cell_size - eye_size - eye_offset_x, y_pos + eye_offset_y, eye_size, eye_size)
                pygame.draw.rect(screen, (0, 0, 0), left_eye_rect)  # Left eye
                pygame.draw.rect(screen, (0, 0, 0), right_eye_rect)  # Right eye

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
        # Play eat sound when a block is added
        eat_sound.play()

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        apel_resized = pygame.transform.scale(apel, (cell_size, cell_size))
        screen.blit(apel_resized, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_dead()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            # Mengatur ulang posisi buahnya
            self.fruit.randomize()
            # Tambahin blok ke ular
            self.snake.add_block()

    def check_dead(self):
        # Mengecek ular keluar dari batas
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        death_sound.play()  # Mainkan suara kematian
        game_over_text = game_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))
        screen.blit(game_over_text, game_over_rect)
        pygame.display.update()

        pygame.time.delay(2000)  # Pause for 2 seconds
        pygame.quit()
        sys.exit()

    def draw_grass(self):
        grass_color = (73, 95, 65)  # Adjust the color to match the main menu image
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

# Fungsi untuk menampilkan menu utama
def show_main_menu():
    in_main_menu = True
    menu_sound.play()  # Play menu sound
    main_menu_img = pygame.image.load('Mainmenu.png')
    main_menu = pygame.transform.scale(main_menu_img, (width, height))

    while in_main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Cek apakah ada klik mouse di menu utama
                in_main_menu = False

        screen.blit(main_menu, (0, 0))
        pygame.display.update()
    
    menu_sound.stop()  # Stop menu sound

# Inisialisasi permainan dan tampilkan menu utama
main_game = MAIN()
show_main_menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == SCREEN_UPDATE:
            main_game.update()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
