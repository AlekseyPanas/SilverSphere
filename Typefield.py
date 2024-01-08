import pygame
import Constants


class Field:
    def __init__(self, pos, length, font, image, allowed_symbols=None, hidden=False, disallowed_symbols=None,
                 color=(0, 0, 0), field_id="", player_id=-1):
        # Draw pos of field
        self.pos = pos
        # Is the type field selected
        self.selected = False
        # The text in the type field
        self.text = ""
        # A surface that will contain the rendered text
        self.rendered_text = None
        # The position where the cursor is
        self.cursor_index = -1
        self.cursor_pos = 0
        # Counter used for the cursor blinking
        self.blink_count = 0
        # Position of text
        self.text_pos = 10
        # image
        self.image = image
        # font
        self.font = font
        # dimensions of the type field
        self.length = length
        self.height = self.font.get_height() + (self.font.get_height() / 2)

        # The surface that everything will be blitted on
        self.surface = pygame.Surface((length, self.height), pygame.SRCALPHA, 32)
        self.text_surface = pygame.Surface((length - 6, self.height), pygame.SRCALPHA, 32)
        # Glass type field image
        self.image = pygame.transform.smoothscale(self.image, (int(length), int(self.height)))

        # Used to adjust cursor for the decimal
        self.decimal_adjust = False

        # All allowed symbols
        self.allowed_symbols = allowed_symbols
        self.disallowed_symbols = disallowed_symbols
        # Shows stars instead of text
        self.hidden = hidden

        self.text_color = color

        # Used to identify the typefield
        self.field_id = field_id
        self.player_id = player_id

    def draw_handler(self, screen):
        if self.selected:
            self.blink_count += 1

        self.surface.fill((255, 255, 255, 0))
        self.text_surface.fill((255, 255, 255, 0))

        # Draws text
        if not self.hidden:
            self.rendered_text = self.font.render(self.text, True, self.text_color)
        else:
            self.rendered_text = self.font.render("".join(["*" for char in range(len(self.text))]), True, self.text_color)
        self.text_surface.blit(self.rendered_text, (self.text_pos, self.height / 2 - self.rendered_text.get_height() / 2))
        self.surface.blit(self.text_surface, (3, 0))

        # Finds cursor position based on index
        text = "".join(["*" for char in range(len(self.text))]) if self.hidden else self.text
        self.cursor_pos = self.font.render(text[:self.cursor_index + 1], True, (0, 0, 0)).get_width()

        # Draws glass typing field image
        self.surface.blit(self.image, (0, 0))

        # Draws cursor
        if self.blink_count % 40 < 20 and self.selected:
            pygame.draw.line(self.surface, (200, 0, 0), ((self.text_pos - 1) + self.cursor_pos + ((2 / 900) * Constants.SCREEN_SIZE[0]), (1 / 6) * self.height),
                             ((self.text_pos - 1) + self.cursor_pos + ((2 / 900) * Constants.SCREEN_SIZE[0]), self.height - (1 / 6) * self.height), 2)

        # Determines if a shift of text is needed
        if (self.text_pos - 1) + self.cursor_pos < 0:
            self.text_pos += (0 - ((self.text_pos - 1) + self.cursor_pos)) + 10
        elif (self.text_pos - 1) + self.cursor_pos > self.length:
            self.text_pos += (self.length - ((self.text_pos - 1) + self.cursor_pos)) - 10

        screen.blit(self.surface, self.pos)

    def clear_field(self):
        self.text = ""
        self.cursor_index = -1

    def event_handler(self, event):
        # Checks to see if the box was clicked which causes it to become selected
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pos[0] < event.pos[0] < self.pos[0] + self.length and self.pos[1] < event.pos[1] < self.pos[1] + self.height:
                self.selected = True
            else:
                self.selected = False
        # Key presses
        elif self.selected and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_index > -1:
                    self.text = self.text[:self.cursor_index] + self.text[self.cursor_index + 1:]
                    # Shifts cursor left
                    self.cursor_index -= 1

            elif event.key == pygame.K_ESCAPE:
                self.clear_field()

            # Checks if arrows were pressed and shifts cursor accordingly
            elif event.key == pygame.K_LEFT and self.cursor_index > -1:
                self.cursor_index -= 1
            elif event.key == pygame.K_RIGHT and self.cursor_index < len(self.text) - 1:
                self.cursor_index += 1

            elif len(event.unicode) > 0 and not event.key == pygame.K_TAB:
                valid = True
                if self.allowed_symbols is not None:
                    if event.unicode not in self.allowed_symbols:
                        valid = False
                if self.disallowed_symbols is not None:
                    if event.unicode in self.disallowed_symbols:
                        valid = False

                if valid:
                    self.text = self.text[:self.cursor_index + 1] + event.unicode + self.text[self.cursor_index + 1:]
                    # Shifts cursor to right
                    self.cursor_index += 1
