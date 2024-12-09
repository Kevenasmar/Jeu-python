import pygame
import random

from unit import *
from Tiles import *
from constante import GameConstantes as GC
from configureWorld import*
from World_Drawer import *
from world import*
from GameLog import * # type: ignore
from menu import *  # Import menu functions
from collectible_items import *
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
        self.game_log = GameLog(500, GC.HEIGHT, GC.WIDTH, 0, self.screen)
        self.tile_map = Map_Aleatoire(tile_map, TERRAIN_TILES, GC.CELL_SIZE)
        self.player_units_p1 = [ 
           #(x, y, points de vie, statistique d'attaque, statistique de défense, vitesse, vision, image, équipe)
            Archer(0, 0, 100, 5, 2, 5, 3, 'Photos/archer.png', 'player'),
            Mage(1, 0, 100, 3, 1, 4, 2, 'Photos/mage.png', 'player'),
            Giant(2, 0, 100, 10, 1, 3, 2, 'Photos/giant.png', 'player'),
            Bomber(3, 0, 100, 7, 1, 4, 2, 'Photos/bomber.png', 'player')
        ] 

<<<<<<< HEAD
        self.enemy_units = [
            Archer(5, 6, 100, 5, 2, 2, 3, 'Photos/enemy_archer.png', 'enemy'),
            Mage(6, 6, 100, 3, 1, 1, 2, 'Photos/enemy_mage.png', 'enemy'),
            Giant(7, 6, 100, 10, 1, 1, 2, 'Photos/enemy_giant.png', 'enemy')
        ]
        
        self.player_units_p2 = [
           #(x, y, health, attack, defense, speed, vision, image_path, team)
=======
        self.player_units_p2 = [ 
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
            Archer(0, 0, 100, 5, 2, 5, 3, 'Photos/enemy_archer.png', 'enemy'),
            Mage(1, 0, 100, 3, 1, 4, 2, 'Photos/enemy_mage.png', 'enemy'),
            Giant(2, 0, 100, 10, 1, 3, 2, 'Photos/enemy_giant.png', 'enemy'),
            Bomber(3, 0, 100, 7, 1, 4, 2, 'Photos/enemy_bomber.png', 'enemy')
        ]
<<<<<<< HEAD
        # Initialize spawn for bomber units as well
=======

        self.tile_map = Map_Aleatoire(tile_map, TERRAIN_TILES, GC.CELL_SIZE)
        self.walkable_tiles = self.inititialize_walkable_tiles()
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
        self.spawn_units()
        
        self.walkable_tiles = self.initisialize_walkable_tiles()
        self.collectible_spawn_timer = 0
        self.spawn_interval = 2  # Seconds between spawns
        self.collectible_items = []
        self.collectible_templates = self.initialize_collectibles(tile_map)

    #-------------------Collectibles Logic------------#
    def initialize_collectibles(self, tile_map):
        self.collectible_items = []
        self.collectible_spawn_timer = 0
        self.spawn_interval = 2  # Seconds between spawns
        
        # Create effects
        effects = {
            "health": Effect("health", "soundeffects/apply_effect.wav"),
            "speed": Effect("speed", "soundeffects/apply_effect.wav"),
            "damage": Effect("damage", "soundeffects/apply_effect.wav")
        }
        
        # Create and return collectible templates
        return {
            "speed": lambda: CollectibleItem(
                effects["speed"],
                'image/speed_potion.png',
                "soundeffects/apply_effect.wav",
                120,
                tile_map,
                self.game_log
            )
            }
    """,
            "health": lambda: CollectibleItem(
                effects["health"],
                'image/health_potion.png',
                "soundeffects/apply_effect.wav",
                120,
                tile_map,
                self.game_log
            "damage": lambda: CollectibleItem(
                effects["damage"],
                'image/power_buff.png',
                "soundeffects/apply_effect.wav",
                120,
                tile_map,
                self.game_log
            )"""

    def spawn_collectible(self):
        print("Spawning collectible...")
        # Choose a random collectible type
        collectible_type = random.choice(list(self.collectible_templates.keys()))
        new_collectible = self.collectible_templates[collectible_type]()
        
        # Find a valid spawn location
        walkable_tiles = []
        for x in range(GC.WORLD_X):
            for y in range(GC.WORLD_Y):
                if self.tile_map.is_walkable(x, y):
                    # Check if location is not too close to any player
                    too_close = False
                    for unit in self.player_units_p1 + self.player_units_p2:
                        if abs(unit.x - x * GC.CELL_SIZE) < GC.CELL_SIZE * 3 and \
                        abs(unit.y - y * GC.CELL_SIZE) < GC.CELL_SIZE * 3:
                            too_close = True
                            break
                    if not too_close:
                        walkable_tiles.append((x, y))
        print(f"Found {len(walkable_tiles)} walkable tiles.")
        if walkable_tiles:
            spawn_x, spawn_y = random.choice(walkable_tiles)
            new_collectible.x = spawn_x 
            new_collectible.y = spawn_y 
            self.collectible_items.append(new_collectible)
            self.game_log.add_message("Collectible spawned", 'other')
            print("Collectible are spawned at", spawn_x, spawn_y)
        else : 
            print('No walkable tile found for collectible!')
        
    def update_collectibles(self, delta_time):
        # Update spawn timer
        self.collectible_spawn_timer += delta_time
        if self.collectible_spawn_timer >= self.spawn_interval:
            self.spawn_collectible()
            self.collectible_spawn_timer = 0
        
        # Update and check collection for existing collectibles
        for item in self.collectible_items[:]:  # Use slice to safely modify list while iterating
            if item.is_active:
                for unit in self.player_units_p1 + self.player_units_p2:
                    item.collect(unit)
                    if not item.is_active:  # If item was collected
                        self.collectible_items.remove(item)  # Remove it from the list
                        break
    """"def update_collectibles(self, delta_time):
        # Update spawn timer
        self.collectible_spawn_timer += delta_time
        #Spawn new collectible if timer exceeds interval
        if self.collectible_spawn_timer >= self.spawn_interval:
            self.spawn_collectible()
            self.collectible_spawn_timer = 0  # Reset timer

        
        # Update existing collectibles
        for item in self.collectible_items[:]:  # Create a copy of the list to modify it safely
            item.update(delta_time)
            # Check collection for all units
            for unit in self.player_units_p1 + self.player_units_p2:
                item.collect(unit)
            
            # Remove inactive items that have exceeded their respawn time
            if not item.is_active and item.respawn_counter >= item.respawn_time:
                self.collectible_items.remove(item)
"""
    def draw_collectibles(self):
        for item in self.collectible_items:
            if item.is_active:
                self.screen.blit(item.image, (item.x * GC.CELL_SIZE, item.y * GC.CELL_SIZE))

    #----------End of this part----------------------#            

    '''--------S'assurer que les unités n'apparaissent pas sur des cases non praticables------------''' 
    def inititialize_walkable_tiles(self) :
        set_walkable_tiles = set () 
        for x in range (GC.WORLD_X):
            for y in range (GC.WORLD_Y):
                if any(self.tile_map.is_walkable(x, y, unit) for unit in self.player_units_p1 + self.player_units_p1 ):
                    set_walkable_tiles.add((x, y))
        return set_walkable_tiles
<<<<<<< HEAD

=======
    
    '''Ici, on gère l'apparition des unités sur la map en début de jeu'''
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
    def get_spawn_sector_p1(self) :
        sector_width = GC.WORLD_X // 3 
        sector_height = GC.WORLD_Y // 3
        player_sector_x_p1 = 0 #Le joueur 1 apparait dans la partie gauche de la map 
        sector_y = random.randint(0,2) 
        return (player_sector_x_p1*sector_width, sector_y*sector_height, sector_width, sector_height) 
    
    def get_spawn_sector_p2(self) :
        sector_width = GC.WORLD_X // 3 
        sector_height = GC.WORLD_Y // 3
        player_sector_x_p2 = 2 #Le joueur 2 apparait dans la partie droite de la map 
        sector_y = random.randint(0,2) 
        return (player_sector_x_p2*sector_width, sector_y*sector_height, sector_width, sector_height) 
    
    def find_spawn_location_p1 (self, nbr_units) :
        sector_x, sector_y, width, height = self.get_spawn_sector_p1()        
        spawn_locations = []
        for x in range(sector_x, sector_x + width):
            for y in range(sector_y, sector_y + height):
                if all(self.tile_map.is_walkable(x, y, unit) for unit in self.player_units_p1):
                    spawn_locations.append((x, y))  
                    if len(spawn_locations) == nbr_units :
                        return spawn_locations
        return spawn_locations
    
    def find_spawn_location_p2 (self, nbr_units) :
        sector_x, sector_y, width, height = self.get_spawn_sector_p2()        
        spawn_locations = []
        for x in range(sector_x, sector_x + width):
            for y in range(sector_y, sector_y + height):
                if all(self.tile_map.is_walkable(x, y, unit) for unit in self.player_units_p2):
                    spawn_locations.append((x, y))  
                    if len(spawn_locations) == nbr_units :
                        return spawn_locations
        return spawn_locations
    
    def spawn_units(self) : 
        self.game_log.add_message("May the best player win!", 'action')

        #spawn joueur 1 
        spawn_location_p1 = self.find_spawn_location_p1 (len(self.player_units_p1))

        for unit , location in zip (self.player_units_p1, spawn_location_p1) :
            unit.x, unit.y = location     
        self.game_log.draw()

        #spawn joueur 2
        spawn_location_p2 = self.find_spawn_location_p2 (len(self.player_units_p2))

        for unit , location in zip (self.player_units_p2, spawn_location_p2) :
            unit.x, unit.y = location     
        self.game_log.draw()

<<<<<<< HEAD
    '''-----------------END OF THIS PART ---------------------------'''
    def is_occupied(self, x, y):
        """
        Checks if a tile is occupied by any unit.
        """
        for unit in self.player_units_p1 + self.player_units_p2:
            if unit.x == x and unit.y == y:
                return True
        return False

    '''Utilities, display and movement'''
=======

    '''------------------Utilitaires, affichage et déplacement-----------------------'''
  
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
    def calculate_valid_cells(self, unit):
        """Retourne les cases accessibles pour une unité, en excluant les cases occupées par d'autres unités dans son rayon de déplacement."""
        valid_cells = []
        # Combiner les positions des unités
        all_units_positions = {(u.x, u.y) for u in self.player_units_p1 + self.player_units_p2}

        for dx in range(-unit.speed, unit.speed + 1):
            for dy in range(-unit.speed, unit.speed + 1):
                if abs(dx) + abs(dy) <= unit.speed:  # Distance de Manhattan 
                    x, y = unit.x + dx, unit.y + dy
                    if (
                        0 <= x < GC.WORLD_X and 0 <= y < GC.WORLD_Y  # Dans les limites de la grille
                        and self.tile_map.is_walkable(x, y, unit)    # La case est praticable
                        and (x, y) not in all_units_positions        # Non occupée par une unité
                    ):
                        valid_cells.append((x, y))

        return valid_cells
    
    def has_line_of_sight(self, start, end):
        """
        Vérifie s'il existe une ligne de vue dégagée entre deux points afin de gérer les attaques.
        Utilise l'algorithme de Bresenham pour tracer la ligne et vérifier les cases solides.
        """
        x0, y0 = start
        x1, y1 = end
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            # Check if the tile at (x0, y0) is a wall
            tile = self.tile_map.terrain_tiles[self.tile_map.terrain_data[y0][x0]]
            if isinstance(tile, UnwalkableTile) and not isinstance(tile, WaterTile):  # Only walls block LoS
                return False

            if (x0, y0) == (x1, y1):  # Reached the target
                return True

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx   
                y0 += sy

    def redraw_static_elements(self):
        """Redessine la grille et les unités"""
        self.screen.fill(GC.GREEN)  # Remplir l'écran avec du vert
        self.tile_map.draw(self.screen)
        # Dessine la grille
        for x in range(0, GC.WIDTH, GC.CELL_SIZE):
            for y in range(0, GC.HEIGHT, GC.CELL_SIZE):
                rect = pygame.Rect(x, y, GC.CELL_SIZE, GC.CELL_SIZE)
        self.draw_collectibles()

        self.game_log.draw()
        pygame.display.flip()  # Mise a jour
    
    def flip_display(self):
        """Retourne l'état du jeu."""
        self.screen.fill(GC.GREEN)  # Effacer l'écran
        self.tile_map.draw(self.screen)  # Dessine la map

        # Dessiner d'abord les cases surlignées
        if hasattr(self, 'valid_cells') and self.valid_cells:  # S'assurer que valid_cells soit bien définie
            self.draw_highlighted_cells(self.valid_cells)

<<<<<<< HEAD
        self.draw_collectibles()

        # Draw all units (including health bars)
=======
        # Dessiner toutes les unités avec leurs bars de vie 
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
        for unit in self.player_units_p1 + self.player_units_p2:
            unit.draw(self.screen)

        self.game_log.draw()  # Dessiner le game log
        pygame.display.flip()  # Mettre à jour l'affichage 
    
<<<<<<< HEAD
    def draw_highlighted_cells(self, move_cells=None, direct_cells=None, secondary_cells=None, is_attack_phase=False):
        """
        Draw highlighted cells with distinct colors:
        - Movement cells: White.
        - Direct attack cells: Red.
        - Secondary affected cells: Yellow.
        - Hovered cell: White for movement phase, Red for attack phase.
        """
        # Default to empty lists if None
        move_cells = move_cells or []
        direct_cells = direct_cells or []
        secondary_cells = secondary_cells or []
=======
    def draw_highlighted_cells(self, valid_cells):
        """Dessiner une bordure blanche externe autour du groupe de cases valides et remplir la case survolée en blanc."""
        #Convertir la liste valid_cells en un ensemble pour accélérer la recherche des voisins.
        valid_cells_set = set(valid_cells)
>>>>>>> a45332278309099374fa68504b2a84aa243a9099

        # Directions pour vérifier les voisins (haut, droite, bas, gauche)
        directions = [
            (0, -1),  # Haut
            (1, 0),   # Droite
            (0, 1),   # Bas
            (-1, 0)   # Gauche
        ]

        # Effacer l'écran et redessiner la grille avant 
        self.tile_map.draw(self.screen)
<<<<<<< HEAD
        self.draw_collectibles()
        # Highlight movement cells (white)
        for x, y in move_cells:
=======

        # Parcourir toutes les cases valides et dessiner des bordures externes.
        for x, y in valid_cells:
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
            for i, (dx, dy) in enumerate(directions):
                neighbor = (x + dx, y + dy)
                if neighbor not in move_cells:
                    start_pos = (x * GC.CELL_SIZE, y * GC.CELL_SIZE)
                    end_pos = list(start_pos)

<<<<<<< HEAD
                    # Adjust line positions for the border
                    if i == 0:  # Top border
=======
                # Si le voisin n'est pas dans valid_cells, dessine la bordure  
                if neighbor not in valid_cells_set:
                    start_pos = (x * GC.CELL_SIZE, y * GC.CELL_SIZE)  # Haut-Gauche de la cellule
                    end_pos = list(start_pos)  # Copie de start_pos

                    # Ajuster les positions des lignes en fonction de la direction.
                    if i == 0:  # Bord supérieur
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
                        end_pos[0] += GC.CELL_SIZE
                    elif i == 1:  # Bord Droit
                        start_pos = (start_pos[0] + GC.CELL_SIZE, start_pos[1])
                        end_pos = (start_pos[0], start_pos[1] + GC.CELL_SIZE)
                    elif i == 2:  # Bord Inférieur
                        start_pos = (start_pos[0], start_pos[1] + GC.CELL_SIZE)
                        end_pos = (start_pos[0] + GC.CELL_SIZE, start_pos[1])
                    elif i == 3:  # Bord Gauche
                        end_pos[1] += GC.CELL_SIZE

<<<<<<< HEAD
                    # Draw the border line (white for movement cells)
                    pygame.draw.line(self.screen, (255, 255, 255), start_pos, end_pos, 2)

        # Highlight direct attack cells (red)
        for x, y in direct_cells:
            rect = pygame.Rect(x * GC.CELL_SIZE, y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)  # Red border for direct cells

        # Highlight secondary affected cells (yellow)
        for x, y in secondary_cells:
            rect = pygame.Rect(x * GC.CELL_SIZE, y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 255, 0), rect, 2)  # Yellow border for secondary cells

        # Highlight the hovered cell
=======
                    # Dessine la ligne de bordure blanche
                    pygame.draw.line(self.screen, (255,255,255), start_pos, end_pos, 2)

>>>>>>> a45332278309099374fa68504b2a84aa243a9099
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_x, hover_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE
        hover_color = (255, 0, 0, 100) if is_attack_phase else (255, 255, 255, 100)

<<<<<<< HEAD
        if (hover_x, hover_y) in move_cells + direct_cells + secondary_cells:
            rect = pygame.Rect(hover_x * GC.CELL_SIZE, hover_y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            pygame.draw.rect(self.screen, hover_color, rect)  # Fill hovered cell with the appropriate color
=======
        # Si la case survolée est dans valid_cells, remplir la case de blanc 
        if (hover_x, hover_y) in valid_cells_set:
            rect = pygame.Rect(hover_x * GC.CELL_SIZE, hover_y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            pygame.draw.rect(self.screen, (255,255,255, 100), rect)  
>>>>>>> a45332278309099374fa68504b2a84aa243a9099

        # Redessine toutes les unités pour s'assurer qu'elles apparaissent au dessus de la case surlignée 
        for unit in self.player_units_p1 + self.player_units_p2:
            unit.draw(self.screen)

        # Mise a jour de l'affichage
        self.game_log.draw()
        pygame.display.update()


<<<<<<< HEAD

    '''Attacks'''
=======
    '''--------------------------------------Attaques-----------------------------------------'''
    
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
    def calculate_valid_attack_cells(self, unit, attack_range, opponent_units):
        '''Retourne les cases d'attaques valides pour une unité'''
        valid_attack_cells = []
        for dx in range(-attack_range, attack_range + 1):
            for dy in range(-attack_range, attack_range + 1):
                if abs(dx) + abs(dy) <= attack_range:  # Distance de Manhattan 
                    cell_x, cell_y = unit.x + dx, unit.y + dy

                    # S'assurer que la cellule soit dans la limite de la grille
                    if 0 <= cell_x < GC.WORLD_X and 0 <= cell_y < GC.WORLD_Y:
                        for opponent in opponent_units:
                            if (opponent.x, opponent.y) == (cell_x, cell_y):
                                if self.has_line_of_sight((unit.x, unit.y), (cell_x, cell_y)):
                                    valid_attack_cells.append(opponent)
                                    break
        return valid_attack_cells

    def calculate_valid_heal_cells(self, unit, heal_range, ally_units):
        '''Retourne les cases valides pour le mage lors de la selection "Heal"'''
        valid_heal_cells = []
        for dx in range(-heal_range, heal_range + 1):
            for dy in range(-heal_range, heal_range + 1):
                if abs(dx) + abs(dy) <= heal_range:  # Distance de Manhattan
                    cell_x, cell_y = unit.x + dx, unit.y + dy

                    # S'assurer que la cellule soit dans la limite de la grille
                    if 0 <= cell_x < GC.WORLD_X and 0 <= cell_y < GC.WORLD_Y:
                        # Vérifier si une unité alliée est dans la cellule
                        for ally in ally_units:
                            if (ally.x, ally.y) == (cell_x, cell_y) and ally.health < 100:  # Inclure uniquement les unités blessées
                                valid_heal_cells.append(ally)
                                break  

        return valid_heal_cells

    '''Les fonctions suivantes gèrent les attaques spécifiques de chaque type d'unité. 
    Elles déterminent les cibles valides pour chaque type d'attaque de l'unité 
    et exécutent l'action appropriée en fonction de la portée et des capacités disponibles.'''
    
    def handle_attack_for_archer(self, archer, opponent_units):
        valid_attacks = {}
        if archer.normal_arrow_range:
            valid_targets = self.calculate_valid_attack_cells(archer, archer.normal_arrow_range, opponent_units)
            if valid_targets:
                valid_attacks["Normal Arrow"] = (archer.normal_arrow, valid_targets)

        if archer.fire_arrow_range:
            valid_targets = self.calculate_valid_attack_cells(archer, archer.fire_arrow_range, opponent_units)
            if valid_targets:
                valid_attacks["Fire Arrow"] = (archer.fire_arrow, valid_targets)

        if not valid_attacks:
            self.game_log.add_message("No enemies in range for Archer.", 'info')
            return

        self.perform_attack(archer, valid_attacks, opponent_units)
     
    def handle_attack_for_giant(self, giant, opponent_units):
        """
        Handles the Giant's attack logic, including Punch and Stomp.
        Highlights:
        - Punch: Direct target cells only.
        - Stomp: Direct cells in red and secondary affected cells in yellow.
        """
        valid_attacks = {}

        # Punch attack
        if giant.punch_range:
            valid_targets = self.calculate_valid_attack_cells(giant, giant.punch_range, opponent_units)
            if valid_targets:
                valid_attacks["Punch"] = (giant.punch, valid_targets)

        # Stomp attack
        if giant.stomp_range:
            valid_targets = self.calculate_valid_attack_cells(giant, giant.stomp_range, opponent_units)
            if valid_targets:
                # Highlight stomp cells
                direct_cells = [(target.x, target.y) for target in valid_targets]
                secondary_cells = [
                    (target.x + dx, target.y + dy)
                    for target in valid_targets
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Surrounding cells
                ]
                self.draw_highlighted_cells(direct_cells=direct_cells, secondary_cells=secondary_cells)

                valid_attacks["Stomp"] = (giant.stomp, valid_targets)

        # If no valid attacks
        if not valid_attacks:
            self.game_log.add_message("No enemies in range for Giant.", 'info')
            return

        # Perform the chosen attack
        self.perform_attack(giant, valid_attacks, opponent_units)


    def handle_attack_for_bomber(self, bomber, opponent_units):
<<<<<<< HEAD
        """
        Handles the Bomber's attack logic, allowing bombs to hit all units within range.
        Highlights:
        - Direct target cells in red.
        - Secondary affected cells in yellow for area-of-effect damage.
        """
        # Calculate valid targets within the Bomber's attack range
        valid_targets = self.calculate_valid_attack_cells(bomber, bomber.bomb_range, opponent_units)
=======
        valid_attacks = {}
>>>>>>> a45332278309099374fa68504b2a84aa243a9099

        if bomber.bomb_range:
            valid_targets = self.calculate_valid_attack_cells(bomber, bomber.bomb_range, opponent_units)
            if valid_targets:
                valid_attacks["Throw Bomb"] = (bomber.throw_bomb, valid_targets)

        if bomber.explode_range:
            all_units = self.player_units_p1 + self.player_units_p2
            valid_attacks["Explode"] = (bomber.explode, all_units) 

        if not valid_attacks:
            self.game_log.add_message("No valid actions for Bomber.", 'info')
            return

<<<<<<< HEAD
        # Highlight the bomb's AoE
        direct_cells = [(target.x, target.y) for target in valid_targets]
        secondary_cells = [
            (cell_x, cell_y)
            for target in valid_targets
            for dx in range(-1, 2)
            for dy in range(-1, 2)
            if (cell_x := target.x + dx) != target.x or (cell_y := target.y + dy) != target.y
        ]
        self.draw_highlighted_cells(direct_cells=direct_cells, secondary_cells=secondary_cells)

        # Perform the bomb attack
        self.perform_attack(bomber, {"Throw Bomb": (bomber.throw_bomb, valid_targets)}, opponent_units)


    
=======
        self.game_log.add_message("Choose your action:", 'attack')
        attack_options = {}
        for i, (action_name, (method, targets)) in enumerate(valid_attacks.items(), start=1):
            attack_options[i] = (method, targets)
            self.game_log.add_message(f"{i}: {action_name}", 'attack')

        self.game_log.draw()
        pygame.display.flip()

        chosen_action = None
        while chosen_action is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.unicode.isdigit():
                    action_index = int(event.unicode)
                    if action_index in attack_options:
                        chosen_action = attack_options[action_index]

        action_method, targets = chosen_action
        if action_method == bomber.explode:
            affected_units = action_method(targets) 
            affected_units_names = [unit.__class__.__name__ for unit in affected_units]
            self.game_log.add_message(
                f"Bomber sacrificed himself & exploded! ", 'attack'
            )

            # Enlever le Bomber du jeu après explosion 
            if bomber in self.player_units_p1:
                self.player_units_p1.remove(bomber)
            elif bomber in self.player_units_p2:
                self.player_units_p2.remove(bomber)
        else:           
            valid_cells = [(unit.x, unit.y) for unit in targets]
            self.draw_highlighted_cells(valid_cells)
            self.game_log.add_message("Choose a target for the bomb.", 'attack')
            self.game_log.draw()
            pygame.display.flip()

            target_chosen = False
            while not target_chosen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        target_x, target_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE
                        if (target_x, target_y) in valid_cells:
                            selected_target = targets[valid_cells.index((target_x, target_y))]
                            action_method(
                                target=selected_target,
                                all_units=self.player_units_p1 + self.player_units_p2,
                                tile_map=self.tile_map,
                                game_instance=self
                            )
                            affected_units = [unit.__class__.__name__ for unit in targets]
                            self.game_log.add_message(
                                f"Bomber threw a bomb and hit: {', '.join(affected_units)}.", 'attack'
                            )
                            target_chosen = True

>>>>>>> a45332278309099374fa68504b2a84aa243a9099
    def handle_attack_for_mage(self, mage, ally_units, opponent_units):
        valid_attacks = {}

        if mage.heal_range:
            valid_heal_targets = self.calculate_valid_heal_cells(mage, mage.heal_range, ally_units)
            if valid_heal_targets:
                valid_attacks["Heal"] = (mage.heal_allies, valid_heal_targets)

        if mage.potion_range:
            valid_attack_targets = self.calculate_valid_attack_cells(mage, mage.potion_range, opponent_units)
            if valid_attack_targets:
                valid_attacks["Potion"] = (mage.potion, valid_attack_targets)

        if not valid_attacks:
            self.game_log.add_message("No valid targets for Mage.", 'info')
            return

        self.perform_attack(mage, valid_attacks, opponent_units + ally_units) 

    def perform_attack(self, unit, valid_attacks, all_units):
        """
<<<<<<< HEAD
        Handles the selection and execution of an attack action for a unit.
        Highlights:
        - Initially, only direct cells are shown.
        - Secondary cells are shown after selecting an ability that involves them.
        """
=======
        Cette fonction exécute une attaque pour une unité donnée. 
        Elle affiche les options d'attaque valides, permet au joueur de choisir une action, 
        et applique l'effet de l'attaque sur la cible sélectionnée. Elle met à jour l'état 
        du jeu, y compris les unités affectées et le journal des événements.
        """
        
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
        if not valid_attacks:
            self.game_log.add_message(f"No valid targets for {unit.__class__.__name__}.", 'info')
            return

<<<<<<< HEAD
        # Display available attack options
        self.game_log.add_message(f"Choose an action for {unit.__class__.__name__}:", 'attack')
        attack_options = {}
        for i, (action_name, (method, targets)) in enumerate(valid_attacks.items(), start=1):
            attack_options[i] = (action_name, method, targets)
=======
        # Afficher les options d'attaque 
        self.game_log.add_message("Choose your action:", 'attack')
        attack_options = {}
        for i, (action_name, (method, targets)) in enumerate(valid_attacks.items(), start=1):
            # Extraire les positions des cibles valides 
            attack_options[i] = (method, [(target.x, target.y) for target in targets])
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
            self.game_log.add_message(f"{i}: {action_name}", 'attack')

        self.game_log.draw()
        pygame.display.flip()

<<<<<<< HEAD
        # Wait for the player to choose an attack
=======
        # Le joueur choisit une action
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
        chosen_action = None
        while chosen_action is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.unicode.isdigit():
                    action_index = int(event.unicode)
                    if action_index in attack_options:
                        chosen_action = attack_options[action_index]

        # Extract the chosen action details
        action_name, action_method, valid_targets = chosen_action

<<<<<<< HEAD
        # Calculate cells to highlight for attack
        direct_cells = [(target.x, target.y) for target in valid_targets]
        secondary_cells = []

        # If the chosen action has secondary effects, calculate them
        if hasattr(unit, 'stomp') and action_method == unit.stomp:
            for target in valid_targets:
                dx, dy = target.x - unit.x, target.y - unit.y
                secondary_cells += [
                    (target.x + dx, target.y + dy),       # Cell behind the target
                    (target.x - dy, target.y - dx),       # Perpendicular cell 1
                    (target.x + dy, target.y + dx)        # Perpendicular cell 2
                ]
        elif hasattr(unit, 'throw_bomb') and action_method == unit.throw_bomb:
            for target in valid_targets:
                secondary_cells += [
                    (target.x + dx, target.y + dy)
                    for dx in range(-1, 2)
                    for dy in range(-1, 2)
                    if (dx, dy) != (0, 0)  # Exclude the target cell itself
                ]

        # Highlight the target cells (include secondary cells only after the ability is selected)
        self.draw_highlighted_cells(direct_cells=direct_cells, secondary_cells=secondary_cells)

        # Wait for the player to select a target
=======
        # Le joueur sélectionne une cible
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
        target_chosen = False
        while not target_chosen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    target_x, target_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE

<<<<<<< HEAD
                    # Check if the selected cell matches any valid target
                    for target in valid_targets:
                        if (target.x, target.y) == (target_x, target_y):
                            # Handle special abilities with additional logic
                            if hasattr(unit, 'stomp') and action_method == unit.stomp:
                                action_method(target, all_units, self.tile_map, self)  # Pass all required context
                            elif hasattr(unit, 'throw_bomb') and action_method == unit.throw_bomb:
                                action_method(target, all_units, self.tile_map, self)
                            else:
                                action_method(target)  # Standard attacks
=======
                    # Vérifier si la case cliquée correspond à une position cible valide
                    for target in all_units:  # Valider par rapport à toutes les unités
                        if (target.x, target.y) == (target_x, target_y) and (target_x, target_y) in valid_cells:
                            # Vérifier un tir à la tête (Headshot) dans la méthode d'action
                            if hasattr(action_method, '__name__') and action_method.__name__ == "normal_arrow":
                                import random
                                headshot_probability = 0.05  # 4% de chance de Headshot
                                if random.random() < headshot_probability:
                                    target.health = 0  # Mort instantanée
                                    self.game_log.add_message(f"Headshot ! {target.__class__.__name__} died in one shot! !", 'action')
                                else:
                                    action_method(target)  # Attaque normale
                            else:
                                action_method(target)  #Exécuter l'action sélectionnée (actions autres que les flèches)
>>>>>>> a45332278309099374fa68504b2a84aa243a9099

                            # Vérifier si la cible est morte 
                            if target.health <= 0:
                                self.game_log.add_message(f"{target.__class__.__name__} has been defeated!", 'dead')
                                if target in self.player_units_p1:
                                    self.player_units_p1.remove(target)
                                elif target in self.player_units_p2:
                                    self.player_units_p2.remove(target)

                            # Log the action and end the target selection
                            self.game_log.add_message(
                                f"{unit.__class__.__name__} used {action_name} on {target.__class__.__name__}.",
                                'attack'
                            )
                            target_chosen = True

                            # Redraw the game state and update the display
                            self.redraw_static_elements()
                            self.flip_display()
                            return


<<<<<<< HEAD


    def handle_player_turn(self, player_name, opponent_units, ally_units, delta_time):
        """Handle the player's turn, including movement and attacks."""
        print(f"{player_name}'s turn started")
=======
    '''----------------------------Logique de Jeu--------------------------------------'''

    def handle_player_turn(self, player_name, opponent_units, ally_units):
        '''Cette fonction gère le tour du joueur, inclus le mouvement et les attaques'''
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
        self.game_log.add_message(f"{player_name}'s turn", 'other')
        
        # Applique les effets DoT (Damage Over Time) pour l'Archer 
        for archer in filter(lambda unit: isinstance(unit, Archer), self.player_units_p1 if player_name == "Player 1" else self.player_units_p2):
            archer.apply_dot()
       
        for selected_unit in (self.player_units_p1 if player_name == "Player 1" else self.player_units_p2):
            if self.check_game_over():
                return False

            selected_unit.is_selected = True
            self.redraw_static_elements()  # S'assurer que la grille est bien dessinée
            self.flip_display()  
            has_acted = False

            # Demander au joueur s'il veut bouger l'unité selectionnée 
            self.game_log.add_message(f"{selected_unit.__class__.__name__}'s turn. Move? (y/n)", 'mouvement')
            self.game_log.draw()
            moving = None
            while moving is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            moving = True
                        elif event.key == pygame.K_n:
                            moving = False
<<<<<<< HEAD
                            selected_unit.is_selected = False  # Deselect the unit if not moved
            # After the player answers movement (y/n), print a confirmation:
            print("Player did  responded to movement prompt")
=======
                            selected_unit.is_selected = False  

>>>>>>> a45332278309099374fa68504b2a84aa243a9099
            if moving:
                valid_cells = self.calculate_valid_cells(selected_unit)              
                while not has_acted:
<<<<<<< HEAD
                    self.screen.fill(GC.GREEN)
                    self.tile_map.draw(self.screen)
                    self.draw_collectibles()  # Draw collectibles before highlighting
                    self.draw_highlighted_cells(move_cells=valid_cells)
=======
                    self.draw_highlighted_cells(valid_cells) 

>>>>>>> a45332278309099374fa68504b2a84aa243a9099
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
                                self.update_collectibles(delta_time)
                                self.game_log.add_message(f"{selected_unit.__class__.__name__} moved", 'mouvement')
                                self.redraw_static_elements()
                                self.flip_display()

<<<<<<< HEAD

            # Determine attack logic
=======
            # Logique d'Attaque
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
            valid_attacks = []
            los_blocked = False
            in_range = False

            for opponent in opponent_units:
                for attack_range in selected_unit.ranges:
                    if selected_unit._in_range(opponent, attack_range):
                        in_range = True
                        if self.has_line_of_sight((selected_unit.x, selected_unit.y), (opponent.x, opponent.y)):
                            valid_attacks.append(opponent)
                        else:
                            los_blocked = True

            if in_range and not valid_attacks and los_blocked:
                # Ennemi dans la "Range" mais pas dans la "Line of Sight" 
                self.game_log.add_message("Enemy in range but not in sight!", 'info')
                selected_unit.is_selected = False  # Desélectionner l'unité
                self.flip_display()
                continue

            if valid_attacks:
                # Ennemi dans la "Range" et dans la "Line of Sight"
                self.game_log.add_message(f"{selected_unit.__class__.__name__}'s turn. Attack? (y/n)", 'attack')
                self.game_log.draw()
                pygame.display.flip()

                attacking = None
                while attacking is None:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_y:
                                attacking = True
                            elif event.key == pygame.K_n:
                                attacking = False
                                selected_unit.is_selected = False  # Pas d'attaque

                if attacking:
                    # Appeler la fonction d'attaque correspondante
                    if isinstance(selected_unit, Archer):
                        self.handle_attack_for_archer(selected_unit, opponent_units)
                    elif isinstance(selected_unit, Giant):
                        self.handle_attack_for_giant(selected_unit, opponent_units)
                    elif isinstance(selected_unit, Mage):
                        self.handle_attack_for_mage(selected_unit, ally_units, opponent_units)
                    elif isinstance(selected_unit, Bomber):
                        self.handle_attack_for_bomber(selected_unit, opponent_units)

                    selected_unit.is_selected = False  # Fin du tour de l'unité
                    self.redraw_static_elements()
                    self.flip_display()
                    continue

            if not in_range and not valid_attacks:
                # No range and no LoS
                self.game_log.add_message("No enemies in range.", 'info')
                selected_unit.is_selected = False  # Desélectionner l'unité
                self.flip_display()
                continue

            if in_range and not valid_attacks:
                # LoS but no range
                self.game_log.add_message("Enemy in range but abilities are out of range.", 'info')
                selected_unit.is_selected = False  # Desélectionner l'unité
                self.flip_display()
                continue

    def handle_enemy_turn(self):
        #Simple AI for the enemy's turn
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
                self.game_log.add_message('Enemy moved', 'mouvement')

            if abs(enemy.x - target.x) <= enemy.ranges and abs(enemy.y - target.y) <= enemy.ranges:
                enemy.attack(target)
                self.game_log.add_message(f"{enemy.__class__.__name__} attacked {target.__class__.__name__}!", 'attack')
                if target.health <= 0:
                    self.player_units.remove(target)
                    self.game_log.add_message(f"{target.__class__.__name__} was defeated!", 'lose')
        self.game_log.draw()
   
    def check_game_over(self):
        """Vérifie si la partie est terminée et affiche le joueur gagnant."""
        if not self.player_units_p1:
            self.game_log.add_message('Player 2 wins!', 'win')
            return True
        elif not self.player_units_p2:
            self.game_log.add_message('Player 1 wins!', 'win')
            return True
        return False

    def display_game_over(self, message):
        """Affiche un message de fin de partie et ferme le jeu"""
        font = pygame.font.Font(None, 72)
        game_over_surface = font.render(message, True, (255, 0, 0))  # Assuming RED is defined
        game_over_rect = game_over_surface.get_rect(center=(GC.WIDTH // 2, GC.HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # Pause for 3 seconds
        pygame.quit()
        exit()


    '''------------------Boucle Main-----------------------------------------------------------'''
    
def main():
    pygame.init()
    # Musique de fond
    pygame.mixer.init()
    try:
<<<<<<< HEAD
        pygame.mixer.music.load("music/music.mp3")  # Replace with your MP3 file's path
        pygame.mixer.music.play(-1)  # -1 makes it loop indefinitely
        pygame.mixer.music.set_volume(0)  # Adjust the volume (0.0 to 1.0)
=======
        pygame.mixer.music.load("music/music.mp3")  
        pygame.mixer.music.play(-1)  
        pygame.mixer.music.set_volume(0.5) 
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
    except pygame.error as e:
        print(f"Error loading music: {e}") 
         
    clock = pygame.time.Clock()
<<<<<<< HEAD
    # Initialize the screen with extra space for the game log
    screen = pygame.display.set_mode((GC.WIDTH + 500, GC.HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption("Rise of Heroes")

    rematch = False  # Tracks if the player wants a rematch
    last_time = pygame.time.get_ticks()
    while True:  # Main loop for handling restarts
=======

    # Initialiser l'écran avec un espace supplémentaire pour le Game Log
    screen = pygame.display.set_mode((GC.WIDTH + 500, GC.HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption("Rise of Heroes")

    rematch = False  # Suivre si le joueur veut une revanche.

    while True:  # Boucle principale 
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
        if not rematch:
            action = main_menu(screen)  # Afficher le menu principal
        else:
            action = "play" 

        rematch = False  

        if action == "play":
<<<<<<< HEAD
            # Directly start the game
            random_seed = random.randint(0, 1000)  # Use a random seed for map generation
            WEIGHTS = [25, 50, 10, 50, 10, 10]  # TERRAIN_TILES weights
=======
            # Lancer le jeu
            random_seed = random.randint(0, 1000)  # Utiliser une graine aléatoire pour la génération de la carte
            WEIGHTS = [25, 40, 10, 40, 10, 10]  # TERRAIN_TILES poids
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
            world = World(GC.WORLD_X, GC.WORLD_Y, random_seed)
            tile_map = world.get_tiled_map(WEIGHTS)
           

            # Créer l'instance du jeu
            game = Game(screen, tile_map)
            winner = None
            running = True
            last_time = pygame.time.get_ticks()
            while running:
<<<<<<< HEAD
                print("Main loop iteration starting...")
                current_time = pygame.time.get_ticks()
                delta_time = (current_time - last_time) / 1000.0  # Convert to seconds
                last_time = current_time
                game.redraw_static_elements()  # Draw the map and initial state
                game.update_collectibles(delta_time)  # Update collectibles
                
                # Player 1's turn
                game.handle_player_turn("Player 1", game.player_units_p2, game.player_units_p1, delta_time)
=======
                game.redraw_static_elements()  # Dessine la map et l'état initial

                # Tour du Joueur 1
                game.handle_player_turn("Player 1", game.player_units_p2, game.player_units_p1)
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
                if game.check_game_over():
                    winner = "Player 1"
                    break

<<<<<<< HEAD
                # Player 2's turn
                game.handle_player_turn("Player 2", game.player_units_p1, game.player_units_p2, delta_time)
                if game.check_game_over():
                    winner = "Player 2"
                    break
                
                game.draw_collectibles()  # Draw collectibles
                pygame.display.flip()  # Update the display once per cycle
=======
                # Tour du Joueur 2
                game.handle_player_turn("Player 2", game.player_units_p1, game.player_units_p2)
                if game.check_game_over():
                    winner = "Player 2"
                    break

                pygame.display.flip()  # Mise a jour de l'affichage une fois par cycle
>>>>>>> a45332278309099374fa68504b2a84aa243a9099
                clock.tick(60)

            # Afficher le menu de fin de jeu 
            if winner:
                action = game_over_menu(screen, winner)
                if action == "rematch":
                    rematch = True  
                elif action == "quit":
                    pygame.quit()
                    sys.exit()

        elif action == "how_to_play":
            # Afficher la page des règles du jeu
            p1_images = [
                pygame.image.load('Photos/archer.png'),
                pygame.image.load('Photos/mage.png'),
                pygame.image.load('Photos/giant.png'),
                pygame.image.load('Photos/bomber.png')
            ]
            p2_images = [
                pygame.image.load('Photos/enemy_archer.png'),
                pygame.image.load('Photos/enemy_mage.png'),
                pygame.image.load('Photos/enemy_giant.png'),
                pygame.image.load('Photos/enemy_bomber.png')
            ]
            for i in range(len(p1_images)):
                p1_images[i] = pygame.transform.scale(p1_images[i], (50, 50))
                p2_images[i] = pygame.transform.scale(p2_images[i], (50, 50))

            rules_action = rules_screen(screen, p1_images, p2_images)
            if rules_action == "back_to_menu":
                continue  # Retourner au menu principal

        elif action == "quit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()