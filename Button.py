import pygame
from pygame.rect import Rect

class Button:
    def __init__(self, center, image, desired_size, outline=(0, 0, 0), fill=(0, 0, 0), text='text',
                 textsize=20, textcolor=(255,255,255)):
        self.center = center
        self.desired_size = desired_size
        # sets the images and resizes it right away to desired size (unless 'rect' is passed)
        if image != 'rect':
            self.image = pygame.transform.scale(image, self.desired_size)
        else:
            self.image = image

        # If the button is manually customized. Must pass 'rect' as image parameter to use this
        self.outline = outline
        self.fill = fill
        self.font = pygame.font.SysFont('Comic Sans MS', textsize)
        self.text = self.font.render(text, False, textcolor)

    def draw(self,screen):
        if self.image == 'rect':
            # Outline for button
            pygame.draw.rect(screen, self.outline, Rect(
                (self.center[0] - (self.desired_size[0] / 2) - 5, self.center[1] - (self.desired_size[1] / 2) - 5),
                (self.desired_size[0] + 10, self.desired_size[1] + 10)))
            # Fill color for button
            pygame.draw.rect(screen, self.fill, Rect(
                (self.center[0] - (self.desired_size[0] / 2), self.center[1] - (self.desired_size[1] / 2)),
                (self.desired_size[0], self.desired_size[1])))
            # Draw text on button
            screen.blit(self.text, (
                (self.center[0] - (self.desired_size[0] / 2)) + 5, (self.center[1] + (self.desired_size[1] / 2)) - 30))
        else:
            # draws image
            screen.blit(self.image,
                        (self.center[0] - (self.desired_size[0] / 2), self.center[1] - (self.desired_size[1] / 2)))

    def click(self, pos):
        # Detects if this button was clicked and returns true
        if pos[0] >= self.center[0] - (self.desired_size[0] / 2) and pos[0] <= self.center[0] + (
                self.desired_size[0] / 2) and pos[1] >= self.center[1] - (self.desired_size[1] / 2) and pos[1] <= \
                self.center[1] + (self.desired_size[1] / 2):
            return True