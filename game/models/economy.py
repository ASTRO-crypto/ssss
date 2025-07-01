"""
Economy model for country management
"""

import random
from game.constants import BASE_TAX_RATE, MIN_TAX_RATE, MAX_TAX_RATE, BASE_GDP_GROWTH

class Economy:
    def __init__(self, initial_gdp=100000, initial_population=1000000):
        self.gdp = initial_gdp
        self.population = initial_population
        self.tax_rate = BASE_TAX_RATE
        self.government_budget = initial_gdp * 0.2
        self.debt = 0
        self.inflation = 0.02
        self.unemployment = 0.05
        
        # Sector breakdown
        self.agriculture = 0.15
        self.industry = 0.35
        self.services = 0.50
        
        # Economic policies
        self.interest_rate = 0.03
        self.trade_balance = 0
        
        # Budget allocation
        self.healthcare_spending = 0.15
        self.education_spending = 0.20
        self.military_spending = 0.10
        self.infrastructure_spending = 0.20
        self.welfare_spending = 0.15
        self.other_spending = 0.20
        
    def calculate_tax_revenue(self):
        """Calculate total tax revenue based on GDP and tax rate"""
        return self.gdp * self.tax_rate
    
    def calculate_gdp_per_capita(self):
        """Calculate GDP per capita"""
        return self.gdp / self.population if self.population > 0 else 0
    
    def update_gdp(self, growth_modifier=1.0, stability_bonus=0.0):
        """Update GDP based on various factors"""
        base_growth = BASE_GDP_GROWTH
        
        # Factor in unemployment (negative effect)
        unemployment_penalty = self.unemployment * 0.5
        
        # Factor in inflation (moderate inflation good, high bad)
        if self.inflation < 0.02:
            inflation_effect = 0.01
        elif self.inflation < 0.05:
            inflation_effect = 0.005
        else:
            inflation_effect = -self.inflation * 0.3
        
        # Factor in education and infrastructure spending
        education_bonus = self.education_spending * 0.1
        infrastructure_bonus = self.infrastructure_spending * 0.08
        
        total_growth = (base_growth + stability_bonus + inflation_effect + 
                       education_bonus + infrastructure_bonus - unemployment_penalty) * growth_modifier
        
        # Add some randomness
        total_growth += random.uniform(-0.01, 0.01)
        
        self.gdp *= (1 + total_growth)
        
        # Update trade balance based on economic health
        self.trade_balance = (total_growth - 0.02) * self.gdp * 0.1
        
    def set_tax_rate(self, new_rate):
        """Set new tax rate within bounds"""
        self.tax_rate = max(MIN_TAX_RATE, min(MAX_TAX_RATE, new_rate))
    
    def allocate_budget(self, healthcare=None, education=None, military=None, 
                       infrastructure=None, welfare=None):
        """Allocate government budget across different sectors"""
        if healthcare is not None:
            self.healthcare_spending = max(0, min(1, healthcare))
        if education is not None:
            self.education_spending = max(0, min(1, education))
        if military is not None:
            self.military_spending = max(0, min(1, military))
        if infrastructure is not None:
            self.infrastructure_spending = max(0, min(1, infrastructure))
        if welfare is not None:
            self.welfare_spending = max(0, min(1, welfare))
        
        # Normalize to ensure total doesn't exceed 1.0
        total = (self.healthcare_spending + self.education_spending + 
                self.military_spending + self.infrastructure_spending + 
                self.welfare_spending)
        
        if total > 1.0:
            scale = 1.0 / total
            self.healthcare_spending *= scale
            self.education_spending *= scale
            self.military_spending *= scale
            self.infrastructure_spending *= scale
            self.welfare_spending *= scale
        
        self.other_spending = max(0, 1.0 - total)
    
    def update_budget(self):
        """Update government budget based on revenue and spending"""
        revenue = self.calculate_tax_revenue()
        spending = revenue  # For now, assume spending equals revenue
        
        # Update debt if spending exceeds revenue
        if spending > revenue:
            self.debt += (spending - revenue)
        elif revenue > spending:
            # Pay down debt if surplus
            debt_payment = min(self.debt, (revenue - spending) * 0.5)
            self.debt -= debt_payment
        
        self.government_budget = revenue
    
    def get_economic_health(self):
        """Calculate overall economic health score (0-100)"""
        gdp_per_capita = self.calculate_gdp_per_capita()
        
        # Base score from GDP per capita
        base_score = min(100, gdp_per_capita / 500)  # Normalize to reasonable range
        
        # Adjust for unemployment
        unemployment_penalty = self.unemployment * 100
        
        # Adjust for inflation
        if self.inflation < 0.02:
            inflation_bonus = 10
        elif self.inflation < 0.05:
            inflation_bonus = 5
        else:
            inflation_bonus = -self.inflation * 200
        
        # Adjust for debt
        debt_ratio = self.debt / self.gdp if self.gdp > 0 else 0
        debt_penalty = min(30, debt_ratio * 50)
        
        health = base_score - unemployment_penalty + inflation_bonus - debt_penalty
        return max(0, min(100, health))
    
    def trigger_economic_event(self, event_type):
        """Handle random economic events"""
        if event_type == "recession":
            self.gdp *= 0.95
            self.unemployment += 0.02
        elif event_type == "boom":
            self.gdp *= 1.05
            self.unemployment = max(0.02, self.unemployment - 0.01)
        elif event_type == "market_crash":
            self.gdp *= 0.9
            self.unemployment += 0.03
        elif event_type == "tech_breakthrough":
            self.gdp *= 1.03
            self.unemployment = max(0.02, self.unemployment - 0.005)
    
    def get_stats(self):
        """Return dictionary of economic statistics"""
        return {
            'gdp': self.gdp,
            'gdp_per_capita': self.calculate_gdp_per_capita(),
            'tax_rate': self.tax_rate,
            'tax_revenue': self.calculate_tax_revenue(),
            'debt': self.debt,
            'unemployment': self.unemployment,
            'inflation': self.inflation,
            'trade_balance': self.trade_balance,
            'economic_health': self.get_economic_health()
        }