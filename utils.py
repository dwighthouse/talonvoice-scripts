# Various generic tools
# To use in other files, for example: "from user.utils import parse_words_as_integer" or "from .utils import parse_words_as_integer"

# NOTE: If you see an error from Talon about "ImportError: cannot import name X", where X is one of these functions, restart Talon

import itertools

# Useful for identifying app/window information for context selection
def context_func(app, win):
    print('---')
    # print(app)
    print(app.bundle)
    print(win)
    print(win.title)
    print(win.doc)
    print('---')
    return True

number_conversions = {
    'oh': '0', # 'oh' => zero
}
for i, w in enumerate(['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']):
    number_conversions.update({
        str(i): str(i),
        w: str(i),
        '%s\\number'%(w): str(i),
    })

# TODO: Once implemented, use number input value rather than manually parsing number words with this function
def parse_words_as_integer(words):
    # Ignore any potential trailing non-number words
    number_words = list(itertools.takewhile(lambda w: str(w) in number_conversions, words))

    # Somehow, no numbers were detected
    if len(number_words) == 0:
        return None

    # Map number words to simple number values
    number_values = list(map(lambda w: number_conversions[w.word], number_words))

    # Join the numbers into single string, and remove leading zeros
    number_string = ''.join(number_values).lstrip('0')

    # If the entire sequence was zeros, return single zero
    if len(number_string) == 0:
        return 0

    return int(number_string)
