import os


class Scene:
    scene = []
    defaultScene = './scenes/default.ffscene'
    currentScene = ''
    scenes = [f'./scenes/{x}' for x in os.listdir('./scenes')]
    P1 = None
    P2 = None
    x_board = 71
    y_board = 15
    save_file = "./game.save"

    def __init__(self, p1, p2):
        self.P1 = p1
        self.P2 = p2
        self.load_scene_from_file(self.defaultScene)

    def get_board(self):
        """
        Return the scene
        """
        return self.scene

    def load_scene_from_file(self, path):
        """
        Load a scene from a local file and assigns it to the variable scene
        """
        try:
            with open(path, 'r') as fp:
                self.currentScene = path
                for count, line in enumerate(fp):
                    if count == 0:
                        self.load_scene(line)
                    else:
                        self.load_scene_from_file(self.defaultScene)
                        raise Exception(
                            "Sorry, scene file not valid.\nMaybe the file contains more than 1 line")
        except Exception as e:
            print(f'{e} | Maybe an incorrect filename ?')

    def load_scene(self, line):
        """
        Load a scene from a string and assigns it to the variable scene
        """
        self.scene = ''
        self.P1.y_position = 0
        self.P2.y_position = 0
        offset = (self.x_board//2)-(len(line)//2)
        self.scene += '_'*offset
        for i, char in enumerate(line):
            if char == '1':
                self.P1.x_position = i + offset - \
                    (len(self.P1.state['idle'][-1])//2)
            elif char == '2':
                self.P2.x_position = i + offset - \
                    (len(self.P2.state['idle'][-1])//2)
            self.scene += char
        new_scene = list(self.scene)
        new_scene += '_'*(self.x_board - len(self.scene))
        self.scene = "".join(new_scene)

    def save_game(self):
        """
        Save the information of the current scene in a game.save file
        """
        with open(self.save_file, 'w') as fp:
            fp.write(str(self.currentScene)+'\n')
            fp.write(str(self.P1.x_position)+'\n')
            fp.write(str(self.P2.x_position)+'\n')
            fp.write(str(self.P1.y_position)+'\n')
            fp.write(str(self.P2.y_position)+'\n')
            fp.write(str(self.P1.score)+'\n')
            fp.write(str(self.P2.score))

    def load_from_save(self):
        """
        Loads the information contained in the game.save file
        """
        try:
            with open(self.save_file, 'r') as fp:
                data = fp.read().split('\n')
                self.currentScene = data[0]
                self.P1.x_position = int(data[1])
                self.P2.x_position = int(data[2])
                self.P1.y_position = int(data[3])
                self.P2.y_position = int(data[4])
                self.P1.score = int(data[5])
                self.P2.score = int(data[6])
        except Exception as e:
            print(f'{e} | Maybe an incorrect filename ?')
