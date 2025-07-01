"""
Reusable UI components
"""

import pygame
from game.constants import *

class Button:
    def __init__(self, x, y, width, height, text, callback=None, font_size=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(None, font_size)
        self.hovered = False
        self.pressed = False
        self.enabled = True
    
    def handle_event(self, event):
        if not self.enabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                if self.callback:
                    self.callback()
                return True
            self.pressed = False
        elif event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        return False
    
    def render(self, surface):
        # Button background
        if not self.enabled:
            color = DARK_GRAY
        elif self.pressed:
            color = UI_ACCENT
        elif self.hovered:
            color = UI_BUTTON_HOVER
        else:
            color = UI_BUTTON
        
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, UI_TEXT, self.rect, 1)
        
        # Button text
        text_color = UI_TEXT if self.enabled else GRAY
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val, label="", callback=None):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.callback = callback
        self.dragging = False
        self.font = pygame.font.Font(None, 20)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                return True
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_value(event.pos[0])
                return True
        
        return False
    
    def update_value(self, mouse_x):
        # Calculate value based on mouse position
        relative_x = mouse_x - self.rect.x
        relative_x = max(0, min(self.rect.width, relative_x))
        
        ratio = relative_x / self.rect.width
        self.val = self.min_val + ratio * (self.max_val - self.min_val)
        
        if self.callback:
            self.callback(self.val)
    
    def set_value(self, value):
        self.val = max(self.min_val, min(self.max_val, value))
    
    def render(self, surface):
        # Slider track
        pygame.draw.rect(surface, DARK_GRAY, self.rect)
        pygame.draw.rect(surface, UI_TEXT, self.rect, 1)
        
        # Slider handle
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + ratio * self.rect.width
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 2, 10, 24)
        pygame.draw.rect(surface, UI_ACCENT, handle_rect)
        
        # Label and value
        if self.label:
            label_text = f"{self.label}: {self.val:.3f}"
            text_surface = self.font.render(label_text, True, UI_TEXT)
            surface.blit(text_surface, (self.rect.x, self.rect.y - 25))

class Panel:
    def __init__(self, x, y, width, height, title=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.font = pygame.font.Font(None, 24)
        self.content_area = pygame.Rect(x + 10, y + 30, width - 20, height - 40)
    
    def render(self, surface):
        # Panel background
        pygame.draw.rect(surface, UI_PANEL, self.rect)
        pygame.draw.rect(surface, UI_TEXT, self.rect, 2)
        
        # Title
        if self.title:
            title_surface = self.font.render(self.title, True, UI_TEXT)
            surface.blit(title_surface, (self.rect.x + 10, self.rect.y + 5))
    
    def get_content_rect(self):
        return self.content_area

class ProgressBar:
    def __init__(self, x, y, width, height, min_val=0, max_val=100, color=GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = min_val
        self.color = color
        self.font = pygame.font.Font(None, 18)
    
    def set_value(self, value):
        self.value = max(self.min_val, min(self.max_val, value))
    
    def render(self, surface, show_text=True):
        # Background
        pygame.draw.rect(surface, DARK_GRAY, self.rect)
        pygame.draw.rect(surface, UI_TEXT, self.rect, 1)
        
        # Progress fill
        if self.value > self.min_val:
            fill_width = ((self.value - self.min_val) / (self.max_val - self.min_val)) * self.rect.width
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(surface, self.color, fill_rect)
        
        # Text
        if show_text:
            text = f"{self.value:.1f}/{self.max_val}"
            text_surface = self.font.render(text, True, UI_TEXT)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

class InfoBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 18)
        self.lines = []
    
    def add_line(self, text, color=UI_TEXT):
        self.lines.append((text, color))
    
    def clear(self):
        self.lines = []
    
    def render(self, surface):
        # Background
        pygame.draw.rect(surface, UI_PANEL, self.rect)
        pygame.draw.rect(surface, UI_TEXT, self.rect, 1)
        
        # Text lines
        y_offset = 5
        for text, color in self.lines:
            if y_offset + 20 > self.rect.height:
                break  # Don't overflow
            
            text_surface = self.font.render(text, True, color)
            surface.blit(text_surface, (self.rect.x + 5, self.rect.y + y_offset))
            y_offset += 20

class Dropdown:
    def __init__(self, x, y, width, options, callback=None, initial_selection=0):
        self.rect = pygame.Rect(x, y, width, 30)
        self.options = options
        self.callback = callback
        self.selected_index = initial_selection
        self.expanded = False
        self.font = pygame.font.Font(None, 20)
        
        # Calculate dropdown height
        self.dropdown_height = min(len(options) * 25, 150)
        self.dropdown_rect = pygame.Rect(x, y + 30, width, self.dropdown_height)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                return True
            elif self.expanded and self.dropdown_rect.collidepoint(event.pos):
                # Calculate which option was clicked
                relative_y = event.pos[1] - self.dropdown_rect.y
                option_index = relative_y // 25
                
                if 0 <= option_index < len(self.options):
                    self.selected_index = option_index
                    if self.callback:
                        self.callback(self.options[option_index])
                
                self.expanded = False
                return True
            else:
                self.expanded = False
        
        return False
    
    def get_selected(self):
        if 0 <= self.selected_index < len(self.options):
            return self.options[self.selected_index]
        return None
    
    def render(self, surface):
        # Main button
        color = UI_BUTTON_HOVER if self.expanded else UI_BUTTON
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, UI_TEXT, self.rect, 1)
        
        # Selected text
        if 0 <= self.selected_index < len(self.options):
            text = self.options[self.selected_index]
            text_surface = self.font.render(text, True, UI_TEXT)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
            surface.blit(text_surface, text_rect)
        
        # Dropdown arrow
        arrow_points = [
            (self.rect.right - 15, self.rect.centery - 3),
            (self.rect.right - 5, self.rect.centery - 3),
            (self.rect.right - 10, self.rect.centery + 3)
        ]
        pygame.draw.polygon(surface, UI_TEXT, arrow_points)
        
        # Dropdown options (if expanded)
        if self.expanded:
            pygame.draw.rect(surface, UI_PANEL, self.dropdown_rect)
            pygame.draw.rect(surface, UI_TEXT, self.dropdown_rect, 1)
            
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.dropdown_rect.x,
                    self.dropdown_rect.y + i * 25,
                    self.dropdown_rect.width,
                    25
                )
                
                # Highlight hovered option
                mouse_pos = pygame.mouse.get_pos()
                if option_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(surface, UI_BUTTON_HOVER, option_rect)
                
                text_surface = self.font.render(option, True, UI_TEXT)
                surface.blit(text_surface, (option_rect.x + 5, option_rect.y + 5))