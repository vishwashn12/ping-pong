import pygame
from game.game_engine import GameEngine
import pygame
from game.game_engine import GameEngine
import os

# Initialize mixer before anything else
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()


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

def replay_menu(screen, engine):
    font_title = pygame.font.SysFont("Arial", 50, bold=True)
    font_option = pygame.font.SysFont("Arial", 40)

    waiting = True
    while waiting:
        screen.fill((0, 0, 0))

        # Title
        title_surface = font_title.render("Select Mode / Replay", True, (255, 215, 0))
        title_rect = title_surface.get_rect(center=(engine.width//2, engine.height//4))
        screen.blit(title_surface, title_rect)

        # Options
        options = [
            "Press 3: Best of 3",
            "Press 5: Best of 5",
            "Press 7: Best of 7",
            "Press ESC: Exit"
        ]
        for i, text in enumerate(options):
            opt_surface = font_option.render(text, True, (255, 255, 255))
            opt_rect = opt_surface.get_rect(center=(engine.width//2, engine.height//2 + i*50))
            screen.blit(opt_surface, opt_rect)

        pygame.display.flip()

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    engine.winning_score = 2
                    engine.reset_game()
                    return True
                elif event.key == pygame.K_5:
                    engine.winning_score = 3
                    engine.reset_game()
                    return True
                elif event.key == pygame.K_7:
                    engine.winning_score = 4
                    engine.reset_game()
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False

def main():
    running = True
    game_over = False
    game_over_start = None

    while running:
        SCREEN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            engine.handle_input()
            engine.update()
            engine.render(SCREEN)

            if engine.check_game_over(SCREEN):
                game_over = True
                game_over_start = pygame.time.get_ticks()
        else:
            # Game Over screen
            engine.render(SCREEN)
            font_title = pygame.font.SysFont("Arial", 60, bold=True)
            font_stats = pygame.font.SysFont("Arial", 40)

            winner_text = "Player Wins!" if engine.player_score >= engine.winning_score else "AI Wins!"
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

            pygame.display.flip()

            # Wait 2 seconds, then show replay menu
            if pygame.time.get_ticks() - game_over_start > 2000:
                if replay_menu(SCREEN, engine):
                    game_over = False  # Reset flag to start new game
                    game_over_start = None
                else:
                    running = False  # Player chose to exit

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
