# Tatsuya Yokota
# CS151S Fall 2015
# This is a program which you can play a space ship shooting game with boss battles!
# FINALLY FINISHED CODING AND COMMENTING!!!! DEC. 12TH, 2015 3:03 AM 


###### RANDOM NOTES ######################################################################
# multiplayer, new state
#	type in text (single/mutli) and make it so that a triangle moves from one to another when use input.
# pause menu, use while loop with time.sleep(0.5)
# powerups, spawn a block (with music) and make a powerup variable True and change the type of ball shot,
#	use time system to do it for only a short time
# spawn a boss when score reaches a certain number. Make it so that the boss has more hp.
# figrue out how to stop music
# try to solve the drawing/lagging problem

# Terminal commands THAT ARE USEFUL
# afplay file.mp3 &
# killall -STOP afplay
# killall -CONT afplay
#########################################################################################

#########################################################################################
#	IMPORT NECESSARY PACKAGES
#########################################################################################

import graphics as gr
import physics_objects as pho
import collision
import math
import random
import time
import os

#########################################################################################
# 	FUNCTIONS THAT DRAW THE SCORE AND HP.
#	CALLED IN THE MAIN FUNC WHEN SCORE IS INCREMENTED AND HP IS DECREMENTED
#########################################################################################

def scorefunc(win, number):
	block1 = pho.Floor(win, 0, 80, 25, 15, 'blue')
	block1.draw()
	score = gr.Text( gr.Point( 125, 40 ), "Score: " + str(number))
	score.setSize(36)
	score.draw(win)

	

def healthfunc(win, number):
	shade = pho.Floor(win, 25, 80, 25, 15, 'blue')
	shade.draw()
	hp = gr.Text( gr.Point( 375, 40 ), "HP: " + str(number))
	hp.setSize(36)
	hp.draw(win)

#########################################################################################
#	MAIN FUNC
#########################################################################################

def main():
	##### ASKS USER FOR HP VALUE #####
	hp = int(input("How much HP do you want for your ship?\n"))
	
	
	win = gr.GraphWin( "Space Invaders", 500, 800, False)
	state = 0
	
	#### LOOPING TO CHECK FOR DIFFERENT STATES ####
	while state != '':
		
		##### START SCREEN ########################################################################
		dt = 0.008
		bgm = False
		drawn = False
		while state == 0:
			if drawn == False:
				visualship = pho.RotShip(win, 25, 50)
				visualship.draw()
		
				wordplace1 = gr.Point( 250, 200 )
				startingwords1 = gr.Text(wordplace1, "SPACE INVADERS")
				startingwords1.setSize(36)
				startingwords1.setFace('courier')
				startingwords1.draw(win)
		
				wordplace2 = gr.Point( 250, 500 )
				words2 = "PRESS SPACE TO PLAY"
				startingwords2 = gr.Text(wordplace2, words2)
				startingwords2.setSize(36)
				startingwords2.setFace('courier')
				startingwords2.draw(win)
				
				startingwords3 = gr.Text(gr.Point(250, 600), "Use the Left and Right Arrow keys to move" + "\n" +"and use the space bar to shoot!")
				startingwords3.setSize(20)
				startingwords3.setFace('courier')
				startingwords3.draw(win)
				
				drawn = True
			else:		
				pass
		
			visualship.update(0.003)
			key = win.checkKey()
			if key == 'space':
				startingwords1.undraw()
				startingwords2.undraw()
				state = 1
		
			elif key == 'q':
				state = 3
				break
		##################################################################################
	
	
		##################################################################################
		##### MAIN PHASE #################################################################
		if state == 1:
			###### REGULATES BGM WHEN STATE GOES BACK TO MAIN PHASE
			if bgm == False:
				os.system("afplay ./music/bgm.mp3 &")
				bgm = True
			else:
				pass
			
			#### ALL OBJECTS SET HERE (EXCEPT FOR ENEMIES)
			ceiling = pho.Floor(win, 0, 80, 50, 15, 'yellow')
			ship = pho.Ship(win, 5, 5, 2, 2, healthcounter = hp)
			ball = pho.Ball(win, ship.getPosition()[0], ship.getPosition()[1] + 3, 2, 2, 'yellow')
			enemyball = pho.Ball(win, ship.getPosition()[0], ship.getPosition()[1] + 3, 3, 3, 'red')
			
			####  MOVING BACKGROUND
			background = pho.Floor(win, 0, 25, 50, 120, 'black')
			stars = []
			starmaking = True
			while starmaking:
				star = pho.Ball( win, random.randrange(0, 50, 2), random.randrange(0, 1000, 2), 0.1, 0.1, 'white')
				star.setVelocity( [0, -100] )
				stars.append( star )
				if len(stars) == 500:
					starmaking = False
			
			#### DRAWING THE OBJECTS HERE
			background.draw()
			for starmade in stars:
				starmade.draw()
			ceiling.draw()
			ship.draw()
	
			#####  SET ALL NECESSARY VARIABLES HERE #####
			########################################################################
			######	int variables###### 	
			frame = 0
			time1 = 0.
			time2 = 0.
			time3 = 0.
			time4 = 0.
			invincibletimer = 0
			bigshottimer = 0
			score = 0
			LEVEL = 1
			
			#### list variables ###
			colors = ['white','salmon2','orange','pink','green','yellow','red']
			enemies = []
			ballList = []
			enemyballList = []
			newballs = []
			newenemyballs = []
			hit1enemies = []
			hit2enemies = []
			deadenemies = []
			
			### booleans ####
			newtime = True
			invincible = False
			shipflash = False
			spawn = True
			bigshots = False
			bossbattle = True
			lagcheck = True
			shot = False
			leveldrawn = False
			start = False
			minibattle = True
			toomany = False
			
			#### other variable
			health = ship.healthcounter
			key = ''
			
			#### DRAWING THE FIRST HEALTH AND SCORE
			scorefunc(win, score)
			healthfunc(win, health)

			##### STARTING THE MAIN LOOP OF MINIBATTLE ###################################
			while state == 1 and minibattle == True:
				key = win.checkKey()
				#print 'minibattle'
				
				##### ALL UPDATE FUNC ####
				ship.update(dt)
				for i in ballList:
					i.update(dt)
				for j in newenemyballs:
					j.update(dt)
				for k in enemies:
					k.update(dt)
				for l in stars:
					l.update(dt)
				
				### SHIP UPGRADES ######
				#####  times the duration of the invincible upgrade
				##### invincible timing: basically invincibletimer gets incremented every time 
				#### through this while loop when invincible is assigned to True
				###   after 200 loops, invincibletimer is set to 0 and invicinble is set to False
				if invincible:
					invincibletimer += 1
					if invincibletimer > 200:
						invincible = False
						invincibletimer =0
						invincibletext.setTextColor('black')
				#### visual effect for when ship is invincible, draws and undraws one after another
				####  every time through the while loop by using booleans
				if invincible == True:
					if shipflash == False:
						ship.undraw()
						shipflash = True
					else:
						ship.draw()
						shipflash = False
				
				##### times the duration of the bigshots upgrade
				if bigshots:
					bigshottimer += 1
					if bigshottimer > 200:
						bigshots = False
						bigshottimer =0
						bigshottext.setTextColor('black')
				
				######################################################################
				######### MOVING SHIP WITH USER INPUT
				# move ship with user input
				if key == 'Left':
					ship.setVelocity( [-90, 0 ] )
					ship.setFlickerOn()
			
				if key == 'Right':
					ship.setVelocity( [90, 0 ] )
					ship.setFlickerOn()
					
				# ship boundaries
				if ship.getPosition()[0] > 50:
					ship.setVelocity( [-30, 0] )
				if ship.getPosition()[0] < 0:
					ship.setVelocity( [30, 0] )
	
				# shoot balls from the ship WITH USER INPUT
				##### REGUALTES THE NUMBER OF BALLS BEING SHOT AT A TIME 
				##### made a self.undrawn field in the physics_objects.py file 
				#### and made it be assigned to True when self.undrawn() is called and vice versa
				#### ALSO ADDED SOUND EFFECT BY USING os package
				if key == 'space':
					if ball.undrawn == True:	
						if bigshots == False:
							ball = pho.Ball(win, ship.getPosition()[0], ship.getPosition()[1] + 3, 2, 2, random.choice(colors))
						else:
							ball = pho.Ball(win, ship.getPosition()[0], ship.getPosition()[1] + 3, 5, 5, random.choice(colors))
						ballList.append( ball )
						ball.setVelocity( [1,60])
						ball.draw()
						os.system("afplay " + "./music/shoot.wav" + "&")
					else:
						pass
				
				######################################################################
				
				
				# undraw the ball when it gets out of bounds
				if ball.getPosition()[1] > 70:
					ball.undraw()
#					ball = pho.Ball(win, ship.getPosition()[0], ship.getPosition()[1] + 3, 2, 2, 'yellow')
				# 	print "undrawn!"
				else:
					newballs.append( ball )
		#		print ball.getPosition()[1]
			

				##########################################################################
			#ENEMY SPAWNING ZONE
				# spawn new enemy every 1 seconds
				if newtime == True:
					time1 = time.time()
				else:
					time2 = time.time()
	
				if time2 - time1 >= 1:
					spawn = True
					newtime = True
				else:
					newtime = False
				
				##### WROTE TO SOLVE LAGGING PROBLEM
				# every 39 seconds increments the time step (dt) so that it looks like it 
				# isn't lagging
				if lagcheck == True:
					time3 = int(time.time())
				else:
					time4 = int(time.time())
				if (time4 - time3) % 40 == 39:
					dt += 0.01
					lagcheck = True
				else:
					lagcheck = False
				
				######################################################################
				
				# regulating number of enemies
				if len(enemies) > 8:
					toomany = True
				else:
					toomany = False
				
				######################################################################
				# the actual spawning part
				if toomany == True:
					pass
				else:
					if spawn == True:
							if random.random() < 0.3:
								enemy = pho.Ship(win, 10, 10, 10, 10, angle = 270., dangle = 270., hit1 = False)	
							elif random.random() < 0.2:
								enemy = pho.Ship(win, 1, 1, 1, 1, angle = 270., dangle = 270., hit1 = False)
							elif random.random() < 0.1:
								enemy = pho.Ship(win, 1, 1, 2, 2, angle = 270., dangle = 270., hit1 = False)
# 							elif score % 31 == 5:
# 								boss = pho.Ship(win, 1, 1, 12, 12, angle = 270., dangle = 270., hit1 = False, hit2 = True, healthcounter = 500)
# 								bossbattle = True
# 								enemies.append( boss )
# 								boss.draw()
# 								boss.setPosition( [ 25, 60 ] )
# 								boss.setVelocity( [0, -30] )
							else:
								enemy = pho.Ship(win, 5, 5, 5, 5, angle = 270., dangle = 270., hit1 = False)
							enemies.append( enemy )
							
							enemy.draw()

							enemy.setPosition( [random.randrange(20, 45, 1), random.randrange(20, 55, 1 )])
							
							enemy.setVelocity( [random.choice([-80, -70, -60, -50, 50, 60, 70, 80]), random.choice([-80, -70, -60, -50, 50, 60, 70, 80])])
							spawn = False
				
				##########################################################################
			
			
			###### ENEMY MOVEMENT CONTROL AND ENEMY BALL SHOOTING 
				for badguy in enemies:
					if badguy.getPosition()[0] > 50:
						badguy.setVelocity( [random.randrange(-60, -40, 1), random.randrange(-30, 30, 10 )] )
					if badguy.getPosition()[0] < 0:
						badguy.setVelocity( [random.randrange(40, 60, 1), random.randrange(-30, 30, 10 )] )	
					if badguy.getPosition()[1] > 65:
						badguy.setVelocity( [random.randrange(-30, 30, 10), random.randrange(-60, -40, 1 )] )
					if badguy.getPosition()[1] < 20:
						badguy.setVelocity( [random.randrange(-30, 30, 1), random.randrange(40, 60, 1 )] )
					if random.random() < 0.05:
						badguy.setVelocity( [random.choice([-80, -70, -60, -50, 50, 60, 70, 80]), random.choice([-80, -70, -60, -50, 50, 60, 70, 80])] )
					
					# ENEMY SHOOTING BALL
					if random.random() < 0.02:
						enemyball = pho.Ball(win, badguy.getPosition()[0], badguy.getPosition()[1] - 4, 2, 2, 'red')
						enemyballList.append( enemyball )
						enemyball.setVelocity( [0,-70])
			#			print ship.getPosition()[0], ship.getPosition()[1]
						enemyball.draw()
			#			print "hi"
		
		###################################################################################

		
		#################################################################################
				# COLLISIONS AND UNDRAWING
				## ENEMY AND SHIP BALL
					if collision.collision( ball, badguy, dt):
						ball.undraw()
						ballList.remove(ball)
						
						###  HERE IT PUTS ENEMIES INTO LISTS ACCORDING TO HOW MANY TIMES 
						##### IT GOT HIT
						if badguy.hit1 == False:
		# 					badguy.vis[0].setFill("green")       	#TESTING
		# 					badguy.vis[0].setOutline("green")		#TESTING
							badguy.hit1 = True
							hit1enemies.append(badguy)
				
						elif badguy.hit2 == False and badguy.hit1 == True:
		# 					badguy.vis[0].setFill("red")
		# 					badguy.vis[0].setOutline("red")
							badguy.hit2 = True
							hit2enemies.append(badguy)
					
						else:
		# 					badguy.hit1 = False
		# 					badguy.hit2 = False
							deadenemies.append(badguy)
							score += 1
							if score % 11 == 10:
								minibattle = False
							scorefunc(win, score)
							if random.random() < 0.08:
								invincible = True
								invincibletext = gr.Text( gr.Point( 250, 400 ), "INVINCIBLE TIME!" )
								invincibletext.setTextColor('white')
								invincibletext.setSize(36)
								invincibletext.draw(win)
							elif random.random() < 0.08:
								bigshots = True
								bigshottext = gr.Text( gr.Point( 250, 500 ), "BIGGER SHOTS!" )
								bigshottext.setTextColor('white')
								bigshottext.setSize(36)
								bigshottext.draw(win)								
					

				##### CHANGES COLORS OF THE ENEMY ACCRODING TO WHICH LIST THEY ARE IN
				for element in hit1enemies:
						element.vis[0].setFill("green")
						element.vis[0].setOutline("green")
				
				for alien in hit2enemies:
						alien.vis[0].setFill("red")
						alien.vis[0].setOutline("red")

				
				for alien1 in deadenemies:
						alien1.undraw()
						os.system("afplay " + "./music/Invaderkilled.wav" + "&")
						enemies.remove(alien1)
	
		
				## SHIP AND ENEMYBALL
				for enball in enemyballList:				
					if collision.collision(enball, ship, dt):
				
						enball.undraw()
						enemyballList.remove( enball )
						if invincible == False:
							health -= 1
						else:
							pass
						healthfunc(win, health)
				
				
				deadenemies = []
				
				#### undraw the ball when it gets out of bounds
				if enemyball.getPosition()[1] < 0:
					enemyball.undraw()
				else:
					newenemyballs.append( enemyball )
				
				##### UPDATES THE WINDOW EVERY 10 LOOPS 
				if frame % 10 == 0:
					win.update()
				
				#### MAKES IT SO THAT ONLY THE BALLS THAT ARE DRAWN ARE UPDATED FOR COLLISION
				#### IN THE NEXT LOOP
				ballList = newballs
				enemyballList = newenemyballs
		
				# GAME OVER 
				if health <= 0:
					os.system("killall afplay ./music/bgm.mp3")
					os.system("afplay ./music/explosion.wav &")
					os.system("afplay ./music/gameover.mov &")
					ship.undraw()
					state = 2
			
				# user input to quit
				if key == 'q':
					state = 3

				frame += 1	

##########################################################################################
				# BOSS BATTLE 
				# BASICALLY THE SAME AS THE CODE ABOVE BUT THE SPAWNING AND THE 
				# REQUIREMENT FOR THE BOSS TO UNDRAW IS DIFFERENT 
				# THE BOSS USES A HP SYSTEM
##########################################################################################

				leveldrawn = False
				while state == 1 and minibattle == False:
					if leveldrawn == False:
						os.system("afplay " + "./music/levelup.mov" + "&")
						lv2 = gr.Text( gr.Point( 250, 100 ), "LEVEL " + str(LEVEL) + " BOSS BATTLE")
						lv2.setTextColor('white')
						lv2.setSize(36)
						instructions = gr.Text( gr.Point(250, 700), "Press Space to Continue")
						instructions.setTextColor('white')
						instructions.draw(win)
						lv2.draw(win)
						leveldrawn = True
					else:
						pass
					key = win.checkKey()
					if key == 'space':
						lv2.setTextColor('black')
						instructions.setTextColor('black')
						start = True
					if key == 'q':
						state = 3
					
					if start == True and minibattle == False:
						while state == 1 and minibattle == False:
							key = win.checkKey()
				
							
							ship.update(dt)
							for i in ballList:
								i.update(dt)
							for j in newenemyballs:
								j.update(dt)
							for k in enemies:
								k.update(dt)
							for l in stars:
								l.update(dt)
				
							if invincible:
								invincibletimer += 1
								if invincibletimer > 200:
									invincible = False
									invincibletimer =0
									invincibletext.setTextColor('black')
						
				
							if invincible == True:
								if shipflash == False:
									ship.undraw()
									shipflash = True
								else:
									ship.draw()
									shipflash = False
						
							if bigshots:
								bigshottimer += 1
								if bigshottimer > 200:
									bigshots = False
									bigshottimer =0
									bigshottext.setTextColor('black')
				
							if bossbattle:
								for everyone in enemies[0:]:
									everyone.undraw()
									enemies.remove(everyone)
						
					
				
							# move ship with user input
							if key == 'Left':
								ship.setVelocity( [-90, 0 ] )
								ship.setFlickerOn()
			
							if key == 'Right':
								ship.setVelocity( [90, 0 ] )	
								ship.setFlickerOn()
					
							# ship boundaries
							if ship.getPosition()[0] > 50:
								ship.setVelocity( [-30, 0] )
							if ship.getPosition()[0] < 0:
								ship.setVelocity( [30, 0] )
	
							# shoot balls from the ship
							if key == 'space':
								if ball.undrawn == True:	
									if bigshots == False:
										ball = pho.Ball(win, ship.getPosition()[0], ship.getPosition()[1] + 3, 2, 2, 'yellow')
									else:
										ball = pho.Ball(win, ship.getPosition()[0], ship.getPosition()[1] + 3, 5, 5, 'yellow')
									ballList.append( ball )
									ball.setVelocity( [1,60])
									ball.draw()
									os.system("afplay " + "./music/shoot.wav" + "&")
								else:
									pass
							# undraw the ball when it gets out of bounds
							if ball.getPosition()[1] > 70:
								ball.undraw()
								newballs.append( ball )
							else:
								newballs.append( ball )

			
							#solve lagging 
							if lagcheck == True:
								time3 = int(time.time())
							else:
								time4 = int(time.time())
							if (time4 - time3) % 40 == 39:
								dt += 0.01
								lagcheck = True
							else:
								lagcheck = False
				
							# regulating number of enemies
							if len(enemies) > 8:
								toomany = True
							else:
								toomany = False
		
							# the actual spawning part
							if toomany == True:
								pass
							else:
								
								if bossbattle == True:							
									boss = pho.Ship(win, 5, 5, 10, 10, angle = 270., dangle = 270., hit1 = False, healthcounter = 50*LEVEL)
									enemies.append( boss )
									boss.draw()
									boss.setPosition( [random.randrange(20, 45, 1), random.randrange(20, 55, 1 )])
									boss.setVelocity( [random.choice([-80, -70, -60, -50, 50, 60, 70, 80]), random.choice([-80, -70, -60, -50, 50, 60, 70, 80])])
									bosshp = gr.Text( gr.Point( 250, 100 ), "BOSS HP: " + str(boss.healthcounter))
									bosshp.setSize(36)
									bosshp.setTextColor('white')
									bosshp.draw(win)
									bossbattle = False
									spawn = False
										
				
	
			
						#ENEMY MOVEMENT CONTROL
							for badguy in enemies:
								if badguy.getPosition()[0] > 50:
									badguy.setVelocity( [random.randrange(-60, -40, 1), random.randrange(-30, 30, 10 )] )
								if badguy.getPosition()[0] < 0:
									badguy.setVelocity( [random.randrange(40, 60, 1), random.randrange(-30, 30, 10 )] )	
								if badguy.getPosition()[1] > 65:
									badguy.setVelocity( [random.randrange(-30, 30, 10), random.randrange(-60, -40, 1 )] )
								if badguy.getPosition()[1] < 20:
									badguy.setVelocity( [random.randrange(-30, 30, 1), random.randrange(40, 60, 1 )] )
								if random.random() < 0.05:
									badguy.setVelocity( [random.choice([-80, -70, -60, -50, 50, 60, 70, 80]), random.choice([-80, -70, -60, -50, 50, 60, 70, 80])] )
						# ENEMY SHOOTING BALL
								if random.random() < 0.1:
									enemyball = pho.Ball(win, badguy.getPosition()[0], badguy.getPosition()[1] - 4, 2, 2, 'red')
									enemyballList.append( enemyball )
									enemyball.setVelocity( [0,-70])
									enemyball.draw()

		
			
							# COLLISIONS AND UNDRAWING
							## ENEMY AND SHIP BALL
								if collision.collision( ball, badguy, dt):
									badguy.healthcounter -= 1
									bosshp.setTextColor('black')
									bosshp = gr.Text( gr.Point( 250, 100 ), "BOSS HP: " + str(boss.healthcounter))
									bosshp.setSize(36)
									bosshp.setTextColor('white')
									bosshp.draw(win)
									
									
									ball.undraw()
									ballList.remove(ball)
									bosscolor = random.choice(colors)
									boss.vis[0].setFill(bosscolor)
									boss.vis[0].setOutline(bosscolor)
									if boss.healthcounter <= 0:
										bosshp.setTextColor('black')
										deadenemies.append(badguy)
										score += 100
										scorefunc(win, score)
										minibattle = True
										start = False
										bossbattle = True
										os.system("afplay " + "./music/BossExplode.mp3" + "&")
										LEVEL += 1
										if random.random() < 0.08:
											invincible = True
											invincibletext = gr.Text( gr.Point( 250, 400 ), "INVINCIBLE TIME!" )
											invincibletext.setTextColor('white')
											invincibletext.setSize(36)
											invincibletext.draw(win)
										elif random.random() < 0.08:
											bigshots = True
											bigshottext = gr.Text( gr.Point( 250, 500 ), "BIGGER SHOTS!" )
											bigshottext.setTextColor('white')
											bigshottext.setSize(36)
											bigshottext.draw(win)								
									

		
							for element in hit1enemies:
									element.vis[0].setFill("green")
									element.vis[0].setOutline("green")
				
							for alien in hit2enemies:
									alien.vis[0].setFill("red")
									alien.vis[0].setOutline("red")
									
							for alien1 in deadenemies:
									alien1.undraw()
									os.system("afplay " + "./music/Invaderkilled.wav" + "&")
									enemies.remove(alien1)
	
		
							## SHIP AND ENEMYBALL
							for enball in enemyballList:				
								if collision.collision(enball, ship, dt):
									enball.undraw()
									enemyballList.remove( enball )
									if invincible == False:
										health -= 1
									else:
										pass
									healthfunc(win, health)
				

							deadenemies = []
							# undraw the ball when it gets out of bounds
							if enemyball.getPosition()[1] < 0:
								enemyball.undraw()
							else:
								newenemyballs.append( enemyball )
			
							if frame % 10 == 0:
								win.update()
		
							ballList = newballs
							enemyballList = newenemyballs
		
							# GAME OVER 
							if health <= 0:
								os.system("killall afplay ./music/bgm.mp3")
								os.system("afplay ./music/explosion.wav &")
								os.system("afplay ./music/gameover.mov &")
								ship.undraw()
								state = 2
			
							# user input to quit
							if key == 'q':
								state = 3

		
							frame += 1	



##########################################################################################
#					GAME OVER SCREEN 
#					user can decide to replay the game or quit
##########################################################################################
		drawn = False
		while state == 2:
			if drawn == False:
				
				
				visualship = pho.RotShip(win, 25, 50)
				visualship.draw()
		
				wordplace3 = gr.Point( 250, 200 )
				words3 = "GAME OVER"
				endingwords1 = gr.Text(wordplace3, words3)
				endingwords1.setSize(36)
				endingwords1.setTextColor('white')
				endingwords1.draw(win)
		
				wordplace4 = gr.Point( 250, 700 )
				words4 = "Press S to Play Again!"
				endingwords2 = gr.Text(wordplace4, words4)
				endingwords2.setSize(36)
				endingwords2.setTextColor('white')
				endingwords2.draw(win)
				
				endingwords3 = gr.Text(gr.Point( 250, 600) , "Score: " + str(score))
				endingwords3.setSize(36)
				endingwords3.setTextColor('white')
				endingwords3.draw(win)
				
				drawn = True
				
			else:		
				pass
		
			visualship.update(dt)
			
			key = win.checkKey()
			if key == 's':
				startingwords1.undraw()
				startingwords2.undraw()
				state = 1
			
			if key == 'q':
				state = 3

##########################################################################################
#				STATE 3: LED TO HERE WHEN USER DECIDES TO QUIT WHEN IN ANY OF THE OTHER SCREENS
#				KILLS THE MUSIC 
##########################################################################################
		if state == 3:
			os.system("killall afplay ./music/bgm.mp3")
			win.close()
			break
	
if __name__ == "__main__":
	main()