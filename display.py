import pygame
from math import ceil
from time import time

# Initialize pygame
pygame.init()

# Initialize screen
window_size = (900, 500)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Sorting Algorithm Visualizer")

# Color palette
grey = (100, 100, 100)
green = (125, 240, 125)
white = (250, 250, 250)
red = (255, 50, 50)
black = (0, 0, 0)
blue = (50, 50, 255)

# Base font
base_font = pygame.font.SysFont("Arial", 24)


class InputBox:
    def __init__(self, name, color, rect):
        self.active = False
        self.name = name
        self.color = color
        self.rect = pygame.Rect(rect)

    def draw(self):
        label = base_font.render(self.name, True, self.color)
        screen.blit(
           label,
           (self.rect.x + (self.rect.w - label.get_width()) / 2,
            self.rect.y - 32)
        )
        pygame.draw.rect(screen, self.color, self.rect, 3)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() != (0, 0, 0):
            if self.rect.collidepoint(mouse_pos):
                self.active = True
            else:
                self.active = False


class TextBox(InputBox):
    def __init__(self, name, color, rect, text="100"):
        super().__init__(name, color, rect)
        self.text = text
        self.draw()     # Establish correct rect width for initial rendering

    def draw(self):
        super().draw()
        surface = base_font.render(self.text, True, self.color)
        screen.blit(surface, (self.rect.x + 10, self.rect.y + 10))
        self.rect.w = max(surface.get_width() + 20, 50)

    def update(self, e):
        super().update()
        if self.active and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if e.unicode.isdigit():
                    self.text += e.unicode


class SliderBox(InputBox):
    def __init__(self, name, color, rect):
        super().__init__(name, color, rect)
        self.start = self.rect.x + 6
        self.end = self.rect.x + self.rect.w - 6
        self.value = self.start

    def draw(self):
        super().draw()
        pygame.draw.line(
            screen,
            self.color,
            (self.start, self.rect.y + 25),
            (self.end, self.rect.y + 25),
            2
        )
        pygame.draw.line(
            screen,
            self.color,
            (self.value, self.rect.y + 5),
            (self.value, self.rect.y + 45),
            12
        )

    def update(self):
        super().update()
        previous_start = self.start
        self.rect.x = size_box.rect.x + size_box.rect.w + 20
        self.start = self.rect.x + 6
        self.end = self.rect.x + self.rect.w - 6
        self.value += self.start - previous_start
        if self.active and pygame.mouse.get_pressed() != (0, 0, 0):
            x = pygame.mouse.get_pos()[0]
            if self.start <= x <= self.end:
                self.value = x


class ButtonBox:
    def __init__(self, true_state_img, false_state_img, rect):
        self.true_img = pygame.image.load(true_state_img)
        self.false_img = pygame.image.load(false_state_img)
        self.active = False
        self.rect = pygame.Rect(rect)

    def draw(self):
        self.rect.x = algorithm_box.rect.x + algorithm_box.rect.w + 20
        pos = (self.rect.x, self.rect.y)
        if self.active:
            screen.blit(self.true_img, pos)
        else:
            screen.blit(self.false_img, pos)

    def update(self):
        self.rect.x = algorithm_box.rect.x + algorithm_box.rect.w + 20
        if self.active:
            self.active = False
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() != (0, 0, 0) and self.rect.collidepoint(mouse_pos):
            self.active = not self.active


class DropdownBox:
    DEFAULT_OPTION = 0

    def __init__(self, name, color, rect):
        self.active = False
        self.name = name
        self.color = color
        self.rect = pygame.Rect(rect)
        self.options = []
        self.options_color = white
        self.active_option = -1

    def add_options(self, options):
        self.options = options
        dropdown_width = ceil((len(self.options) - 1) * self.rect.h / self.rect.y) * self.rect.w
        self.dropdown_rect = pygame.Rect(self.rect.x, 0, dropdown_width, self.rect.y)

    def get_active_option(self):
        return self.options[self.DEFAULT_OPTION]

    def draw(self):
        label = base_font.render(self.name, True, self.color)
        screen.blit(label, (self.rect.x + (self.rect.w - label.get_width()) / 2, self.rect.y - 32))
        pygame.draw.rect(screen, self.color, self.rect, 3)
        option_text = base_font.render(self.options[self.DEFAULT_OPTION], True, grey)
        screen.blit(option_text, option_text.get_rect(center=self.rect.center))

        if self.active:
            column = 0
            index = 0
            rect_start = self.rect.y - self.rect.h
            for i in range(self.DEFAULT_OPTION + 1, len(self.options)):
                rect = self.rect.copy()
                rect.y -= (index + 1) * self.rect.h
                if rect.y <= 0:
                    column += 1
                    index = 0
                    rect.y = rect_start
                index += 1
                rect.x = self.rect.x + column * self.rect.w

                option_color = black if i - 1 == self.active_option else grey
                pygame.draw.rect(screen, self.options_color, rect, 0)
                pygame.draw.rect(screen, self.color, rect, 3)
                option_text = base_font.render(self.options[i][:12], True, option_color)
                screen.blit(option_text, option_text.get_rect(center=rect.center))

    def update(self):
        self.rect.x = delay_box.rect.x + delay_box.rect.w + 20
        mouse_pos = pygame.mouse.get_pos()
        column = 0
        index = 0
        rect_start = self.rect.y - self.rect.h
        for i in range(len(self.options) - 1):
            rect = self.rect.copy()
            rect.y -= (index + 1) * self.rect.h
            if rect.y <= 0:
                column += 1
                index = 0
                rect.y = rect_start
            index += 1
            rect.x = self.rect.x + column * self.rect.w

            if rect.collidepoint(mouse_pos):
                self.active_option = i

        if pygame.mouse.get_pressed() != (0, 0, 0):
            if self.active and self.dropdown_rect.collidepoint(mouse_pos):
                # Swap
                self.options[self.DEFAULT_OPTION], self.options[self.active_option + 1] = self.options[self.active_option + 1], self.options[self.DEFAULT_OPTION]

                self.active_option = - 1
            self.active = self.rect.collidepoint(mouse_pos)
        if not self.active:
            self.active_option = - 1


size_box = TextBox("Size", grey, (30, 440, 50, 50), "100")
delay_box = SliderBox("Delay", grey, (105, 440, 112, 50))
algorithm_box = DropdownBox("Algorithm", grey, (242, 440, 200, 50))
start_button = ButtonBox(
    "images/play_button.png",
    "images/stop_button.png",
    (390, 435, 50, 50)
)

num_bars = 0
delay = 0
timer = 0
paused = False
to_draw = False


def draw_bars(numbers, red_bar_1, red_bar_2, blue_bar_1, blue_bar_2, green_rows={}):
    if num_bars != 0:
        bar_width = ceil(900 / num_bars)

    for num in range(num_bars):
        if num in (red_bar_1, red_bar_2):
            color = red
        elif num in (blue_bar_1, blue_bar_2):
            color = blue
        elif num in green_rows:
            color = green
        else:
            color = grey
        pygame.draw.rect(screen, color, (num * bar_width, 400 - numbers[num], bar_width, numbers[num]))


def draw_bottom_menu():
    size_box.draw()
    delay_box.draw()
    algorithm_box.draw()
    start_button.draw()


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


def draw_ui(numbers, red_bar_1, red_bar_2, blue_bar_1, blue_bar_2, **kwargs):
    screen.fill(white)
    draw_bars(numbers, red_bar_1, red_bar_2, blue_bar_1, blue_bar_2, **kwargs)

    if paused and (time() - timer) < 0.5:
        draw_rect_alpha(screen, (255, 255, 0, 127), [(850 / 2) + 10, 150 + 10, 10, 50])
        draw_rect_alpha(screen, (255, 255, 0, 127), [(850 / 2) + 40, 150 + 10, 10, 50])
    elif not paused and (time() - timer) < 0.5:
        x, y = (850 / 2), 150
        draw_polygon_alpha(screen, (150, 255, 150, 127), ((x + 10, y + 10), (x + 10, y + 50 + 10), (x + 50, y + 25 + 10))) 

    draw_bottom_menu()
    pygame.display.update()


def update_ui(event):
    size_box.update(event)
    delay_box.update()
    algorithm_box.update()
    start_button.update()


def draw_algorithm_step(numbers, red_bar_1, red_bar_2, blue_bar_1, blue_bar_2):
    global to_draw, timer, paused

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.rect.collidepoint(event.pos):
                to_draw = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = True
                timer = time()
    if to_draw:
        while paused:
            draw_ui(numbers, red_bar_1, red_bar_2, blue_bar_1, blue_bar_2)
            for event in pygame.event.get():
                delay_box.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        paused = False
                        timer = time()

        draw_ui(numbers, red_bar_1, red_bar_2, blue_bar_1, blue_bar_2)
        delay = delay_box.value - delay_box.rect.x - 6
        pygame.time.wait(delay)
