import random
import sys
import pygame

# Initialize Pygame
pygame.init()

# LÖVE2D defaults to an 800x600 window unless configured otherwise
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Beachball Drop")
clock = pygame.time.Clock()
pygame.event.set_grab(True)

# Load images (using convert_alpha() to preserve transparency)
beachball_img = pygame.image.load("BeachBallSmall.png").convert_alpha()
drink_img = pygame.image.load("DrinkSmall.png").convert_alpha()
background_img = pygame.image.load("Background_Drop.png").convert()

ball_w, ball_h = beachball_img.get_size()
drink_w, drink_h = drink_img.get_size()

# Font setup for score (approximating LÖVE's 2x scaled default text)
font = pygame.font.SysFont("arial", 28, bold=True)

# Initialize 5 beachball positions
startx = [random.randint(0, SCREEN_WIDTH - ball_w) for _ in range(5)]
starty = [-random.randint(ball_h, ball_h * 2) for _ in range(5)]

# Game state variables
beach_balls_clicked = 0
normal_speed = 140
slow_speed = 100
current_speed = normal_speed

slow_timer = 0.0
slow_duration = 10.0

drink_active = True
drink_respawn_timer = 0.0
spawn_x = 0
spawn_y = 0


def spawn_drink():
  global spawn_x, spawn_y
  spawn_x = random.randint(0, SCREEN_WIDTH - drink_w)
  spawn_y = random.randint(0, SCREEN_HEIGHT - drink_h)


# Initial drink spawn
spawn_drink()

# Main Game Loop
running = True
while running:
  # Delta time (dt) in seconds, capped at 60 FPS
  dt = clock.tick(60) / 1000.0

  # -------------------------------------------------
  # EVENT HANDLING (Replaces love.mousepressed)
  # -------------------------------------------------
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.event.set_grab(False)
      running = False

    # Check for left mouse click (button 1)
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      if not pygame.event.get_grab():
        pygame.event.set_grab(True)
      mouse_x, mouse_y = event.pos

      # Check if any beachball was clicked
      for i in range(len(startx)):
        if (
            startx[i] <= mouse_x <= startx[i] + ball_w
            and starty[i] <= mouse_y <= starty[i] + ball_h
        ):
          # Reset X and Y positions above the top of the screen
          startx[i] = random.randint(0, SCREEN_WIDTH - ball_w)
          starty[i] = -random.randint(ball_h, ball_h * 2)
          beach_balls_clicked += 1

      # Check if the active drink was clicked
      if drink_active:
        if (
            spawn_x <= mouse_x <= spawn_x + drink_w
            and spawn_y <= mouse_y <= spawn_y + drink_h
        ):
          current_speed = slow_speed
          slow_timer = slow_duration
          drink_active = False
          drink_respawn_timer = 15.0

  # -------------------------------------------------
  # UPDATE LOGIC (Replaces love.update)
  # -------------------------------------------------
  # Handle slowdown timer countdown
  if slow_timer > 0:
    slow_timer -= dt
    if slow_timer <= 0:
      current_speed = normal_speed

  # Handle drink respawn countdown
  if not drink_active:
    drink_respawn_timer -= dt
    if drink_respawn_timer <= 0:
      spawn_drink()
      drink_active = True

  # Move beachballs and check for bottom collision
  for i in range(len(starty)):
    if starty[i] + ball_h >= SCREEN_HEIGHT:
      running = False  # Quit game when a ball hits the bottom
    starty[i] += current_speed * dt

  # Check win condition
  if beach_balls_clicked >= 100:
    running = False

  # -------------------------------------------------
  # DRAWING (Replaces love.draw)
  # -------------------------------------------------
  screen.blit(background_img, (0, 0))

  for i in range(len(startx)):
    screen.blit(beachball_img, (startx[i], starty[i]))

  if drink_active:
    screen.blit(drink_img, (spawn_x, spawn_y))

  # Render and draw score text
  score_surface = font.render(
      f"SCORE: {beach_balls_clicked}", True, (255, 255, 255)
  )
  screen.blit(score_surface, (20, 20))

  pygame.display.flip()

pygame.event.set_grab(False)
pygame.quit()
sys.exit()