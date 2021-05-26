import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 15
GRAVITY = 1
PLAYER_JUMP_SPEED = 1

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

RIGHT_FACING = 0
LEFT_FACING = 1

MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 7

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()
        main_path = "images/player"
        self.idle_texture_pair = load_texture_pair(f"{main_path}player_stand_right.png")
        self.walk_textures = []
        texture = load_texture_pair("images/player/player_stand_right.png")
        self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 5 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]


class MyGame(arcade.Window):
    """ Главный класс приложения. """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0
        self.score = 0
        # self.collect_coin_sound = arcade.load_sound("sounds/get_coin.wav")
        arcade.set_background_color((0, 150, 255))

    def setup(self):
        # Инициализируем три объекта: игрок, стены, монеты
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)


        # Load textures for walking
        self.walk_textures = []
        texture = load_texture_pair("images/player/player_stand_right.png")
        self.walk_textures.append(texture)

        self.player_sprite = arcade.Sprite("images/player/player_stand_right.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)

        # Set up the player, specifically placing it at these coordinates.
        for x in range(0, 1250, 64):
            grass = arcade.Sprite("images/textures/grass.png", TILE_SCALING)
            grass.center_x = x
            grass.center_y = 32
            self.wall_list.append(grass)
        coordinate_list = [[256, 120],
                           [512, 150],
                           [750, 200]]
        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite("images/textures/block.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)
        # Use a loop to place some coins for our character to pick up
        for x in range(128, 1250, 256):
            coin = arcade.Sprite("images/textures/coin.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.coin_list.append(coin)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

        # self.walk_textures = []
        # texture = arcade.load_texture("images/player/player_stand_right.png")
        # self.walk_textures.append(texture)
        # texture = arcade.load_texture("images/player/player_stand_left.png")
        # self.walk_textures.append(texture)

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 350 + self.view_left, 550 + self.view_bottom,
                arcade.csscolor.WHITE, 30)

    def update(self, delta_time):
        # Move the player with the physics engine
        self.player_list.update_animation()
        self.physics_engine.update()

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            self.score += 1
            # arcade.play_sound(self.collect_coin_sound)

        # --- Manage Scrolling ---
        # Track if we need to change the viewport
        changed = False
        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True
        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True
        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True
        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True
        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
       """Called when the user releases a key. """
       if key == arcade.key.UP or key == arcade.key.W:
           self.player_sprite.change_y = 0
       elif key == arcade.key.DOWN or key == arcade.key.S:
           self.player_sprite.change_y = 0
       elif key == arcade.key.LEFT or key == arcade.key.A:
           # self.player_sprite = arcade.Sprite("images/player/player_stand_left.png", CHARACTER_SCALING)
           # self.player_list.append(self.player_sprite)
           texture = arcade.load_texture("images/player/player_stand_left.png", flipped_horizontally=True)
           self.player_sprite.set_texture(texture)
           self.player_sprite.change_x = 0
       elif key == arcade.key.RIGHT or key == arcade.key.D:
           self.player_sprite.change_x = 0

    # def update_animation(self, delta_time: float = 1 / 60):
    #     # Walking animation
    #     self.cur_texture += 1
    #     if self.cur_texture > 7:
    #         self.cur_texture = 0
    #     self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()