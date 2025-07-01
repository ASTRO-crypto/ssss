"""
Population model for country management
"""

import random
from game.constants import BASE_POPULATION_GROWTH, MAX_POPULATION_GROWTH, BASE_HAPPINESS

class Population:
    def __init__(self, initial_population=1000000):
        self.total = initial_population
        self.happiness = BASE_HAPPINESS
        self.health = 70  # Average health score
        self.education = 60  # Average education level
        self.growth_rate = BASE_POPULATION_GROWTH
        
        # Age distribution (percentages)
        self.children = 0.25  # 0-17
        self.adults = 0.65    # 18-64
        self.elderly = 0.10   # 65+
        
        # Social indicators
        self.literacy_rate = 0.85
        self.life_expectancy = 75
        self.birth_rate = 0.015
        self.death_rate = 0.008
        
        # Needs satisfaction (0-100)
        self.healthcare_satisfaction = 50
        self.education_satisfaction = 50
        self.economic_satisfaction = 50
        self.security_satisfaction = 50
    
    def update_population(self, healthcare_spending, education_spending, 
                         welfare_spending, economic_health, stability):
        """Update population metrics based on government policies"""
        
        # Update health based on healthcare spending
        healthcare_effect = healthcare_spending * 50  # 0-50 bonus
        self.health = min(100, self.health + (healthcare_effect - 70) * 0.01)
        self.healthcare_satisfaction = min(100, healthcare_spending * 100)
        
        # Update education based on education spending
        education_effect = education_spending * 50  # 0-50 bonus
        self.education = min(100, self.education + (education_effect - 60) * 0.01)
        self.education_satisfaction = min(100, education_spending * 100)
        
        # Economic satisfaction based on economic health
        self.economic_satisfaction = economic_health
        
        # Security satisfaction based on stability
        self.security_satisfaction = min(100, stability * 100)
        
        # Calculate overall happiness
        self.happiness = (self.healthcare_satisfaction + self.education_satisfaction + 
                         self.economic_satisfaction + self.security_satisfaction) / 4
        
        # Update growth rate based on conditions
        base_growth = self.birth_rate - self.death_rate
        
        # Health affects birth and death rates
        health_modifier = (self.health - 70) / 100  # -0.7 to 0.3
        happiness_modifier = (self.happiness - 50) / 200  # -0.25 to 0.25
        
        self.growth_rate = base_growth + health_modifier * 0.005 + happiness_modifier * 0.003
        self.growth_rate = max(0, min(MAX_POPULATION_GROWTH, self.growth_rate))
        
        # Update population
        self.total *= (1 + self.growth_rate)
        
        # Update other metrics
        self.life_expectancy = 70 + (self.health - 70) * 0.2
        self.literacy_rate = min(1.0, 0.5 + self.education * 0.005)
    
    def handle_event(self, event_type):
        """Handle population-affecting events"""
        if event_type == "epidemic":
            self.health -= random.uniform(5, 15)
            self.happiness -= random.uniform(10, 20)
            self.total *= random.uniform(0.95, 0.98)
        elif event_type == "baby_boom":
            self.birth_rate += 0.005
            self.children += 0.02
        elif event_type == "brain_drain":
            self.education -= random.uniform(5, 10)
            self.total *= random.uniform(0.98, 0.995)
        elif event_type == "immigration_wave":
            self.total *= random.uniform(1.02, 1.05)
            self.adults += 0.01
    
    def get_approval_rating(self):
        """Calculate government approval rating based on satisfaction"""
        weights = {
            'economic': 0.35,
            'healthcare': 0.25,
            'education': 0.20,
            'security': 0.20
        }
        
        approval = (self.economic_satisfaction * weights['economic'] +
                   self.healthcare_satisfaction * weights['healthcare'] +
                   self.education_satisfaction * weights['education'] +
                   self.security_satisfaction * weights['security'])
        
        return max(0, min(100, approval))
    
    def get_workforce(self):
        """Calculate available workforce"""
        return int(self.total * self.adults)
    
    def get_dependency_ratio(self):
        """Calculate dependency ratio (non-working age / working age)"""
        dependents = self.children + self.elderly
        return dependents / self.adults if self.adults > 0 else 0
    
    def trigger_protest_risk(self):
        """Calculate risk of protests based on dissatisfaction"""
        dissatisfaction = 100 - self.happiness
        
        # Higher risk with high dissatisfaction and low security satisfaction
        base_risk = dissatisfaction / 100
        security_modifier = (100 - self.security_satisfaction) / 200
        
        protest_risk = base_risk + security_modifier
        return min(1.0, protest_risk)
    
    def get_stats(self):
        """Return dictionary of population statistics"""
        return {
            'total': self.total,
            'happiness': self.happiness,
            'health': self.health,
            'education': self.education,
            'growth_rate': self.growth_rate,
            'life_expectancy': self.life_expectancy,
            'literacy_rate': self.literacy_rate,
            'approval_rating': self.get_approval_rating(),
            'workforce': self.get_workforce(),
            'dependency_ratio': self.get_dependency_ratio(),
            'protest_risk': self.trigger_protest_risk(),
            'healthcare_satisfaction': self.healthcare_satisfaction,
            'education_satisfaction': self.education_satisfaction,
            'economic_satisfaction': self.economic_satisfaction,
            'security_satisfaction': self.security_satisfaction
        }