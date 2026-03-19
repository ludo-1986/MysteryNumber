from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from start import Start
from game import Game


class WindowManager(MDScreenManager):
    pass


class MainApp(MDApp):
    
    def build(self):
        
        # Importing KV files
        Builder.load_file("start.kv")
        Builder.load_file("game.kv")
        
        self.theme_cls.primary_palette = "OliveDrap"
        
        self.theme_cls.theme_style = "Light"
        
        sm = WindowManager()
        sm.add_widget(Start(name="home_page"))
        sm.add_widget(Game(name="game_page"))
        
        return sm
    
    def switch_theme_style(self):
        
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        
        
if __name__ == "_main__":
    MainApp().run()
