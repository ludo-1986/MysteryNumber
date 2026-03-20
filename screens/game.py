import random

from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty

from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
    MDDialogIcon,
)
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.screen import MDScreen


class GameScreen(MDScreen):
    
    # Les variables
    dialog_alert = None
    dialog_error = None
    dialog_final = None
    dialog_stop = None
    start_text_app_bar = "Entrez un nombre entre"
    
    max_number = NumericProperty(100)
    min_number = NumericProperty(1)
    mystery_number = NumericProperty(0)
    score = NumericProperty(1)
    user_number = NumericProperty(0)
    
    smaller_larger = StringProperty("!!! Bonne chance !!!")
    text_app_bar = StringProperty("Entrez un nombre entre")
    
    # Les fonctions de départ et d'arrêt
    def on_pre_enter(self, *args):
        
        if self.text_app_bar == self.start_text_app_bar:
            self.text_app_bar += f" {self.min_number} et {self.max_number}"
        
        self.mystery_number = random.randint(self.min_number, self.max_number)
        self.score = 1
        self.user_number = 0
        
    def stop_restart(self, dialog, page="", *args): # Ajoute *args car MDButton envoie l'instance du bouton
    
        stop_dialog = {
            "stop": self.dialog_stop,
            "final": self.dialog_final,
            "error": self.dialog_error,
            "alert": self.dialog_alert
        }
        
        pages = {
            "game": "game_page",
            "home": "home_page"
        }
        
        # 1. On ferme le dialogue d'abord pour libérer l'interface
        if stop_dialog.get(dialog):
            stop_dialog[dialog].dismiss()
            stop_dialog[dialog] = None
        
            # 2. On change d'écran après une micro-seconde (optionnel mais plus sûr)
            if page:
                if dialog == "final" and page == "game":
                    self.alert_restart()
                self.mystery_number = random.randint(self.min_number, self.max_number)
                self.score = 1
                self.user_number = 0
                self.smaller_larger = "!!! Bonne chance !!!"
                self.manager.current = pages[page]
                
    
    # Les fonctions d'alerte
    def alert_restart(self):
        
        if not self.dialog_alert:
            
            self.dialog_alert = MDDialog(
                MDDialogIcon(icon="reload"),
                MDDialogHeadlineText(text="Le jeux à été réinitialisé", role="medium"),
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="OK"),
                        style="text",
                        on_release=lambda x: self.stop_restart(dialog="alert")
                    ),
                    spacing=dp(10),
                ),
            )
        self.dialog_alert.open()
            
    def end_game(self):
        
        if not self.dialog_final:
            self.dialog_final = MDDialog(
                MDDialogIcon(icon="party-popper"),
                MDDialogHeadlineText(text=f"!!! BRAVO !!!, vous avez trouvé {self.mystery_number}"),
                MDDialogContentContainer(
                    MDLabel(
                        text="Voulez vous rejouer ?",
                        font_style="Display",
                        role="medium",
                        halign="center"
                    )
                ),
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonIcon(icon="restart"),
                        MDButtonText(text="OUI"),
                        style="text",
                        on_release=lambda x: self.stop_restart(dialog="final", page="game")
                    ),
                    MDButton(
                        MDButtonIcon(icon="location-exit"),
                        MDButtonText(text="NON"),
                        style="text",
                        on_release=lambda x: self.stop_restart(dialog="final", page="home")
                    ),
                    spacing=dp(10)
                ),
            )
        
        self.dialog_final.open()
    
    def stopped_game(self):
        
        if self.score != 1:
            if not self.dialog_stop:
                
                self.dialog_stop = MDDialog(
                    MDDialogIcon(
                        icon="cancel",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.onErrorContainerColor,
                    ),
                    MDDialogHeadlineText(text="Voulez-vous arrêter le jeux et perdre votre progression ?", role="medium"),
                    MDDialogButtonContainer(
                        MDButton(
                            MDButtonText(text="Annuler"),
                            style="text",
                            on_release=lambda x: self.stop_restart(dialog="stop")
                        ),
                        MDButton(
                            MDButtonText(text="Accepter"),
                            style="text",
                            on_release=lambda x: self.stop_restart(dialog="stop", page="home")
                        ),
                        spacing=dp(10),
                    ),
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.errorContainerColor,
                )
            self.dialog_stop.open()
            
        else:
            self.manager.current = "home_page"
        
    def dialog_error_number(self):
        
        if not self.dialog_error:
            # Création du champ interne pour pouvoir y accéder facilement
            self.number_input_field = MDTextField(
                MDTextFieldHintText(text=f"Entrez un nombre entre {self.min_number} et {self.max_number}"),
                input_filter="int",
            )

            self.dialog_error = MDDialog(
                MDDialogIcon(
                    icon="alert-circle",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.onErrorColor,
                ),
                MDDialogHeadlineText(text=f"Vous devez rentrer un nombre entre {self.min_number} et {self.max_number}"),
                MDDialogContentContainer(self.number_input_field),
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="Valider la réponse"),
                        style="text",
                        # On appelle une fonction dédiée au clic
                        on_release=self.process_dialog_number 
                    ),
                ),
                theme_bg_color="Custom",
                md_bg_color=self.theme_cls.errorContainerColor,
            )
        self.dialog_error.open()

    def process_dialog_number(self, *args):
        
        age_text = self.number_input_field.text
        
        if age_text:
            # On met à jour le champ de l'écran principal pour rester synchro
            self.ids.field_user_number.text = age_text
            self.stop_restart(dialog="error")
            # On relance la validation globale
            self.game()
    
    # Les fonctions du jeux
    def small_large(self):
        
        if self.mystery_number > self.user_number:
            self.smaller_larger = f"C'est plus grand que {self.user_number}"
        elif self.mystery_number < self.user_number:
            self.smaller_larger = f"C'est plus petit que {self.user_number}"
        else:
            self.end_game()
            
        self.ids.field_user_number.text = ""
        self.ids.field_user_number.focus = False
        self.score += 1
        
    def game(self):
        
        if not self.mystery_number:
            # Il sera réinitialisé dans la fonction "end_game"
            self.mystery_number = random.randint(self.min_number, self.max_number)
            
        user_answer = self.ids.field_user_number.text
        
        # On vérifie l'entrée de l'utilisateur
        if not user_answer:
            self.dialog_error_number()
        else:
            self.user_number = int(self.ids.field_user_number.text)
            self.small_large()
