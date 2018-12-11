import pyglet
import colorsys
from pyglet import resource
import math
import random
from pyglet import window
from pyglet import canvas
from pyglet.window import key
from GameObjects import GameObject, preload_image
from math import atan2,degrees

platform = pyglet.window.get_platform()
display = platform.get_default_display()
default_screen = display.get_default_screen()

def point_direction(p1, p2):
    xDiff = p2[0] - p1[0]
    yDiff = p2[1] - p1[1]
    return degrees(atan2(yDiff, xDiff))

def obj_distance(obj1, obj2):
	distance = ((obj2.sprite.x - obj1.sprite.x)**2) + ((obj2.sprite.y - obj1.sprite.y)**2) 
	distance = distance**0.5
	return distance

def set_anchor(img, x, y):
	if isinstance(img, pyglet.image.Animation):
		for f in img.frames:
			f.image.anchor_x = x
			f.image.anchor_y = y
	else:
		img.anchor_x = x
		img.anchor_y = y

class GameWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.frame_rate =  1/60.0
		window.width = 1000
		window.height = 800

		screen = default_screen

		self.screen_xpos = 0
		self.screen_ypos = 0
		self.shake = 0
		self.points = 0

		self.shooting = False
		self.count = 0
		methods = ['single','autimatic']
		types = ['single','triple','double_sided']
		self.shooting_method = random.choice(methods)
		self.shooting_type = random.choice(types)

		self.player_character = GameObject(window.width/2,window.height/2,'player.png')
		self.sprite_change_occured = True
		self.player_moving = False
		self.player_xscale = 4
		self.player_yscale = 4

		self.player = GameObject(window.width/2,window.height/2, 'gun.png')
		self.player.spd = 400;
		self.player.sprite.scale = 1.5

		self.player_bullet = 'bullet_red.png'
		self.player_bullet_spd = 200
		self.player_bullet_list = []

		enemy = resource.image('enemy_running.png')
		enemy.anchor_x = (enemy.width/2) * 4
		enemy.anchor_y = (enemy.height/2) * 4
		enemy_seq = pyglet.image.ImageGrid(enemy, 1, int(enemy.width/32), item_width=32, item_height=32)
		enemy_texture = pyglet.image.TextureGrid(enemy_seq)
		self.enemy_anim = pyglet.image.Animation.from_image_sequence(enemy_texture[0:], 0.1, loop=True)
		set_anchor(self.enemy_anim,16,16)

		self.enemy = 'enemy.png'
		self.enemy_spd = 50
		self.enemy_list = []
		self.enemy_count = 0
		self.num_enemies = 0
		self.spawn_rate = random.randint(5,20)

		self.circle_black = 'circle_black.png'
		self.circle_white = 'circle_white.png'
		self.circle_list = []
		self.circle_count = 0
		self.circle_color = 0

		self.color_increase = 0
		self.color_increment = 0.01
		self.label_color = (0,0,0,255)
		self.label = pyglet.text.Label(str(self.points), 
							font_name = 'Arial',
							bold = True,
							italic = True,
							font_size = 80,
							x = window.width/2, 
							y = window.height/2,
							anchor_x = 'center',
							anchor_y = 'center',
							color = (self.label_color))

	def update_points_label(self,dt):
		self.color_increase += self.color_increment

		color = colorsys.hsv_to_rgb(self.color_increase, 0.57, 1)
		if self.color_increase == 1.0 or self.color_increase == 0.0:
			self.color_increment = -self.color_increment

		self.label.text = str(self.points)
		self.label.x = window.width/2 
		self.label.y = window.height/2
		self.label.color = (int(color[0]*255),int(color[1]*255),int(color[2]*255),255)

	def on_key_press(self, symbol, modifiers):
		# player movement
		if symbol == key.D:
			self.player.right = True
		if symbol == key.A:
			self.player.left = True
		if symbol == key.W:
			self.player.up = True
		if symbol == key.S:
			self.player.down = True

		if (symbol == key.D or symbol == key.A or symbol == key.W or symbol == key.S) and (self.player_moving == False):
			self.player_moving = True
			self.sprite_change_occured = True

		# aim control
		if symbol == key.RIGHT:
			self.player.image_angle = 400
		if symbol == key.LEFT:
			self.player.image_angle = -400

		# shooting
		if symbol == key.SPACE:
			self.count = 0
			self.shooting = True

		# leave game
		if symbol == key.ESCAPE:
			pyglet.app.exit()

	def on_key_release(self, symbol, modifiers):
		# player movement
		if symbol == key.D:
			self.player.right = False
		if symbol == key.A:
			self.player.left = False
		if symbol == key.W:
			self.player.up = False
		if symbol == key.S:
			self.player.down = False

		# aim control
		if symbol == key.RIGHT:
			self.player.image_angle = 0
		if symbol == key.LEFT:
			self.player.image_angle = 0
	
		# stop shooting
		if symbol == key.SPACE:
			self.shooting = False

	def on_draw(self):
		self.clear()
		for circle in self.circle_list:
			circle.draw()

		self.label.draw()

		for enemy in self.enemy_list:
			enemy.draw()
		for bullet in self.player_bullet_list:
			bullet.draw()
		self.player_character.draw()
		self.player.draw()
	
	def update_player(self, dt):
		self.player.update(dt)

		# horizontal movement
		self.player.velx = 0
		self.player.vely = 0

		if self.player.right == True:
			self.player.velx = 1
			self.player_xscale = 4
		if self.player.left == True:
			self.player.velx = -1
			self.player_xscale = -4

		# vertical movement
		if self.player.up == True:
			self.player.vely = 1
		if self.player.down == True:
			self.player.vely = -1

		if self.player.velx == 0 and self.player.vely == 0 and self.player_moving == True:
			self.player_moving = False
			self.sprite_change_occured = True

		# wrap around
		if self.player.sprite.x > window.width:
			self.player.sprite.x = 0
		if self.player.sprite.x < 0:
			self.player.sprite.x = window.width

		if self.player.sprite.y > window.height:
			self.player.sprite.y = 0
		if self.player.sprite.y < 0:
			self.player.sprite.y = window.height

	def bullet_type_create(self):
		if self.shooting_type == 'single':
			bullet = GameObject(self.player.sprite.x, self.player.sprite.y,self.player_bullet)
			bullet.sprite.rotation = self.player.sprite.rotation
			self.player_bullet_list.append(bullet)

		if self.shooting_type == 'double_sided':
			side = 0
			for i in range(2): 
				bullet = GameObject(self.player.sprite.x, self.player.sprite.y,self.player_bullet)
				bullet.sprite.rotation = self.player.sprite.rotation + (side*180)
				self.player_bullet_list.append(bullet)
				side += 1

		if self.shooting_type == 'triple':
			for i in range(-1,2):
				bullet = GameObject(self.player.sprite.x, self.player.sprite.y,self.player_bullet)
				bullet.sprite.rotation = self.player.sprite.rotation + (i*30)
				self.player_bullet_list.append(bullet)

	def update_shooting(self):
		# autimatic shooting
		if self.shooting:
			if (self.count % 3 == 0):
				self.bullet_type_create()
				self.shake = 10
				if (self.shooting_method == 'single'):
					self.shooting = False
		self.count += 1

	def update_player_bullet(self, dt):
		for bullet in self.player_bullet_list:
			bullet.update(dt)
			bullet.spd = self.player_bullet_spd

			#https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/programming_guide/examplegame.html
			angle_radians = -math.radians(bullet.sprite.rotation)
			force_x = math.cos(angle_radians) * dt
			force_y = math.sin(angle_radians) * dt
			bullet.velx = force_x * bullet.spd
			bullet.vely = force_y * bullet.spd

			if bullet in self.player_bullet_list:
				if bullet.sprite.y > window.height or bullet.sprite.y < 0:
					self.player_bullet_list.remove(bullet)

			if bullet in self.player_bullet_list:
				if bullet.sprite.x > window.width or bullet.sprite.x < 0:
					self.player_bullet_list.remove(bullet)

	def update_enemy_creation(self):
		if self.enemy_count % self.spawn_rate == 0 and self.num_enemies < 200:
			choice = random.choice([-1,1])

			if choice == 1:
				x_pos = random.randint(0,window.width)
				y_pos = random.choice([-100,window.height+100])
				enemy = GameObject(x_pos, y_pos, self.enemy)
			else:
				x_pos = random.choice([-100,window.width+100])
				y_pos = random.randint(0,window.height)
				enemy = GameObject(x_pos, y_pos, self.enemy)

			enemy.sprite.rotation = random.randint(0,360)
			enemy.spd = random.randint(75,100)

			enemy_sprite = pyglet.sprite.Sprite(self.enemy_anim, x = enemy.sprite.x, y = enemy.sprite.y)
			enemy_sprite.scale_x = 4
			enemy_sprite.scale_y = 4
			enemy.sprite = enemy_sprite

			self.enemy_list.append(enemy)
			self.num_enemies += 1
		self.enemy_count += 1

	def update_enemy_attributes(self, dt, scale = 4):
		for enemy in self.enemy_list:
			enemy.update(dt)

			enemy_cord = (enemy.sprite.x, enemy.sprite.y)
			player_cord = (self.player.sprite.x, self.player.sprite.y)
			ang = point_direction(enemy_cord, player_cord)
			enemy.angle = -ang
			#https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/programming_guide/examplegame.html
			angle_radians = -math.radians(enemy.angle)
			force_x = math.cos(angle_radians) * dt
			force_y = math.sin(angle_radians) * dt
			enemy.velx = force_x * enemy.spd
			enemy.vely = force_y * enemy.spd
			if self.player.sprite.x > enemy.sprite.x + 20:
				scale = 4
			if self.player.sprite.x < enemy.sprite.x - 20:
				scale = -4

			enemy.sprite.scale_x = scale
			enemy.sprite.scale_y = 4

	def enemy_bullet_collision(self):
		for enemy in self.enemy_list:
			for bullet in self.player_bullet_list:
				distance = obj_distance(enemy, bullet)
				if distance < (16*4):
					if bullet in self.player_bullet_list:
						self.player_bullet_list.remove(bullet)
					if enemy in self.enemy_list:
						self.enemy_list.remove(enemy)
						self.points += 15
						self.num_enemies -= 1
					break

	def update_screen(self):
		self.shake *= 0.9
		self.set_location(self.screen_xpos + random.uniform(-self.shake,self.shake),self.screen_ypos + random.uniform(-self.shake,self.shake))
	
	def circle_creation(self):
		if self.circle_color % 2 == 0:
			circle = GameObject(window.width/2,window.height/2,self.circle_white)
		else: 
			circle = GameObject(window.width/2,window.height/2,self.circle_black)

		self.circle_list.append(circle)
		self.circle_color += 1

	def circle_update(self, dt):
		if self.circle_count % 30 == 0:
			self.circle_creation()
		for circle in self.circle_list:
			circle.update(dt)
			circle.sprite.scale += 0.2
			circle.sprite.rotation += 1

		for circle in self.circle_list:
			if circle.sprite.width >= window.width*2:
				self.circle_list.remove(circle)
		self.circle_count += 1

	def player_character_update(self, dt):
		self.player_character.update(dt)
		if self.player_xscale > 0:
			self.player_character.sprite.x = self.player.sprite.x - self.player.sprite.width/2
			self.player_character.sprite.y = self.player.sprite.y - self.player.sprite.height/2
		else:
			self.player_character.sprite.x = self.player.sprite.x + self.player.sprite.width/2
			self.player_character.sprite.y = self.player.sprite.y - self.player.sprite.height/2

		self.player_character.sprite.scale_x = self.player_xscale
		self.player_character.sprite.scale_y = self.player_yscale

		if self.sprite_change_occured:
			if self.player_moving:
				image = 'player_running.png'
			else:
				image = 'player_idle.png'

			player = resource.image(image)
			player_seq = pyglet.image.ImageGrid(player, 1, int(player.width/32), item_width=32, item_height=32)
			player_texture = pyglet.image.TextureGrid(player_seq)
			player_anim = pyglet.image.Animation.from_image_sequence(player_texture[0:], 0.1, loop=True)
			player_sprite = pyglet.sprite.Sprite(player_anim, x = self.player_character.sprite.x, y = self.player_character.sprite.y)
			player_sprite.scale_x = self.player_xscale
			player_sprite.scale_y = self.player_yscale
			self.player_character.sprite = player_sprite
			self.sprite_change_occured = False

	def update(self, dt):
		self.update_points_label(dt)
		self.player_character_update(dt)
		self.circle_update(dt)
		self.update_screen()
		self.enemy_bullet_collision()
		self.update_enemy_creation()
		self.update_enemy_attributes(dt)
		self.update_player(dt)
		self.update_shooting()
		self.update_player_bullet(dt)

if __name__ == "__main__":
	window = GameWindow(default_screen.width,default_screen.height, "Game Final", resizable = False, style=window.Window.WINDOW_STYLE_BORDERLESS)
	window.set_fullscreen()
	pyglet.clock.schedule_interval(window.update, window.frame_rate)
	pyglet.app.run()

