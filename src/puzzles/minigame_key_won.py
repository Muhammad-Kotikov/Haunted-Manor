from main import * 

def winning_message():
    SCREEN.fill(BLACK)
    winning_text = SMALL_FONT.render("Congratulations!", True, WHITE)
    text_rect = winning_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(winning_text, text_rect)
    pygame.display.flip()