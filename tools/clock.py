emoji_hours = ['🕧🕛', '🕐🕜', '🕝🕑', '🕞🕒', '🕟🕓', '🕠🕔', '🕡🕕', '🕢🕖', '🕣🕗', '🕤🕘', '🕥🕙', '🕥🕙',
               '🕧🕛', '🕐🕜', '🕝🕑', '🕞🕒', '🕟🕓', '🕠🕔', '🕡🕕', '🕢🕖', '🕣🕗', '🕤🕘', '🕥🕙', '🕥🕙']


def clock_emoji(hour, minute):
    half = False

    match minute:
        case num if num in range(20, 40):
            half = True
        case num if num in range(40, 60):
            hour += 1

    return emoji_hours[hour][half]
