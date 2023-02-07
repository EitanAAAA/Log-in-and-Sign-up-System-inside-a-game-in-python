import pygame
import pandas as pd
from ShipRace.data import *
from ShipRace.spaceShip import SpaceShip
from ShipRace.steroids import steroids_list
from LogInSignUp.data_main import running

pygame.init()

space_ship = SpaceShip(230, 500)

# display the window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ShipRace")

clock = pygame.time.Clock()


# import pictures and sounds
back_ground = pygame.transform.scale(pygame.image.load("pic/BG.png"), (WIDTH, HEIGHT))
coll_sound = pygame.mixer.Sound("sounds/hit.wav")
click_sound = pygame.mixer.Sound("sounds/hover.wav")
win_sound = pygame.mixer.Sound("sounds/win_sound.wav")
coll_sound.set_volume(0.5)

def draWindow():
    win.blit(back_ground, (0,0))
    clock.tick(FPS)
    space_ship.draw(win, steroids_list, coll_sound) # draw the ship

    writeOnWindow(str(space_ship._timer)[0:5], 100, GRAY, 350, 20) # write the timer

    for s in steroids_list:
        s.draw(win)

    pygame.display.update()


def writeOnWindow(text, size, color, x, y, rotate=False):
    font = pygame.font.SysFont('comicsans', size)
    _text = font.render(text, True, color)
    if rotate:
        _text = pygame.transform.rotate(_text, 30)
    win.blit(_text, (x, y))


def run():
    name, password = menu()
    df = pd.read_csv("UsersData.csv") # import the users data
    # set background music
    pygame.mixer.music.load("sounds/music.mp3")
    pygame.mixer.music.set_volume(0.2)

    # check if the user connect and click on the start button
    if coll:
        pygame.mixer.music.play(-1)
        while True:
            events()
            draWindow()
            if space_ship.y <= 0:
                win_sound.play() # play the winning sound
                # check if the current score is smaller than the high score
                if df.loc[df["name"] == name, "high_score"].iloc[0] > float(space_ship.score):
                    # change the value of the score to the new score and export the new data
                    df.loc[df["name"] == name, "high_score"] = float(space_ship.score)
                    df.to_csv("UsersData.csv", index=False)

                top_score_board(df)


def menu():
    global coll
    connect = False

    win_menu = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ShipRace")

    clock = pygame.time.Clock()

    df = pd.read_csv("UsersData.csv") # import the users data
    ev, name, password = 0,0,0

    def collision(x,y,w,h):
        return (x <= mouse[0] <= x+w) and (y <= mouse[1] <= y+h)

    # buttons rects
    connect_rect = pygame.Rect(200, 400, 150, 50)
    start_rect = pygame.Rect(200, 500, 150, 50)

    button_color_conn = PURPLE
    button_color_start = PURPLE

    while True:
        win.blit(back_ground, (0,0))
        clock.tick(60)

        writeOnWindow("Deadly Meteors", 80, (150,10,90), 90, 20) # write the name of the game

        # display the buttons
        pygame.draw.rect(win_menu, button_color_conn, connect_rect)
        pygame.draw.rect(win_menu, button_color_start, start_rect)
        writeOnWindow("Connect", 50, HARD_GRAY, connect_rect.x+5, connect_rect.y+10)
        writeOnWindow("Start", 50, HARD_GRAY, connect_rect.x+30, connect_rect.y+110)

        # if the data is not empty, write the name of the player with the best score
        if not(df.empty):
            writeOnWindow("The player in the 1st place is: ", 50, (204,204,0), 40, 100)
            min_score = df["high_score"].min()
            st_player = df.loc[df["high_score"] == min_score, "name"].iloc[0]
            writeOnWindow(f"{st_player} with {min_score}", 50, (170,170,0), 150, 150)

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # check clicking
            if event.type == pygame.MOUSEBUTTONDOWN:
                if collision(connect_rect.x, connect_rect.y, connect_rect.w, connect_rect.h):
                    if not(connect):
                        click_sound.play()
                        ev, name, password = running(df)
                        connect = True

                if collision(start_rect.x, start_rect.y, start_rect.w, start_rect.h):
                    click_sound.play()
                    if connect:
                        coll = True
                        return name, password


        # change the color to light purple if the mouse is hover the button
        button_color_conn = LIGHT_PURPLE if collision(connect_rect.x, connect_rect.y, connect_rect.w, connect_rect.h) else  PURPLE
        button_color_start = LIGHT_PURPLE if collision(start_rect.x, start_rect.y, start_rect.w, start_rect.h) else PURPLE


        # check the event
        if ev == 'Sign up':
            writeOnWindow(f"New Player, Welcome {name}!", 50, GRAY,40, 200,True)
        elif ev == "Log in":
            writeOnWindow(f"Its you again, {name}", 50, GRAY, 40, 200, True)

        pygame.display.update()


def top_score_board(df):

    df.to_csv("UsersData", index=False)# import the users data or the new users data(if they changed)

    win_board = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ShipRace")

    clock = pygame.time.Clock()

    scores = list(df["high_score"])
    # get the five players with the best scores
    if len(scores) >= 5:
        length = 5
    else:
        length=len(scores)
    top_5 = []
    for i in range(length):
        top_5.append(min(scores))
        scores.remove(min(scores))


    r,g,b = 255,255,0
    up, down = True, False
    while True:
        win.blit(back_ground, (0,0))
        clock.tick(60)
        writeOnWindow("High Score Board", 80, (150,10,90), 50, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        # drawing the top 5 players scores
        for index, score in enumerate(top_5):
            score_rect = pygame.Rect(150, (index+1)*100, 200, 50)
            name_rect = pygame.Rect(score_rect.x+170, score_rect.y, 100, 50)
            pygame.draw.rect(win_board, (r,g,b), score_rect)
            pygame.draw.rect(win_board,(r,g,b), name_rect)
            writeOnWindow(str(score), 40, BLACK, score_rect.x+20, score_rect.y + 10)
            writeOnWindow(str(df.loc[df["high_score"]==score,"name"].iloc[0]), 30, BLACK, name_rect.x+20, name_rect.y + 10)

            # change the squares colors
            if r == 255 and g == 255:down = True;up = False

            elif r == 200 and g ==200:up = True;down = False

            if down:r-=1;g-=1

            if up:r+=1;g+=1

        pygame.display.update()

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

