import pygame, sys, random
import view
from view import T

pygame.display.init()
pygame.display.set_caption("Floppy Blard")
pygame.font.init()
forceres = "--forceres" in sys.argv
view.set_mode((600, 400), forceres = forceres)

fonts = {}
def write(text, fontsize, pos = None, **kw):
	if fontsize not in fonts:
		fonts[fontsize] = pygame.font.Font(None, fontsize)
	surf = fonts[fontsize].render(text, True, (255, 255, 255))
	view.screen.blit(surf, pos or surf.get_rect(**kw))


x, y, vx, vy, slope = 0, 200, 80, 0, 0
clock = pygame.time.Clock()
alive = True
playing = True
while playing:
	dt = clock.tick() * 0.001
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False
			if event.key == pygame.K_1:
				view.set_mode(height = 200)
			if event.key == pygame.K_2:
				view.set_mode(height = 300)
			if event.key == pygame.K_3:
				view.set_mode(height = 400)
			if event.key == pygame.K_4:
				view.set_mode(height = 500)
			if event.key == pygame.K_f:
				view.toggle_fullscreen()
			if event.key == pygame.K_SPACE:
				if alive:
					vy = -500
				else:
					alive = True
					x, y, vx, vy, slope = 0, 200, 80, 0, 0
	if alive:
		accel = 1000
		x += vx * dt
		y += vy * dt + 0.5 * accel * dt ** 2
		vy += accel * dt
		if x > 600:
			slope = random.uniform(-0.3, 0.3)
			x, y = 0, 200 - slope * 300
		y0 = 200 + (x - 300) * slope
		if abs(y0 - y) > 100:
			alive = False

	view.screen.fill((0, 0, 0))
	# Draw the slopes
	dx = 300 * slope
	ps = (0, 0), (600, 0), (600, 100 + dx), (0, 100 - dx)
	pygame.draw.polygon(view.screen, (0, 75, 0), T(ps))
	ps = (0, 400), (600, 400), (600, 300 + dx), (0, 300 - dx)
	pygame.draw.polygon(view.screen, (0, 75, 0), T(ps))
	# Draw the Blard
	rect = pygame.Rect((0, 0, 20, 20 + 0.02 * vy))
	rect.center = x, y
	pygame.draw.ellipse(view.screen, (255, 255, 200), T(rect))
	write("Floppy Blard", T(50), centerx = view.centerx, top = T(10))
	lines = [
		"Actual resolution: %dx%d" % view.size,
		"Baseline resolution: %dx%d" % view.size0,
		"Apsect ratio: %.2f" % view.aspect,
		"1-4: select resolution",
		"F: toggle fullscreen",
		"Space: flop",
		"Esc: quit",
	]
	for jline, line in enumerate(reversed(lines)):
		write(line, T(16), bottomleft = T(5, 395 - 12 * jline))
	pygame.display.flip()

