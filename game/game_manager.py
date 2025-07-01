"""
Main game manager that coordinates all systems
"""

import pygame
from game.world import WorldMap
from game.ui.game_ui import GameUI

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Initialize game systems
        self.world = WorldMap(800, 600)  # Map area size
        self.ui = GameUI(self.screen_width, self.screen_height)
        
        # Connect UI to world
        self.ui.set_world(self.world)
        
        # Game state
        self.running = True
        self.game_time = 0
        
        # Initialize font system
        pygame.font.init()
    
    def handle_event(self, event):
        """Handle game events"""
        # First, try UI event handling
        if self.ui.handle_event(event):
            return  # UI handled the event
        
        # Handle map events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = event.pos
                
                # Check if click is in map area
                if mouse_x < 800 and mouse_y < 600:
                    clicked_country = self.world.handle_click(mouse_x, mouse_y)
                    if clicked_country:
                        self.ui.selected_country = clicked_country
        
        # Handle keyboard shortcuts
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.ui.toggle_pause()
            elif event.key == pygame.K_1:
                self.ui.set_tab("overview")
            elif event.key == pygame.K_2:
                self.ui.set_tab("economy")
            elif event.key == pygame.K_3:
                self.ui.set_tab("diplomacy")
            elif event.key == pygame.K_4:
                self.ui.set_tab("government")
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.ui.speed_up()
    
    def update(self, dt):
        """Update game state"""
        # Apply game speed and pause
        if not self.ui.paused:
            effective_dt = dt * self.ui.game_speed
            self.game_time += effective_dt
            
            # Update world
            self.world.update(effective_dt)
        
        # Update UI
        self.ui.update(dt)
    
    def render(self):
        """Render the game"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Create map surface
        map_surface = pygame.Surface((800, 600))
        self.world.render_map(map_surface)
        self.screen.blit(map_surface, (0, 0))
        
        # Render UI
        self.ui.render(self.screen)
        
        # Render debug info if needed
        self.render_debug_info()
    
    def render_debug_info(self):
        """Render debug information"""
        font = pygame.font.Font(None, 24)
        
        # Game time
        time_text = f"Game Time: {self.game_time:.1f}s"
        time_surface = font.render(time_text, True, (255, 255, 255))
        self.screen.blit(time_surface, (10, 10))
        
        # World stats
        world_stats = self.world.get_world_stats()
        stats_lines = [
            f"Countries: {world_stats['total_countries']}",
            f"Wars: {world_stats['active_wars']}",
            f"Alliances: {world_stats['active_alliances']}"
        ]
        
        for i, line in enumerate(stats_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, 40 + i * 25))
        
        # Selected country info
        if self.world.selected_country:
            country = self.world.selected_country
            selected_text = f"Selected: {country.name}"
            if country.is_player:
                selected_text += " (PLAYER)"
            
            selected_surface = font.render(selected_text, True, (255, 255, 0))
            self.screen.blit(selected_surface, (10, 570))
    
    def cleanup(self):
        """Cleanup resources"""
        # Any cleanup needed when shutting down
        pass