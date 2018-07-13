# Provides various facilities to interact with Talon itself
# "talon sleep" - Disables recognition except for other Talon control features listed here
# "talon wake" - Re-enables recognition
# And other commands for activating and controlling the various eye tracking modes

# WARNING: Because this script uses ContextGroup, changes to the script may not be recognized until a Talon restart.

from talon import app
from talon.api import lib
from talon.engine import engine
from talon.voice import Context, ContextGroup, talon
import eye_mouse, os

# Because the Voice Commands on this Context are in their own ContextGroup, they are treated separatedly from the other ContextGroups (including the default one: talon)
# By disabling the default talon ContextGroup, we can effectively turn off recognition, save for the Voice Commands in this file
def enable_talon():
    talon.enable()
    app.icon_color(0, 0.7, 0, 1)
    lib.menu_check(b'!Enable Speech Recognition', True)

    # Ensure Dragon dictation is off, even if it wasn't enabled
    engine.mimic('go to sleep'.split())

def disable_talon():
    talon.disable()
    app.icon_color(1, 0, 0, 1)
    lib.menu_check(b'!Enable Speech Recognition', False)

def enable_dragon_mode():
    disable_talon()
    engine.mimic('wake up'.split())

# Creates extra menu item for toggling Speech Recognition
def on_menu(item):
    if item == '!Enable Speech Recognition':
        if talon.enabled:
            disable_talon()
        else:
            enable_talon()

app.register('menu', on_menu)



# Adapted from debug.py listed in the Slash channel
def debug_listener(topic, m):
    if topic == 'cmd' and m['cmd']['cmd'] == 'g.load' and m['success'] == True:
        print('[grammar reloaded]')
    else:
        print(topic, m)

is_debug_enabled = False

def set_debug_enabled(enable):
    global is_debug_enabled

    # Respect the enabled-ness of default talon ContextGroup for these Voice Commands
    # Also, no point in re-registering
    if not talon.enabled or enable == is_debug_enabled:
        return

    if enable:
        engine.register('', debug_listener)
    else:
        engine.unregister('', debug_listener)

    is_debug_enabled = enable



def open_debug_log(m):
    # Opens the Talon logs in Console.app, which is where print statements and debugging data is usually sent unless Repl is active
    os.system('open -a Console ~/.talon/talon.log')



def on_eye_control(menu_string):
    # Respect the enabled-ness of default talon ContextGroup for these Voice Commands
    if talon.enabled:
        eye_mouse.on_menu(menu_string)



context_group = ContextGroup('talon_control')
context = Context('talon_control', group=context_group)

context.keymap({
    # Enable/disable voice recognition
    'talon [voice] sleep': lambda m: disable_talon(),
    'talon [voice] wake': lambda m: enable_talon(),

    # Switch between Dragon dictation and Talon recognition
    'talon dragon mode': lambda m: enable_dragon_mode(),
    'talon standard mode': lambda m: enable_talon(),

    # Enable/disable debug logging to console
    'talon [voice] debugging on': lambda m: set_debug_enabled(True),
    'talon [voice] debugging off': lambda m: set_debug_enabled(False),

    # Open talon.log in Console.app
    'talon show log': open_debug_log,

    # Toggle various eye tracking systems
    'talon (calibrate | calibration)': lambda m: on_eye_control('Eye Tracking >> Calibrate'),
    'talon mouse [control]': lambda m: on_eye_control('Eye Tracking >> Control Mouse'),
    'talon zoom [mouse]': lambda m: on_eye_control('Eye Tracking >> Control Mouse (Zoom)'), # Currently doesn't work for unknown reasons
    'talon keyboard': lambda m: on_eye_control('Eye Tracking >> Keyboard'), # Currently doesn't work for unknown reasons
    'talon eye debug': lambda m: on_eye_control('Eye Tracking >> Show Debug Overlay'),
    'talon eye camera': lambda m: on_eye_control('Eye Tracking >> Show Camera Overlay'),
})

# Startup.
enable_talon()
context_group.load()
