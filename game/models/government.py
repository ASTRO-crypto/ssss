"""
Government model for political system management
"""

import random
from game.constants import GOVERNMENT_TYPES

class PoliticalParty:
    def __init__(self, name, ideology, popularity=0.2):
        self.name = name
        self.ideology = ideology  # 'left', 'center', 'right'
        self.popularity = popularity
        self.corruption_level = random.uniform(0.1, 0.3)
        
        # Policy preferences (0-1 scale)
        if ideology == 'left':
            self.tax_preference = random.uniform(0.25, 0.45)
            self.welfare_preference = random.uniform(0.20, 0.35)
            self.military_preference = random.uniform(0.05, 0.15)
        elif ideology == 'right':
            self.tax_preference = random.uniform(0.10, 0.25)
            self.welfare_preference = random.uniform(0.05, 0.15)
            self.military_preference = random.uniform(0.15, 0.25)
        else:  # center
            self.tax_preference = random.uniform(0.15, 0.25)
            self.welfare_preference = random.uniform(0.10, 0.20)
            self.military_preference = random.uniform(0.10, 0.20)

class Government:
    def __init__(self, government_type='democracy'):
        self.type = government_type
        self.stability = 70
        self.corruption = 20
        self.years_in_power = 0
        self.next_election = GOVERNMENT_TYPES[government_type]['election_frequency']
        
        # Create political parties
        self.parties = [
            PoliticalParty("Progressive Party", "left", 0.25),
            PoliticalParty("Conservative Party", "right", 0.25),
            PoliticalParty("Centrist Alliance", "center", 0.30),
            PoliticalParty("Nationalist Party", "right", 0.20)
        ]
        
        # Current ruling party
        self.ruling_party = max(self.parties, key=lambda p: p.popularity)
        
        # Laws and policies
        self.laws = {
            'freedom_of_press': True,
            'universal_healthcare': False,
            'mandatory_education': True,
            'death_penalty': False,
            'gun_control': True,
            'environmental_protection': True
        }
        
        # Government effectiveness
        self.bureaucracy_efficiency = 60
        self.transparency = 50
        
    def update_government(self, population_approval, economic_health):
        """Update government metrics"""
        self.years_in_power += 1/12  # Assuming monthly updates
        
        # Update stability based on approval and government type
        gov_data = GOVERNMENT_TYPES[self.type]
        
        approval_effect = (population_approval - 50) * 0.2
        self.stability += approval_effect * 0.1
        
        # Add government type stability bonus
        self.stability += gov_data['stability_bonus']
        
        # Update corruption
        corruption_resistance = gov_data['corruption_resistance']
        corruption_change = random.uniform(-0.5, 1.0) * (1 - corruption_resistance)
        self.corruption = max(0, min(100, self.corruption + corruption_change))
        
        # Corruption affects stability
        self.stability -= self.corruption * 0.1
        
        self.stability = max(0, min(100, self.stability))
        
        # Update party popularity based on performance
        self.update_party_popularity(population_approval, economic_health)
        
        # Check for elections
        if self.next_election <= 0 and GOVERNMENT_TYPES[self.type]['election_frequency'] > 0:
            self.hold_election()
    
    def update_party_popularity(self, approval, economic_health):
        """Update political party popularity based on current conditions"""
        ruling_performance = (approval + economic_health) / 2
        
        # Ruling party gains/loses popularity based on performance
        performance_change = (ruling_performance - 50) * 0.002
        self.ruling_party.popularity += performance_change
        
        # Other parties gain when ruling party loses
        if performance_change < 0:
            for party in self.parties:
                if party != self.ruling_party:
                    party.popularity += abs(performance_change) / len(self.parties)
        
        # Normalize popularity
        total_popularity = sum(party.popularity for party in self.parties)
        if total_popularity > 0:
            for party in self.parties:
                party.popularity = party.popularity / total_popularity
    
    def hold_election(self):
        """Hold an election and determine the winner"""
        if GOVERNMENT_TYPES[self.type]['election_frequency'] == 0:
            return  # No elections in this government type
        
        # Add some randomness to the election
        for party in self.parties:
            party.popularity += random.uniform(-0.05, 0.05)
        
        # Normalize
        total = sum(party.popularity for party in self.parties)
        for party in self.parties:
            party.popularity = max(0, party.popularity / total)
        
        # Determine winner
        winner = max(self.parties, key=lambda p: p.popularity)
        
        if winner != self.ruling_party:
            self.ruling_party = winner
            self.years_in_power = 0
            # New government might mean policy changes
            self.stability -= 5  # Transition instability
        
        # Reset election timer
        self.next_election = GOVERNMENT_TYPES[self.type]['election_frequency']
    
    def change_government_type(self, new_type):
        """Change the type of government"""
        if new_type in GOVERNMENT_TYPES:
            old_type = self.type
            self.type = new_type
            
            # Reset some values
            self.years_in_power = 0
            self.next_election = GOVERNMENT_TYPES[new_type]['election_frequency']
            
            # Changing government type causes instability
            if old_type != new_type:
                self.stability -= random.uniform(10, 30)
                self.stability = max(0, self.stability)
    
    def pass_law(self, law_name, value):
        """Pass or repeal a law"""
        if law_name in self.laws:
            old_value = self.laws[law_name]
            self.laws[law_name] = value
            
            # Some laws affect stability
            if old_value != value:
                stability_change = random.uniform(-2, 2)
                self.stability += stability_change
    
    def trigger_political_event(self, event_type):
        """Handle political events"""
        if event_type == "corruption_scandal":
            self.corruption += random.uniform(5, 15)
            self.stability -= random.uniform(5, 10)
            self.ruling_party.popularity *= 0.9
        elif event_type == "successful_reform":
            self.corruption -= random.uniform(2, 8)
            self.stability += random.uniform(3, 8)
            self.bureaucracy_efficiency += random.uniform(2, 5)
        elif event_type == "coup_attempt":
            if self.stability < 30:
                # Coup might succeed
                if random.random() < 0.3:
                    self.change_government_type("dictatorship")
                    self.stability = 20
                else:
                    self.stability -= 15
            else:
                self.stability -= 5
        elif event_type == "protest":
            self.stability -= random.uniform(2, 8)
    
    def get_growth_modifier(self):
        """Get economic growth modifier based on government type and effectiveness"""
        base_modifier = GOVERNMENT_TYPES[self.type]['growth_modifier']
        efficiency_bonus = (self.bureaucracy_efficiency - 50) * 0.002
        stability_bonus = (self.stability - 50) * 0.001
        corruption_penalty = self.corruption * 0.001
        
        return base_modifier + efficiency_bonus + stability_bonus - corruption_penalty
    
    def get_stats(self):
        """Return dictionary of government statistics"""
        return {
            'type': self.type,
            'stability': self.stability,
            'corruption': self.corruption,
            'years_in_power': self.years_in_power,
            'next_election': self.next_election,
            'ruling_party': self.ruling_party.name,
            'ruling_party_popularity': self.ruling_party.popularity,
            'bureaucracy_efficiency': self.bureaucracy_efficiency,
            'transparency': self.transparency,
            'growth_modifier': self.get_growth_modifier(),
            'parties': [(p.name, p.popularity, p.ideology) for p in self.parties],
            'laws': self.laws.copy()
        }