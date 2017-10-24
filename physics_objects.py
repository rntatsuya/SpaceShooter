# Tatsuya Yokota
# CS151s Fall 2015
# 11/11/2015

import graphics as gr
import random
import math

class Thing:
	
	def __init__(self, win, _type, position, mass, radius):
		self.type = _type
		self.mass = mass
		self.radius = radius
		self.position = position
		self.velocity = [0., 0.]
		self.acceleration = [0., 0.]
		self.force = [0., 0.]
		self.elasticity = 1.
		self.scale = 10.0
		self.win = win
		self.vis = []
		self.angle = 0.0
		self.undrawn = True

#-----------------------------------------------------------------------------------------

	def getType(self):
		return self.type
	
	def getMass(self):
		return self.mass
	
	def getRadius(self):
		return self.radius
	
	def getPosition(self):
		return self.position
	
	def getVelocity(self):
		return self.velocity
	
	def getAcceleration(self):
		return self.acceleration
	
	def getForce(self):
		return self.force
	
	def getElasticity(self):
		return self.elasticity
	
	def getScale(self):
		return scale

#-----------------------------------------------------------------------------------------
	
	def setType(self, t):
		self.type = t
	
	def setMass(self, m):
		self.mass = m
	
	def setRadius(self, r):
		self.radius = r
	
	def setPosition(self, p):
		for item in self.vis:
			dx = self.scale * (p[0] - self.position[0])
			dy = self.win.getHeight() - self.scale * (p[1] - self.position[1])
			item.move(dx, dy)
		
		self.position = [p[0], p[1]]
		
		
	def setPuttPosition(self,p, x0, y0):
		self.position = p [:]
		
		for item in self.vis:
			dx = self.position[0] * self.scale - x0
			dy = self.win.getHeight() - self.position[1] * self.scale - y0
			
			item.move(dx, dy)
	
	
	def setVelocity(self, v):
		self.velocity = v[:]
	
	def setAcceleration(self, a):
		self.acceleration = a[:]
	
	def setForce(self, f):
		self.force = f[:]
	
	def setElasticity(self, e):
		self.elasticity = e
	
	def setScale(self, s):
		scale = s

#-----------------------------------------------------------------------------------------

	def update(self, dt):
		self.position = [self.position[0] + dt * self.velocity[0], self.position[1] + dt * self.velocity[1]]

		dx = self.velocity[0] * dt * self.scale
		dy = -self.velocity[1] * dt * self.scale
		
		
		for item in self.vis:
			item.move(dx, dy)
		
		self.velocity[0] += dt * self.acceleration[0]
		self.velocity[1] += dt * self.acceleration[1]
		
		self.velocity[0] += dt * self.force[0] / self.mass
		self.velocity[1] += dt * self.force[1] / self.mass

		self.velocity[0] *= 0.998
		self.velocity[1] *= 0.998

#-----------------------------------------------------------------------------------------

	def draw(self):
		for item in self.vis:
			item.draw(self.win)
		self.undrawn = False
	
	def undraw(self):
		for item in self.vis:
			item.undraw()
		self.undrawn = True

#-----------------------------------------------------------------------------------------


class Ball(Thing):
	
	def __init__(self, win, x0, y0, mass, radius, color = 'blue'):
		Thing.__init__(self, win, "ball", position = [x0, y0], mass = mass, radius = radius)
		
		self.vis = [ gr.Circle( gr.Point(self.position[0]*self.scale,
										win.getHeight()-self.position[1]*self.scale),
								self.radius * self.scale ) ]
		
		self.vis[0].setFill(color)
#-----------------------------------------------------------------------------------------



class Floor(Thing):
	
	def __init__(self, win, x0, y0, length, thickness, color = 'blue'):
		Thing.__init__(self, win, "floor", position = [x0, y0], mass = 1 , radius = 0)
		
		self.width = length
		self.height = thickness
		
		self.vis = [ gr.Rectangle( 	gr.Point( x0 * self.scale, win.getHeight() - (y0 + self.height/2) * self.scale), 
							gr.Point( (x0 + self.width) * self.scale, 
									win.getHeight() - (y0 - self.height/2) * self.scale) )]
		
		self.vis[0].setFill(color)
	
	def getHeight(self):
		return self.height
	
	def getWidth(self):
		return self.width
		
	
#-----------------------------------------------------------------------------------------

class Wall(Thing):
	
	def __init__(self, win, x0, y0, height, thickness, color = 'blue'):
		Thing.__init__(self, win, "wall", position = [x0, y0], mass = 0, radius = 0)		
		
		self.height = height
		self.width = thickness
		
		self.vis = [ gr.Rectangle( 	gr.Point((x0 - self.width/2)*self.scale, win.getHeight() - y0 * self.scale), 
									gr.Point( (x0+self.width/2)*self.scale, win.getHeight() - (y0 + self.height) * self.scale) )]
	
		self.vis[0].setFill(color)
		
	def getHeight(self):
		return self.height
	
	def getWidth(self):
		return self.width
		
#-----------------------------------------------------------------------------------------

class Block(Thing):
	
	def __init__(self, win, x0, y0, width, height, color = 'blue', mass = 1, radius = 0):
		Thing.__init__(self, win, "block", position = [x0, y0], mass = mass, radius = radius)
		
		self.width = width
		self.height = height
		self.x0 = x0
		self.y0 = y0
		
		self.vis = [ gr.Rectangle( gr.Point((x0-self.width/2)*self.scale, win.getHeight() - (y0-self.height/2)*self.scale), 
								gr.Point((x0+self.width/2)*self.scale, win.getHeight() - (y0+self.height/2)*self.scale)) ]

		self.bodypts = [[(x0-self.width/2)*self.scale, win.getHeight() - (y0-self.height/2)*self.scale, 
								(x0+self.width/2)*self.scale, win.getHeight() - (y0+self.height/2)*self.scale]]
		self.vis[0].setFill(color)
		

	def getWidth(self):
		return self.width
		
	def getHeight(self):
		return self.height	
	
	def render(self):

		# get the cos and sin of the current orientation
		theta = math.pi * self.angle / 180.
		cth = math.cos(theta)
		sth = math.sin(theta)

		# rotate each point around the object's center
		pts = []
		for vertex in self.bodypts:
			# move the object's center to 0, 0, which it is already in model coordinates
			xt = vertex[0]
			yt = vertex[1]

			# rotate the vertex by theta around the Z axis
			xtt = cth*xt - sth*yt
			ytt = sth*xt + cth*yt

			# move the object's center back to its original location
			xf = xtt + self.position[0]
			yf = ytt + self.position[1]

			# create a point with the screen space coordinates
			pts.append( gr.Point(self.scale * xf, self.win.getHeight() - self.scale * yf) )

		# make the two objects
		self.vis = [  gr.Rectangle( gr.Point((self.x0-self.width/2)*self.scale, self.win.getHeight() - (self.y0-self.height/2)*self.scale), 
								gr.Point((self.x0+self.width/2)*self.scale, self.win.getHeight() - (self.y0+self.height/2)*self.scale)) ]

	
	
	
	def draw(self):
		for item in self.vis:
			item.undraw()
		self.render()
		for item in self.vis:
			item.draw(self.win)
		self.drawn = True
		
#-----------------------------------------------------------------------------------------

class Octagon(Thing):
	
	def __init__(self, win, x0, y0, width, height, color = 'blue'):
		Thing.__init__(self, win, "ball", position = [x0, y0], mass = 5, radius = width/2)
		
		self.width = width
		self.height = height
		
		self.vis = [ gr.Polygon( gr.Point((x0 + self.width/4)*self.scale,win.getHeight()-y0*self.scale),
								gr.Point((x0+self.width*3/4)*self.scale,win.getHeight()-y0*self.scale),
								gr.Point((x0+self.width)*self.scale,win.getHeight()-(y0+self.height/4)*self.scale),
								gr.Point((x0+self.width)*self.scale,win.getHeight()-(y0+self.height*3/4)*self.scale),
								gr.Point((x0+self.width*3/4)*self.scale,win.getHeight()-(y0+self.height)*self.scale),
								gr.Point((x0+self.width/4)*self.scale,win.getHeight()-(y0+self.height)*self.scale),
								gr.Point(x0*self.scale,win.getHeight()-(y0+self.height*3/4)*self.scale),
								gr.Point(x0*self.scale,win.getHeight()-(y0+self.height/4)*self.scale)) ]
		
		self.vis[0].setFill(color)
								
	def getWidth(self):
			return self.width
		
	def getHeight(self):
			return self.height


#-----------------------------------------------------------------------------------------
class Putt(Thing):
	
	def __init__(self, win, x0, y0, width, height, color='blue'):
		Thing.__init__(self, win, "ball", position = [x0, y0], mass = 5, radius = width/2)
		
		self.x0 = x0
		self.y0 = y0
		self.width = width
		self.height = height
			
		self.vis = [ 	gr.Polygon( gr.Point(x0*self.scale, win.getHeight() - y0*self.scale),
									gr.Point((x0+width)*self.scale, win.getHeight() - y0*self.scale),
									gr.Point((x0+width)*self.scale, win.getHeight() - (y0+height)*self.scale),
									gr.Point(x0*self.scale, win.getHeight() - (y0+height)*self.scale) ) ]
										
										
		self.vis[0].setFill(color)
		
	
	def getWidth(self):
		return self.width
	
	def getHeight():
		return self.height
			
			
			
					
#-----------------------------------------------------------------------------------------
class RotatingBlock(Thing):
	
	def __init__(self, win, x0, y0, width, height, Ax = None, Ay = None, color = 'blue'):
		Thing.__init__(self, win, "rotating block", position = [x0, y0], mass = 5, radius = 2)
		self.width = width
		self.height = height
		self.points = [	[-self.width/2, -self.height/2], [self.width/2, -self.height/2], 
						[self.width/2, self.height/2], [ -self.width/2, self.height/2] ]
		self.angle = 0.0
		self.rvel = 0.0 
		self.pos = [x0, y0]
		if Ax == None and Ay == None:
			self.anchor = [x0, y0]
		else:
			self.anchor = [Ax, Ay]
		self.drawn = False
		
		self.color = color

	def render(self):
		theta = math.pi*self.angle/180
		cth = math.cos(theta)
		sth = math.sin(theta)
		
		pts = []
		for vertex in self.points:
			xt = (vertex[0] + self.pos[0]) - self.anchor[0]
			yt = (vertex[1] + self.pos[1]) - self.anchor[1]
		
			xtt = cth * xt - sth*yt
			ytt = sth * xt + cth*yt
		
			xf = xtt + self.anchor[0]
			yf = ytt + self.anchor[1]
		
			pts.append( gr.Point(xf * self.scale, self.win.getHeight() - yf * self.scale) )
		
		self.vis = [ gr.Polygon(pts[0],pts[1], pts[2], pts[3]) ]
		self.vis[0].setFill(self.color)
	def draw(self):
		for i in self.vis:
			i.undraw()
		
		self.render()
		
		for j in self.vis:
			j.draw(self.win)
		
		self.drawn = True
	
	def getAngle(self):
		return self.angle
	
	def setAngle(self, angle):
		self.angle = angle
		if self.drawn == True:
			self.draw()
	
	def getAnchor(self):
		return self.anchor
		
	def setAnchor(self, anchor):
		self.anchor = anchor[:]
		if self.drawn == True:
			self.draw()
	
	def rotate(self, rotation):
		self.angle += rotation
		if self.drawn == True:
			self.draw()		

	def getRotVelocity(self):
		return self.rvel
	
	def setRotVelocity(self, rvel):
		self.rvel = rvel
		if self.drawn == True:
			self.draw()

	def rotate(self, rotation):
		self.angle += rotation
		if self.drawn == True:
			self.draw()		



	def update(self, dt):
		da = self.rvel * dt
		if da != 0:
			self.rotate(da)
		Thing.update(self, dt)

#-----------------------------------------------------------------------------------------

class Ship(Thing):
	
	def __init__(self, win, x0=0, y0=0, mass=1, radius=3, healthcounter = 3, angle = 90., dangle = 90., hit1 = False, hit2 = False):
		Thing.__init__(self, win, "ball", position=[x0, y0], mass=mass, radius=radius)

		# anchor point is by default the center of the ship/circle so we don't need it
		self.angle = angle
		self.dangle = dangle

		# visualization properties
		# This is a two-part visualization
		# the ship is a triangle
		self.bodypts = [ (radius, 0),
						 (- radius*0.5,	  1.732*radius*0.5),
						 (- radius*0.5, - 1.732*radius*0.5) ]
		# the exhaust is another triangle
		self.flamepts = [ (- radius*0.5,   0.5*radius),
						  (- radius*0.5, - 0.5*radius),
						  (- radius*1.732, 0) ]

		self.scale = 10.
		self.vis = []
		self.drawn = False

		# these are for handling the flicker of the exhaust
		self.flickertime = 6
		self.flicker = False
		self.countdown = 0
		self.healthcounter = healthcounter
		self.hit1 = hit1
		self.hit2 = hit2
		self.dead = False

	# draw the object into the window
	def draw(self):
		for item in self.vis:
			item.undraw()
		self.render()
		for item in self.vis:
			item.draw(self.win)
		self.drawn = True

	# undraw the object from the window
	def undraw(self):
		for item in self.vis:
			item.undraw()
		self.drawn = False

	# get and set the angle of the object
	# these are unique to rotators
	def getAngle(self):
		return self.angle

	# setAngle has to update the visualization
	def setAngle(self, a):
		self.angle = a
		if self.drawn:
			self.draw()

	# get and set rotational velocity
	def setRotVelocity(self, rv):
		self.dangle = rv # degrees per second

	def getRotVelocity(self):
		return self.dangle

	# incrementally rotate by da (in degrees)
	# has to update the visualization
	def rotate(self, da):
		self.angle += da
		if self.drawn:
			self.draw()

	# special ship methods
	def setFlickerOn(self, countdown = 50):
		self.flicker = True
		self.countdown = countdown

	def setFlickerOff(self):
		self.countdown = 0
		self.flicker = False
		
	# simplified render function since the ship always rotates around its center
	def render(self):

		# get the cos and sin of the current orientation
		theta = math.pi * self.angle / 180.
		cth = math.cos(theta)
		sth = math.sin(theta)

		# rotate each point around the object's center
		pts = []
		for vertex in self.bodypts + self.flamepts:
			# move the object's center to 0, 0, which it is already in model coordinates
			xt = vertex[0]
			yt = vertex[1]

			# rotate the vertex by theta around the Z axis
			xtt = cth*xt - sth*yt
			ytt = sth*xt + cth*yt

			# move the object's center back to its original location
			xf = xtt + self.position[0]
			yf = ytt + self.position[1]

			# create a point with the screen space coordinates
			pts.append( gr.Point(self.scale * xf, self.win.getHeight() - self.scale * yf) )

		# make the two objects
		self.vis = [ gr.Polygon( pts[:3] ), gr.Polygon( pts[3:] ) ]
		self.vis[0].setFill("dark blue")
		self.vis[0].setOutline("dark red")
		self.vis[1].setOutline("yellow")

	# update the various state variables
	# add a unique flicker touch
	def update(self, dt):
		# update the angle based on rotational velocity
#		da = self.dangle * dt
#		if da != 0.0: # don't bother updating if we don't have to
#			self.rotate( da )
		if self.drawn:
			self.draw()
		# flicker the flames
		# this should be a field of the object
# 		if self.flicker and self.countdown > 0:
# 			if self.countdown % self.flickertime < self.flickertime/2:
# 				self.vis[1].setFill( 'yellow' )
# 			else:
# 				self.vis[1].setFill( 'orange' )
# 			self.countdown -= 1
# 		else:
# 			self.vis[1].setFill( 'white' )

		# call the parent update for the rest of it
		Thing.update(self, dt)





class RotShip(Thing):
	
	def __init__(self, win, x0=0, y0=0, mass=1, radius=3, healthcounter = 3, angle = 90., dangle = 90., hit1 = False):
		Thing.__init__(self, win, "ball", position=[x0, y0], mass=mass, radius=radius)

		# anchor point is by default the center of the ship/circle so we don't need it
		self.angle = angle
		self.dangle = dangle

		# visualization properties
		# This is a two-part visualization
		# the ship is a triangle
		self.bodypts = [ (radius, 0),
						 (- radius*0.5,	  1.732*radius*0.5),
						 (- radius*0.5, - 1.732*radius*0.5) ]
		# the exhaust is another triangle
		self.flamepts = [ (- radius*0.5,   0.5*radius),
						  (- radius*0.5, - 0.5*radius),
						  (- radius*1.732, 0) ]

		self.scale = 10.
		self.vis = []
		self.drawn = False

		# these are for handling the flicker of the exhaust
		self.flickertime = 6
		self.flicker = False
		self.countdown = 0
		self.healthcounter = healthcounter
		self.hit1 = hit1
		self.hit2 = False
		self.dead = False

	# draw the object into the window
	def draw(self):
		for item in self.vis:
			item.undraw()
		self.render()
		for item in self.vis:
			item.draw(self.win)
		self.drawn = True

	# undraw the object from the window
	def undraw(self):
		for item in self.vis:
			item.undraw()
		self.drawn = False

	# get and set the angle of the object
	# these are unique to rotators
	def getAngle(self):
		return self.angle

	# setAngle has to update the visualization
	def setAngle(self, a):
		self.angle = a
		if self.drawn:
			self.draw()

	# get and set rotational velocity
	def setRotVelocity(self, rv):
		self.dangle = rv # degrees per second

	def getRotVelocity(self):
		return self.dangle

	# incrementally rotate by da (in degrees)
	# has to update the visualization
	def rotate(self, da):
		self.angle += da
		if self.drawn:
			self.draw()

	# special ship methods
	def setFlickerOn(self, countdown = 50):
		self.flicker = True
		self.countdown = countdown
		print "working"

	def setFlickerOff(self):
		self.countdown = 0
		self.flicker = False
		
	# simplified render function since the ship always rotates around its center
	def render(self):

		# get the cos and sin of the current orientation
		theta = math.pi * self.angle / 180.
		cth = math.cos(theta)
		sth = math.sin(theta)

		# rotate each point around the object's center
		pts = []
		for vertex in self.bodypts + self.flamepts:
			# move the object's center to 0, 0, which it is already in model coordinates
			xt = vertex[0]
			yt = vertex[1]

			# rotate the vertex by theta around the Z axis
			xtt = cth*xt - sth*yt
			ytt = sth*xt + cth*yt

			# move the object's center back to its original location
			xf = xtt + self.position[0]
			yf = ytt + self.position[1]

			# create a point with the screen space coordinates
			pts.append( gr.Point(self.scale * xf, self.win.getHeight() - self.scale * yf) )

		# make the two objects
		self.vis = [ gr.Polygon( pts[:3] ), gr.Polygon( pts[3:] ) ]
		self.vis[0].setFill("dark blue")
		self.vis[0].setOutline("dark red")
		self.vis[1].setOutline("yellow")

	# update the various state variables
	# add a unique flicker touch
	def update(self, dt):
		# update the angle based on rotational velocity
		da = self.dangle * dt
		if da != 0.0: # don't bother updating if we don't have to
			self.rotate( da )
		if self.drawn:
			self.draw()
		# flicker the flames
		# this should be a field of the object
		if self.flicker and self.countdown > 0:
			if self.countdown % self.flickertime < self.flickertime/2:
				self.vis[1].setFill( 'yellow' )
			else:
				self.vis[1].setFill( 'orange' )
			self.countdown -= 1
		else:
			self.vis[1].setFill( 'white' )

		# call the parent update for the rest of it
		Thing.update(self, dt)


