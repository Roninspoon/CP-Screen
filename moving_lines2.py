import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions (adjust as needed)
WIDTH = 480  # Example
HEIGHT = 320 # Example
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Lines and Blinking Rectangle")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# --- Line Class ---
class Line:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.speed = 5
        self.direction = 1
        self.target_x = 0
        self.target_y = 0
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
        pygame.draw.line(screen, self.color, (self.x1, self.y1), (self.x2, self.y2), 2)

# --- Create Lines ---
line1 = Line(0, 0, WIDTH - 1, 0, WHITE)
line1.target_y = random.randint(int(HEIGHT * 0.15), int(HEIGHT * 0.85))

line2 = Line(0, 0, WIDTH - 1, 0, GREEN)
line2.start_delay = random.uniform(0, 2)

line3 = Line(0, 0, 0, HEIGHT - 1, BLUE)
line3.target_x = random.randint(int(WIDTH * 0.15), int(WIDTH * 0.85))

line4 = Line(0, 0, 0, HEIGHT - 1, YELLOW)
line4.start_delay = random.uniform(0, 2)

lines = [line1, line2, line3, line4]
lines_stopped = False
start_time = pygame.time.get_ticks()

# Blinking Rectangle Variables
blinking = False
blink_start_time = 0
blink_duration = 0
blink_interval = 0.5  # Seconds between blink on/off
last_blink_toggle = 0
rectangle_visible = False
rectangle_rect = pygame.Rect(0, 0, 0, 0) # Initialize

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000

    # Clear the screen
    screen.fill(BLACK)

    # --- Update and Draw Lines ---
    all_stopped = True
    for i, line_obj in enumerate(lines):
        if i == 1 and elapsed_time <= line_obj.start_delay:
            continue
        if i == 3 and elapsed_time <= line_obj.start_delay:
            continue

        line_obj.move()
        line_obj.draw(screen)
        if not line_obj.stopped:
            all_stopped = False
        elif i == 1 and not line2.target_y:
            line2.target_y = line1.target_y + random.randint(-int(HEIGHT * 0.05), int(HEIGHT * 0.05))
            line2.target_y = max(int(HEIGHT * 0.15), min(int(HEIGHT * 0.85), line2.target_y))
        elif i == 3 and not line4.target_x:
            line4.target_x = line3.target_x + random.randint(-int(WIDTH * 0.05), int(WIDTH * 0.05))
            line4.target_x = max(int(WIDTH * 0.15), min(int(WIDTH * 0.85), line4.target_x))

    # --- Check if all lines have stopped and initiate blinking ---
    if all_stopped and not blinking and elapsed_time > max(line2.start_delay, line4.start_delay):
        blinking = True
        blink_start_time = current_time
        blink_duration = random.uniform(2, 15)
        last_blink_toggle = current_time
        rectangle_visible = True

        # Calculate rectangle coordinates
        min_x = min(line3.x1, line4.x1)
        max_x = max(line3.x1, line4.x1)
        min_y = min(line1.y1, line2.y1)
        max_y = max(line1.y1, line2.y1)
        rectangle_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    # --- Handle Blinking ---
    if blinking:
        blink_elapsed = (current_time - blink_start_time) / 1000
        if blink_elapsed < blink_duration:
            if (current_time - last_blink_toggle) / 1000 >= blink_interval:
                rectangle_visible = not rectangle_visible
                last_blink_toggle = current_time

            if rectangle_visible:
                pygame.draw.rect(screen, RED, rectangle_rect)
        else:
            blinking = False

    # Update the display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)

pygame.quit()