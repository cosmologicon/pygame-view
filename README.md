# pygame-view
Convenience module for working with multiple window resolutions in pygame

The main point of this module is to allow your pygame-based game to support multiple resolutions
that share an aspect ratio. It allows you to develop your game with a particular baseline
resolution in mind, and provides a function to easily map screen coordinates and sizes from your
baseline resolution to the actual resolution. These values can be passed to pygame methods to allow
for a scaled version of your original graphics.

## Quick usage example

	import pview
	from pview import T
	
	# Baseline resolution: 640x480. Actual height: 720
	pview.set_mode((640, 480), 720)
	
	# draw a circle in the lower right
	pygame.draw.circle(pview.screen, (255, 255, 255), T(630, 470), T(10))

	# Auto-select the largest fullscreen resolution with the same aspcet ratio as 640x480.
	pview.toggle_fullscreen()

## To install

Download `pview.py` and put it in your source directory. To install from command line:

	curl https://raw.githubusercontent.com/cosmologicon/pygame-view/master/pview.py > my-source-directory/pview.py

## Detailed usage

### `pview.set_mode`

	pview.set_mode(size0 = None, height = None, fullscreen = None, forceres = None)

Call this function once to set at least the baseline resolution (`size0`). You can subsequently
update any of the options by calling it again with keyword arguments. Each call to this function
results in a call to `pygame.display.set_mode` with the updated options.

Normally, the `height` option is only considered in window (non-fullscreen) mode. If `fullscreen` is
set to `True` then the `height` option is ignored. However, if `forceres` is set to `True`, then the
resolution will be chosen to match `height`, just like in window mode. Otherwise fullscreen mode
will have the largest possible resolution that matches the aspect ratio of `size0`.

### `pview.toggle_fullscreen`

	pview.toggle_fullscreen()

Calls `pview.set_mode` with the appropriate fullscreen option.

### `pview.T`

This function is a convenient way to scale values from the baseline resolution to the actual
resolution. For example, if the baseline resolution is 640x480 and the actual resolution is
1280x960, then this function will scale values up by a factor of 2. It can take single values,
sequences of values, multiple values to be mapped to a sequence, or `Rect`s. For example:

	from pview import T

	T(10) -> 20
	T(4.4) -> 9  # Always maps to ints
	T(0.001) -> 1  # Rounds away from 0
	T([1, 2, 3]) -> [2, 4, 6]
	T(1, 2, 3) -> [2, 4, 6]
	T(pygame.Rect(10, 10, 50, 50)) -> pygame.Rect(20, 20, 100, 100)

Typically you will call `T` on:

* numerical arguments of functions to `pygame.draw` methods
* the font size when loading a font with `pygame.font.Font`
* the target image size of `pygame.transform.scale`, if you're scaling images that will appear on
the screen
* the rectangle list in `pygame.display.update`

The reason `T` returns ints and rounds away from 0 is because many pygame functions require integer
pixel values, and some require positive values, such as the `width` parameter in
`pygame.draw.circle`. So this avoids throwing an exception in those cases when the actual resolution
gets too small.

### `pview` attributes

These are updated every time you call `pview.set_mode`.

	pview.screen: the display surface
	pview.rect: a Rect with the actual dimensions
	pview.rect0: a Rect with the baseline dimensions
	pview.aspect: the aspect ratio (width0 / height0)
	pview.f: ratio of actual dimensions to baseline dimensions (height / height0)

### `pview` rect attributes

The pview module also has attributes that mirror the attributes of `pygame.Rect`. The same
attributes with a suffix of `0` refer to the baseline resolution.

For example, if the actual resolution is 600x400, then it will have the following values:

	pview.size = 600, 400
	pview.w = 600
	pview.midtop = 300, 0

and if the baseline resolution is 300x200, then it will have the following values:

	pview.size0 = 300, 200
	pview.h0 = 200
	pview.centery0 = 100
	pview.bottomright0 = 300, 200

Unlike with `pygame.Rect`, these attributes are *not* magical, and setting them will not have any
effect on the behavior of the `pview` module. The complete set of attributes are (along with their
corresponding `0` versions):

	x y top left bottom right
	topleft bottomleft topright bottomright
	midtop midleft midbottom midright
	center centerx centery size width height w h
	diag area s

The attributes `diag`, `area`, and `s` are not used by `pygame.Rect`. They are defined as:

	diag = sqrt(w ** 2 + h ** 2)
	area = w * h
	s = sqrt(area)

where `diag` and `s` are rounded to the nearest integer.

### `pview.fill`

	pview.fill(color, rect = None)

Similar to calling `pview.screen.fill(color, rect)`, except that alpha values of the color are
respected. If the color has an alpha value less than 255, transparency blending will be used.

### `pview.cycle_height`

	pview.cycle_height(heights, reverse = False)

Given a list of heights, choose a height from the list based on the current height. If the current
height is in the list of heights, then choose the next largest (wrapping around to the smallest if
the current height is equal to the largest height in the list). If `reverse` is set to `True`, then
instead choose the next smallest.

### `pview.screenshot`

	pview.screenshot()

Takes a screenshot of the current screen and saves it to a timestamped file. The location can be
specified by setting `pview.SCREENSHOT_DIRECTORY`, which defaults to `"."`. The filename template
(which is passed to `strftime`) can be specified by setting `pview.SCREENSHOT_TEMPLATE`, which
defaults to `"screenshot-%Y%m%d%H%M%S.png"`.

### `pview.I`

	from pview import I
	I(2.2, -2.2) -> [3, -3]

Rounds away from 0 and converts to integer. `pview.I` is similar to `pview.T`, except it does not
scale to match the actual resolution.

### flags

If you want `pview.set_mode` to pass any flags to `pygame.display.set_mode`, set the values
`pview.WINDOW_FLAGS` and `pview.FULLSCREEN_FLAGS` before calling `pview.set_mode`. These default to
`0` and `HWSURFACE | DOUBLEBUF`, respectively.
