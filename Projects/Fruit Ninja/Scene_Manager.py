import Game, Menu

def open_scene(scene_name):
    if scene_name == "Menu":
        Menu.menu()
    elif scene_name == "Game":
        Game.game()