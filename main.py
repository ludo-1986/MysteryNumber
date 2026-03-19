import os
import sys

from kivy.lang import Builder
from kivy.resources import resource_add_path

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from screens.start import StartScreen, ClickableImage
from screens.game import GameScreen


class WindowManager(MDScreenManager):
    pass


class MainApp(MDApp):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 1. On définit la racine du projet (là où se trouve main.py)
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # 2. On ajoute les dossiers importants au chemin de recherche de Kivy
        resource_add_path(base_path)
        resource_add_path(os.path.join(base_path, 'assets', 'icons'))
        resource_add_path(os.path.join(base_path, 'assets', 'images'))
    
    def build(self):
        
        # Importing KV files
        Builder.load_file("screens/start.kv")
        Builder.load_file("screens/game.kv")
        
        self.theme_cls.primary_palette = "LightGreen"
        
        self.theme_cls.theme_style = "Light"
        
        sm = WindowManager()
        sm.add_widget(StartScreen(name="home_page"))
        sm.add_widget(GameScreen(name="game_page"))
        
        return sm
    
    def switch_theme_style(self):
        
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        
        
if __name__ == "__main__":
    MainApp().run()
