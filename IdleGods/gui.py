import sys
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
#from IdleGods import launchAfky, launchCalcBestMonumentPath, launchCalcCreations, launchCalcDivGen, launchCalcPets, launchSkillTraining, launchUseSkills

class MyManager(ScreenManager):
    pass

class General(StackLayout):
    pass

class Choices(Screen):
    pass
    #def buttonPress(self, choice):
    #    options = {"Auto Afky": launchAfky, "Use Skills": launchUseSkills, "Calculate\nCreations": launchCalcCreations, "Pets": launchCalcPets, "Divinity\nGenerator": launchCalcDivGen, "Monuments": launchCalcBestMonumentPath,
    #               "Skill Training": launchSkillTraining, "Quit": sys.exit}
    #    options[choice]()

class Creations(StackLayout):
    pass

class Pets(Screen):
    pass

class DivinityGenerator(object):
    pass

class Monuments(object):
    pass

class Training(object):
    pass

class MainWindow(App):
    def build(self):
        Window.size = (500, 150)
        self.title = "Idle Gods Controller"
        return MyManager()