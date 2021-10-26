import pygame
import random
import sys
import time

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BACKGROUND_COLOR = (0,0,0)

player_size = 50
player_pos = [WIDTH/2, HEIGHT-2*player_size]
player_movement = 10

enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

bossphase_size = 50
bossphase_pos = [random.randint(0,WIDTH-enemy_size), 0]
bossphase_list = [bossphase_pos]

friend_size = 30
friend_pos = [random.randint(0,WIDTH-friend_size), 0]
friend_list = [friend_pos]

SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

bossflag = False

move_left = False

move_right = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

def play_music():
	file = 'goodVibes.mp3'

	pygame.mixer.music.stop()
	pygame.mixer.music.load(file)
	pygame.mixer.music.play(-1) # If the loops is -1 then the music will repeat indefinitely.
	
def play_bossmusic():
	file = 'boss.mp3'

	pygame.mixer.music.stop()
	pygame.mixer.music.load(file)
	pygame.mixer.music.play(-1) # If the loops is -1 then the music will repeat indefinitely.

def set_level(score, SPEED):
	if score < 30:
		SPEED = 5
	elif score < 50:
		SPEED = 7
	elif score < 80:
		SPEED = 10
	else:
		SPEED = 13
	return SPEED
	# SPEED = score/5 + 1


def drop_entities():
	global friend_list, friend_size, enemy_list, enemy_size
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos = random.randint(0,WIDTH-enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])
	if len(friend_list) < 2 and delay < 0.1:
		x_pos = random.randint(0,WIDTH-friend_size)
		y_pos = 0
		friend_list.append([x_pos, y_pos])
		
def drop_bossphase():
	global friend_list, friend_size, enemy_list, enemy_size
	delay = random.random()
	if len(enemy_list) < 16 and delay < 0.17:
		x_pos = random.randint(0,WIDTH-enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])
	

def draw_entities():
	global enemy_list, friend_list
	# Enemies
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
	# Friends
	for friend_pos in friend_list:
		pygame.draw.rect(screen, GREEN, (friend_pos[0], friend_pos[1], friend_size, friend_size))
	# Player
	pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))


def update_enemy_positions(enemy_list, score):
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += SPEED
		else:
			enemy_list.pop(idx)
			score += 1
	return score


def update_friend_positions(friend_list, score):
	for idx, friend_pos in enumerate(friend_list):
		if friend_pos[1] >= 0 and friend_pos[1] < HEIGHT:
			friend_pos[1] += SPEED
		else:
			friend_list.pop(idx)
	return score


def collision_check(enemy_list, player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos):
			return True
	return False


def collision_check_friends(friend_list, player_pos,score):
	for idx, friend_pos in enumerate(friend_list):
		if detect_collision(friend_pos, player_pos):
			score = score+10
			friend_list.pop(idx)
	return score


def detect_collision(player_pos, enemy_pos):
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
			return True
	return False


def reset_game():
	global player_pos, player_movement, enemy_pos, friend_pos, enemy_list, friend_list
	global score, move_left, move_right, SPEED, game_over, clock

	player_size = 50
	player_pos = [WIDTH/2, HEIGHT-2*player_size]
	player_movement = 10

	enemy_size = 50
	enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
	enemy_list = [enemy_pos]

	friend_size = 30
	friend_pos = [random.randint(0,WIDTH-friend_size), 0]
	friend_list = [friend_pos]
	
	bossphase_size = 50
	bossphase_pos = [random.randint(0,WIDTH-enemy_size), 0]
	bossphase_list = [bossphase_pos]

	move_left = False
	move_right = False

	score = 0

	game_over = False
	
	bossflag = False

	SPEED = 10

	play_music()

	clock = pygame.time.Clock()

reset_game()

while True:
	if not game_over:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					move_left = True
					#x -= player_movement
				elif event.key == pygame.K_RIGHT:
					move_right = True
					#x += player_movement
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					move_left = False
					#x -= player_movement
				elif event.key == pygame.K_RIGHT:
					move_right = False
					#x += player_movement

			
		x = player_pos[0]
		y = player_pos[1]	
		if move_left == True:
			if( x > player_movement):
				x -= player_movement
		if move_right == True:
			if ( x < WIDTH-player_movement):
				x += player_movement
		player_pos = [x,y]

		screen.fill(BACKGROUND_COLOR)

		#drop_entities()
		if score > 400 and score < 550:
			if not bossflag:
				play_bossmusic()
				bossflag = True
			drop_bossphase()
			text = "BOSSPHASE!"
			label = myFont.render(text, 1, RED)
			screen.blit(label, (WIDTH/2 - 100, HEIGHT/2))
		else:
			drop_entities()
			if bossflag:
				play_music()
				bossflag = False
				
		
			
		score = update_enemy_positions(enemy_list, score)
		score = update_friend_positions(friend_list, score)
		score = collision_check_friends(friend_list, player_pos, score)
		SPEED = set_level(score, SPEED)

		if collision_check(enemy_list, player_pos):
			game_over = True
			screen.fill(BACKGROUND_COLOR)
			text = "Final Score:" + str(score)
			label = myFont.render(text, 1, YELLOW)
			screen.blit(label, (WIDTH/2 - 100, HEIGHT/2))
			text = "Press R to Restart"
			label = myFont.render(text, 1, RED)
			screen.blit(label, (WIDTH/2, HEIGHT-40))
		else:
			draw_entities()
			text = "Score:" + str(score)
			label = myFont.render(text, 1, YELLOW)
			screen.blit(label, (WIDTH-200, HEIGHT-40))

		clock.tick(30)

		pygame.display.update()
	else:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					reset_game()
				elif event.key == pygame.K_SPACE:
					sys.exit()
					
