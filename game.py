import pygame
import random

from unit import *
from Tiles import *
from constante import GameConstantes as GC
from configureWorld import*
from World_Drawer import *
from world import*

# Setup tiles
tiles_kind = [
    SandTile(),  # False veut dire que la case n'est pas solide tu peux marcher
    RockTile(),
    WaterTile()
]

map = Map("map/start.map", tiles_kind, GC.CELL_SIZE)

class Game:
    def __init__(self, screen, tile_map):
        self.screen = screen
        self.player_units = [
           #(x, y, health, attack, defense, speed, vision, image_path, team)
            Archer(0, 0, 100, 5, 2, 2, 3, 'Photos/archer.jpg', 'player'),
            Mage(1, 0, 100, 3, 1, 1, 2, 'Photos/mage.jpg', 'player'),
            Giant(2, 0, 100, 10, 1, 1, 2, 'Photos/giant.jpg', 'player')
        ]

        self.enemy_units = [
            Archer(5, 6, 100, 5, 2, 2, 3, 'Photos/enemy_archer.jpg', 'enemy'),
            Mage(6, 6, 100, 3, 1, 1, 2, 'Photos/enemy_mage.png', 'enemy'),
            Giant(7, 6, 100, 10, 1, 1, 2, 'Photos/enemy_giant.png', 'enemy')
        ]

        self.tile_map = Map_Aleatoire(tile_map, TERRAIN_TILES, GC.CELL_SIZE)
    #Call spawn_units after initializing player_units
        self.spawn_units()
        self.logs = [] 
    def display_log(self, message):
        """Displays a game log at the bottom of the screen."""
        font = pygame.font.Font(None, 36)
        log_surface = font.render(message, True, (255, 255, 255))  # Assuming WHITE is defined
        log_rect = log_surface.get_rect(center=(GC.WIDTH // 2, GC.HEIGHT + 20))
        self.screen.blit(log_surface, log_rect)
        pygame.display.flip()

    def calculate_valid_cells(self, unit):
        """Calculate accessible cells for a unit, excluding cells occupied by other units within its speed range."""
        valid_cells = []
        # Combine all units' positions
        all_units_positions = {(u.x, u.y) for u in self.player_units + self.enemy_units}

        for dx in range(-unit.speed, unit.speed + 1):
            for dy in range(-unit.speed, unit.speed + 1):
                if abs(dx) + abs(dy) <= unit.speed:  # Manhattan distance
                    x, y = unit.x + dx, unit.y + dy
                    if (
                        0 <= x < GC.WORLD_X and 0 <= y < GC.WORLD_Y  # Within grid bounds
                        and self.tile_map.is_walkable(x, y, unit)    # Tile is walkable
                        and (x, y) not in all_units_positions        # Not occupied by another unit
                    ):
                        valid_cells.append((x, y))

        return valid_cells

    #------------------Make Sure that the units doesn't spawn on non walkable tiles----------------#
    def get_valid_spawn_locations(self, tile_map, enemy_units, min_distance):
        """Get valid spawn locations that are walkable and far from enemies."""
        valid_spawn_locations = []
        all_enemy_positions = {(enemy.x, enemy.y) for enemy in enemy_units}

        for x in range(GC.WORLD_X):
            for y in range(GC.WORLD_Y):
                if tile_map.is_walkable(x, y):  # Check if the tile is walkable
                    # Check distance from all enemy units
                    if all(abs(x - enemy.x) + abs(y - enemy.y) >= min_distance for enemy in enemy_units):
                        valid_spawn_locations.append((x, y))

        return valid_spawn_locations

    def spawn_units(self):
        min_distance_from_enemy = 8  # Set your desired minimum distance
        valid_spawn_locations = self.get_valid_spawn_locations(self.tile_map, self.enemy_units, min_distance_from_enemy)

        if valid_spawn_locations:
            # Randomly select a spawn location for the first unit
            spawn_location = random.choice(valid_spawn_locations)
            start_x, start_y = spawn_location

            # List of offsets to spawn units next to each other
            offsets = [(0, 0), (1, 0), (0, 1), (1, 1)]  # Adjust this as needed for more formations

            for unit in self.player_units:
                while True:
                    # Randomly select an offset
                    offset = random.choice(offsets)
                    new_x, new_y = start_x + offset[0], start_y + offset[1]

                    # Check if the new position is valid
                    if (0 <= new_x < GC.WORLD_X and 0 <= new_y < GC.WORLD_Y and
                        self.tile_map.is_walkable(new_x, new_y) and (new_x, new_y) not in {(u.x, u.y) for u in self.player_units}):
                        unit.x, unit.y = new_x, new_y
                        break
    #---------------------END OF THIS PART-----------------------------------------------#
    
    #----------------------Creating The game Log-----------------------------------------#
    def display_log(self, message, position=(10, GC.HEIGHT - GC.LOG_HEIGHT + 10)):
        """Displays a single log message at the bottom of the screen."""
        font = pygame.font.Font(None, 24)
        log_surface = font.render(message, True, (255, 255, 255))  # White text
        self.screen.blit(log_surface, position)  # Position the log
        # Draw action options
        font = pygame.font.Font(None, 36)
        actions = ["Attack", "Defend", "Skip"]
        for i, action in enumerate(actions):
            text_surface = font.render(action, True, (255, 255, 255))  # White text
            self.screen.blit(text_surface, (100 + i * 150, GC.HEIGHT - GC.LOG_HEIGHT + 25))  # Position the action options
    
    def handle_action_selection():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:  # Attack
                        return "attack"
                    elif event.key == pygame.K_d:  # Defend
                        return "defend"
                    elif event.key == pygame.K_s:  # Skip
                        return "skip"
    
    def add_log(self, message):
        """Add a log message and ensure only the last 5 messages are kept."""
        self.logs.append(message)
    
    def draw_game_log(self):
        """Draws the log area and renders the latest log messages."""
        pygame.draw.rect(self.screen, (0, 0, 0), (0, GC.HEIGHT - GC.LOG_HEIGHT, GC.WIDTH, GC.LOG_HEIGHT))  # Black background

        font = pygame.font.Font(None, 24)
        for i, message in enumerate(self.logs):
            text_surface = font.render(message, True, (255, 255, 255))  # White text
            self.screen.blit(text_surface, (10, GC.HEIGHT - GC.LOG_HEIGHT + 10 + i * 20))  # Position messages
    

    
    #-----------------END OF THIS PART---------------------------------------------------#
    
    def redraw_static_elements(self):
        """Redraw the grid and units."""
        self.screen.fill(GC.GREEN)  # Fill the screen with GREEN
        self.tile_map.draw(self.screen)
        # Draw the grid
        for x in range(0, GC.WIDTH, GC.CELL_SIZE):
            for y in range(0, GC.HEIGHT, GC.CELL_SIZE):
                rect = pygame.Rect(x, y, GC.CELL_SIZE, GC.CELL_SIZE)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)

        pygame.display.flip()  # Update once
    
    def flip_display(self):
        """Renders the game state."""
        self.screen.fill(GC.GREEN) # Fill the screen with black
        self.tile_map.draw(self.screen)  # Draw the map

        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)  # Draw units

        pygame.display.flip()  # Update the display

    def draw_highlighted_cells(self, valid_cells):
        """Draw accessible cells and highlight the one under the cursor with transparency."""
        # Create transparent surfaces
        valid_cell_surface = pygame.Surface((GC.CELL_SIZE, GC.CELL_SIZE), pygame.SRCALPHA)
        valid_cell_surface.fill((0, 0, 0, 0))  # Surface complètement transparente
        pygame.draw.rect(valid_cell_surface, (255, 255, 120), valid_cell_surface.get_rect())

        hover_surface = pygame.Surface((GC.CELL_SIZE, GC.CELL_SIZE), pygame.SRCALPHA)
        hover_surface.fill((0, 0, 0, 0))  # Surface complètement transparente
        pygame.draw.rect(hover_surface, (255, 0, 0, 128), hover_surface.get_rect())

        # Draw valid cells
        for x, y in valid_cells:
            rect = pygame.Rect(x * GC.CELL_SIZE, y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            self.screen.blit(valid_cell_surface, rect.topleft)

        # Get mouse position and check hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_x, hover_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE

        # Highlight hovered cell if it's a valid cell
        if (hover_x, hover_y) in valid_cells:
            hover_rect = pygame.Rect(hover_x * GC.CELL_SIZE, hover_y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            self.screen.blit(hover_surface, hover_rect.topleft)

        # Redraw all units
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Update display
        pygame.display.update()


    def handle_player_turn(self):
        """Handle the player's turn without flickering."""
        for selected_unit in self.player_units:
            if self.check_game_over():
                return has_acted == False
            selected_unit.is_selected == True

            valid_cells = self.calculate_valid_cells(selected_unit)

            self.redraw_static_elements()  # Grid and units
            self.draw_highlighted_cells(valid_cells)
            has_acted = False
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        new_x, new_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE

                        if (new_x, new_y) in valid_cells:
                            selected_unit.move(new_x, new_y)
                            has_acted = True
                            selected_unit.is_selected = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:  # Skip turn pour la touche s 
                            has_acted = True
                            selected_unit.is_selected = False
                        if (new_x, new_y) in valid_cells:
                            selected_unit.move(new_x, new_y)
                            self.add_log(f"{selected_unit.__class__.__name__} moved to ({new_x}, {new_y}).")
                            has_acted = True

                self.draw_highlighted_cells(valid_cells)

    def handle_enemy_turn(self):
        """Simple AI for the enemy's turn."""
        for enemy in self.enemy_units:
            if self.check_game_over():
                return

            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            new_x = enemy.x + dx
            new_y = enemy.y + dy

            if abs(new_x - enemy.x) + abs(new_y - enemy.y) <= enemy.speed and self.tile_map.is_walkable(new_x, new_y):
                enemy.move(new_x, new_y)

            if abs(enemy.x - target.x) <= enemy.range and abs(enemy.y - target.y) <= enemy.range:
                enemy.attack(target)
                self.display_log(f"{enemy.__class__.__name__} attacked {target.__class__.__name__}!")
                if target.health <= 0:
                    self.player_units.remove(target)
                    self.display_log(f"{target.__class__.__name__} was defeated!")

            if abs(enemy.x - target.x) <= enemy.range and abs(enemy.y - target.y) <= enemy.range:
                enemy.attack(target)
                self.add_log(f"{enemy.__class__.__name__} attacked {target.__class__.__name__}!")
                if target.health <= 0:
                    self.player_units.remove(target)
                    self.add_log(f"{target.__class__.__name__} was defeated!")
            

    def check_game_over(self):
        """Checks if the game is over and displays the winner."""
        if not self.player_units:
            self.display_game_over("Enemy Wins!")
            return True
        elif not self.enemy_units:
            self.display_game_over("Player Wins!")
            return True
        return False

    def display_game_over(self, message):
        """Displays a game over message and stops the game."""
        font = pygame.font.Font(None, 72)
        game_over_surface = font.render(message, True, (255, 0, 0))  # Assuming RED is defined
        game_over_rect = game_over_surface.get_rect(center=(GC.WIDTH // 2, GC.HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # Pause for 3 seconds
        pygame.quit()
        exit()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    WEIGHTS = [25, 40, 10, 40, 10, 10]
    random_seed = 8

    world = World(GC.WORLD_X, GC.WORLD_Y, random_seed)
    tile_map = world.get_tiled_map(WEIGHTS)

    screen = pygame.display.set_mode((GC.WIDTH, GC.HEIGHT), pygame.SRCALPHA)  # Added space for the game log
    pygame.display.set_caption("Game")

    game = Game(screen, tile_map)
    # Example selected unit
    selected_unit = Archer(0, 0, 100, 5, 2, 2, 3, 'Photos/archer.jpg', 'player')  # Replace with your actual unit
    running = True
    while running:
        game.redraw_static_elements()  # Draw grid, units, and static elements
        game.draw_game_log()  # Draw the log messages
        game.handle_player_turn()
    
        if game.check_game_over():
            break
        game.handle_enemy_turn()
        if game.check_game_over():
            break
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()