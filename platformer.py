import arcade

WIDTH = 600
HEIGHT = 600
TITLE = 'My game'

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.CELADON_BLUE)
        self.player = arcade.Sprite(':resources:images/animated_characters/male_person/malePerson_idle.png')
        self.player.center_x = WIDTH/2
        self.player.center_y = HEIGHT/2


    def on_draw(self):
        self.clear()
        self.player.draw()

    def on_update(self, delta_time: float):
        self.player.update()

        # keep player from going off edge
        if self.player.center_x < 0:
            self.player.center_x = 0
        if self.player.center_x > WIDTH:
            self.player.center_x = WIDTH
        if self.player.center_y < 0:
            self.player.center_y = 0
        if self.player.center_y > HEIGHT:
            self.player.center_y = HEIGHT

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.player.change_y = 10
        if symbol == arcade.key.S:
            self.player.change_y = -10
        if symbol == arcade.key.A:
            self.player.change_x = -10
        if symbol == arcade.key.D:
            self.player.change_x = 10

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W or symbol == arcade.key.S:
            self.player.change_y = 0
        if symbol == arcade.key.A or symbol == arcade.key.D:
            self.player.change_x = 0
        

game = MyGame()
arcade.run()