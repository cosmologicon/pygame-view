import pygame, sys
import view
from view import T

pygame.display.init()
pygame.font.init()
forceres = "--forceres" in sys.argv
view.set_mode((640, 360), forceres = forceres)

fonts = {}
def write(text, fontsize, pos = None, **kw):
	if fontsize not in fonts:
		fonts[fontsize] = pygame.font.Font(None, fontsize)
	surf = fonts[fontsize].render(text, True, (255, 255, 255))
	rect = surf.get_rect(**kw)
	view.screen.blit(surf, pos or rect)

playing = True
while playing:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False
			if event.key == pygame.K_1:
				view.set_mode(height = 240)
			if event.key == pygame.K_2:
				view.set_mode(height = 360)
			if event.key == pygame.K_3:
				view.set_mode(height = 480)
			if event.key == pygame.K_4:
				view.set_mode((360, 640))
				view.set_mode(height = 640)
			if event.key == pygame.K_f:
				view.toggle_fullscreen()
	view.screen.fill((0, 0, 0))
	write("The game", T(28), centerx = view.centerx, top = T(10))
	lines = [
		"Actual resolution: %dx%d" % view.size,
		"Baseline resolution: %dx%d" % view.size0,
		"1-4: select resolution",
		"F: toggle fullscreen",
		"Esc: quit",
	]
	for jline, line in enumerate(reversed(lines)):
		write(line, T(16), bottomleft = T(5, 355 - 12 * jline))
	pygame.display.flip()

