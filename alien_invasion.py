import sys
import pygame
from time import sleep	

from settings import Settings
from ship import Ship
from bullet import Bullet 
from alien import Alien
from game_stats import GameStats
from button import Button

class AlienInvasion:
	"""Overall class to manage game assets and behaviour. chiendeptrainhatthegioi"""

	def __init__(self):
		"""Initialize the game, create game resources."""
		pygame.init()
		self.settings = Settings()

		self.screen = 	pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		#self.screen = 	pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion - Chiendeptrainhatthegioi")
		# Create an instance to store game statistics
		self.stats = GameStats(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		# Make the play button
		self.play_button = Button(self, "Play")
	

	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

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
			# Mouse clicks
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self,mouse_pos):
		"""Start a new game when the player clicks Play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self._start_game()


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
		# Make bullet when press barspace
		elif event.key == pygame.K_p and not self.stats.game_active:
			self._start_game(	)
		elif event.key == pygame.K_SPACE and len(self.bullets) < self.settings.bullets_allowed:
			self._fire_bullet()

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
		# Draw bullets group to screen
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		# Draw the play button if the game is inactive
		if not self.stats.game_active:
			self.play_button.draw_button()
		# Make the most recently drawn screen visible.
		pygame.display.flip()

	def _fire_bullet(self):
		"""Create a bullet and add it to the bullets group"""
		new_bullet = Bullet(self)
		self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets"""
		#Update each bullet in bullets list
		self.bullets.update()	
		#Deleting bullets that have disappeared
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

		
		 

	def _check_bullet_alien_collisions(self):
		"""Response to bullet-alien collisions"""
		# Check if any bullets that have hit the alien.
			#if so get rid of the bullet and alien though "True,True"
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True , True)

		# Make new fleet if no alien left.
		if not self.aliens:
			# Destroy existing bullets and create new fleet.
			self.bullets.empty()
			self._create_fleet()


	def _update_aliens(self):
		"""Check if the fleet is at the adge,
			Then update the positions of all aliens in the fleet"""
		self._check_fleet_edges()
		self.aliens.update()

		# Look for ship-alein collisions
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		# Look for aliens hitting the bottom of the screen
		self._check_aliens_bottom()

	def _create_fleet(self):
		""" Create a fleet of aliens"""
		# create an alien to dind how many alien in a row
		# Spacing between each alien is equal to one alien width
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size

		# Calculate number in a row
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_alien_x = available_space_x // (2 * alien_width)

		#Calculate how many rows in a screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height 
									- (3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		# Create the full fleet of aliens.
		for row_number in range(number_rows):
			for alien_number in range(number_alien_x):
				self._creat_alien(alien_number, row_number)
			
	def _creat_alien(self,alien_number, row_number):
		"""Create and place an alien based on its number in a row"""
		alien = Alien(self)
		alien_width,alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien_height + 2 * alien_height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		""" Response appropriately if any alien have reached an age"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change its direciton"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		# change direction of fleet
		self.settings.fleet_direction *= -1

	def _ship_hit(self):
		"""Response to the ship being hit by an alien"""

		if self.stats.ships_left > 0:
			# Decrement number of ship left : ships_left
			self.stats.ships_left -= 1

			# Get rid of any remaining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()

			# Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()

			# Pause game
			sleep(1)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

		

	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if (alien.rect.bottom) >= (screen_rect.bottom):
				# Treat this the same as if the ship got hit.
				self._ship_hit()
				break	

	def _start_game(self):
		""" Start the game when the game is inactive"""
		# Reset the game statistics
		self.stats.reset_stats()
		self.stats.game_active = True

		# Get rid of any remaining aliens and bullets
		self.aliens.empty()
		self.bullets.empty()

		# Create a new fleet and center the ship
		self._create_fleet()
		self.ship.center_ship()

		# Hide the mouse cursor
		pygame.mouse.set_visible(False)



if __name__ == "__main__":
	# Make a game instance.
	ai = AlienInvasion()
	ai.run_game()