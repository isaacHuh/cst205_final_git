import pyglet
from pyglet.window import key
from GameObjects import GameObject

class GameWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_location(400, 100)
		self.frame_rate =  1/60.0

		self.player = GameObject(400,200, 'plane.png')
		self.player.spd = 400;






		'''		
		anchor_x = (self.player.sprite.width/2)
		anchor_y = (self.player.sprite.height/2)
		self.player.sprite.blit(x, y)
		'''

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

		# aim control
		if symbol == key.RIGHT:
			self.player.image_angle = 5
		if symbol == key.LEFT:
			self.player.image_angle = -5

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
	
	def on_draw(self):
		self.clear()
		self.player.draw()
	
	def update_player(self,dt):
		self.player.update(dt)

		# horizontal movement
		self.player.velx = 0
		self.player.vely = 0

		if self.player.right == True:
			self.player.velx = 1
		if self.player.left == True:
			self.player.velx = -1

		# vertical movement
		if self.player.up == True:
			self.player.vely = 1
		if self.player.down == True:
			self.player.vely = -1


	def update(self, dt):
		self.update_player(dt)


if __name__ == "__main__":
	window = GameWindow(800,800, "Game Final", resizable = False)
	pyglet.clock.schedule_interval(window.update, window.frame_rate)
	pyglet.app.run()

