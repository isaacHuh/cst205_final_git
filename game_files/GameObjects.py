import pyglet
from pyglet import resource

from pyglet.gl import *
glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

def preload_image(image):
	img = pyglet.image.load(image)
	return img


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
		self.scaling = False
		self.scale_spd = 0
		self.angle = 0
		
		if image != None:
			# self.image = pyglet.image.load(image)
			self.image = resource.image(image) 
			self.image.anchor_x = self.image.width // 2
			self.image.anchor_y = self.image.height // 2

			# https://gamedev.stackexchange.com/questions/20297/how-can-i-resize-pixel-art-in-pyglet-without-making-it-blurry
			self.sprite = pyglet.sprite.Sprite(self.image, x = self.posx, y = self.posy)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

	def draw(self):
		self.sprite.draw()

	def update(self, dt):
		self.sprite.x += self.spd*self.velx*dt
		self.sprite.y += self.spd*self.vely*dt
		self.sprite.rotation += self.image_angle * dt
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)


