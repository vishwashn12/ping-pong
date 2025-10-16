import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    game_over = False
    game_over_start = None

    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            engine.handle_input()
            engine.update()
            engine.render(SCREEN)

            # Check if someone reached 5 points
            if engine.check_game_over(SCREEN):
                game_over = True
                game_over_start = pygame.time.get_ticks()
        else:
            # Game over screen
            engine.render(SCREEN)  # Draw last frame

            # Fonts
            font_title = pygame.font.SysFont("Arial", 60, bold=True)
            font_stats = pygame.font.SysFont("Arial", 40)

            winner_text = "Player Wins!" if engine.player_score >= 5 else "AI Wins!"
            title_surface = font_title.render(winner_text, True, (255, 215, 0))
            title_rect = title_surface.get_rect(center=(engine.width//2, engine.height//3))
            SCREEN.blit(title_surface, title_rect)

            final_score = f"Final Score: Player {engine.player_score} - AI {engine.ai_score}"
            score_surface = font_stats.render(final_score, True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(engine.width//2, engine.height//2))
            SCREEN.blit(score_surface, score_rect)

            stats_surface = font_stats.render(f"Total Paddle Hits: {engine.total_hits}", True, (180, 180, 180))
            stats_rect = stats_surface.get_rect(center=(engine.width//2, engine.height*2//3))
            SCREEN.blit(stats_surface, stats_rect)

            # Keep screen for 4 seconds
            if pygame.time.get_ticks() - game_over_start > 4000:
                running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
