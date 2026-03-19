
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.uix.screen import MDScreen


class ClickableImage(CircularRippleBehavior, ButtonBehavior, Image):
    
    def __init__(self, **kwargs):
        self.ripple_scale = 0.75
        super().__init__(**kwargs)


class StartScreen(MDScreen):
    pass
