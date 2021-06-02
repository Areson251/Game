import arcade, PlayerCharacter, time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Platformer_course-work"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

START_LEVEL = 1
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
PLAYER_MOVEMENT_SPEED = 15

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 7

PLAYER_START_X = 125
PLAYER_START_Y = 200

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)


class MyGame(arcade.Window):
    """ Главный класс приложения. """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0
        self.score = 0
        arcade.set_background_color((0, 150, 255))
        # Level
        self.level = START_LEVEL
        self.game_over = None
        self.player_sprite = PlayerCharacter.PlayerCharacter()

    def setup(self, level):
        # Инициализируем 3 объекта: стены, монеты, враги
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.enemy_list = arcade.SpriteList()

        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        coins_layer_name = 'Coins'
        self.dont_touch_list = None
        dont_touch_layer_name = "Don't Touch"
        map_name = f"maps/map_level_{level}.tmx"
        my_map = arcade.tilemap.read_tmx(map_name)
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                        layer_name = platforms_layer_name,
                                                        scaling = TILE_SCALING,
                                                        use_spatial_hash = True)
        self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name, TILE_SCALING)
        # -- Don't Touch Layer
        self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            dont_touch_layer_name,
                                                            TILE_SCALING,
                                                            use_spatial_hash=True)

        if self.level == 1:
            # -- Draw a enemy1 on the platform
            enemy1 = arcade.Sprite(":resources:images/enemies/wormGreen.png", SPRITE_SCALING)
            enemy1.bottom = SPRITE_SIZE *3.2
            enemy1.left = SPRITE_SIZE * 3
            # Set boundaries on the left/right the enemy can't cross
            enemy1.boundary_right = SPRITE_SIZE * 6
            enemy1.boundary_left = SPRITE_SIZE * 3
            enemy1.change_x = 2
            self.enemy_list.append(enemy1)

            # -- Draw a enemy2 on the platform
            enemy2 = arcade.Sprite(":resources:images/enemies/wormGreen.png", SPRITE_SCALING)
            enemy2.bottom = SPRITE_SIZE *14.2
            enemy2.left = SPRITE_SIZE * 7
            # Set boundaries on the left/right the enemy can't cross
            enemy2.boundary_right = SPRITE_SIZE * 10
            enemy2.boundary_left = SPRITE_SIZE * 7
            enemy2.change_x = 4
            self.enemy_list.append(enemy2)

            # -- Draw a enemy2 on the platform
            enemy3 = arcade.Sprite(":resources:images/enemies/wormGreen.png", SPRITE_SCALING)
            enemy3.bottom = SPRITE_SIZE *12.2
            enemy3.left = SPRITE_SIZE * 16
            # Set boundaries on the left/right the enemy can't cross
            enemy3.boundary_right = SPRITE_SIZE * 19
            enemy3.boundary_left = SPRITE_SIZE * 16
            enemy3.change_x = 1
            self.enemy_list.append(enemy3)

            # -- Draw a enemy2 on the platform
            enemy4 = arcade.Sprite(":resources:images/enemies/wormGreen.png", SPRITE_SCALING)
            enemy4.bottom = SPRITE_SIZE *5.2
            enemy4.left = SPRITE_SIZE * 10
            # Set boundaries on the left/right the enemy can't cross
            enemy4.boundary_right = SPRITE_SIZE * 13
            enemy4.boundary_left = SPRITE_SIZE * 10
            enemy4.change_x = 3
            self.enemy_list.append(enemy4)

            # -- Draw a enemy2 on the platform
            enemy5 = arcade.Sprite(":resources:images/enemies/wormGreen.png", SPRITE_SCALING)
            enemy5.bottom = SPRITE_SIZE *2.2
            enemy5.left = SPRITE_SIZE * 7
            # Set boundaries on the left/right the enemy can't cross
            enemy5.boundary_right = SPRITE_SIZE * 30
            enemy5.boundary_left = SPRITE_SIZE * 7
            enemy5.change_x = 5
            self.enemy_list.append(enemy5)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def update(self, delta_time):
        # Move the player with the physics engine
        self.player_list.update_animation()
        self.physics_engine.update()

        if self.level == 3:
            time.sleep(1000000)

        if self.game_over:
            time.sleep(3)
            self.game_over = False

        # Update the player based on the physics engine
        if not self.game_over:
            # Move the enemies
            self.enemy_list.update()

        # Check each enemy
        for enemy in self.enemy_list:
            # If the enemy hit a wall, reverse
            if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                enemy.change_x *= -1
            # If the enemy hit the left boundary, reverse
            elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                enemy.change_x *= -1
            # If the enemy hit the right boundary, reverse
            elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                enemy.change_x *= -1

        # Track if we need to change the viewport
        changed_viewport = False

        # See if player hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            self.score += 1
                # arcade.play_sound(self.collect_coin_sound)

        # See if the player hit a worm. If so, game over.
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
            self.game_over = True
        # Track if player gone away from the map
        if self.player_sprite.center_x > 1800 or self.player_sprite.center_x < -150 or self.player_sprite.center_y > 1500:
            self.game_over = True
        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(self.player_sprite, self.dont_touch_list):
            self.game_over = True

        # --- Manage Scrolling ---
        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True
        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True
        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True
        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if self.game_over:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        # next level
        if self.score == 15:
            # Advance to the next level
            self.score = 0
            self.level += 1
            # Load the next level
            if self.level==2:
                self.setup(self.level)
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        self.wall_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()
        self.dont_touch_list.draw()

        level_text = f"Level: {self.level}"
        score_text = f"Score: {self.score}"
        arcade.draw_text(level_text, 300 + self.view_left, 550 + self.view_bottom,
                         arcade.csscolor.WHITE, 30)
        arcade.draw_text(score_text, 450 + self.view_left, 550 + self.view_bottom,
                arcade.csscolor.WHITE, 30)

        if self.game_over:
            end_text = f"GAME OVER"
            arcade.draw_text(end_text, 250 + self.view_left, 300 + self.view_bottom,
                             arcade.csscolor.BLACK, 50)
            end_text = f"you will start over in 3 seconds"
            arcade.draw_text(end_text, 185 + self.view_left, 250 + self.view_bottom,
                             arcade.csscolor.BLACK, 30)

        if self.level == 3:
            end_text = f"!!!YOU WIN!!!"
            arcade.draw_text(end_text, 250 + self.view_left, 300 + self.view_bottom,
                             arcade.csscolor.BLACK, 50)


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
           self.player_sprite.change_x = 0
       elif key == arcade.key.RIGHT or key == arcade.key.D:
           self.player_sprite.change_x = 0


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup(START_LEVEL)
    arcade.run()


if __name__ == "__main__":
    main()