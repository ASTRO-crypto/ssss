"""
Main game UI screens and interfaces
"""

import pygame
from game.ui.ui_components import *
from game.constants import *
from game.models.diplomacy import DiplomaticAction

class GameUI:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_tab = "overview"
        
        # UI Layout
        self.map_area = pygame.Rect(0, 0, 800, 600)
        self.sidebar_area = pygame.Rect(800, 0, 400, 800)
        
        # Initialize UI components
        self.init_components()
        
        # State
        self.selected_country = None
        self.player_country = None
        self.world = None
    
    def init_components(self):
        """Initialize UI components"""
        # Tab buttons
        self.tab_buttons = {
            "overview": Button(810, 10, 80, 30, "Overview", lambda: self.set_tab("overview")),
            "economy": Button(900, 10, 80, 30, "Economy", lambda: self.set_tab("economy")),
            "diplomacy": Button(990, 10, 80, 30, "Diplomacy", lambda: self.set_tab("diplomacy")),
            "government": Button(1090, 10, 90, 30, "Government", lambda: self.set_tab("government"))
        }
        
        # Overview tab components
        self.overview_info = InfoBox(810, 50, 380, 200)
        self.stats_bars = {}
        
        # Economy tab components
        self.tax_slider = Slider(820, 100, 200, MIN_TAX_RATE, MAX_TAX_RATE, BASE_TAX_RATE, 
                               "Tax Rate", self.on_tax_change)
        
        self.budget_sliders = {
            'healthcare': Slider(820, 150, 200, 0, 0.4, 0.15, "Healthcare", 
                                lambda v: self.on_budget_change('healthcare', v)),
            'education': Slider(820, 200, 200, 0, 0.4, 0.20, "Education",
                               lambda v: self.on_budget_change('education', v)),
            'military': Slider(820, 250, 200, 0, 0.4, 0.10, "Military",
                              lambda v: self.on_budget_change('military', v)),
            'infrastructure': Slider(820, 300, 200, 0, 0.4, 0.20, "Infrastructure",
                                   lambda v: self.on_budget_change('infrastructure', v)),
            'welfare': Slider(820, 350, 200, 0, 0.4, 0.15, "Welfare",
                             lambda v: self.on_budget_change('welfare', v))
        }
        
        # Diplomacy tab components
        self.country_dropdown = Dropdown(820, 100, 200, [], self.on_country_select)
        self.diplomatic_buttons = [
            Button(820, 140, 120, 30, "Improve Relations", 
                  lambda: self.diplomatic_action(DiplomaticAction.IMPROVE_RELATIONS)),
            Button(950, 140, 120, 30, "Trade Deal", 
                  lambda: self.diplomatic_action(DiplomaticAction.TRADE_DEAL)),
            Button(820, 180, 120, 30, "Alliance", 
                  lambda: self.diplomatic_action(DiplomaticAction.ALLIANCE)),
            Button(950, 180, 120, 30, "Declare War", 
                  lambda: self.diplomatic_action(DiplomaticAction.WAR_DECLARATION)),
            Button(820, 220, 120, 30, "Peace Treaty", 
                  lambda: self.diplomatic_action(DiplomaticAction.PEACE_TREATY)),
            Button(950, 220, 120, 30, "Sanctions", 
                  lambda: self.diplomatic_action(DiplomaticAction.SANCTIONS)),
            Button(820, 260, 120, 30, "Foreign Aid", 
                  lambda: self.diplomatic_action(DiplomaticAction.FOREIGN_AID))
        ]
        
        self.diplomacy_info = InfoBox(820, 300, 360, 300)
        
        # Government tab components
        gov_types = list(GOVERNMENT_TYPES.keys())
        self.government_dropdown = Dropdown(820, 100, 200, gov_types, self.on_government_change)
        self.laws_info = InfoBox(820, 150, 360, 400)
        
        # Action buttons
        self.action_buttons = [
            Button(820, 650, 80, 30, "Pass Time", self.pass_time),
            Button(910, 650, 80, 30, "Pause", self.toggle_pause),
            Button(1000, 650, 80, 30, "Speed Up", self.speed_up)
        ]
        
        # Event log
        self.event_log = InfoBox(810, 700, 380, 90)
        
        # Game state
        self.paused = False
        self.game_speed = 1.0
    
    def set_world(self, world):
        """Set the world reference"""
        self.world = world
        self.player_country = world.player_country
        self.selected_country = world.selected_country
        self.update_country_dropdown()
    
    def set_tab(self, tab_name):
        """Switch to a different tab"""
        self.current_tab = tab_name
    
    def update_country_dropdown(self):
        """Update the diplomacy country dropdown"""
        if self.world:
            countries = [c.name for c in self.world.countries if not c.is_player]
            self.country_dropdown.options = countries
    
    def on_tax_change(self, value):
        """Handle tax rate change"""
        if self.player_country:
            self.player_country.economy.set_tax_rate(value)
    
    def on_budget_change(self, category, value):
        """Handle budget allocation change"""
        if self.player_country:
            kwargs = {category: value}
            self.player_country.economy.allocate_budget(**kwargs)
    
    def on_country_select(self, country_name):
        """Handle country selection in diplomacy"""
        if self.world:
            country = self.world.get_country_by_name(country_name)
            if country:
                self.world.selected_country = country
    
    def diplomatic_action(self, action):
        """Perform diplomatic action"""
        if not self.player_country or not self.world.selected_country:
            return
        
        if self.world.selected_country.is_player:
            return  # Can't do diplomacy with yourself
        
        success, message = self.world.diplomacy.perform_diplomatic_action(
            self.player_country, self.world.selected_country, action, player_initiated=True
        )
        
        # Add to event log
        color = GREEN if success else RED
        self.add_event(message, color)
    
    def on_government_change(self, gov_type):
        """Handle government type change"""
        if self.player_country:
            self.player_country.government.change_government_type(gov_type)
            self.add_event(f"Government changed to {GOVERNMENT_TYPES[gov_type]['name']}", YELLOW)
    
    def pass_time(self):
        """Manually advance time"""
        if self.world:
            for _ in range(30):  # Advance 30 days
                self.world.update(1.0)
    
    def toggle_pause(self):
        """Toggle game pause"""
        self.paused = not self.paused
    
    def speed_up(self):
        """Increase game speed"""
        self.game_speed = min(5.0, self.game_speed * 1.5)
    
    def add_event(self, message, color=UI_TEXT):
        """Add event to the event log"""
        self.event_log.lines.append((message, color))
        if len(self.event_log.lines) > 4:
            self.event_log.lines = self.event_log.lines[-4:]  # Keep last 4 events
    
    def handle_event(self, event):
        """Handle UI events"""
        handled = False
        
        # Handle tab buttons
        for button in self.tab_buttons.values():
            if button.handle_event(event):
                handled = True
        
        # Handle current tab components
        if self.current_tab == "economy":
            if self.tax_slider.handle_event(event):
                handled = True
            for slider in self.budget_sliders.values():
                if slider.handle_event(event):
                    handled = True
        
        elif self.current_tab == "diplomacy":
            if self.country_dropdown.handle_event(event):
                handled = True
            for button in self.diplomatic_buttons:
                if button.handle_event(event):
                    handled = True
        
        elif self.current_tab == "government":
            if self.government_dropdown.handle_event(event):
                handled = True
        
        # Handle action buttons
        for button in self.action_buttons:
            if button.handle_event(event):
                handled = True
        
        return handled
    
    def update(self, dt):
        """Update UI state"""
        if not self.world:
            return
        
        self.selected_country = self.world.selected_country
        
        # Update sliders to reflect current values
        if self.player_country:
            self.tax_slider.set_value(self.player_country.economy.tax_rate)
            
            # Update budget sliders
            economy = self.player_country.economy
            self.budget_sliders['healthcare'].set_value(economy.healthcare_spending)
            self.budget_sliders['education'].set_value(economy.education_spending)
            self.budget_sliders['military'].set_value(economy.military_spending)
            self.budget_sliders['infrastructure'].set_value(economy.infrastructure_spending)
            self.budget_sliders['welfare'].set_value(economy.welfare_spending)
        
        # Update info displays
        self.update_info_displays()
        
        # Add random events to log
        if self.player_country and self.player_country.recent_events:
            for event in self.player_country.recent_events[-1:]:  # Show latest event
                if event not in getattr(self, '_shown_events', set()):
                    self.add_event(event['description'])
                    getattr(self, '_shown_events', set()).add(event)
    
    def update_info_displays(self):
        """Update information displays"""
        if not self.selected_country:
            return
        
        country = self.selected_country
        stats = country.get_full_stats()
        
        # Overview info
        self.overview_info.clear()
        self.overview_info.add_line(f"Country: {country.name}")
        self.overview_info.add_line(f"Government: {stats['type']}")
        self.overview_info.add_line(f"Population: {stats['total']:,.0f}")
        self.overview_info.add_line(f"GDP: ${stats['gdp']:,.0f}")
        self.overview_info.add_line(f"GDP per Capita: ${stats['gdp_per_capita']:,.0f}")
        self.overview_info.add_line(f"Happiness: {stats['happiness']:.1f}%")
        self.overview_info.add_line(f"Stability: {stats['stability']:.1f}%")
        self.overview_info.add_line(f"Approval: {stats['approval_rating']:.1f}%")
        
        # Diplomacy info
        if self.current_tab == "diplomacy" and self.world:
            self.diplomacy_info.clear()
            if country != self.player_country:
                relation = self.world.diplomacy.get_relation(
                    self.player_country.name, country.name
                )
                if relation:
                    self.diplomacy_info.add_line(f"Relations: {relation.relation_value:.1f}")
                    self.diplomacy_info.add_line(f"Status: {relation.get_relation_type().name}")
                    if relation.trade_deal:
                        self.diplomacy_info.add_line("Trade Deal: Active", GREEN)
                    if relation.alliance:
                        self.diplomacy_info.add_line("Alliance: Active", GREEN)
                    if relation.at_war:
                        self.diplomacy_info.add_line("At War", RED)
                    if relation.sanctions:
                        self.diplomacy_info.add_line("Sanctions: Active", ORANGE)
        
        # Laws info
        if self.current_tab == "government":
            self.laws_info.clear()
            self.laws_info.add_line("Current Laws:")
            for law, status in stats['laws'].items():
                status_text = "Active" if status else "Inactive"
                color = GREEN if status else RED
                self.laws_info.add_line(f"{law.replace('_', ' ').title()}: {status_text}", color)
            
            self.laws_info.add_line("")
            self.laws_info.add_line("Political Parties:")
            for name, popularity, ideology in stats['parties']:
                self.laws_info.add_line(f"{name}: {popularity:.1%} ({ideology})")
    
    def render(self, surface):
        """Render the UI"""
        # Render sidebar background
        pygame.draw.rect(surface, UI_BACKGROUND, self.sidebar_area)
        
        # Render tab buttons
        for tab_name, button in self.tab_buttons.items():
            if tab_name == self.current_tab:
                # Highlight active tab
                pygame.draw.rect(surface, UI_ACCENT, button.rect)
            button.render(surface)
        
        # Render current tab content
        if self.current_tab == "overview":
            self.overview_info.render(surface)
        
        elif self.current_tab == "economy":
            # Economy controls
            font = pygame.font.Font(None, 24)
            title = font.render("Economic Controls", True, UI_TEXT)
            surface.blit(title, (820, 70))
            
            self.tax_slider.render(surface)
            
            # Budget allocation
            budget_title = font.render("Budget Allocation", True, UI_TEXT)
            surface.blit(budget_title, (820, 120))
            
            for slider in self.budget_sliders.values():
                slider.render(surface)
        
        elif self.current_tab == "diplomacy":
            # Diplomacy controls
            font = pygame.font.Font(None, 24)
            title = font.render("Diplomacy", True, UI_TEXT)
            surface.blit(title, (820, 70))
            
            self.country_dropdown.render(surface)
            
            for button in self.diplomatic_buttons:
                button.render(surface)
            
            self.diplomacy_info.render(surface)
        
        elif self.current_tab == "government":
            # Government controls
            font = pygame.font.Font(None, 24)
            title = font.render("Government", True, UI_TEXT)
            surface.blit(title, (820, 70))
            
            self.government_dropdown.render(surface)
            self.laws_info.render(surface)
        
        # Render action buttons
        for button in self.action_buttons:
            button.render(surface)
        
        # Render event log
        self.event_log.render(surface)
        
        # Render game speed indicator
        font = pygame.font.Font(None, 18)
        speed_text = f"Speed: {self.game_speed:.1f}x"
        if self.paused:
            speed_text += " (PAUSED)"
        speed_surface = font.render(speed_text, True, UI_TEXT)
        surface.blit(speed_surface, (1090, 655))