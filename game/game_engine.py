import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine
WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.total_hits = 0
        self.winning_score = 3  # default: Best of 5 (first to 3 wins)

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.total_hits = 0
        self.ball.reset()
        # Reset paddles to center
        self.player.y = self.height // 2 - self.player.height // 2
        self.ai.y = self.height // 2 - self.ai.height // 2

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)
    
    def update(self):
        # Move the ball first
        self.ball.move()

        # --- Collision with paddles ---
        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.velocity_x *= -1
            hit_pos = (self.ball.y + self.ball.height / 2) - (self.player.y + self.player.height / 2)
            self.ball.velocity_y += hit_pos * 0.05
            self.total_hits += 1  # Count paddle hit

        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.velocity_x *= -1
            hit_pos = (self.ball.y + self.ball.height / 2) - (self.ai.y + self.ai.height / 2)
            self.ball.velocity_y += hit_pos * 0.05
            self.total_hits += 1  # Count paddle hit

        # Score handling
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # AI paddle movement
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        return self.player_score >= self.winning_score or self.ai_score >= self.winning_score
