import arcade


RIGHT_FACING = 0
LEFT_FACING = 1


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = RIGHT_FACING

        main_path = "images/player/"
        self.idle_texture_pair = self.load_texture_pair(f"{main_path}player_stand_right.png")
        self.walk_textures = self.load_texture_pair(f"{main_path}player_stand_right.png")
        self.fly_textures = self.load_texture_pair(f"{main_path}player_fly_right.png")
        self.fall_textures = self.load_texture_pair(f"{main_path}player_fall_right.png")

    def load_texture_pair(self, filename):
        """
        Load a texture pair, with the second being a mirror image.
        """
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, mirrored=True)
        ]


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

        # Walking
        self.texture = self.walk_textures[self.character_face_direction]

        # Flying and falling
        if self.change_y > 0: #and not self.is_on_ladder:
            self.texture = self.fly_textures[self.character_face_direction]
            return
        elif self.change_y < 0: #and not self.is_on_ladder:
            self.texture = self.fall_textures[self.character_face_direction]
            return
