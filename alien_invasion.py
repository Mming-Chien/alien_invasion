import sys
import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
	"""Overall class to manage game assets and behaviour. chiendeptrainhatthegioi"""

	def __init__(self):
		"""Initialize the game, create game resources."""
		pygame.init()
		self.settings = Settings()

		self.screen = 	pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion - Chiendeptrainhatthegioi")

		self.ship = Ship(self)
	

	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			self._check_events()
			self.ship.update()
			self._update_screen()
			

	def _check_events(self):
		"""Response to keypresses and mouse events"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			# Press key
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			# Release key
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_keydown_events(self, event):
		"""Response to keypresses"""
		if event.key == pygame.K_RIGHT:
			# Move the ship to the right.
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			#move the ship to the left
			self.ship.moving_left = True
		# Exit the game when player presses "Q"
		if event.key == pygame.K_q:
			sys.exit()

	def _check_keyup_events(self, event):
		"""Response to key releases"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False


	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen"""
		self.screen.fill(self.settings.bg_color)
		#Make the ship
		self.ship.blitme()

		# Make the most recently drawn screen visible.
		pygame.display.flip()

if __name__ == "__main__":
	# Make a game instance.
	ai = AlienInvasion()
	ai.run_game()