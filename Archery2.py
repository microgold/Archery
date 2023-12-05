import pygame
import random
from Sprites import Archer, Arrow, ArrowMarker, MovingBar, Target, GameText


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

# initialize the Archer
archer_x, archer_y = 100, height // 2
archer_img = pygame.image.load('Sprites/ArcherStrip.png')  # Load your sprite here
archer = Archer(archer_img, (archer_x, archer_y))
archer_width = 150

# Initialize the arrow
arrow_img = pygame.image.load('Sprites/Arrow.png')  # Load your arrow sprite here
arrow = Arrow(arrow_img, (archer_x + archer_width, archer_y + 55))
arrow.speed = 10
arrow.fired = False

# Initialize the moving bar
moving_bar = MovingBar((0, height - 50), width, height)

# Initialize the arrow markers
hit_positions = pygame.sprite.Group()

#intitialize the statistics
score_text = GameText('Score: 0', 36, BLACK, (100, 20))
arrow_count_text = GameText(f'Arrows Left: {arrow.num_arrows}', 36, BLACK, (300, 20))
game_over_text = GameText('Game Over', 36, RED, (width // 2 - 50, height // 2 - 20))
play_again_text = GameText('Play Again? (y/n)', 36, GREEN, (width // 2 - 50, height // 2 + 10))
game_over = False

# initialize target
target = Target((target_x, target_y), target_radius)

def handle_arrow_firing():
    global hit_x, hit_y, bar_center
    
    arrow.reset()
    arrow.fire()
    archer.current_frame = 0
    archer.animation_counter = 0
    
    # Determine the hit position
    bar_center = moving_bar.bar_x + moving_bar.bar_width // 2
    bar_position_ratio = ( moving_bar.button_x -  moving_bar.bar_x) /  moving_bar.bar_width
    hit_position_ratio = (2 * bar_position_ratio - 1)  # -1 (left) to 1 (right)

    # Calculate the hit position on the target
    hit_deviation = hit_position_ratio * target.radius # Distance from bullseye
    target_x, target_y = target.position
    hit_x = target_x + hit_deviation
    # Adjust vertical offset based on proximity to bullseye
    max_offset = 5  # Maximum vertical offset
    abs_deviation = abs(hit_deviation)
    if abs_deviation <= target_radius * 0.4:
        max_offset = 3  # Smaller offset for closer to bullseye
    vertical_offset = random.uniform(-max_offset, max_offset)
    hit_y = target_y + vertical_offset
    arrow.decrement_arrows() # Decrement the arrow count
    return hit_deviation


def reset_game():
    global hit_positions, score, hit_x, hit_y
    
    arrow.reset()
    arrow.num_arrows = 10
    archer.reset()
    # track game over state
    game_over = False

    hit_positions.empty()
    score = 0
    hit_x = 0
    hit_y = 0


reset_game()


arrow_marker = None
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
            if event.key == pygame.K_SPACE and not arrow.fired:
                archer.current_frame = 0
                hit_deviation = handle_arrow_firing()
               
        
    if game_over: continue # Skip the rest of the game loop if game is over

    # Collision detection
    arrow_x, arrow_y = arrow.position
    target_x, target_y = target.position
    archer_x, archer_y = archer.position
    
    distance_to_target = ((arrow_x - target_x)**2 + (arrow_y - target_y)**2)**0.5
    if distance_to_target <= target.radius and arrow.moving:
        arrow.moving = False

    # Update arrow position
    if arrow.fired:
        if archer.current_frame < archer.num_frames:
            archer.animate()
        else:            
            # Once animation is done, start moving the arrow
            if not arrow.moving:
                arrow.initial_update(archer_x, archer_y, archer_width)                
                arrow.moving = True
            else:
                arrow.update()
                if arrow_x > width or (target_x - arrow_x <= target_radius):
                    if arrow.moving:   
                        arrow.fired = False
                        arrow.moving = False                   
                        # Add the hit position to the list and calculate score
                        mark_color = target.get_mark_color(hit_deviation)
                        arrow_marker = ArrowMarker((hit_x, hit_y), mark_color)
                        hit_positions.add(arrow_marker)
                        score += target.calculate_score(hit_deviation)
                       
                         # Check for game over
                        if arrow.num_arrows <= 0:
                            game_over_text.draw(screen)   
                            game_over = True                            
                            play_again_text.draw(screen)
    # Draw the target
    target.draw(screen)
    
    # display the arrow markers where they hit on the target
    hit_positions.draw(screen)
    
    # Draw the moving bar
    moving_bar.update()
    moving_bar.draw(screen)
        

    # Display the score
    score_text.update_text(f'Score: {score}')
    score_text.draw(screen)
    
    #Display the arrow count
    arrow_count_text.update_text(f'Arrows Left: {arrow.num_arrows}')
    arrow_count_text.draw(screen)

   

    # Draw the archer
    archer.draw(screen)

    # Draw the arrow only if it's moving
    if arrow.moving:
        arrow.draw(screen)
        # screen.blit(arrow_img, (arrow_x, arrow_y))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
