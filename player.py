from enum import Enum
from pygame import mixer
import time


class Direction(Enum):
    LEFT = -1
    RIGHT = 1
    BOTTOM = 0


class Player:
    username = str()
    score = 0
    x_position = int()
    y_position = 0
    is_defending = False
    is_attacking = False
    is_moving = False
    config = {
        'movement_speed': 5,
        'attacking_speed': 5,
        'attacking_range': 5,
        'defending_range': 5,
        'blocking_time': 15
    }
    id_state = 0  # Current state ex. 0:idle 1:attack etc...
    state = {
        'idle': [
            ['<o> ',  ' |_/', ' |  ', '/|  ', ],
            [' <o>', '\_| ', '  | ', '  | ', '  | ', '  | ', '  |\\', ],
        ],
        'attack': [
            ['<o> ',  ' |__', ' |  ', '/|  ', ],
            [' <o>', '__| ', '  | ', '  | ', '  | ', '  | ', '  |\\', ],
        ],
        'block': [
            ['<o> ',  ' |_|', ' |  ', '/|  ', ],
            [' <o>', '|_| ', '  | ', '  | ', '  | ', '  | ', '  |\\', ],
        ]
    }

    #  ['<o>', ' |_', ' |\033[1;32;40m \\ ', '/| '],
    #  ['<o>', ' |_\033[1;32;40m |', ' | ', '/| '],

    def __init__(self, username: str,
                 position: int = 0,
                 is_player_2: bool() = False,
                 score: int = 0):
        self.username = username
        self.x_position = position
        self.score = score
        new_state = dict.fromkeys(self.state, None)
        new_state['idle'] = self.state['idle'][is_player_2]
        new_state['attack'] = self.state['attack'][is_player_2]
        new_state['block'] = self.state['block'][is_player_2]
        self.state = new_state

    def move(self, direction: Direction, scene, frame_rate):
        """
        Move the player according to the direction in parameter

        Increment or decrement self.x_position
        """
        if not self.is_moving and self.can_go(direction, scene):
            print('move')
            self.is_moving = True
            time.sleep(self.config['movement_speed']/frame_rate)
            self.play_sound('./sfx/03_Step_grass_03.mp3')
            self.x_position += direction.value
            self.is_moving = False
        if self.y_position == 1 and self.can_go(Direction.BOTTOM, scene):
            self.y_position = 0

    def jump(self, direction, scene, frame_rate):
        """
        Move the player upward

        Increment and decrement self.y_position if possible
        """
        self.y_position = 1
        time.sleep(self.config['movement_speed']/frame_rate)
        self.move(direction, scene, frame_rate)
        time.sleep(self.config['movement_speed']/frame_rate)
        if self.can_go(Direction.BOTTOM, scene):
            self.y_position = 0

    def block(self, frame_rate):
        """
        Switches to defense mode for a period defined in the parameter
        """
        if not self.is_attacking:
            self.is_defending = True
            self.id_state = 2
            time.sleep(self.config['blocking_time']/frame_rate)
            self.id_state = 0
            self.is_defending = False

    def attack(self, other_plr, frame_rate, scene):
        """
        Performs an attack and increases the player's score if successful
        """
        if not self.is_defending:
            time.sleep(self.config['attacking_speed']/frame_rate)
            distance = abs(self.x_position - other_plr.x_position)
            self.is_attacking = True
            self.id_state = 1
            if distance <= self.config['attacking_range']:
                if other_plr.config['defending_range'] < distance or not other_plr.is_defending:
                    self.score += 1
                    scene.load_scene_from_file(scene.currentScene)

            time.sleep(1/frame_rate)
            self.id_state = 0
            self.is_attacking = False

    def can_go(self, direction, scene):
        """
        Ensures that the direction entered in parameter is possible or not
        """
        other_plr = scene.P1 if self != scene.P1 else scene.P2
        if direction != Direction.BOTTOM:
            if self.y_position == 1:
                return True
        if self == scene.P1:
            if abs((self.x_position + len(self.state['idle'][-1]) + direction.value) - (other_plr.x_position)) == 0:
                return False
        else:
            if abs((self.x_position + direction.value) - (other_plr.x_position + len(self.state['idle'][-1]))) == 0:
                return False
        for i in range(len(self.state['idle'][-1])):
            if list(scene.get_board())[self.x_position + i + direction.value] == 'x' and self.state['idle'][-1][i] != ' ':
                return False
        return True

    def play_sound(self, sound):
        """
        Plays the sound in parameter in a channel other than the background music channel
        """
        mixer.Channel(1).play(mixer.Sound(sound))
