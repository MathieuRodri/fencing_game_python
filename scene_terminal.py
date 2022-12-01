from scene import Scene
import os
from pygame import mixer


class SceneTerminal(Scene):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)
        mixer.init()
        mixer.music.load('./songs/battleThemeA.mp3')
        mixer.music.set_volume(.1)
        mixer.music.play(loops=-1)

    def display_board(self):
        """
        Executed in a loop in main, displays on the terminal the game
        """
        import os
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')

        line = [' '*self.x_board, ] * self.y_board

        for plr in (self.P1, self.P2):
            for i in range(len(plr.state['idle']), 0, -1):
                line[-(i+plr.y_position)] = list(line[-(i+plr.y_position)])
                line[-(i+plr.y_position)][plr.x_position:plr.x_position +
                                          len(plr.state['idle'][-i])] = list(plr.state.values())[plr.id_state][-i]
                line[-(i+plr.y_position)] = ''.join(line[-(i+plr.y_position)])

        for i in range(len(self.get_board())):
            line[-1] = list(line[-1])
            if self.get_board()[i] == 'x':
                line[-1][i] = 'x'
            line[-1] = "".join(line[-1])

        line[1] = list(line[1])
        score_formated = f'{self.P1.score} | {self.P2.score}'
        line[1][self.x_board//2 - len(score_formated)//2:self.x_board//2 + len(
            score_formated) - (len(score_formated)//2)] = score_formated
        line[1] = "".join(line[1])

        print('_'*(len(line[-1])+2))
        for y in (line):
            print(f'|{y}|')
        print("#"*(len(line[-1])+2))

    def show_start_screen(self):
        """
        Executed in a loop in main, displays on the terminal the start screen
        """
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        print('\nBy Mathieu RODRIGUES')
        print(" _____              _               _____                      \n|  ___|            (_)             |  __ \                     \n| |_ ___ _ __   ___ _ _ __   __ _  | |  \/ __ _ _ __ ___   ___ \n|  _/ _ \ '_ \ / __| | '_ \ / _` | | | __ / _` | '_ ` _ \ / _ \\\n| ||  __/ | | | (__| | | | | (_| | | |_\ \ (_| | | | | | |  __/\n\_| \___|_| |_|\___|_|_| |_|\__, |  \____/\__,_|_| |_| |_|\___|\n                             __/ |                             \n                            |___/")
        print('\'enter\' to start')
        print('\'s\' to select a scene')
        print('\'l\' to load a game')
        print('\'q\' to quit')

    def show_controlls(self):
        """
        Executed in a loop in main, displays on the terminal the pause menu
        """
        p1_controlls = {
            'left': 'q',
            'right': 'd',
            'jump left': 'a',
            'jump_right': 'e',
            'attack': 'z',
            'defend': 's',
        }
        p2_controlls = {
            'left': '←',
            'right': '→',
            'jump left': 'l',
            'jump_right': 'm',
            'attack': 'o',
            'defend': 'p',
        }
        max = 0
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        print('Controlls : ')
        line = '\n'
        line += ' '*(15-2)
        line += 'Player1'
        line += ' '*(25-1-len(line))
        line += 'Player2\n'
        print(line)
        for key in p1_controlls.keys():
            line = f'{key}: '
            line += ' '*(15-len(line))
            line += f'{p1_controlls[key]}'

            line += ' '*(25-len(line))
            line += f'{p2_controlls[key]}'
            print(line)

        print('\n\'l\' to load the saved game')
        print('\'s\' to save the game')
        print('\nPress \'esc\' to resume or \'q\' to quit')

    def select_scenes(self):
        """
        Executed in a loop in main, displays on the terminal the available scenes
        """
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        print('\nSelect a scene : \n')
        for i in range(len(self.scenes)):
            print(f'{i} - {self.scenes[i]}')

        print('\nPress \'esc\' to go back')
