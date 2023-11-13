import math

import pygame
import sys

from button import Button

pygame.init()

WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.transform.scale(pygame.image.load("assets/background.jpg"), (WIDTH, HEIGHT))
PG1 = pygame.transform.scale(pygame.image.load("assets/PG1.jpg"), (WIDTH, HEIGHT))
PG2 = pygame.transform.scale(pygame.image.load("assets/PG2.jpg"), (WIDTH, HEIGHT))
PG3 = pygame.transform.scale(pygame.image.load("assets/PG3.jpg"), (WIDTH, HEIGHT))
PG4 = pygame.transform.scale(pygame.image.load("assets/PG4.jpg"), (WIDTH, HEIGHT))
PG5 = pygame.transform.scale(pygame.image.load("assets/PG5.jpg"), (WIDTH, HEIGHT))


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        pygame.init()

        G_WIDTH, G_HEIGHT = 1280, 720
        win = pygame.display.set_mode((G_WIDTH, G_HEIGHT))
        pygame.display.set_caption("Gravitational Slingshot Effect")

        PLANET_MASS = 100
        SHIP_MASS = 5
        G = 5
        FPS = 60
        PLANET_SIZE = 50
        OBJ_SIZE = 5
        VEL_SCALE = 100

        GMG = pygame.transform.scale(pygame.image.load("assets/background.jpg"), (G_WIDTH, G_HEIGHT))
        PLANET = pygame.transform.scale(pygame.image.load("assets/jupiter.png"), (PLANET_SIZE * 2, PLANET_SIZE * 2))

        WHITE = (255, 255, 255)
        RED = (255, 0, 0)

        class Planet:
            def __init__(self, x, y, mass):
                self.x = x
                self.y = y
                self.mass = mass

            def draw(self):
                win.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))

        class Spacecraft:
            def __init__(self, x, y, vel_x, vel_y, mass):
                self.x = x
                self.y = y
                self.vel_x = vel_x
                self.vel_y = vel_y
                self.mass = mass

            def move(self, planet=None):
                distance = math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)
                force = (G * self.mass * planet.mass) / distance ** 2

                acceleration = force / self.mass
                angle = math.atan2(planet.y - self.y, planet.x - self.x)

                acceleration_x = acceleration * math.cos(angle)
                acceleration_y = acceleration * math.sin(angle)

                self.vel_x += acceleration_x
                self.vel_y += acceleration_y

                self.x += self.vel_x
                self.y += self.vel_y

            def draw(self):
                pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)

        def create_ship(location, mouse):
            t_x, t_y = location
            m_x, m_y = mouse
            vel_x = (m_x - t_x) / VEL_SCALE
            vel_y = (m_y - t_y) / VEL_SCALE
            obj = Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)
            return obj

        def main():
            running = True
            clock = pygame.time.Clock()

            planet = Planet(G_WIDTH // 2, G_HEIGHT // 2, PLANET_MASS)
            objects = []
            temp_obj_pos = None

            while running:
                clock.tick(FPS)

                mouse_pos = pygame.mouse.get_pos()
                for EVENT in pygame.event.get():
                    if EVENT.type == pygame.QUIT:
                        running = False

                    if EVENT.type == pygame.MOUSEBUTTONDOWN:
                        if temp_obj_pos:
                            obj = create_ship(temp_obj_pos, mouse_pos)
                            objects.append(obj)
                            temp_obj_pos = None
                        else:
                            temp_obj_pos = mouse_pos

                win.blit(GMG, (0, 0))

                if temp_obj_pos:
                    pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
                    pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)

                for obj in objects[:]:
                    obj.draw()
                    obj.move(planet)
                    off_screen = obj.x < 0 or obj.x > G_WIDTH or obj.y < 0 or obj.y > G_HEIGHT
                    collided = math.sqrt((obj.x - planet.x) ** 2 + (obj.y - planet.y) ** 2) <= PLANET_SIZE
                    if off_screen or collided:
                        objects.remove(obj)

                planet.draw()

                pygame.display.update()

            pygame.quit()

        if __name__ == "__main__":
            main()

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("WHITE")

        OPTIONS_TEXT = get_font(45).render("THEORY", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_PG1 = Button(image=None, pos=(1105, 680),
                             text_input="Page1", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK = Button(image=None, pos=(180, 680),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_PG1.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_PG1.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_PG1.checkForInput(OPTIONS_MOUSE_POS):
                    slide_1()

        pygame.display.update()


def slide_1():
    while True:
        SCREEN.blit(PG1, (0, 0))

        S1_MOUSE_POS = pygame.mouse.get_pos()

        S1_NEXT = Button(image=None, pos=(1105, 680),
                         text_input="Page2", font=get_font(75), base_color="Black", hovering_color="Green")

        S1_BACK = Button(image=None, pos=(180, 680),
                         text_input="Back", font=get_font(75), base_color="Black", hovering_color="Green")

        S1_BACK.changeColor(S1_MOUSE_POS)
        S1_BACK.update(SCREEN)
        S1_NEXT.changeColor(S1_MOUSE_POS)
        S1_NEXT.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if S1_BACK.checkForInput(S1_MOUSE_POS):
                    options()
                if S1_NEXT.checkForInput(S1_MOUSE_POS):
                    slide_2()

        pygame.display.update()


def slide_2():
    while True:
        SCREEN.blit(PG2, (0, 0))

        S2_MOUSE_POS = pygame.mouse.get_pos()

        S2_NEXT = Button(image=None, pos=(1105, 680),
                         text_input="Page3", font=get_font(75), base_color="Black", hovering_color="Green")

        S2_BACK = Button(image=None, pos=(180, 680),
                         text_input="Page1", font=get_font(75), base_color="Black", hovering_color="Green")

        S2_BACK.changeColor(S2_MOUSE_POS)
        S2_BACK.update(SCREEN)
        S2_NEXT.changeColor(S2_MOUSE_POS)
        S2_NEXT.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if S2_BACK.checkForInput(S2_MOUSE_POS):
                    slide_1()
                if S2_NEXT.checkForInput(S2_MOUSE_POS):
                    slide_3()

        pygame.display.update()


def slide_3():
    while True:
        SCREEN.blit(PG3, (0, 0))

        S3_MOUSE_POS = pygame.mouse.get_pos()

        S3_NEXT = Button(image=None, pos=(1105, 680),
                         text_input="Page4", font=get_font(75), base_color="Black", hovering_color="Green")

        S3_BACK = Button(image=None, pos=(180, 680),
                         text_input="Page2", font=get_font(75), base_color="Black", hovering_color="Green")

        S3_BACK.changeColor(S3_MOUSE_POS)
        S3_BACK.update(SCREEN)
        S3_NEXT.changeColor(S3_MOUSE_POS)
        S3_NEXT.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if S3_BACK.checkForInput(S3_MOUSE_POS):
                    slide_2()
                if S3_NEXT.checkForInput(S3_MOUSE_POS):
                    slide_4()

        pygame.display.update()


def slide_4():
    while True:
        SCREEN.blit(PG4, (0, 0))

        S4_MOUSE_POS = pygame.mouse.get_pos()

        S4_NEXT = Button(image=None, pos=(1105, 680),
                         text_input="Page5", font=get_font(75), base_color="Black", hovering_color="Green")

        S4_BACK = Button(image=None, pos=(180, 680),
                         text_input="Page3", font=get_font(75), base_color="Black", hovering_color="Green")

        S4_BACK.changeColor(S4_MOUSE_POS)
        S4_BACK.update(SCREEN)
        S4_NEXT.changeColor(S4_MOUSE_POS)
        S4_NEXT.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if S4_BACK.checkForInput(S4_MOUSE_POS):
                    slide_3()
                if S4_NEXT.checkForInput(S4_MOUSE_POS):
                    slide_5()

        pygame.display.update()


def slide_5():
    while True:
        SCREEN.blit(PG5, (0, 0))

        S5_MOUSE_POS = pygame.mouse.get_pos()

        S5_NEXT = Button(image=None, pos=(1000, 680),
                         text_input="Visualisation", font=get_font(40), base_color="Black", hovering_color="Green")

        S5_BACK = Button(image=None, pos=(180, 680),
                         text_input="Page4", font=get_font(75), base_color="Black", hovering_color="Green")

        S5_BACK.changeColor(S5_MOUSE_POS)
        S5_BACK.update(SCREEN)
        S5_NEXT.changeColor(S5_MOUSE_POS)
        S5_NEXT.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if S5_BACK.checkForInput(S5_MOUSE_POS):
                    slide_4()
                if S5_NEXT.checkForInput(S5_MOUSE_POS):
                    play()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(76).render("Slingshot Effect", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=None, pos=(640, 250),
                             text_input="Visualisation", font=get_font(75), base_color="#d7fcd4",
                             hovering_color="White")
        OPTIONS_BUTTON = Button(image=None, pos=(640, 400),
                                text_input="Theory", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
