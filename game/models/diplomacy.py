"""
Diplomacy system for managing international relations
"""

import random
from enum import Enum

class RelationType(Enum):
    HOSTILE = -2
    POOR = -1
    NEUTRAL = 0
    FRIENDLY = 1
    ALLIED = 2

class DiplomaticAction(Enum):
    IMPROVE_RELATIONS = "improve_relations"
    WORSEN_RELATIONS = "worsen_relations"
    TRADE_DEAL = "trade_deal"
    ALLIANCE = "alliance"
    WAR_DECLARATION = "war_declaration"
    PEACE_TREATY = "peace_treaty"
    SANCTIONS = "sanctions"
    FOREIGN_AID = "foreign_aid"

class DiplomaticRelation:
    def __init__(self, country1, country2):
        self.country1 = country1
        self.country2 = country2
        self.relation_value = 0  # -100 to 100
        self.trade_deal = False
        self.alliance = False
        self.at_war = False
        self.sanctions = False
        self.trade_volume = 0
        
        # Initialize based on country traits and distance
        self.initialize_relation()
    
    def initialize_relation(self):
        """Initialize relation based on country characteristics"""
        # Distance factor (closer countries have stronger relations)
        distance = ((self.country1.x - self.country2.x)**2 + 
                   (self.country1.y - self.country2.y)**2)**0.5
        distance_factor = max(-10, -distance / 10)
        
        # Trait compatibility
        trait_factor = 0
        if 'peaceful' in self.country1.traits and 'peaceful' in self.country2.traits:
            trait_factor += 10
        if 'militaristic' in self.country1.traits and 'militaristic' in self.country2.traits:
            trait_factor -= 5
        
        # Random factor
        random_factor = random.uniform(-20, 20)
        
        self.relation_value = distance_factor + trait_factor + random_factor
        self.relation_value = max(-100, min(100, self.relation_value))
    
    def get_relation_type(self):
        """Get the categorical relation type"""
        if self.at_war:
            return RelationType.HOSTILE
        elif self.alliance:
            return RelationType.ALLIED
        elif self.relation_value >= 60:
            return RelationType.FRIENDLY
        elif self.relation_value <= -60:
            return RelationType.POOR
        else:
            return RelationType.NEUTRAL
    
    def update_relation(self, change):
        """Update relation value"""
        self.relation_value += change
        self.relation_value = max(-100, min(100, self.relation_value))
        
        # Auto-break incompatible states
        if self.relation_value < -80 and self.alliance:
            self.alliance = False
        if self.relation_value < -90 and self.trade_deal:
            self.trade_deal = False

class DiplomacySystem:
    def __init__(self):
        self.relations = {}  # (country1_name, country2_name) -> DiplomaticRelation
        self.recent_actions = []
        self.wars = []  # List of active wars
        self.trade_deals = []  # List of active trade deals
        self.alliances = []  # List of active alliances
    
    def add_countries(self, countries):
        """Initialize relations between all countries"""
        for i, country1 in enumerate(countries):
            for country2 in countries[i+1:]:
                key = self.get_relation_key(country1.name, country2.name)
                self.relations[key] = DiplomaticRelation(country1, country2)
                
                # Set up bidirectional relation references
                country1.relations[country2.name] = self.relations[key]
                country2.relations[country1.name] = self.relations[key]
    
    def get_relation_key(self, country1_name, country2_name):
        """Get standardized key for country pair"""
        return tuple(sorted([country1_name, country2_name]))
    
    def get_relation(self, country1_name, country2_name):
        """Get relation between two countries"""
        key = self.get_relation_key(country1_name, country2_name)
        return self.relations.get(key)
    
    def perform_diplomatic_action(self, actor_country, target_country, action, player_initiated=False):
        """Perform a diplomatic action"""
        relation = self.get_relation(actor_country.name, target_country.name)
        if not relation:
            return False, "No diplomatic relation exists"
        
        success = False
        message = ""
        
        if action == DiplomaticAction.IMPROVE_RELATIONS:
            # Send diplomats, cultural exchange, etc.
            improvement = random.uniform(5, 15)
            relation.update_relation(improvement)
            success = True
            message = f"{actor_country.name} improves relations with {target_country.name}"
        
        elif action == DiplomaticAction.TRADE_DEAL:
            if relation.relation_value > 20 and not relation.at_war:
                relation.trade_deal = True
                # Economic benefits for both countries
                trade_benefit = min(actor_country.economy.gdp, target_country.economy.gdp) * 0.02
                actor_country.economy.gdp += trade_benefit
                target_country.economy.gdp += trade_benefit
                success = True
                message = f"{actor_country.name} signs trade deal with {target_country.name}"
            else:
                message = "Trade deal rejected - insufficient relations"
        
        elif action == DiplomaticAction.ALLIANCE:
            if relation.relation_value > 50 and not relation.at_war:
                relation.alliance = True
                relation.update_relation(10)
                success = True
                message = f"{actor_country.name} forms alliance with {target_country.name}"
            else:
                message = "Alliance rejected - insufficient relations"
        
        elif action == DiplomaticAction.WAR_DECLARATION:
            if not relation.alliance:
                relation.at_war = True
                relation.alliance = False
                relation.trade_deal = False
                relation.update_relation(-30)
                
                # Economic impact of war
                actor_country.economy.military_spending += 0.05
                target_country.economy.military_spending += 0.05
                
                success = True
                message = f"{actor_country.name} declares war on {target_country.name}!"
            else:
                message = "Cannot declare war on ally"
        
        elif action == DiplomaticAction.PEACE_TREATY:
            if relation.at_war:
                relation.at_war = False
                relation.update_relation(20)
                
                # Reduce military spending
                actor_country.economy.military_spending = max(0.05, 
                    actor_country.economy.military_spending - 0.05)
                target_country.economy.military_spending = max(0.05,
                    target_country.economy.military_spending - 0.05)
                
                success = True
                message = f"{actor_country.name} signs peace treaty with {target_country.name}"
            else:
                message = "No active war to end"
        
        elif action == DiplomaticAction.SANCTIONS:
            if not relation.alliance and relation.relation_value < 0:
                relation.sanctions = True
                relation.trade_deal = False
                relation.update_relation(-10)
                
                # Economic impact
                target_country.economy.gdp *= 0.98
                target_country.population.happiness -= 5
                
                success = True
                message = f"{actor_country.name} imposes sanctions on {target_country.name}"
            else:
                message = "Cannot impose sanctions"
        
        elif action == DiplomaticAction.FOREIGN_AID:
            if actor_country.economy.gdp > target_country.economy.gdp * 2:
                aid_amount = actor_country.economy.gdp * 0.01
                actor_country.economy.gdp -= aid_amount
                target_country.economy.gdp += aid_amount
                relation.update_relation(15)
                
                success = True
                message = f"{actor_country.name} provides foreign aid to {target_country.name}"
            else:
                message = "Insufficient resources for foreign aid"
        
        if success:
            self.recent_actions.append({
                'actor': actor_country.name,
                'target': target_country.name,
                'action': action.value,
                'message': message,
                'player_initiated': player_initiated
            })
        
        return success, message
    
    def update_ai_diplomacy(self, countries):
        """AI countries make diplomatic decisions"""
        for country in countries:
            if country.is_player:
                continue
            
            # AI decision making based on country characteristics
            self.ai_diplomatic_decisions(country, countries)
    
    def ai_diplomatic_decisions(self, country, all_countries):
        """Make diplomatic decisions for AI country"""
        # Simple AI logic
        for other_country in all_countries:
            if other_country == country:
                continue
            
            relation = self.get_relation(country.name, other_country.name)
            if not relation:
                continue
            
            # Random chance of diplomatic action
            if random.random() < 0.02:  # 2% chance per update
                
                # Determine action based on relation and country traits
                if relation.relation_value < -70 and not relation.at_war:
                    if 'militaristic' in country.traits and random.random() < 0.3:
                        self.perform_diplomatic_action(country, other_country, 
                                                     DiplomaticAction.WAR_DECLARATION)
                
                elif relation.relation_value > 60 and not relation.alliance:
                    if 'peaceful' in country.traits and random.random() < 0.4:
                        self.perform_diplomatic_action(country, other_country,
                                                     DiplomaticAction.ALLIANCE)
                
                elif relation.relation_value > 20 and not relation.trade_deal:
                    if random.random() < 0.5:
                        self.perform_diplomatic_action(country, other_country,
                                                     DiplomaticAction.TRADE_DEAL)
                
                elif relation.relation_value < 0:
                    if random.random() < 0.3:
                        self.perform_diplomatic_action(country, other_country,
                                                     DiplomaticAction.IMPROVE_RELATIONS)
    
    def resolve_wars(self, countries):
        """Resolve ongoing wars"""
        for relation in self.relations.values():
            if relation.at_war:
                # Simple war resolution based on military strength and stability
                country1_strength = (relation.country1.military_strength * 
                                   (relation.country1.government.stability / 100))
                country2_strength = (relation.country2.military_strength * 
                                   (relation.country2.government.stability / 100))
                
                # War causes continuous damage
                relation.country1.economy.gdp *= 0.999
                relation.country2.economy.gdp *= 0.999
                relation.country1.population.happiness -= 0.1
                relation.country2.population.happiness -= 0.1
                relation.country1.government.stability -= 0.1
                relation.country2.government.stability -= 0.1
                
                # Random chance of war ending
                if random.random() < 0.01:  # 1% chance per update
                    winner = relation.country1 if country1_strength > country2_strength else relation.country2
                    loser = relation.country2 if winner == relation.country1 else relation.country1
                    
                    # War ends
                    relation.at_war = False
                    
                    # Winner gains some territory/resources (simplified)
                    winner.economy.gdp *= 1.05
                    loser.economy.gdp *= 0.95
                    
                    # Both reduce military spending
                    winner.economy.military_spending = max(0.05, winner.economy.military_spending - 0.03)
                    loser.economy.military_spending = max(0.05, loser.economy.military_spending - 0.03)
    
    def get_diplomatic_summary(self, country_name):
        """Get diplomatic summary for a country"""
        summary = {
            'relations': {},
            'wars': [],
            'alliances': [],
            'trade_deals': []
        }
        
        for key, relation in self.relations.items():
            if country_name in key:
                other_country = key[0] if key[1] == country_name else key[1]
                summary['relations'][other_country] = {
                    'value': relation.relation_value,
                    'type': relation.get_relation_type().name,
                    'at_war': relation.at_war,
                    'alliance': relation.alliance,
                    'trade_deal': relation.trade_deal,
                    'sanctions': relation.sanctions
                }
                
                if relation.at_war:
                    summary['wars'].append(other_country)
                if relation.alliance:
                    summary['alliances'].append(other_country)
                if relation.trade_deal:
                    summary['trade_deals'].append(other_country)
        
        return summary