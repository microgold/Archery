__package__ = "ArcherGame"
import pygame

WHITE = (255, 255, 255)
GRAY = (227, 228, 221)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
LIGHTGRAY = (200, 200, 200)




class Archer(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.position = position
        self.num_frames = 5
        self.frame_width, self.frame_height = self.image.get_width() // 5, self.image.get_height()
        self.frames = self.get_frames(self.image, self.frame_width, self.frame_height, self.num_frames)
        self.current_frame = 0
        self.animation_speed = 5  # Adjust this value to control the speed of the animation
        self.animation_counter = 0
    
    def get_frames(self, image, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            frame = image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames
    
    def reset(self):
        self.current_frame = 0
        self.animation_counter = 0
    
    def animate(self):        
        if self.animation_counter >= self.animation_speed:
            self.current_frame += 1
            self.animation_counter = 0  # Reset counter after updating frame
        self.animation_counter += 1
    
    def draw(self, screen):
        screen.blit(self.frames[self.current_frame - 1], self.position)
    
        

class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.position = position
        self.starting_position = position
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 10
        self.fired = True
        self.moving = False  # New variable to track arrow movement
        self.num_arrows = 10  # Number of arrows per game

    def initial_update(self, archer_x, archer_y, archer_width):
        if self.moving:
            self.position = self.starting_position
    
    def update(self):
        if self.moving:
            (x,y) = self.position
            self.position = (x + self.speed, y)
            self.rect = self.image.get_rect(topleft=self.position)
    
    def reset(self):
        self.moving = False
        self.fired = False
        self.position = self.starting_position
    
    def decrement_arrows(self):
        self.num_arrows -= 1
        
    def fire(self):
        self.fired = True
        self.moving = False
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Target(pygame.sprite.Sprite):
    def __init__(self, position, radius):
        super().__init__()
        self.position = position
        self.radius = radius
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        colors = [WHITE, BLACK, BLUE, RED, YELLOW]
        for i, color in enumerate(colors):
            pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius - i * 10)
            screen.blit(self.image, self.rect)
    
    def get_mark_color(self, hit_deviation):
        # Function to determine the color of the mark based on the hit deviation
        if abs(hit_deviation) <= self.radius * 0.2:  # Bullseye (Yellow)
            return BLACK  # Black mark for visibility
        elif abs(hit_deviation) <= self.radius * 0.4:  # Red
            return LIGHTGRAY  # White or grey mark for visibility
        elif abs(hit_deviation) <= self.radius * 0.6:  # Blue
            return LIGHTGRAY  # Black mark should be visible on blue
        elif abs(hit_deviation) <= self.radius * 0.8:  # BLACK
            return LIGHTGRAY  # Black mark should be visible on blue
        else:  # Black or White ring
            return LIGHTGRAY  # White mark for visibility on blac
            
    def calculate_score(self, deviation):
        abs_deviation = abs(deviation)
        if abs_deviation <= self.radius * 0.2:  # Bullseye
            return 10
        elif abs_deviation <= self.radius * 0.4:
            return 5
        elif abs_deviation <= self.radius * 0.6:
            return 3
        elif abs_deviation <= self.radius:
            return 1
        else:
            return 0  # Missed the target 


# archer_strip_img = pygame.image.load('Sprites/ArcherStrip.png')  # Load your sprite strip here
# archer = Archer(archer_strip_img, (0, 0))