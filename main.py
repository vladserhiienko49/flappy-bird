import pygame
import random

WIN_SIZE = (1000, 650)
SPEED = 8
BG_COLOR = "#2C64FF"

pygame.init()
window = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

class Button(pygame.Rect):
    def __init__(self, x, y, width, height, colors_background, colors_text, text):
        super().__init__(x, y, width, height)
        self.colors = colors_background
        self.colors_text = colors_text
        self.color = self.colors[0]
        self.text_str = text
        self.font = pygame.font.SysFont("Robotic", 45, bold=True)
        self.text = self.font.render(self.text_str, True, self.colors_text[0])
        self.clicked = False

    def draw(self, window):
        pygame.draw.rect(window, self.color, self)
        window.blit(
            self.text,
            (self.centerx - self.text.get_width() // 2, self.centery - self.text.get_height() // 2)
        )

    def active(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        if self.collidepoint(mouse_pos):
            self.color = self.colors[1]
            self.text = self.font.render(self.text_str, True, self.colors_text[1])
            if mouse_click and not self.clicked:
                self.clicked = True
                return True
        else:
            self.color = self.colors[0]
            self.text = self.font.render(self.text_str, True, self.colors_text[0])
        if not mouse_click:
            self.clicked = False
        return False

def make_tubes(count, width=80, height_max=450, gap=150, interval=400):
    tmp_list = []
    x = WIN_SIZE[0]
    for i in range(count):
        y = random.randint(-400, 0)
        tmp_list.append(pygame.Rect(x, y, width, height_max))
        tmp_list.append(pygame.Rect(x, y + height_max + gap, width, height_max))
        x += interval
    return tmp_list

title_font = pygame.font.SysFont("Robotic", 90, bold=True)
title_text = title_font.render("FLAPPY BIRD", True, "yellow")

score_font = pygame.font.SysFont("Robotic", 50, bold=True)

btn_colors = ("#30E04D", "yellow")
txt_colors = ("#2C64FF", "#2C64FF")

play_button = Button(390, 260, 220, 85, btn_colors, txt_colors, "PLAY")
close_button = Button(390, 375, 220, 85, btn_colors, txt_colors, "CLOSE")
back_button = Button(20, 20, 140, 50, btn_colors, txt_colors, "MENU")

player = pygame.Rect(20, 270, 50, 50)
tube_list = make_tubes(100)
passed_tubes = []
score = 0

game = True
which_window = "MENU"

while game:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game = False

    if which_window == "MENU":
        window.fill(BG_COLOR)
        window.blit(title_text, (WIN_SIZE[0] // 2 - title_text.get_width() // 2, 80))
        
        if score > 0:
            last_score_text = score_font.render(f"SCORE: {score}", True, "yellow")
            window.blit(last_score_text, (WIN_SIZE[0] // 2 - last_score_text.get_width() // 2, 180))
        
        play_button.draw(window)
        close_button.draw(window)

        if play_button.active():
            player.x = 20
            player.y = 270
            tube_list = make_tubes(100)
            passed_tubes = []
            score = 0
            which_window = "GAME"
        if close_button.active():
            game = False

    elif which_window == "GAME":
        window.fill("#2C64FF")
        pygame.draw.rect(window, "yellow", player)
        #шевелись блядо
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player.y > 0:
            player.y -= SPEED
        if keys[pygame.K_s] and player.bottom <= WIN_SIZE[1]:
            player.y += SPEED
            
        for i in range(0, len(tube_list), 2):
            top_tube = tube_list[i]
            bottom_tube = tube_list[i + 1]
            
            pygame.draw.rect(window, "#30E04D", top_tube)
            pygame.draw.rect(window, "#30E04D", bottom_tube)
            
            top_tube.x -= 5
            bottom_tube.x -= 5
        #просрав лох 
            if player.colliderect(top_tube) or player.colliderect(bottom_tube):
                which_window = "MENU"
                
            if top_tube.right < player.left and i not in passed_tubes:
                passed_tubes.append(i)
                score += 1

        score_text = score_font.render(f"SCORE: {score}", True, "yellow")
        window.blit(score_text, (WIN_SIZE[0] - score_text.get_width() - 30, 25))

        back_button.draw(window)
        if back_button.active():
            which_window = "MENU"

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
