import board
import displayio
import adafruit_display_shapes.line as line
import time
import random

# Initialize display
display = board.DISPLAY

# Create a display group
group = displayio.Group()
display.show(group)

# Get display width and height
WIDTH = display.width
HEIGHT = display.height

# --- Line 1 (Horizontal) ---
LINE1_Y_START = 0
LINE1_Y_END = HEIGHT - 1
LINE1_X_START = 0
LINE1_X_END = WIDTH - 1
line1_obj = line.Line(LINE1_X_START, LINE1_Y_START, LINE1_X_END, LINE1_Y_START, 0xFFFFFF)  # White line
group.append(line1_obj)

# Line 1 variables
SPEED = 5
direction1 = 1
TARGET_Y_MIN = int(HEIGHT * 0.15)
TARGET_Y_MAX = int(HEIGHT * 0.85)
target_y1 = random.randint(TARGET_Y_MIN, TARGET_Y_MAX)
animation1_stopped = False

# --- Line 2 (Horizontal) ---
# ... (Same as before)

# --- Line 3 (Vertical) ---
LINE3_X_START = 0
LINE3_X_END = WIDTH - 1
LINE3_Y_START = 0
LINE3_Y_END = HEIGHT - 1
line3_obj = line.Line(LINE3_X_START, LINE3_Y_START, LINE3_X_END, LINE3_Y_END, 0x0000FF)  # Blue line
# Starts hidden
# group.append(line3_obj)

# Line 3 variables
direction3 = 1
target_x3 = 0
animation3_started = False
animation3_stopped = False
line3_start_delay = random.uniform(0, 2)

# --- Line 4 (Vertical) ---
LINE4_X_START = 0
LINE4_X_END = WIDTH - 1
LINE4_Y_START = 0
LINE4_Y_END = HEIGHT - 1
line4_obj = line.Line(LINE4_X_START, LINE4_Y_START, LINE4_X_END, LINE4_Y_END, 0xFFFF00) # Yellow
# Starts hidden
# group.append(line4_obj)

#Line 4 variables
direction4 = 1
target_x4 = 0
animation4_started = False
animation4_stopped = False
line4_start_delay = random.uniform(0,2)

start_time = time.monotonic()

# Main loop
while True:
    current_time = time.monotonic()
    elapsed_time = current_time - start_time

    # --- Line 1 & 2 (Horizontal) animations (same as before)
    # ...

    # --- Line 3 & 4 (Vertical) Animations ---
    if elapsed_time > line3_start_delay and not animation3_started:
        group.append(line3_obj)
        animation3_started = True

    if animation3_started and not animation3_stopped:
        line3_obj.x1 += SPEED * direction3
        line3_obj.x2 = line3_obj.x1

        if abs(line3_obj.x1 - target_x3) < SPEED:
            line3_obj.x1 = target_x3
            line3_obj.x2 = line3_obj.x1
            animation3_stopped = True

            target_x4 = target_x3 + random.randint(-int(WIDTH * 0.05), int(WIDTH * 0.05))
            target_x4 = max(int(WIDTH * 0.15), min(int(WIDTH * 0.85), target_x4))

        elif line3_obj.x1 <= 0:
            line3_obj.x1 = 0
            line3_obj.x2 = 0
            direction3 = 1
        elif line3_obj.x1 >= LINE3_X_END:
            line3_obj.x1 = LINE3_X_END
            line3_obj.x2 = LINE3_X_END
            direction3 = -1

    if elapsed_time > line4_start_delay and not animation4_started:
        group.append(line4_obj)
        animation4_started = True

    if animation4_started and not animation4_stopped:
        line4_obj.x1 += SPEED * direction4
        line4_obj.x2 = line4_obj.x1

        if abs(line4_obj.x1 - target_x4) < SPEED:
            line4_obj.x1 = target_x4
            line4_obj.x2 = line4_obj.x1
            animation4_stopped = True

        elif line4_obj.x1 <= 0:
            line4_obj.x1 = 0
            line4_obj.x2 = 0
            direction4 = 1
        elif line4_obj.x1 >= LINE4_X_END:
            line4_obj.x1 = LINE4_X_END
            line4_obj.x2 = LINE4_X_END
            direction4 = -1

    # Redraw the display
    group.update()

    # Control frame rate
    time.sleep(0.02)
