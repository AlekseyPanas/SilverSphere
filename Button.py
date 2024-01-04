import pygame


class Button:
    def __init__(self, top_left_corner, size, image, box=False, border_color=(0, 0, 0), text_color=(40, 40, 40),
                 fill_color=(255, 255, 255), text="", border_thickness=0, font=None, state_quantity=3):
        # Position of top left corner of button.
        self.top_left = top_left_corner

        # Width/height of image and the loaded image.
        self.size = size
        self.image = None
        if image is not None:
            self.image = pygame.transform.smoothscale(image, (size[0], size[1] * state_quantity))

        # Image contains 2 states of the button. These 2 surfaces will hold each state.
        self.static = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        self.hover = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        self.pressed = pygame.Surface(self.size, pygame.SRCALPHA, 32)

        self.border_color = border_color
        self.fill_color = fill_color
        self.border_thickness = border_thickness

        self.font = font
        self.text = text
        self.text_color = text_color

        if not box:
            self.static.blit(self.image, (0, 0))
            self.hover.blit(self.image, (0, -self.size[1]))
            self.pressed.blit(self.image, (0, -2 * self.size[1]))
        else:
            self.set_colors(fill_color, border_color)

        self.button_rect = self.static.get_rect()
        self.button_rect.center = top_left_corner[0] + size[0] / 2, top_left_corner[1] + size[1] / 2

        self.button_state = "static"

    def set_colors(self, fill_color=None, border_color=None):
        if fill_color is not None:
            self.fill_color = fill_color
        if border_color is not None:
            self.border_color = border_color

        self.static.fill(self.border_color)
        pygame.draw.rect(self.static, self.fill_color, (self.border_thickness, self.border_thickness,
                                                        self.size[0] - 2 * self.border_thickness,
                                                        self.size[1] - 2 * self.border_thickness))
        if self.font is not None:
            rendered_text = self.font.render(self.text, True, self.text_color)
            rect = rendered_text.get_rect()
            rect.center = (self.size[0] / 2, self.size[1] / 2)
            self.static.blit(rendered_text, rect)

        self.hover.blit(self.static, (0, 0))

    def draw(self, screen):
        if self.button_state == "pressed":
            screen.blit(self.pressed, self.top_left)
        else:
            screen.blit(self.hover if self.button_state == "hover" else self.static, self.top_left)

    def is_hover(self, pos):
        if not self.button_state == "pressed":
            self.button_state = "hover" if pygame.Rect(self.top_left, self.size).collidepoint(pos) else "static"

    def draw_and_hover(self, screen, pos):
        self.draw(screen)
        self.is_hover(pos)

    def is_clicked(self, pos):
        return pygame.Rect(self.top_left, self.size).collidepoint(pos)
