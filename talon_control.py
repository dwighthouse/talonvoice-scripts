# Provides various facilities to interact with Talon itself
# "talon sleep" - Disables recognition except for other Talon control features listed here
# "talon wake" - Re-enables recognition
# And other commands for activating and controlling the various eye tracking modes

from talon import app
from talon.api import lib
from talon.voice import Context, ContextGroup, talon
import eye_mouse

# Because the Voice Commands on this Context are in their own ContextGroup, they are treated separatedly from the other ContextGroups (including the default one: talon)
# By disabling the default talon ContextGroup, we can effectively turn off recognition, save for the Voice Commands in this file
def set_enabled(enable):
    if enable:
        talon.enable()
        app.icon_color(0, 0.7, 0, 1)
    else:
        talon.disable()
        app.icon_color(1, 0, 0, 1)

    lib.menu_check(b'!Enable Speech Recognition', enable)

# Creates extra menu item for toggling Speech Recognition
def on_menu(item):
    if item == '!Enable Speech Recognition':
        set_enabled(not talon.enabled)

app.register('menu', on_menu)


# Respect the enabled-ness of default talon ContextGroup for these Voice Commands
def on_eye_control(menu_string):
    if talon.enabled:
        eye_mouse.on_menu(menu_string)


context_group = ContextGroup('talon_control')
context = Context('talon_control', group=context_group)

context.keymap({
    # Enable/disable voice recognition
    'talon sleep': lambda m: set_enabled(False),
    'talon wake': lambda m: set_enabled(True),

    # Toggle various eye tracking systems
    'talon (calibrate | calibration)': lambda m: on_eye_control('Eye Tracking >> Calibrate'),
    'talon mouse [control]': lambda m: on_eye_control('Eye Tracking >> Control Mouse'),
    'talon zoom [mouse]': lambda m: on_eye_control('Eye Tracking >> Control Mouse (Zoom)'), # Currently doesn't work for unknown reasons
    'talon keyboard': on_eye_control('Eye Tracking >> Keyboard'), # Currently doesn't work for unknown reasons
    'talon eye debug': lambda m: on_eye_control('Eye Tracking >> Show Debug Overlay'),
    'talon eye camera': lambda m: on_eye_control('Eye Tracking >> Show Camera Overlay'),

    # TODO: Enable/Disable the CLI debug info
    # TODO: Open Console to talon.log at "Now"
    # TODO: Restart Talon (for reloading ContextGroups)
})

# Startup
set_enabled(talon.enabled)
context_group.load()
