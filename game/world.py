"""
World map generation and management
"""

import random
import pygame
import math
from game.models.country import Country
from game.models.diplomacy import DiplomacySystem
from game.constants import INITIAL_COUNTRIES, GOVERNMENT_TYPES

class WorldMap:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.countries = []
        self.diplomacy = DiplomacySystem()
        self.selected_country = None
        self.player_country = None
        
        # Generate world
        self.generate_world()
        
        # Set up diplomacy
        self.diplomacy.add_countries(self.countries)
        
        # Set first country as player controlled
        if self.countries:
            self.countries[0].set_player_controlled(True)
            self.player_country = self.countries[0]
            self.selected_country = self.countries[0]
    
    def generate_world(self):
        """Generate a procedural world with countries"""
        # Generate country names
        country_names = self.generate_country_names()
        
        # Generate countries with positions
        for i in range(INITIAL_COUNTRIES):
            name = country_names[i] if i < len(country_names) else f"Nation {i+1}"
            
            # Generate position (avoid overlapping)
            x, y = self.generate_country_position()
            
            # Generate government type (bias towards democracy for variety)
            gov_types = list(GOVERNMENT_TYPES.keys())
            government_type = random.choices(
                gov_types,
                weights=[3, 1, 1, 2],  # Favor democracy and republic
                k=1
            )[0]
            
            # Create country
            country = Country(name, x, y, government_type=government_type)
            self.countries.append(country)
    
    def generate_country_names(self):
        """Generate unique country names"""
        prefixes = [
            "Astra", "Bella", "Cypher", "Delta", "Echo", "Ferro", "Gamma",
            "Hexa", "Ignis", "Jade", "Kappa", "Luna", "Magna", "Nova",
            "Omega", "Prima", "Quantum", "Radiant", "Stellar", "Terra",
            "Ultra", "Vega", "Xenon", "Yara", "Zeta"
        ]
        
        suffixes = [
            "land", "ia", "stan", "burg", "shire", "mark", "gard",
            "haven", "ford", "field", "wald", "meer", "dale", "ton"
        ]
        
        names = []
        used_names = set()
        
        while len(names) < INITIAL_COUNTRIES * 2:  # Generate extra names
            prefix = random.choice(prefixes)
            suffix = random.choice(suffixes)
            name = prefix + suffix
            
            if name not in used_names:
                names.append(name)
                used_names.add(name)
        
        return names
    
    def generate_country_position(self):
        """Generate a position for a country, avoiding overlap"""
        max_attempts = 50
        min_distance = 80
        
        for _ in range(max_attempts):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            
            # Check distance from existing countries
            too_close = False
            for country in self.countries:
                distance = math.sqrt((x - country.x)**2 + (y - country.y)**2)
                if distance < min_distance:
                    too_close = True
                    break
            
            if not too_close:
                return x, y
        
        # If we couldn't find a good position, just use a random one
        return random.randint(50, self.width - 50), random.randint(50, self.height - 50)
    
    def update(self, dt):
        """Update world state"""
        # Update all countries
        for country in self.countries:
            country.update(dt)
            
            # AI decision making for non-player countries
            if not country.is_player:
                country.ai_make_decisions()
        
        # Update diplomacy
        self.diplomacy.update_ai_diplomacy(self.countries)
        self.diplomacy.resolve_wars(self.countries)
    
    def render_map(self, surface):
        """Render the world map"""
        # Draw background
        surface.fill((50, 70, 90))  # Ocean blue-ish
        
        # Draw countries
        for country in self.countries:
            # Country circle
            radius = max(10, min(30, int(math.sqrt(country.population.total / 100000))))
            
            # Highlight selected country
            if country == self.selected_country:
                pygame.draw.circle(surface, (255, 255, 0), (int(country.x), int(country.y)), radius + 3, 2)
            
            # Country color based on government type and health
            color = country.color
            
            # Modify color based on state
            if any(rel.at_war for rel in country.relations.values()):
                # Red tint for war
                color = (min(255, color[0] + 50), max(0, color[1] - 30), max(0, color[2] - 30))
            elif country.government.stability < 30:
                # Gray tint for instability
                avg = sum(color) // 3
                color = (avg, avg, avg)
            
            pygame.draw.circle(surface, color, (int(country.x), int(country.y)), radius)
            
            # Country border
            pygame.draw.circle(surface, (255, 255, 255), (int(country.x), int(country.y)), radius, 1)
            
            # Country name
            font = pygame.font.Font(None, 20)
            text = font.render(country.name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(country.x, country.y - radius - 15))
            surface.blit(text, text_rect)
            
            # Player indicator
            if country.is_player:
                pygame.draw.circle(surface, (0, 255, 0), (int(country.x), int(country.y)), radius + 5, 2)
        
        # Draw relations (simplified)
        self.draw_relations(surface)
    
    def draw_relations(self, surface):
        """Draw lines representing diplomatic relations"""
        for relation in self.diplomacy.relations.values():
            country1 = relation.country1
            country2 = relation.country2
            
            # Only draw significant relations
            if abs(relation.relation_value) < 30:
                continue
            
            # Color based on relation type
            if relation.at_war:
                color = (255, 0, 0)  # Red for war
                width = 3
            elif relation.alliance:
                color = (0, 255, 0)  # Green for alliance
                width = 2
            elif relation.trade_deal:
                color = (0, 150, 255)  # Blue for trade
                width = 1
            elif relation.relation_value > 50:
                color = (100, 255, 100)  # Light green for good relations
                width = 1
            elif relation.relation_value < -50:
                color = (255, 100, 100)  # Light red for bad relations
                width = 1
            else:
                continue
            
            # Draw line
            start_pos = (int(country1.x), int(country1.y))
            end_pos = (int(country2.x), int(country2.y))
            pygame.draw.line(surface, color, start_pos, end_pos, width)
    
    def handle_click(self, x, y):
        """Handle mouse click on the map"""
        # Find clicked country
        for country in self.countries:
            distance = math.sqrt((x - country.x)**2 + (y - country.y)**2)
            radius = max(10, min(30, int(math.sqrt(country.population.total / 100000))))
            
            if distance <= radius:
                self.selected_country = country
                return country
        
        return None
    
    def get_country_by_name(self, name):
        """Get country by name"""
        for country in self.countries:
            if country.name == name:
                return country
        return None
    
    def get_world_stats(self):
        """Get overall world statistics"""
        total_population = sum(country.population.total for country in self.countries)
        total_gdp = sum(country.economy.gdp for country in self.countries)
        active_wars = sum(1 for relation in self.diplomacy.relations.values() if relation.at_war)
        active_alliances = sum(1 for relation in self.diplomacy.relations.values() if relation.alliance)
        
        return {
            'total_countries': len(self.countries),
            'total_population': total_population,
            'total_gdp': total_gdp,
            'active_wars': active_wars,
            'active_alliances': active_alliances,
            'player_country': self.player_country.name if self.player_country else None
        }