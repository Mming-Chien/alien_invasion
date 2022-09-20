import pygame.font
from pygame.sprite import Group
from ship import Ship

class ScoreBoard:
	"""A class to report scoring imformation"""
	def __init__(self, ai_game):
		"""Initialize scorekeeping attributes"""
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats

		# Font settings for scoring information
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None, 48)

		self.prep_images()
		

	def prep_images(self):
		"""Prepare images for scoreboard"""
		# Prepare the initial score and level iamges
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()


	def prep_score(self):
		"""Turn the score into the rendered image"""
		# Round the score and insert commas
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)

		self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

		# Display the score at the top right of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		"""Turn the high score into the rendered image"""
		# Round the score and insert commas
		high_score = round(self.stats.high_score, -1)
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
		self.high_score_rect = self.high_score_image.get_rect()

		# Center the high score at the top of the screen
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def prep_level(self):
		"""Turn the level into rendered image"""
		level_str = str(self.stats.level)
#		level_str = "level " + level_str
		self.level_image = self.font.render(level_str, True , self.text_color, self.settings.bg_color)
		self.level_image_rect = self.level_image.get_rect()
		# Place level image beneath the score image
		self.level_image_rect.right = self.score_rect.right
		self.level_image_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		"""Display the remaining ships of the player"""
		remain_ships = str(self.stats.ships_left)
		remain_ships = "ships left " + remain_ships

		self.ships_left_image = self.font.render(remain_ships, True , self.text_color, self.settings.bg_color)
		self.ships_left_rect = self.ships_left_image.get_rect()
		self.ships_left_rect.x = 10
		self.ships_left_rect.y = 10


	def show_score(self):
		"""Draw score, level, ship to the screen"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_image_rect)
		self.screen.blit(self.ships_left_image, self.ships_left_rect)

	def check_high_score(self):
		""" Check to see if there's a new high score"""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()
