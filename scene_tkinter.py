from scene import Scene
from pygame import mixer
import tkinter as tk


class SceneTkinter(Scene):
    root = tk.Tk()
    WIDTH = 700
    HEIGHT = 300
    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()

    image_bg = None

    img_bg = tk.PhotoImage(file="./assets/background.png")

    image_P1 = None
    image_P2 = None

    img_P1 = tk.PhotoImage(file='./assets/P1_idle.png')
    img_P2 = tk.PhotoImage(file='./assets/P2_idle.png')

    def __init__(self, p1, p2):
        super().__init__(p1, p2)
        mixer.init()
        mixer.music.load('./songs/battleThemeA.mp3')
        mixer.music.set_volume(.1)
        mixer.music.play(loops=-1)
        self.root.title("Fencing Game")
        self.image_bg = self.canvas.create_image(
            0, 0, anchor="nw", image=self.img_bg)
        self.image_P1 = self.canvas.create_image(
            0, 0, anchor="nw", image=self.img_P1)
        self.image_P2 = self.canvas.create_image(
            0, 0, anchor="nw", image=self.img_P2)

    def display_board(self):
        """
        Executed in a loop in main, displays on the terminal the game
        """
        self.canvas.moveto(self.image_P1, x=self.P1.x_position * 10,
                           y=self.HEIGHT - 65 - self.P1.y_position * 10)
        self.canvas.moveto(self.image_P2, x=self.P2.x_position * 10,
                           y=self.HEIGHT - 65 - self.P2.y_position * 10)
        self.root.update()
