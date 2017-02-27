# pygame-view
Convenience module for working with multiple window resolutions in pygame

The main point of this module is to allow your pygame-based game to support multiple resolutions
that share an aspect ratio. It allows you to develop your game with a particular baseline
resolution in mind, and provides a function to easily map screen coordinates and sizes from your
baseline resolution to the actual resolution. These values can be passed to pygame methods to allow
for a scaled version of your original graphics.

## Quick usage example

	import view
	from view import T
	
	# Target resolution: 640x480. Actual height: 720
	view.set_mode((640, 480), 720)
	
	# draw a circle in the lower right
	pygame.draw.circle(view.screen, (255, 255, 255), T(630, 470), T(10))

	# Auto-select the largest fullscreen resolution with the same aspcet ratio as 640x480.
	view.toggle_fullscreen()

## To install

Download `view.py` and put it in your source directory. To install from command line:

	curl https://raw.githubusercontent.com/cosmologicon/pygame-view/master/view.py > my-source-directory/view.py

## Detailed usage

### `view.set_mode`

	view.set_mode(size0 = None, height = None, fullscreen = None, forceres = None)

Call this function once to set at least the baseline resolution (`size0`). You can update any of
the options by calling it again with keyword arguments. Each call to this function resizes the
actual window.

Normally, the `height` option is only used in window mode. If `fullscreen` is set to `True` then the
`height` option is ignored. However, if `forceres` is set to `True`, then the resolution will be
chosen to match `height`, just like in window mode. Otherwise fullscreen mode will have the largest
possible resolution that matches the aspect ratio of `size0`.

### `view.toggle_fullscreen`

Calls `view.set_mode` with the appropriate fullscreen option.

### `view.T`

This function is designed to be a convenient way to scale values from the baseline resolution to the
actual resolution. For example, if the baseline resolution is 640x480 and the actual resolution is
1280x960, then this function will scale values up by a factor of 2. For example:

	from view import T

	T(10) -> 20
	T(4.4) -> 9  # Always maps to ints
	T(0.001) -> 1  # Rounds away from 0
	T([1, 2, 3]) -> [2, 4, 6]
	T(1, 2, 3) -> [2, 4, 6]
	T(pygame.Rect(10, 10, 50, 50)) -> pygame.Rect(20, 20, 100, 100)

The reason it returns ints and rounds away from 0 is because many pygame functions require integer
pixel values, and some require positive values, such as the `width` parameter in
`pygame.draw.circle`. So this avoids throwing an exception in those cases when the actual resolution
gets too small.

### `view` attributes

These are updated every time you call `view.set_mode`.

	view.screen: the display surface
	view.rect: a Rect with the actual dimensions
	view.rect0: a Rect with the baseline dimensions
	view.aspect: the aspect ratio (width / height)
	view.f: ratio of actual dimensions to baseline dimensions

This is set to the display surface every time you call `view.set_mode`.

### `view` rect attributes

The view module also has attributes that mirror the attributes of `pygame.Rect`. The same attributes
with a suffix of `0` refer to the baseline resolution.

For example, if the actual resolution is 600x400, then it will have the following values:

	view.size = 600, 400
	view.w = 600
	view.midtop = 300, 0

and if the baseline resolution is 300x200, then it will have the following values:

	view.size0 = 300, 200
	view.h0 = 200
	view.centery0 = 100
	view.bottomright0 = 300, 200

Unlike with `pygame.Rect`, these attributes are *not* magical, and setting them will not have any
effect on the behavior of the `view` module.

### flags

If you want `view.set_mode` to pass any flags to `pygame.display.set_mode`, set the values
`view.WINDOW_FLAGS` and `view.FULLSCREEN_FLAGS` before calling `view.set_mode`. These default to
`0` and `HWSURFACE | DOUBLEBUF`, respectively.
