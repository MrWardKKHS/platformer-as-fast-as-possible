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
        self.scene = arcade.Scene()
        self.scene.add_sprite('player', self.player)
        
        self.scene.add_sprite_list('walls')
        for i in range(-WIDTH*2, WIDTH*2, 128): 
            wall = arcade.Sprite(':resources:images/tiles/grassMid.png', 1, center_x=i, center_y=64)
            self.scene['walls'].append(wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, walls=self.scene['walls'])
        self.camera = arcade.Camera(WIDTH, HEIGHT)


    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

    def on_update(self, delta_time: float):
        self.player.update()
        self.physics_engine.update()
        self.center_camera_on_player()

    def center_camera_on_player(self):
        camera_x = self.player.center_x - WIDTH / 2
        camera_y = self.player.center_y - HEIGHT / 2

        if self.player.center_x < WIDTH / 2:
            camera_x = 0
        if self.player.center_y < HEIGHT / 2:
            camera_y = 0
        self.camera.move_to((camera_x, camera_y))

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W and self.physics_engine.can_jump():
            self.player.change_y = 10
        # if symbol == arcade.key.S:
        #     self.player.change_y = -10
        if symbol == arcade.key.A:
            self.player.change_x = -10
        if symbol == arcade.key.D:
            self.player.change_x = 10

    def on_key_release(self, symbol: int, modifiers: int):
        # if symbol == arcade.key.W or symbol == arcade.key.S:
        #     self.player.change_y = 0
        if symbol == arcade.key.A or symbol == arcade.key.D:
            self.player.change_x = 0
        

game = MyGame()
arcade.run()