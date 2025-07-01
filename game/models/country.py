"""
Country model that integrates all systems
"""

import random
from game.models.economy import Economy
from game.models.population import Population
from game.models.government import Government

class Country:
    def __init__(self, name, x, y, population=None, gdp=None, government_type='democracy'):
        self.name = name
        self.x = x  # Map position
        self.y = y  # Map position
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        
        # Initialize population first
        initial_pop = population or random.randint(500000, 5000000)
        self.population = Population(initial_pop)
        
        # Initialize economy
        initial_gdp = gdp or (initial_pop * random.uniform(20, 80))
        self.economy = Economy(initial_gdp, initial_pop)
        
        # Initialize government
        self.government = Government(government_type)
        
        # Country traits
        self.traits = self.generate_traits()
        
        # Military
        self.military_strength = random.uniform(0.5, 1.5)
        
        # Resources
        self.natural_resources = {
            'oil': random.uniform(0, 1),
            'minerals': random.uniform(0, 1),
            'agriculture': random.uniform(0.3, 1),
            'technology': random.uniform(0.2, 0.8)
        }
        
        # Events tracking
        self.recent_events = []
        self.event_cooldown = {}
        
        # Relations with other countries (will be set by diplomacy system)
        self.relations = {}
        
        # Player country flag
        self.is_player = False
    
    def generate_traits(self):
        """Generate random country traits that affect gameplay"""
        trait_options = [
            'agricultural', 'industrial', 'technological', 'militaristic',
            'peaceful', 'corrupt', 'efficient', 'resource_rich', 'educated'
        ]
        return random.sample(trait_options, random.randint(1, 3))
    
    def update(self, dt):
        """Update all country systems"""
        # Update economy
        growth_modifier = self.government.get_growth_modifier()
        stability_bonus = (self.government.stability - 50) * 0.001
        
        # Apply trait bonuses
        if 'industrial' in self.traits:
            growth_modifier *= 1.1
        if 'technological' in self.traits:
            growth_modifier *= 1.05
        if 'agricultural' in self.traits:
            stability_bonus += 0.005
        
        self.economy.update_gdp(growth_modifier, stability_bonus)
        self.economy.update_budget()
        
        # Update population
        self.population.update_population(
            self.economy.healthcare_spending,
            self.economy.education_spending,
            self.economy.welfare_spending,
            self.economy.get_economic_health(),
            self.government.stability / 100
        )
        
        # Update government
        approval = self.population.get_approval_rating()
        economic_health = self.economy.get_economic_health()
        self.government.update_government(approval, economic_health)
        
        # Sync population count between systems
        self.economy.population = self.population.total
        
        # Check for random events
        self.check_random_events()
        
        # Clean up old events
        self.clean_old_events()
    
    def check_random_events(self):
        """Check for and trigger random events"""
        # Base event probability per update
        base_probability = 0.001  # Very low per frame
        
        # Adjust probability based on stability
        stability_factor = 1.0 + (50 - self.government.stability) / 100
        
        if random.random() < base_probability * stability_factor:
            self.trigger_random_event()
    
    def trigger_random_event(self):
        """Trigger a random event"""
        possible_events = [
            'economic_boom', 'recession', 'natural_disaster', 'epidemic',
            'corruption_scandal', 'protest', 'tech_breakthrough', 'resource_discovery'
        ]
        
        # Filter out events on cooldown
        available_events = [e for e in possible_events if e not in self.event_cooldown]
        
        if not available_events:
            return
        
        event = random.choice(available_events)
        self.handle_event(event)
        
        # Set cooldown for this event type
        self.event_cooldown[event] = 100  # Prevent same event for 100 updates
    
    def handle_event(self, event_type):
        """Handle a specific event"""
        event_description = ""
        
        if event_type == 'economic_boom':
            self.economy.trigger_economic_event('boom')
            event_description = f"{self.name} experiences an economic boom!"
        elif event_type == 'recession':
            self.economy.trigger_economic_event('recession')
            event_description = f"{self.name} enters a recession."
        elif event_type == 'natural_disaster':
            self.economy.gdp *= random.uniform(0.95, 0.98)
            self.population.handle_event('epidemic')  # Similar effects
            event_description = f"Natural disaster strikes {self.name}!"
        elif event_type == 'epidemic':
            self.population.handle_event('epidemic')
            event_description = f"Disease outbreak in {self.name}!"
        elif event_type == 'corruption_scandal':
            self.government.trigger_political_event('corruption_scandal')
            event_description = f"Corruption scandal rocks {self.name}!"
        elif event_type == 'protest':
            if self.population.trigger_protest_risk() > 0.5:
                self.government.trigger_political_event('protest')
                event_description = f"Protests break out in {self.name}!"
        elif event_type == 'tech_breakthrough':
            self.economy.trigger_economic_event('tech_breakthrough')
            event_description = f"{self.name} achieves technological breakthrough!"
        elif event_type == 'resource_discovery':
            resource = random.choice(['oil', 'minerals'])
            self.natural_resources[resource] += random.uniform(0.1, 0.3)
            self.economy.gdp *= 1.02
            event_description = f"New {resource} deposits discovered in {self.name}!"
        
        if event_description:
            self.recent_events.append({
                'description': event_description,
                'timestamp': 0  # Will be managed by game time
            })
    
    def clean_old_events(self):
        """Clean up old events and cooldowns"""
        # Decrease cooldowns
        for event in list(self.event_cooldown.keys()):
            self.event_cooldown[event] -= 1
            if self.event_cooldown[event] <= 0:
                del self.event_cooldown[event]
        
        # Keep only recent events (last 10)
        if len(self.recent_events) > 10:
            self.recent_events = self.recent_events[-10:]
    
    def set_player_controlled(self, is_player=True):
        """Set whether this country is player-controlled"""
        self.is_player = is_player
    
    def ai_make_decisions(self):
        """AI decision making for non-player countries"""
        if self.is_player:
            return
        
        # Simple AI decision making
        approval = self.population.get_approval_rating()
        economic_health = self.economy.get_economic_health()
        
        # Adjust tax rate based on approval and economic health
        if approval < 40:
            # Lower taxes to increase approval
            self.economy.set_tax_rate(self.economy.tax_rate * 0.99)
        elif economic_health < 40:
            # Might need to raise taxes for government spending
            self.economy.set_tax_rate(self.economy.tax_rate * 1.01)
        
        # Adjust budget allocation based on needs
        if self.population.health < 60:
            self.economy.allocate_budget(healthcare=min(0.25, self.economy.healthcare_spending * 1.1))
        
        if self.population.education < 60:
            self.economy.allocate_budget(education=min(0.25, self.economy.education_spending * 1.1))
        
        if approval < 30 and self.government.stability < 40:
            # Risk of unrest, might change government
            if random.random() < 0.01:  # 1% chance per update
                from game.constants import GOVERNMENT_TYPES
                new_gov = random.choice(list(GOVERNMENT_TYPES.keys()))
                self.government.change_government_type(new_gov)
    
    def get_full_stats(self):
        """Get comprehensive country statistics"""
        stats = {
            'name': self.name,
            'position': (self.x, self.y),
            'color': self.color,
            'traits': self.traits,
            'is_player': self.is_player,
            'military_strength': self.military_strength,
            'natural_resources': self.natural_resources.copy(),
            'recent_events': self.recent_events.copy()
        }
        
        # Add subsystem stats
        stats.update(self.economy.get_stats())
        stats.update(self.population.get_stats())
        stats.update(self.government.get_stats())
        
        return stats
    
    def get_power_score(self):
        """Calculate overall country power for diplomacy"""
        economic_power = self.economy.gdp / 1000000  # Scale down
        military_power = self.military_strength * (self.population.total / 1000000)
        stability_factor = self.government.stability / 100
        
        return (economic_power + military_power) * stability_factor