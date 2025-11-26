import Game, Menu
from time import sleep


def open_scene(scene_name):
    sleep(0.25)
    if scene_name == "Menu":
        Menu.Menu()
    elif scene_name == "Game":
        Game.Game()