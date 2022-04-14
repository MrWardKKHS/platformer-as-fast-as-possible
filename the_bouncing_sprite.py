import arcade
import math

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
        self.player.change_x = 7
        self.player.change_y = 3
        self.bullets = arcade.SpriteList()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        bullet = arcade.Sprite(":resources:gui_basic_assets/items/sword_gold.png")
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y

        adj = self._mouse_x - bullet.center_x
        opp = self._mouse_y - bullet.center_y 
        angle = math.atan2(opp, adj)
        deg = math.degrees(angle) - 90
        bullet.angle = deg

        bullet.change_x = 10 * math.cos(angle)
        bullet.change_y = 10 * math.sin(angle)
        self.bullets.append(bullet)

    def on_draw(self):
        self.clear()
        self.player.draw()
        self.bullets.draw()

    def on_update(self, delta_time: float):
        adj = self.player.center_x - self._mouse_x
        opp = self.player.center_y - self._mouse_y
        angle = math.atan2(opp, adj)
        deg = math.degrees(angle)
        self.player.angle = deg + 90
        self.bullets.update()

        self.player.update()
        # keep player from going off edge
        if self.player.center_x < 0:
            self.player.change_x *= -1
        if self.player.center_x > WIDTH:
            self.player.change_x *= -1
        if self.player.center_y < 0:
            self.player.change_y *= -1
        if self.player.center_y > HEIGHT:
            self.player.change_y *= -1
        
        # for bullet in self.bullets:
        #     if bullet.center_x < 0:
        #         bullet.change_x *= -1
        #     if bullet.center_x > WIDTH:
        #         bullet.change_x *= -1
        #     if bullet.center_y < 0:
        #         bullet.change_y *= -1
        #     if bullet.center_y > HEIGHT:
        #         bullet.change_y *= -1
        
game = MyGame()
arcade.run()