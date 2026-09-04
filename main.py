import pygame
import random
import sys


pygame.init()
# Display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissors")


# Colors
col1 = (229, 115, 140)
col2 = (95, 133, 117)
bg = (13, 33, 31)


# Font
font = pygame.font.SysFont("arial", 24)


# Variables
player_1 = None
player_2 = None
computer_1 = None
score_1 = 0
score_2 = 0
winner = ""
rounds_wanted = 0
total_rounds = 0
gamemode = None
p1_name = "Player 1"
p2_name = "Computer"
entering_names = False
name_input_stage = 0
name_buffer = ""
waiting_p2 = False


def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


# Round winner
def find_winner(choice1, choice2, name1, name2):
    global score_1, score_2
    if choice1 == choice2:
        score_1 += 1
        score_2 += 1
        return "It's a Tie!"
    elif (choice1 == "Rock" and choice2 == "Scissors") or \
         (choice1 == "Paper" and choice2 == "Rock") or \
         (choice1 == "Scissors" and choice2 == "Paper"):
        score_1 += 1
        return f"{name1} Wins!"
    else:
        score_2 += 1
        return f"{name2} Wins!"


# Final winner
def final_winner():
    if score_1 > score_2:
        return f"{p1_name} Wins the Game!"
    elif score_2 > score_1:
        return f"{p2_name} Wins the Game!"
    else:
        return "It's a Tie Overall!"


# Draw screen
def draw():
    screen.fill(bg)
    draw_text("Rock, Paper, Scissors", col1, WIDTH//2, 0.1*HEIGHT)


    # Home screen
    if gamemode is None and not entering_names:
        draw_text("Choose Gamemode:", col2, WIDTH//2, 0.3*HEIGHT)
        draw_text("1 - Computer vs Computer", col2, WIDTH//2, 0.4*HEIGHT)
        draw_text("2 - Human vs Computer", col2, WIDTH//2, 0.5*HEIGHT)
        draw_text("3 - Human vs Human", col2, WIDTH//2, 0.6*HEIGHT)
        return


    # Names
    if entering_names:
        if name_input_stage == 0:
            draw_text("Enter Player 1 Name:", col2, WIDTH//2, 0.4*HEIGHT)
        elif name_input_stage == 1 and gamemode == "hvh":
            draw_text("Enter Player 2 Name:", col2, WIDTH//2, 0.4*HEIGHT)
        draw_text(name_buffer + "|", col1, WIDTH//2, 0.5*HEIGHT)
        return


    # Round select
    if rounds_wanted == 0:
        draw_text("Enter number of rounds! (1-10)", col2, WIDTH//2, 0.8*HEIGHT)


    # Show choices
    if player_1 and gamemode != "hvh":
        draw_text(f"{p1_name} chose: {player_1}", col1, WIDTH//2, 0.2*HEIGHT)
    if player_2:
        draw_text(f"{p2_name} chose: {player_2}", col1, WIDTH//2, 0.3*HEIGHT)


    if winner:
        draw_text(f"{winner}", col1, WIDTH//2, 0.4*HEIGHT)


    if score_1 or score_2:
        draw_text(f"{p1_name} Score: {score_1}", col1, WIDTH//2, 0.5*HEIGHT)
        draw_text(f"{p2_name} Score: {score_2}", col1, WIDTH//2, 0.6*HEIGHT)


    if rounds_wanted:
        draw_text(f"Rounds: {total_rounds}/{rounds_wanted}", col1, WIDTH//2, 0.7*HEIGHT)


    if rounds_wanted > 0 and total_rounds == rounds_wanted:
        draw_text(f"Final Winner: {final_winner()}", col1, WIDTH//2, 0.9*HEIGHT)
        draw_text("Press SPACE to return Home", col2, WIDTH//2, 0.95*HEIGHT)


# Reset game
def reset_game():
    global player_1, player_2, computer_1, score_1, score_2, winner, rounds_wanted, total_rounds, gamemode, entering_names
    global waiting_p2
    player_1 = None
    player_2 = None
    computer_1 = None
    score_1 = 0
    score_2 = 0
    winner = ""
    rounds_wanted = 0
    total_rounds = 0
    gamemode = None
    entering_names = False
    waiting_p2 = False


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


        if event.type == pygame.KEYDOWN:
            # Home screen selection
            if gamemode is None and not entering_names:
                if event.key == pygame.K_1:
                    gamemode = "cvc"
                    p1_name, p2_name = "Computer 1", "Computer 2"
                elif event.key == pygame.K_2:
                    gamemode = "hvc"
                    entering_names = True
                    name_input_stage = 0
                    name_buffer = ""
                elif event.key == pygame.K_3:
                    gamemode = "hvh"
                    entering_names = True
                    name_input_stage = 0
                    name_buffer = ""


            # Name entry
            elif entering_names:
                if event.key == pygame.K_RETURN:
                    if name_input_stage == 0:
                        p1_name = name_buffer if name_buffer.strip() else "Player 1"
                        name_buffer = ""
                        if gamemode == "hvc":
                            entering_names = False
                            p2_name = "Computer"
                        else:
                            name_input_stage = 1
                    elif name_input_stage == 1:
                        p2_name = name_buffer if name_buffer.strip() else "Player 2"
                        entering_names = False
                        name_buffer = ""
                elif event.key == pygame.K_BACKSPACE:
                    name_buffer = name_buffer[:-1]
                else:
                    if len(name_buffer) < 12 and event.unicode.isprintable():
                        name_buffer += event.unicode


            # Round selection
            elif rounds_wanted == 0 and event.key in [
                pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                nums = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4,
                        pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8,
                        pygame.K_9: 9, pygame.K_0: 10}
                rounds_wanted = nums[event.key]
                score_1 = 0
                score_2 = 0
                total_rounds = 0
                winner = ""


            # Gameplay
            elif rounds_wanted > 0 and total_rounds < rounds_wanted:
                if gamemode == "cvc":  # computer vs computer
                    player_1 = random.choice(["Rock", "Paper", "Scissors"])
                    player_2 = random.choice(["Rock", "Paper", "Scissors"])
                    winner = find_winner(player_1, player_2, p1_name, p2_name)
                    total_rounds += 1
                elif gamemode == "hvc":  # human vs computer
                    if event.key in (pygame.K_i, pygame.K_o, pygame.K_p):
                        choices = {pygame.K_i: "Rock", pygame.K_o: "Paper", pygame.K_p: "Scissors"}
                        player_1 = choices[event.key]
                        player_2 = random.choice(["Rock", "Paper", "Scissors"])
                        winner = find_winner(player_1, player_2, p1_name, p2_name)
                        total_rounds += 1
                elif gamemode == "hvh":  # human vs human (hidden)
                    if not waiting_p2 and event.key in (pygame.K_i, pygame.K_o, pygame.K_p):
                        choices = {pygame.K_i: "Rock", pygame.K_o: "Paper", pygame.K_p: "Scissors"}
                        player_1 = choices[event.key]
                        waiting_p2 = True
                    elif waiting_p2 and event.key in (pygame.K_q, pygame.K_w, pygame.K_e):
                        choices = {pygame.K_q: "Rock", pygame.K_w: "Paper", pygame.K_e: "Scissors"}
                        player_2 = choices[event.key]
                        winner = find_winner(player_1, player_2, p1_name, p2_name)
                        total_rounds += 1
                        waiting_p2 = False


            # Reset after game
            if rounds_wanted > 0 and total_rounds == rounds_wanted:
                if event.key == pygame.K_SPACE:
                    reset_game()


    draw()
    pygame.display.flip()


pygame.quit()
sys.exit()

