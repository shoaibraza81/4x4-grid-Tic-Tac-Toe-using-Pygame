import pygame
import sys
import time
import gamelogic as ttt

pygame.init()
size = width, height = 800, 600

# Colors
black = (0, 0, 0)
gray = (90, 90, 90)
white = (241, 250, 238)
shadow = (50, 50, 50)  # Shadow color for the button

screen = pygame.display.set_mode(size)

smallFont = pygame.font.Font("Asul-Bold.ttf", 30)
mediumFont = pygame.font.Font("Asul-Bold.ttf", 60)
largeFont = pygame.font.Font("Asul-Bold.ttf", 90)
moveFont = pygame.font.Font("Asul-Bold.ttf", 50)

user = None
board = ttt.initial_state()
ai_turn = False

# Function to draw modern 3D style button
def draw_3d_button(surface, rect, text, font, base_color, shadow_color, text_color, hover=False):
    shadow_offset = 4
    border_radius = 10

    # Shadow
    shadow_rect = pygame.Rect(rect.x + shadow_offset, rect.y + shadow_offset, rect.width, rect.height)
    pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=border_radius)

    # Main button
    color = (min(base_color[0] + 20, 255), min(base_color[1] + 20, 255), min(base_color[2] + 20, 255)) if hover else base_color
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)

    # Text
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(gray)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 120)
        screen.blit(title, titleRect)

        lowertitle = smallFont.render("(Using py-game)", True, white)
        titleRect = lowertitle.get_rect()
        titleRect.center = ((width / 2), 190)
        screen.blit(lowertitle, titleRect)

        # Draw buttons with modern 3D look
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        hover_x = playXButton.collidepoint(pygame.mouse.get_pos())
        draw_3d_button(screen, playXButton, "Play as X", smallFont, white, shadow, black, hover=hover_x)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        hover_o = playOButton.collidepoint(pygame.mouse.get_pos())
        draw_3d_button(screen, playOButton, "Play as O", smallFont, white, shadow, black, hover=hover_o)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        # Draw 4x4 game board
        grid_size = 4
        tile_size = 100
        tile_origin = (width / 2 - (grid_size / 2 * tile_size), height / 2 - (grid_size / 2 * tile_size))
        tiles = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                rect = pygame.Rect(tile_origin[0] + j * tile_size, tile_origin[1] + i * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, black, rect)
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = mediumFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 70)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board, depth_limit=3)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(grid_size):
                for j in range(grid_size):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            # Draw Retry button with modern 3D look
            againButton = pygame.Rect(width / 5, height - 85, width / 4, 50)
            hover_retry = againButton.collidepoint(pygame.mouse.get_pos())
            draw_3d_button(screen, againButton, "Retry", smallFont, white, shadow, black, hover=hover_retry)

            # Draw Quit button with modern 3D look
            quitButton = pygame.Rect(3 * (width / 5), height - 85, width / 4, 50)
            hover_quit = quitButton.collidepoint(pygame.mouse.get_pos())
            draw_3d_button(screen, quitButton, "Quit", smallFont, white, shadow, black, hover=hover_quit)

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False
                elif quitButton.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

    pygame.display.flip()
