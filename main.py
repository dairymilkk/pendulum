import pygame
import math
from random import randint
import settings
from scipy.integrate import odeint
import numpy as np


def run():
    class pendulum_arm(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.time_plot = np.linspace(0, 20, 240)
            self.time = 0
            global x_pos, y_pos
            x_pos = 250
            y_pos = 270

        def calculations(self):
            global velocity, kinetic_energy, potential_energy
            self.time += 1/60

            self.amplitude = settings.start_amplitude * \
                math.e**(-self.time * settings.air_resistance)

            self.angular_velocity = math.sqrt(settings.gravity/settings.length)
            self.angular_displacement = self.amplitude * \
                math.cos(self.angular_velocity * self.time)

            velocity = self.angular_velocity * \
                (math.sqrt((self.amplitude**2 - self.angular_displacement**2)))
            kinetic_energy = (0.5*settings.mass)*(velocity**2)
            potential_energy = (settings.mass * settings.gravity *
                                (settings.length*(1 - math.cos(self.angular_displacement))))
            print(potential_energy + kinetic_energy)

        def draw(self):
            self.pendulum_render = pygame.draw.line(screen, (255, 255, 255), (250, 270), ((math.sin(
                self.angular_displacement)*settings.length*100 + (x_pos)), (math.cos(self.angular_displacement)*settings.length*100 + (y_pos))), width=1)

            self.image = self.pendulum_render

        def ticks(self):
            global positions
            positions = (math.sin(self.angular_displacement)*settings.length*100 +
                         (x_pos - 1), ((y_pos - 1) + settings.length*100*math.cos(self.angular_displacement)))

        def update(self):
            self.calculations()
            self.draw()
            self.ticks()

    class trace(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.coords_list = []

        def draw(self):
            for i in range(1, len(self.coords_list)):
                self.draw_line = pygame.draw.line(
                    screen, (randint(10, 250), randint(10, 250), randint(10, 250)), self.coords_list[i-1], self.coords_list[i])

        def tick(self):
            if len(self.coords_list) < 20:
                self.coords_list.append(positions)
            else:
                self.coords_list.remove(
                    self.coords_list[0])
                self.coords_list.append(positions)

        def update(self):
            self.tick()
            self.draw()

    class text_numbers(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.font = pygame.font.SysFont(None, 25)

        def draw(self):
            self.velocity_text = self.font.render(
                f'Velocity: {round(velocity,2)}', False, (255, 255, 255))
            self.velocity_text_rect = self.velocity_text.get_rect(
                center=(250, 100))
            self.kinetic_energy_text = self.font.render(
                f'Kinetic Energy: {round(kinetic_energy,2)}', False, (255, 255, 255))
            self.kinetic_energy_text_rect = self.kinetic_energy_text.get_rect(
                center=(250, 150))
            self.potential_energy_text = self.font.render(
                f'Potential Energy: {round(potential_energy,2)}', False, (255, 255, 255))
            self.potential_energy_text_rect = self.potential_energy_text.get_rect(
                center=(250, 200))
            screen.blit(self.velocity_text, self.velocity_text_rect)
            screen.blit(self.kinetic_energy_text,
                        self.kinetic_energy_text_rect)
            screen.blit(self.potential_energy_text,
                        self.potential_energy_text_rect)

            self.length_option = self.font.render(
                f'Length: ', False, (255, 255, 255))
            self.length_option_rect = self.length_option.get_rect(
                center=(218, 450))
            screen.blit(self.length_option, self.length_option_rect)

            self.gravity_option = self.font.render(
                f'Gravity: ', False, (255, 255, 255))
            self.gravity_option_rect = self.gravity_option.get_rect(
                center=(218, 480))
            screen.blit(self.gravity_option, self.gravity_option_rect)

            self.amplitude_option = self.font.render(
                f'Amplitude: ', False, (255, 255, 255))
            self.amplitude_option_rect = self.amplitude_option.get_rect(
                center=(206, 510))
            screen.blit(self.amplitude_option, self.amplitude_option_rect)

            self.amplitude_option = self.font.render(
                f'Air Resistance: ', False, (255, 255, 255))
            self.amplitude_option_rect = self.amplitude_option.get_rect(
                center=(190, 540))
            screen.blit(self.amplitude_option, self.amplitude_option_rect)

        def update(self):
            self.draw()

    class interaction_renders(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.speed_options = [0.25, 0.5, 1, 2]
            self.font = pygame.font.SysFont(None, 20)
            self.speed_colour_one = True
            self.length_increase_colour_one = True
            self.length_decrease_colour_one = True
            self.clicked = True
            self.multiplier = 2

        def tick(self):
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_pressed = pygame.mouse.get_pressed()

        def sim_speed(self):
            global simulation_speed
            simulation_speed = self.speed_options[int(self.multiplier)] * 60

        def speed_change_draw(self):
            if self.speed_colour_one:
                self.speed_button = pygame.draw.rect(
                    screen, (0, 0, 0), [20, 20, 30, 30])
                self.speed_button_text = self.font.render(
                    f'{self.speed_options[int(self.multiplier)]}x', False, (255, 255, 255))
                self.speed_button_text_rect = self.speed_button_text.get_rect(
                    center=(35, 35))
                screen.blit(self.speed_button_text,
                            self.speed_button_text_rect)
            else:
                self.speed_button = pygame.draw.rect(
                    screen, (255, 255, 255), [20, 20, 30, 30])
                self.speed_button_text = self.font.render(
                    f'{self.speed_options[int(self.multiplier)]}x', False, (0, 0, 0))
                self.speed_button_text_rect = self.speed_button_text.get_rect(
                    center=(35, 35))
                screen.blit(self.speed_button_text,
                            self.speed_button_text_rect)

        def speed_change_user_input(self):
            if self.speed_button.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                self.speed_colour_one = False
            else:
                self.speed_colour_one = True
            if self.mouse_pressed[0] == 1 and self.speed_button.collidepoint(self.mouse_pos[0], self.mouse_pos[1]) and self.clicked:
                if self.speed_options[int(self.multiplier)] == 2:
                    self.multiplier = 0
                    self.clicked = False
                else:
                    self.multiplier += 1
                    self.clicked = False
            if self.mouse_pressed[0] == 0:
                self.clicked = True

        def constants_user_input(self):
            if self.length_increase.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                self.length_increase_colour_one = False
            else:
                self.length_increase_colour_one = True

            if self.length_decrease.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                self.length_decrease_colour_one = False
            else:
                self.length_decrease_colour_one = True

            if self.mouse_pressed[0] == 1 and self.length_increase.collidepoint(self.mouse_pos[0], self.mouse_pos[1]) and self.clicked:
                self.clicked = False
                if settings.length == 1.5:
                    settings.length += 0
                else:
                    settings.length = ((settings.length * 10) + 1) / 10
            if self.mouse_pressed[0] == 0:
                self.clicked = True

            if self.mouse_pressed[0] == 1 and self.length_decrease.collidepoint(self.mouse_pos[0], self.mouse_pos[1]) and self.clicked:
                self.clicked = False
                if settings.length == 0.2:
                    settings.length += 0
                else:
                    settings.length = ((settings.length * 10) - 1) / 10
            if self.mouse_pressed[0] == 0:
                self.clicked = True

        def constants_draw(self):
            if self.length_increase_colour_one:
                self.length_increase = pygame.draw.rect(
                    screen, (0, 0, 0), [310, 442.5, 15, 15])
                self.length_text = self.font.render(
                    f'{(settings.length)}', False, (255, 255, 255))
                self.length_text_rect = self.length_text.get_rect(
                    center=(286, 450))
                screen.blit(self.length_text, self.length_text_rect)
                self.legnth_increase_arrow_1 = pygame.draw.line(
                    screen, (255, 255, 255), (315, 444), (320, 449))
                self.legnth_increase_arrow_2 = pygame.draw.line(
                    screen, (255, 255, 255), (320, 449), (315, 454))
            else:
                self.length_increase = pygame.draw.rect(
                    screen, (255, 255, 255), [310, 442.5, 15, 15])
                self.length_text = self.font.render(
                    f'{settings.length}', False, (255, 255, 255))
                self.length_text_rect = self.length_text.get_rect(
                    center=(286, 450))
                screen.blit(self.length_text, self.length_text_rect)
                self.legnth_increase_arrow_1 = pygame.draw.line(
                    screen, (0, 0, 0), (315, 444), (320, 449))
                self.legnth_increase_arrow_2 = pygame.draw.line(
                    screen, (0, 0, 0), (320, 449), (315, 454))

            if self.length_decrease_colour_one:
                self.length_decrease = pygame.draw.rect(
                    screen, (0, 0, 0), [250, 442.5, 15, 15])
                self.legnth_decrease_arrow_1 = pygame.draw.line(
                    screen, (255, 255, 255), (259, 444), (254, 449))
                self.legnth_decrease_arrow_2 = pygame.draw.line(
                    screen, (255, 255, 255), (254, 449), (259, 454))
            else:
                self.length_decrease = pygame.draw.rect(
                    screen, (255, 255, 255), [250, 442.5, 15, 15])
                self.legnth_decrease_arrow_1 = pygame.draw.line(
                    screen, (0, 0, 0), (259, 444), (254, 449))
                self.legnth_decrease_arrow_2 = pygame.draw.line(
                    screen, (0, 0, 0), (254, 449), (259, 454))

            self.gravity_increase = pygame.draw.rect(
                screen, (255, 255, 255), [310, 472.5, 15, 15])
            self.gravity_decrease = pygame.draw.rect(
                screen, (255, 255, 255), [250, 472.5, 15, 15])
            self.gravity_text = self.font.render(
                f'{settings.gravity}', False, (255, 255, 255))
            self.gravity_text_rect = self.gravity_text.get_rect(
                center=(287, 480))
            screen.blit(self.gravity_text, self.gravity_text_rect)

            self.start_amplitude_increase = pygame.draw.rect(
                screen, (255, 255, 255), [310, 502.5, 15, 15])
            self.start_amplitude_decrease = pygame.draw.rect(
                screen, (255, 255, 255), [250, 502.5, 15, 15])
            self.start_amplitude_text = self.font.render(
                f'{settings.start_amplitude}', False, (255, 255, 255))
            self.start_amplitude_text_rect = self.gravity_text.get_rect(
                center=(289, 510))
            screen.blit(self.start_amplitude_text,
                        self.start_amplitude_text_rect)

            self.air_resistance_increase = pygame.draw.rect(
                screen, (255, 255, 255), [310, 532.5, 15, 15])
            self.start_amplitude_decrease = pygame.draw.rect(
                screen, (255, 255, 255), [250, 532.5, 15, 15])
            self.air_resistance_text = self.font.render(
                f'{settings.air_resistance}', False, (255, 255, 255))
            self.air_resistance_text_rect = self.gravity_text.get_rect(
                center=(295, 540))
            screen.blit(self.air_resistance_text,
                        self.air_resistance_text_rect)

        def update(self):
            self.tick()
            self.constants_draw()
            self.constants_user_input()
            self.speed_change_draw()
            self.speed_change_user_input()
            self.sim_speed()

    pygame.init()
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption("pendulum")
    clock = pygame.time.Clock()

    pendulum = pygame.sprite.GroupSingle()
    pendulum.add(pendulum_arm())

    trail = pygame.sprite.GroupSingle()
    trail.add(trace())

    text = pygame.sprite.GroupSingle()
    text.add(text_numbers())

    interactions = pygame.sprite.GroupSingle()
    interactions.add(interaction_renders())

    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False

        screen.fill((0, 0, 0))

        pendulum.update()
        # trail.update()
        text.update()
        interactions.update()

        pygame.display.update()
        clock.tick(simulation_speed)


run()
