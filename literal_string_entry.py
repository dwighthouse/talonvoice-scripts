# Allows entry of any word or phrase with optional formatting, without worrying about any other interpretation by other Talon Rules.
# For instance, a Rule that causes the spacebar to be pressed when saying "space", saying "phrasing space" will still insert the word "space"

# WARNING: Because this script uses ContextGroup, changes to the script may not be recognized until a Talon restart.

from talon.voice import Context, ContextGroup, Str, talon

capitalization_formatters = ['camel', 'title', 'lower', 'caps']
separator_formatters = ['cram', 'snake', 'line']

capitalization_string = ' | '.join(capitalization_formatters)
formatter_string = ' | '.join(capitalization_formatters + separator_formatters)

def enabled():
    # HACK: Hook into the enabled-ness of the default talon ContextGroup which can be disabled by TalonControl.py
    return talon.enabled

def parse_word(word):
    word = str(word)

    parts = word.split('\\')

    # Probably detected punctuation character, return the literal word (ending value)
    if len(parts) >= 3:
        return parts[-1]

    # Otherwise, we probably want the first detected value:
    # '_\\letter', '_\\number', '_\\determiner', '_\\pronound'
    return parts[0]

def parse_dgndictation(dgndictation):
    word_list = []

    for w in dgndictation._words:
        # Split on space-separated "words", like "Home Depot"
        word_list += parse_word(w).split(' ')

    return word_list

def format(word_list, formatters):
    # Any capitalization formatting will clear out auto-capitalization (like "Home Depot" and the pronoun I)
    # If 'lower' is a formatter, this will lowercase the words without requiring an explicit lowercasing later
    if not formatters.isdisjoint(capitalization_formatters):
        word_list = [w.lower() for w in word_list]

    titleAll = False
    upperAll = False
    lowerFirstLetter = False

    separator = ' '

    if 'camel' in formatters:
        separator = ''
        titleAll = True
        lowerFirstLetter = True
    if 'title' in formatters:
        titleAll = True
        lowerFirstLetter = False
    if 'caps' in formatters:
        upperAll = True
        lowerFirstLetter = False

    if 'cram' in formatters:
        separator = ''
    if 'snake' in formatters:
        separator = '_'
    if 'line' in formatters:
        separator = '-'

    if upperAll:
        # CAPS overrides other capitalization schemes
        word_list = [w.upper() for w in word_list]
    else:
        if titleAll:
            word_list = [w.capitalize() for w in word_list]
        if lowerFirstLetter:
            word_list = [word_list[0].lower()] + word_list[1:]

    return separator.join(word_list)

def get_unique_formatters(m):
    return set([str(w) for w in m._words[1:-1]])

# Allowing almost any word or phrase to be entered literally, with optional formatting
# Examples:
#   "phrasing title" => 'title'
#   "phrasing title title" => 'Title'
#   "phrasing caps line this is a test" => 'THIS-IS-A-TEST'
#   "phrasing camel camel title snake this is a test" => 'This_Is_A_Test'
def formatted_literal_phrase(m):
    if enabled():
        Str(format(parse_dgndictation(m.dgndictation[0]), get_unique_formatters(m)))(None)

# Allowing the input of formatter words, with optional formatting
# Some formatter words can be entered by using "phrasing", but not all of them accurately, thus this extra method
# Examples:
#   "phraser cram" => 'cram'
#   "phraser title cram" => 'Cram'
#   "phraser caps caps" => 'CAPS'
def formatted_literal_formatter(m):
    if enabled():
        Str(format([parse_word(m._words[-1])], get_unique_formatters(m)))(None)

# Allowing the input of trigger word 'phrasing', with optional formatting
# Examples:
#   "phraser phrasing" => 'phrasing'
#   "phraser caps phrasing" => 'PHRASING'
def formatted_literal_phrasing(m):
    if enabled():
        Str(format(['phrasing'], get_unique_formatters(m)))(None)

context_group = ContextGroup('literal_string_entry')
context = Context('literal_string_entry', group=context_group)

context.keymap({
    'phraser (%s)* phrasing'%(capitalization_string): formatted_literal_phrasing,
    'phraser (%s)+'%(formatter_string): formatted_literal_formatter,
    'phrasing (%s)* <dgndictation>'%(formatter_string): formatted_literal_phrase,
})

context_group.load()
