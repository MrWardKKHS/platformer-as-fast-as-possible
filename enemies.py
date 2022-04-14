import arcade
import random

WIDTH = 600
HEIGHT = 600
TITLE = 'My game'
ENEMY_SPEED = 5

class Player(arcade.Sprite):
    def __init__(self, foldername, filename):
        super().__init__(f':resources:images/animated_characters/{foldername}/{filename}_idle.png')
        self.walk_textures = []
        self.idle_textures = arcade.load_texture_pair(f':resources:images/animated_characters/{foldername}/{filename}_idle.png')
        self.face_direction = 0
        self.current_texture = 0
        self.odo = 0

        for i in range(8):
            tex = arcade.load_texture_pair(f':resources:images/animated_characters/{foldername}/{filename}_walk{i}.png')
            self.walk_textures.append(tex)

    def update_animation(self):
        if self.change_x > 0: 
            self.face_direction = 0
        if self.change_x < 0: 
            self.face_direction = 1

        if self.change_x == 0:
            self.texture = self.idle_textures[self.face_direction]
        else:
            self.texture = self.walk_textures[self.current_texture][self.face_direction]
            self.odo += 1
            if self.odo % 4 == 0:
                self.current_texture += 1
                self.current_texture = self.current_texture % 8


class Enemy(arcade.AnimatedTimeBasedSprite):
    def __init__(self, filename, **kwargs):
        super().__init__()
        self.change_x = ENEMY_SPEED
        self.flipped_frames = None
        self.unflipped_frames = None

    def update(self, delta_time: float = 1 / 60):
        if self.flipped_frames is None:
            self.unflipped_frames = self.frames[:]
            self.flipped_frames = self.load_flipped_images()
        if self.center_x >= self.properties['right_boundary']:
            self.change_x = -ENEMY_SPEED
        if self.center_x <= self.properties['left_boundary']:
            self.change_x = ENEMY_SPEED 
        self.update_animation()
        super().update()

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0:
            self.frames = self.flipped_frames
        else:
            self.frames = self.unflipped_frames
        super().update_animation()

    def load_flipped_images(self):
        return [
            arcade.AnimationKeyframe(
                frame.tile_id, 
                frame.duration, 
                arcade.load_texture(frame.texture.name.split('.png')[0]+".png", flipped_horizontally=True) # clean filename
                ) 
                for frame in self.frames
            ]
    


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.CELADON_BLUE)
        self.player = None
        self.tilemap = None
        self.scene = None
        self.HUD = None
        self.physics_engine = None
        self.camera = None
        self.HUD_camera = None
        self.score = 0
        self.level = 0

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.bg_music = arcade.load_sound(":resources:music/funkyrobot.mp3")
        self.bg_music.play()
        self.setup()


    def setup(self):
        self.player = Player('male_person', "malePerson")
        self.player.center_x = WIDTH/2
        self.player.center_y = HEIGHT

        layer_options = {
                "enemies": {
                    "custom_class": Enemy
                },
            }

        self.tilemap = arcade.load_tilemap(f'map{self.level}.tmx', layer_options=layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tilemap)

        self.HUD = arcade.Scene()
        self.scene.add_sprite('player', self.player)
        self.HUD.add_sprite_list('health')
        self.score = 0
        
        # add mushrooms as health
        for i in range(5):
            x = 25 + 50 * i
            y = HEIGHT - 25
            mushy = arcade.Sprite(':resources:images/tiles/mushroomRed.png', 0.5, center_x=x, center_y=y)
            self.HUD['health'].append(mushy)

        # add in coins
        self.scene.add_sprite_list('coins')
        for i in range(-WIDTH*2, WIDTH**2, 128):
            # add a coin 5% of the time
            if random.random() > 0.95:
                coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.5, center_x=i, center_y=150)
                self.scene['coins'].append(coin)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, walls=self.scene['ground'])
        self.camera = arcade.Camera(WIDTH, HEIGHT)
        self.HUD_camera = arcade.Camera(WIDTH, HEIGHT)
        self.scene.move_sprite_list_after('foreground', 'player')


    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

        self.HUD_camera.use()
        self.HUD.draw()
        arcade.draw_text(f"Score: {self.score}", WIDTH-100, HEIGHT-50)

    def on_update(self, delta_time: float):
        self.scene.update()
        self.physics_engine.update()
        self.center_camera_on_player()
        colliding = arcade.check_for_collision_with_list(self.player, self.scene['coins'])
        for coin in colliding:
            coin.kill()
            self.collect_coin_sound.play()
            self.score += 1

        if self.player.center_y < 0:
            self.setup()

        colliding = arcade.check_for_collision_with_list(self.player, self.scene["don't touch"])
        if colliding:
            self.setup()
            
        colliding = arcade.check_for_collision_with_list(self.player, self.scene['enemies'])
        if colliding:
            self.setup()

        colliding = arcade.check_for_collision_with_list(self.player, self.scene["win"])
        if colliding:
            self.level += 1
            self.setup()

    def center_camera_on_player(self):
        camera_x = self.player.center_x - WIDTH / 2
        camera_y = self.player.center_y - HEIGHT / 2

        if self.player.center_x < WIDTH / 2:
            camera_x = 0
        if self.player.center_y < HEIGHT / 2:
            camera_y = 0
        self.camera.move_to((camera_x, camera_y))

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE and self.physics_engine.can_jump():
            self.player.change_y = 15
            self.jump_sound.play()
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