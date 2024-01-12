import curses
from howlongtobeatpy import HowLongToBeat
from tabulate import tabulate
import sys
import time
import re


def main(scr):
    # Remove character Esc delay.
    curses.set_escdelay(25)
    buttons = ['Backlog', 'Search', 'Delete', 'Quit']

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    scr.clear()
    scr.refresh()

    index = selection(scr, buttons, 'ma')
    match path(index):
        case 0:
            backlog(scr)
        case 1:
            search(scr)
        case 2:
            delete(scr)
        case 3:
            return


def path(index):
    if index not in [0, 1, 2, 3]:
        raise ValueError('Unexpected path in selection')
    return index


def selection(scr, buttons, mode, games=None):
    curses.curs_set(0)
    current = 0
    while True:
        scr.clear()
        print_buttons(buttons, current, scr, mode=mode, games=games)

        scr.refresh()
        new_action = False

        while not new_action:
            key = scr.getch()
            new_action = True

            match key:
                case curses.KEY_UP:
                    current -= 1
                    if current < 0:
                        current = len(buttons) - 1
                case curses.KEY_DOWN:
                    current += 1
                    if current > len(buttons) - 1:
                        current = 0
                # Key enter.
                case 10:
                    scr.clear()
                    return current
                # Key Esc.
                case 27:
                    if mode == 'ma':
                        sys.exit()
                    elif mode == 'gi':
                        search(scr)
                        sys.exit()
                case _:
                    new_action = False


def print_buttons(buttons, current, scr, mode=None, games=None):
    h, w = scr.getmaxyx()

    for i, button in enumerate(buttons):
        y, x = yx_values(h, w, i, button)

        if i == current:
            scr.attron(curses.color_pair(1))
            if mode == 'ma':
                scr.addstr(y - (len(buttons) // 2), x, button)
            elif mode == 'gi':
                scr.addstr(y - (len(buttons) // 2), x, f'{button}({games[i].release_world})')
            scr.attroff(curses.color_pair(1))
        else:
            if mode == 'ma':
                scr.addstr(y - (len(buttons) // 2), x, button)
            elif mode == 'gi':
                scr.addstr(y - (len(buttons) // 2), x, f'{button}({games[i].release_world})')


def yx_values(h, w, i, button):
    y = (h // 2) + i
    x = (w - len(button)) // 2

    return y, x


def search(scr):
    curses.curs_set(1)
    text = []

    while True:
        scr.clear()
        scr.addstr(0, 0, 'Search for a Game:\n')

        for i, c in enumerate(text):
            try:
                scr.addstr(1, i, c)
            except curses.error:
                text.pop()

        scr.refresh()
        key = scr.getch()

        match key:
            case curses.KEY_BACKSPACE:
                if text:
                    text.pop()
                else:
                    pass
        # Key Esc.
            case 27:
                main(scr)
                return
        # Key enter.
            case 10:
                game_info(scr, text)
                return
            case _:
                text.append(chr(key))


def game_info(scr, old_text):
    curses.curs_set(0)
    text = ''.join(old_text)

    scr.clear()

    scr.attron(curses.color_pair(3))
    scr.addstr(0, 0, 'Loading...')
    scr.attroff(curses.color_pair(3))

    scr.refresh()

    results = HowLongToBeat().search(text)
    if not results:
        scr.clear()

        scr.attron(curses.color_pair(2))
        scr.addstr(0, 0, 'Game not Found')
        scr.attroff(curses.color_pair(2))

        scr.refresh()
        time.sleep(1)

        search(scr)
        return

    games = sorted(results, key=lambda element: element.similarity, reverse=True)
    games = games[:10]

    results = [game.game_name for game in games]
    index = selection(scr, results, 'gi', games = games)

    print_game(scr, games[index], old_text)


def print_game(scr, game, text):
    scr.clear()

    info = {
    'Game': game.game_name, 'Year of Release': str(game.release_world), 'Developer': game.profile_dev,
    'Review Score': str(game.review_score), 'Campaign Duration': f'{game.main_story} Hours',
    '100% Duration': f'{game.completionist} Hours', 'Platforms': ', '.join(game.profile_platforms)
    }

    table = tabulate(list(info.items()), tablefmt='rounded_grid')

    scr.addstr(4, 0, table)
    scr.addstr(0, 0, '[ENTER] Add Game to the Backlog')
    scr.addstr(1, 0, '[BACKSPACE] Return to the Munu')
    scr.addstr(2, 0, '[ESC] Back')
    scr.refresh()

    new_action = False

    while not new_action:
        key = scr.getch()
        new_action = True

        match key:
            # Key Esc
            case 27:
                game_info(scr, text)
                return
            # Key enter
            case 10:
                add(scr, game)
                return
            case curses.KEY_BACKSPACE:
                main(scr)
                return
            case _:
                new_action = False


def add(scr, game):
    scr.clear()
    with open ('backlog.txt', 'r') as file:
        lines = file.readlines()

        if f'{game.game_name}({game.release_world})\n' in lines:
            scr.attron(curses.color_pair(2))
            scr.addstr('Game Already in Backlog')
            scr.attroff(curses.color_pair(2))

            scr.refresh()
            time.sleep(1)

            main(scr)
            return

    try:
        with open('backlog.txt', 'a') as file:
            file.write(f'{game.game_name}({game.release_world})\n')
    except:
        scr.attron(curses.color_pair(2))
        scr.addstr('Unable to Add Game')
        scr.attroff(curses.color_pair(2))
        scr.refresh()

        time.sleep(1)
        main(scr)
        return

    scr.attron(curses.color_pair(4))
    scr.addstr('Game Added Successfully')
    scr.attroff(curses.color_pair(4))

    scr.refresh()
    time.sleep(1)

    main(scr)
    return


def backlog(scr):
    scr.clear()
    with open('backlog.txt', 'r') as file:
        try:
            lines = file.readlines()
            lines.reverse()
        except:
            scr.attron(curses.color_pair(2))
            scr.addstr('Unable to read backlog')
            scr.attroff(curses.color_pair(2))

            scr.refresh()
            time.sleep(1)

            main(scr)
            return

        if not lines:
            scr.attron(curses.color_pair(3))
            scr.addstr(0, 0, 'The List is Empty')
            scr.attroff(curses.color_pair(3))

            scr.refresh()
            scr.getch()

            main(scr)
            return

        for i, line in enumerate(lines):
            scr.addstr(i, 0, line)

        scr.refresh()
        scr.getch()
        main(scr)
        return


def delete(scr):
    curses.curs_set(1)

    text = []
    while True:
        scr.clear()
        scr.addstr(0, 0,'Wich Game to Delete?\n')

        with open('backlog.txt', 'r') as file:
            try:
                lines = file.readlines()
                lines.reverse()
            except:
                scr.attron(curses.color_pair(2))
                scr.addstr('Unable to read backlog')
                scr.attroff(curses.color_pair(2))

                scr.refresh()
                time.sleep(1)

                main(scr)
                return

        if not lines:
            curses.curs_set(0)
            scr.clear()
            scr.attron(curses.color_pair(3))
            scr.addstr(0, 0, 'The List is Empty')
            scr.attroff(curses.color_pair(3))

            scr.refresh()
            scr.getch()

            main(scr)
            return

        for i, line in enumerate(lines):
            scr.addstr(i + 3, 0, line)

        if not text:
            scr.move(1, 0)

        for i, c in enumerate(text):
            try:
                scr.addstr(1, i, c)
                scr.move(1, i + 1)
                scr.refresh()
            except curses.error:
                text.pop()

        key = scr.getch()

        match key:
            case curses.KEY_BACKSPACE:
                if text:
                    text.pop()
                else:
                    pass
        # Key Esc.
            case 27:
                main(scr)
                return
        # Key enter.
            case 10:
                find_del(scr, text)
                return
            case _:
                text.append(chr(key))


def find_del(scr, text):
    text = ''.join(text).lower()
    found = False

    with open('backlog.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if validate(text, line.lower()):
                found = True
                game = line
                break
    if not found:
        curses.curs_set(0)
        scr.clear()

        scr.attron(curses.color_pair(2))
        scr.addstr('Game not Found')
        scr.attroff(curses.color_pair(2))

        scr.refresh()
        time.sleep(1)

        main(scr)
        return

    lines.remove(game)

    with open('backlog.txt', 'w') as file:
        for line in lines:
            file.write(line)

    curses.curs_set(0)
    scr.clear()

    scr.attron(curses.color_pair(4))
    scr.addstr('Game Removed Successfully')
    scr.attroff(curses.color_pair(4))

    scr.refresh()
    time.sleep(1)

    main(scr)
    return


def validate(text, line):
    regex = fr'^{text}(\(\d+\))$'
    result = re.search(regex, line)
    return result


if __name__ == '__main__':
    curses.wrapper(main)
