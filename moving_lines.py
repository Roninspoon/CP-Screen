import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions (adjust as needed)
WIDTH = 480  # Example
HEIGHT = 320 # Example
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Lines")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# --- Line Class (to make code cleaner) ---
class Line:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.speed = 5
        self.direction = 1  # 1 for down/right, -1 for up/left
        self.target_x = 0  # For vertical lines
        self.target_y = 0  # For horizontal lines
        self.stopped = False
        self.start_delay = 0

    def move(self):
        if not self.stopped:
            if self.x1 == self.x2: # Vertical line
                self.x1 += self.speed * self.direction
                self.x2 = self.x1
                if abs(self.x1 - self.target_x) < self.speed:
                    self.x1 = self.target_x
                    self.x2 = self.target_x
                    self.stopped = True
            else: # Horizontal line
                self.y1 += self.speed * self.direction
                self.y2 = self.y1
                if abs(self.y1 - self.target_y) < self.speed:
                    self.y1 = self.target_y
                    self.y2 = self.target_y
                    self.stopped = True
            
            if self.x1 == self.x2: # Vertical line
                if self.x1 <= 0:
                    self.x1 = 0
                    self.x2 = 0
                    self.direction = 1
                elif self.x1 >= WIDTH - 1:
                    self.x1 = WIDTH - 1
                    self.x2 = WIDTH - 1
                    self.direction = -1
            else: # Horizontal line
                if self.y1 <= 0:
                    self.y1 = 0
                    self.y2 = 0
                    self.direction = 1
                elif self.y1 >= HEIGHT - 1:
                    self.y1 = HEIGHT - 1
                    self.y2 = HEIGHT - 1
                    self.direction = -1

    def draw(self, screen):
        pygame.draw.line(screen, self.color, (self.x1, self.y1), (self.x2, self.y2), 2)  # 2 is the line thickness


# --- Create Lines ---
line1 = Line(0, 0, WIDTH - 1, 0, GREEN)  # Horizontal
line1.target_y = random.randint(int(HEIGHT * 0.15), int(HEIGHT * 0.85))

line2 = Line(0, 0, WIDTH - 1, 0, GREEN)  # Horizontal
line2.start_delay = random.uniform(0, 2)

line3 = Line(0, 0, 0, HEIGHT - 1, YELLOW)  # Vertical
line3.target_x = random.randint(int(WIDTH * 0.15), int(WIDTH * 0.85))

line4 = Line(0, 0, 0, HEIGHT - 1, YELLOW)  # Vertical
line4.start_delay = random.uniform(0, 2)


start_time = pygame.time.get_ticks()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000  # Convert to seconds

    # Clear the screen
    screen.fill(BLACK)  # Black background

    # --- Update and Draw Lines ---
    line1.move()
    line1.draw(screen)

    if elapsed_time > line2.start_delay:
        line2.move()
        line2.draw(screen)
        if not line2.target_y: # Set target only once line1 has stopped
            line2.target_y = line1.target_y + random.randint(-int(HEIGHT * 0.05), int(HEIGHT * 0.05))
            line2.target_y = max(int(HEIGHT * 0.15), min(int(HEIGHT * 0.85), line2.target_y))


    line3.move()
    line3.draw(screen)

    if elapsed_time > line4.start_delay:
        line4.move()
        line4.draw(screen)
        if not line4.target_x: # Set target only once line3 has stopped
            line4.target_x = line3.target_x + random.randint(-int(WIDTH * 0.05), int(WIDTH * 0.05))
            line4.target_x = max(int(WIDTH * 0.15), min(int(WIDTH * 0.85), line4.target_x))


    # Update the display
    pygame.display.flip()

    # Control frame rate (adjust as needed)
    pygame.time.Clock().tick(60)  # Cap at 60 frames per second

pygame.quit()