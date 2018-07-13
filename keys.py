# Provides basic mapping for all physical keyboard keys using logical, though possibly verbose, Rule phrases
# Also supports all holdable modifier key combinations for use as keyboard-based shortcuts
# This, combined with other scripts, is my replacement for the Voice Commands in std.py

from talon.voice import Word, Context, Key, Rep, RepPhrase, Str, press
import string, itertools

# Alternate spoken forms must have their own entry
holdable_keys = {
    'command': 'cmd',
    'apple': 'cmd',
    'control': 'ctrl',
    'shift': 'shift',
    'alt': 'alt',
    'option': 'alt',

    # At this time, fn key is not handled the same as other modifier keys due to underlying OS implementations
    # Talon can detect this, but creating shortcuts with the fn key is still a mystery, so these are disabled for now
    # 'function key': 'fn',
    # 'funky': 'fn',
    # 'effin': 'fn',
}

glyph_keys = {}
operation_keys = {}

# Alphabet Keys
# Same as std.py
alphabet_names = 'air bat cap die each fail gone harm sit jury crash look mad near odd pit quest red sun trap urge vest whale box yes zip'.split()
glyph_keys.update(dict(list(zip(alphabet_names, string.ascii_lowercase))))

# Number Keys
number_names = [str(n) for n in range(10)]
glyph_keys.update(dict(list(zip(number_names, number_names))))
glyph_keys.update({ 'oh': '0' })

# Symbol Keys
glyph_keys.update({
    '[back] tick': '`',
    'tilde': '~',

    'exclamation [point]': '!',
    'at sign': '@',
    '(pound [sign] | hash [sign] | number sign)': '#',
    'dollar [sign]': '$',
    'percent [sign]': '%',
    'caret': '^',
    '(and sign | ampersand)': '&',
    '(star | asterisk | times | multiply)': '*',

    '(minus | dash)': '-',
    '(underscore | downscore)': '_',

    'equals [sign]': '=',
    '(plus [sign] | plusign)': '+',

    'backslash': '\\',
    'pipe': '|',

    '(semi | semicolon)': ';',
    'colon': ':',

    '[single] quote': "'",
    '(dubquote | double quote)': '"',

    'comma': ',',
    '(dot | period | point)': '.',

    '([forward] slash | divide)': '/',
    '(question [mark] | question-mark)': '?',

    '[(L | left)] (paren | parentheses | parenthesis)': '(',
    '(R | right) (paren | parentheses | parenthesis)': ')',

    '([(L | left)] square [bracket] | [(L | left)] bracket)': '[',
    '((R | right) square [bracket] | [(R | right)] bracket)': ']',

    '[(L | left)] [curly] brace': '{',
    '(R | right) [curly] brace': '}',

    '([(L | left)] angle | langle | less than [symbol])': '<',
    '((R | right) angle | rangle | greater than [symbol])': '>',
})

# Function Keys
operation_keys.update({'(function | ef) %s'%(n): 'f%s'%(n) for n in range(1, 21)})

# Keypad Keys
operation_keys.update({'(keypad | number pad | number key) %s'%(n): 'keypad_%s'%(n) for n in range(10)})
operation_keys.update({
    '(keypad | number pad | number key) clear': 'keypad_clear',
    '(keypad | number pad | number key) equals [sign]': 'keypad_equals',
    '(keypad | number pad | number key) ([forward] slash | divide)': 'keypad_divide',
    '(keypad | number pad | number key) (star | asterisk | times | multiply)': 'keypad_multiply',
    '(keypad | number pad | number key) (minus | dash)': 'keypad_minus',
    '(keypad | number pad | number key) (plus [sign] | plusign)': 'keypad_plus',
    '(keypad | number pad | number key) (dot | period | point)': 'keypad_decimal',
    '(keypad | number pad | number key) (enter | return)': 'keypad_enter',
})

# Other Physical Keys
operation_keys.update({
    'escape': 'escape',
    '(backspace | backward delete)': 'backspace',
    'tab': 'tab',
    '(caps [lock] | capslock)': 'capslock', # Currently doesn't actually toggle caps lock system wide
    '(enter | return)': 'return',
    '(space | spacebar)': 'space',

    '(delete | forward delete)': 'delete',
    'home': 'home',
    'end': 'end',
    'page up': 'pageup',
    'page down': 'pagedown',

    'up [arrow]': 'up',
    'down [arrow]': 'down',
    'left [arrow]': 'left',
    'right [arrow]': 'right',
})

# Non-Standard Keys
operation_keys.update({
    'key help': 'help',
    'key volume up': 'volup',
    'key volume down': 'voldown',
    'key mute': 'mute',
})

def do_shortcut(key_name, m):
    modifiers = []

    last = ''
    for w in m._words:
        w = str(w)

        # Handle the odd case of the function key
        if w == 'function':
            pass
        elif last == 'function' and w == 'key':
            modifiers.append(holdable_keys['function key'])
        elif w in holdable_keys:
            modifiers.append(holdable_keys[w])
        else:
            break

        last = w

    press('-'.join([*list(set(modifiers)), key_name]))

def gen_shortcut(key_name):
    return lambda m: do_shortcut(key_name, m)

holdable_key_string = ' | '.join(holdable_keys.keys())

context = Context('keys')
context.keymap({
    # All bare keypresses
    **glyph_keys,
    **{phrase: Key(key_name) for phrase, key_name in operation_keys.items()},

    # All shortcut combinations
    **{'(%s)+ (%s)'%(holdable_key_string, phrase): gen_shortcut(key_name) for phrase, key_name in {**glyph_keys, **operation_keys}.items()},
})
