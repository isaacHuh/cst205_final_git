import pyglet

class GameObject:
	def __init__(self, posx, posy, image = None):
		self.posx = posx
		self.posy = posy
		self.right = False
		self.left = False
		self.up = False
		self.down = False
		self.image_angle = 0
		self.spd = 0
		self.velx = 0
		self.vely = 0
		if image != None:
			image = pyglet.image.load(image)
			image.anchor_x = image.width // 2
			image.anchor_y = image.height // 2
			#image.blit(x, y)
			self.sprite = pyglet.sprite.Sprite(image, x = self.posx, y = self.posy)

	def draw(self):
		self.sprite.draw()

	def update(self, dt):
		self.sprite.x += self.spd*self.velx*dt
		self.sprite.y += self.spd*self.vely*dt
		self.sprite.rotation += self.image_angle