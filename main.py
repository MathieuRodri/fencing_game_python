import time
import threading
import os

# --Personal Imports
from pynput import keyboard
from player import Player, Direction

GAME_SWITCH = True
GAME_MENU = True
GAME_PAUSE = False
GAME_SELECT = False
FRAME_RATE = 30

GAME_STATUS = False

os.system('cls' if os.name in ('nt', 'dos') else 'clear')
print('\nBy Mathieu RODRIGUES')
print(" _____              _               _____                      \n|  ___|            (_)             |  __ \                     \n| |_ ___ _ __   ___ _ _ __   __ _  | |  \/ __ _ _ __ ___   ___ \n|  _/ _ \ '_ \ / __| | '_ \ / _` | | | __ / _` | '_ ` _ \ / _ \\\n| ||  __/ | | | (__| | | | | (_| | | |_\ \ (_| | | | | | |  __/\n\_| \___|_| |_|\___|_|_| |_|\__, |  \____/\__,_|_| |_| |_|\___|\n                             __/ |                             \n                            |___/")
mode = input('\n1 - Terminal Version (Recommended)\n2 - Graphic Version\n\n')
if mode == '2':
    GAME_MENU = False
    from scene_tkinter import SceneTkinter as Scene
else:
    from scene_terminal import SceneTerminal as Scene


scene = Scene(Player('P1', is_player_2=False), Player('P2', is_player_2=True))


def stop_game():
    global GAME_SWITCH
    GAME_SWITCH = False


def pause_game():
    global GAME_PAUSE
    GAME_PAUSE = not GAME_PAUSE


def controller_listener():
    listener = keyboard.Listener(
        on_press=on_press)
    return listener


def on_press(key):
    global GAME_MENU, GAME_PAUSE, GAME_SELECT, GAME_SWITCH
    if GAME_MENU:
        if not GAME_SELECT:
            try:
                #   Go to left  ----------------------------
                if key == keyboard.Key.enter:
                    GAME_MENU = False
                elif key == keyboard.KeyCode.from_char('l'):
                    scene.load_from_save()
                    GAME_MENU = False
                elif key == keyboard.KeyCode.from_char('s'):
                    GAME_SELECT = True
                elif key == keyboard.KeyCode.from_char('q'):
                    GAME_MENU = False
                    stop_game()
            except AttributeError:
                pass
        else:
            if key == keyboard.Key.esc:
                GAME_SELECT = False
            else:
                try:
                    value = int(key.char)
                    if value < len(scene.scenes):
                        scene.load_scene_from_file(scene.scenes[value])
                        GAME_MENU = False
                except:
                    pass

    elif not GAME_PAUSE:
        try:
            #   Go to left  ----------------------------
            if key == keyboard.KeyCode.from_char('q'):
                threading.Thread(target=scene.P1.move, args=(
                    Direction.LEFT, scene, FRAME_RATE,)).start()
            elif key == keyboard.Key.left:
                threading.Thread(target=scene.P2.move, args=(
                    Direction.LEFT, scene, FRAME_RATE,)).start()
            #   Go to right  ---------------------------
            elif key == keyboard.KeyCode.from_char('d'):
                threading.Thread(target=scene.P1.move, args=(
                    Direction.RIGHT, scene, FRAME_RATE,)).start()
            elif key == keyboard.Key.right:
                threading.Thread(target=scene.P2.move, args=(
                    Direction.RIGHT, scene, FRAME_RATE,)).start()
            #   Jump to the left  ----------------------
            elif key == keyboard.KeyCode.from_char('a'):
                threading.Thread(target=scene.P1.jump, args=(
                    Direction.LEFT, scene, FRAME_RATE,)).start()
            elif key == keyboard.KeyCode.from_char('l'):
                threading.Thread(target=scene.P2.jump, args=(
                    Direction.LEFT, scene, FRAME_RATE,)).start()
            #   Jump to the right  ---------------------
            elif key == keyboard.KeyCode.from_char('e'):
                threading.Thread(target=scene.P1.jump, args=(
                    Direction.RIGHT, scene, FRAME_RATE,)).start()
            elif key == keyboard.KeyCode.from_char('m'):
                threading.Thread(target=scene.P2.jump, args=(
                    Direction.RIGHT, scene, FRAME_RATE,)).start()
            #   Attack  --------------------------------
            elif key == keyboard.KeyCode.from_char('z'):
                threading.Thread(target=scene.P1.attack,
                                 args=(scene.P2, FRAME_RATE, scene,)).start()
            elif key == keyboard.KeyCode.from_char('o'):
                threading.Thread(target=scene.P2.attack,
                                 args=(scene.P1, FRAME_RATE, scene,)).start()
            #   Block  ---------------------------------
            elif key == keyboard.KeyCode.from_char('s'):
                threading.Thread(target=scene.P1.block,
                                 args=(FRAME_RATE, )).start()
            elif key == keyboard.KeyCode.from_char('p'):
                threading.Thread(target=scene.P2.block,
                                 args=(FRAME_RATE, )).start()
            elif key == keyboard.Key.esc:
                pause_game()
        except AttributeError:
            pass
    else:
        try:
            #   Quit the game  ----------------------------
            if key == keyboard.KeyCode.from_char('q'):
                stop_game()
            elif key == keyboard.KeyCode.from_char('l'):
                scene.load_from_save()
                GAME_PAUSE = False
            elif key == keyboard.KeyCode.from_char('s'):
                scene.save_game()
        except AttributeError:
            pass


def start_game():
    global GAME_MENU
    listener = controller_listener()
    listener.start()
    while GAME_MENU:
        time.sleep(1/FRAME_RATE)
        if GAME_SELECT:
            scene.select_scenes()
            pass
        else:
            scene.show_start_screen()
    while GAME_SWITCH:
        time.sleep(1/FRAME_RATE)
        if not GAME_PAUSE:
            scene.display_board()
            print('\nPress \'esc\' to pause')
        else:
            scene.show_controlls()
            pass


start_game()
