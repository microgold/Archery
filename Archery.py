import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Archery Game')

# Game variables
running = True
clock = pygame.time.Clock()
fps = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (227, 228, 221)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
LIGHTGRAY = (200, 200, 200)

# Target settings
target_x, target_y = width - 100, height // 2 + 50
target_radius = 50

# Bar settings
bar_width, bar_height = 200, 20
bar_x, bar_y = (width - bar_width) // 2, height - 50
button_width, button_height = 20, 20
button_x, button_y = bar_x, bar_y
button_speed = 5
button_direction = 1

# Archer settings
archer_x, archer_y = 100, height // 2
archer_img = pygame.image.load('Sprites/Archer.png')  # Load your sprite here
arrow_img = pygame.image.load('Sprites/Arrow.png')  # Load your arrow sprite here
arrow_speed = 10
arrow_fired = False
archer_width = 150

arrow_x, arrow_y = archer_x + archer_width, archer_y + 55

def draw_target():
    # Draw the target with multiple concentric circles
    target_radius = 50  # Outermost circle radius
    colors = [WHITE, BLACK, BLUE, RED, YELLOW]  # Colors from outer to inner

    for i, color in enumerate(colors):
        pygame.draw.circle(screen, color, (target_x, target_y), target_radius - i * 10)


def get_frames(image, frame_width, frame_height, num_frames):
    frames = []
    for i in range(num_frames):
        frame = image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames

def calculate_score(deviation):
    abs_deviation = abs(deviation)
    if abs_deviation <= target_radius * 0.2:  # Bullseye
        return 10
    elif abs_deviation <= target_radius * 0.4:
        return 5
    elif abs_deviation <= target_radius * 0.6:
        return 3
    elif abs_deviation <= target_radius:
        return 1
    else:
        return 0  # Missed the target
    
def get_mark_color(hit_deviation):
    # Function to determine the color of the mark based on the hit deviation
    if abs(hit_deviation) <= target_radius * 0.2:  # Bullseye (Yellow)
        return BLACK  # Black mark for visibility
    elif abs(hit_deviation) <= target_radius * 0.4:  # Red
        return LIGHTGRAY  # White or grey mark for visibility
    elif abs(hit_deviation) <= target_radius * 0.6:  # Blue
        return LIGHTGRAY  # Black mark should be visible on blue
    elif abs(hit_deviation) <= target_radius * 0.8:  # BLACK
        return LIGHTGRAY  # Black mark should be visible on blue
    else:  # Black or White ring
        return LIGHTGRAY  # White mark for visibility on blac

def reset_game():
    global arrow_fired, arrow_moving, arrow_embedded, arrow_missed, arrow_shooting, num_arrows, hit_positions, score, hit_x, hit_y
    arrow_fired = False
    arrow_moving = False
    arrow_embedded = False
    arrow_missed = False
    arrow_shooting = False  # Add a new flag for arrow shooting
    num_arrows = 10  # Number of arrows per game

    # track game over state
    game_over = False

    hit_positions = []
    score = 0
    hit_x = 0
    hit_y = 0

archer_strip_img = pygame.image.load('Sprites/ArcherStrip.png')  # Load your sprite strip here
frame_width, frame_height = archer_strip_img.get_width() // 5, archer_strip_img.get_height()
num_frames = 5

# Animation control
animation_speed = 5  # Adjust this value to control the speed of the animation
animation_counter = 0

# Get individual frames
archer_frames = get_frames(archer_strip_img, frame_width, frame_height, num_frames)
current_frame = 0

# Track arrow states
arrow_moving = False
arrow_embedded = False
arrow_missed = False
arrow_shooting = False  # Add a new flag for arrow shooting
num_arrows = 10  # Number of arrows per game

# track game over state
game_over = False

hit_positions = []
score = 0
hit_x = 0
hit_y = 0

while running:
    screen.fill(GRAY)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_y:
                game_over = False
                reset_game()
            if game_over and event.key == pygame.K_n:
                running = False
            if event.key == pygame.K_SPACE and not arrow_fired:
                arrow_fired = True
                arrow_shooting = True  # Start shooting
                arrow_moving = False  # New variable to track arrow movement
                arrow_embedded = False  # New variable to track arrow embedding
                current_frame = 0
                animation_counter = 0
                
               # Determine the hit position
                bar_center = bar_x + bar_width // 2
                bar_position_ratio = (button_x - bar_x) / bar_width
                hit_position_ratio = (2 * bar_position_ratio - 1)  # -1 (left) to 1 (right)

                # Calculate the hit position on the target
                hit_deviation = hit_position_ratio * target_radius # Distance from bullseye
                hit_x = target_x + hit_deviation
               # Adjust vertical offset based on proximity to bullseye
                max_offset = 5  # Maximum vertical offset
                abs_deviation = abs(hit_deviation)
                if abs_deviation <= target_radius * 0.4:
                    max_offset = 3  # Smaller offset for closer to bullseye
                vertical_offset = random.uniform(-max_offset, max_offset)
                hit_y = target_y + vertical_offset
                num_arrows -= 1  # Decrement the arrow count
        
    if game_over: continue # Skip the rest of the game loop if game is over

    # Update button position
    button_x += button_speed * button_direction
    if button_x < bar_x or button_x + button_width > bar_x + bar_width:
        button_direction *= -1
        
    # Collision detection
    distance_to_target = ((arrow_x - target_x)**2 + (arrow_y - target_y)**2)**0.5
    if distance_to_target <= target_radius and arrow_moving:
        arrow_moving = False
        arrow_embedded = True  # New variable to         

    # Update arrow position
    if arrow_fired:
        if current_frame < num_frames:
            if animation_counter >= animation_speed:
                archer_img = archer_frames[current_frame]
                current_frame += 1
                animation_counter = 0  # Reset counter after updating frame
            animation_counter += 1
        else:
            
            # Once animation is done, start moving the arrow
            if not arrow_moving:
                arrow_x, arrow_y = archer_x + archer_width, archer_y + 55 # Reset arrow position
                arrow_moving = True

            if arrow_moving:
                arrow_x += arrow_speed
                if arrow_x > width or (target_x - arrow_x <= target_radius):
                    arrow_fired = False
                    arrow_moving = False
                    if arrow_shooting:                       
                        # Add the hit position to the list and calculate score
                        mark_color = get_mark_color(hit_deviation)
                        hit_positions.append((hit_x, hit_y, mark_color))
                        score += calculate_score(hit_deviation)
                        arrow_shooting = False  # Stop shooting
                        
                         # Check for game over
                        if num_arrows <= 0:
                            game_over_text = font.render("Game Over", True, RED)
                            screen.blit(game_over_text, (width // 2 - 50, height // 2 - 20))    
                            game_over = True
                            
                            play_again_text = font.render("Play Again? (y/n)", True, GREEN)
                            screen.blit(play_again_text, (width // 2 - 50, height // 2 + 10))  # Adjust position as needed
                            
                    arrow_fired = False
                    arrow_moving = False
                    arrow_embedded = True  # Arrow is now embedded
                    
            # Arrow has hit the target
            if not arrow_embedded:
                arrow_embedded = True  # Flag to indicate arrow is embedded in the target
                    
    else:
        archer_img = archer_frames[0]  # Reset to default frame
        arrow_embedded = False

    # Draw the target
    draw_target()
    
    # Inside the game loop, after drawing the target
    for pos_x, pos_y, color in hit_positions:
        pygame.draw.circle(screen, color, (int(pos_x), int(pos_y)), 5)  # Small dot for the hit

    # Display the score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))  # Position the score text on the screen
    
    #Display the arrow count
    arrow_count_text = font.render(f'Arrows Left: {num_arrows}', True, BLACK)
    screen.blit(arrow_count_text, (10, 50))

   

    
    # Drawing the arrow
    if arrow_embedded and not game_over:
        screen.blit(arrow_img, (arrow_x, arrow_y))

    # Draw the moving bar
    pygame.draw.rect(screen, BLUE, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (button_x, button_y, button_width, button_height))

    # Draw the archer
    screen.blit(archer_img, (archer_x, archer_y))

    # Draw the arrow only if it's moving
    if arrow_moving:
        screen.blit(arrow_img, (arrow_x, arrow_y))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
