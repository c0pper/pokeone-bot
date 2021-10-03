import pyautogui
import time
import random

time.sleep(1)
print(pyautogui.position())
overworld_screen = pyautogui.locateCenterOnScreen("route29ref.png", grayscale=True)
print(overworld_screen)

cursor_away = 5

# Screen regions
sideparty_region = [1234, 470, 1365, 767]
battlecheck_region = [1100, 650, 1300, 750]
select_oth_pk_region = [565, 114, 794, 159]
pokecenter_region = [500, 100, 650, 250]

# Flags
botting = True
in_battle = False

# Buttons
fight_btn_x, fight_btn_y = 647, 650
run_btn_x, run_btn_y = 845, 730
choose_other_pk_btn_x, choose_other_pk_btn_y = 678, 240
move1_x, move1_y = 522, 586
move2_x, move2_y = 814, 589
move3_x, move3_y = 522, 652
move4_x, move4_y = 814, 652
chatbar_x, chatbar_y = 330, 755

# Route steps
grass_to_pc = ["down", "down", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left",
               "left", "left", "left", "left", "left", "left", "left", "left", "left", "up", "up", "up", "up",
               "up", "left", "up"]
pc_to_grass = ["right", "down", "down", "down", "down", "down", "right", "right", "right", "right", "right",
               "right", "right", "right", "right", "right", "right", "right", "right", "right", "down",
               "down"]


# Functions
def get_party_num():  # it returns 6 if bot starts during battle
    empty_slots = pyautogui.locateAllOnScreen('empty_slot.png', region=sideparty_region)
    pk_in_party = 6 - len(list(empty_slots))
    return pk_in_party


def walk(direction, walk_time):
    pyautogui.keyDown(direction)
    time.sleep(walk_time)
    pyautogui.keyUp(direction)


def single_press(direction):
    pyautogui.keyDown(direction)
    time.sleep(0.1)
    pyautogui.keyUp(direction)
    time.sleep(0.15)


def use_move(move_x, move_y):
    pyautogui.click(fight_btn_x, fight_btn_y)
    time.sleep(0.5)
    pyautogui.click(move_x, move_y)
    pyautogui.moveTo(cursor_away, cursor_away)
    time.sleep(0.5)


def leave_pcenter():
    for step in range(11):
        single_press("down")
    time.sleep(8)


def heal_at_pcenter():
    time.sleep(6)
    for step in range(8):
        single_press("up")
    for step in range(8):
        single_press("space")
        pyautogui.moveRel(5, 5)
    time.sleep(8)
    pyautogui.moveTo(cursor_away, cursor_away)
    single_press("space")
    leave_pcenter()
    time.sleep(8)


def move_between_pc_grass(destination):
    for step in destination:
        single_press(step)


def run_away():
    pyautogui.click(run_btn_x, run_btn_y)
    time.sleep(4)


def chat_debug(debug_message):
    pyautogui.click(chatbar_x, chatbar_y)
    pyautogui.write(debug_message)
    time.sleep(0.4)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    pyautogui.click(cursor_away, cursor_away)
    log = open("log.txt", "a+")
    log.write(debug_message + "\n")
    log.close()


party_num = get_party_num()
chat_debug("You have " + str(party_num) + " pokemon")

while botting:

    pyautogui.moveTo(cursor_away, cursor_away)

    # check if battle
    overworld_screen = pyautogui.locateCenterOnScreen("not_battle.png", region=battlecheck_region)

    if overworld_screen is not None:  # we're not in battle
        chat_debug("no battle")

        # check if 1st pokemon alive (if party 2, check 1st pok, if party 6, check 5th pok)
        fainted_on_screen = len(list(pyautogui.locateAllOnScreen("fainted_pkmn.png", region=sideparty_region)))

        while fainted_on_screen == party_num - 1:
            chat_debug("pokemon fainted")

            # go up right in the corner
            walk("up", 5)
            walk("right", 5)
            overworld_screen = pyautogui.locateCenterOnScreen("not_battle.png", region=battlecheck_region)
            if overworld_screen is None:
                in_battle = True
                break
            # go to pokecenter, heal, go back
            move_between_pc_grass(grass_to_pc)
            heal_at_pcenter()
            move_between_pc_grass(pc_to_grass)
            break

        # check if wiped (in pokemon center)
        pokecenter_on_screen = pyautogui.locateCenterOnScreen("pokecenter.png", region=pokecenter_region)

        if fainted_on_screen != party_num - 1:  # if not 5/6 fainted
            chat_debug("party_num not " + str(party_num - 1))
            if pokecenter_on_screen is None:  # and it's not because we wiped and are at pc
                chat_debug("we not in pc")

                # Walk in grass square
                chat_debug("walking around in grass")
                while not in_battle:
                    for step in range(random.randint(1, 5)):
                        single_press("down")
                    for step in range(random.randint(1, 4)):
                        single_press("up")
                    overworld_screen = pyautogui.locateCenterOnScreen("not_battle.png", region=battlecheck_region, grayscale=True)
                    if overworld_screen is None:
                        in_battle = True
                    else:
                        pass
            else:
                # walk to grass
                chat_debug("wiped! walking back to grass")
                leave_pcenter()
                move_between_pc_grass(pc_to_grass)

    else:
        in_battle = True
        while in_battle:
            chat_debug("battle")
            for try_attack in range(10):  # try attacking for 10 seconds
                use_move(move4_x, move4_y)

            current_pk_dead = pyautogui.locateCenterOnScreen("fainted_in_battle.png", region=select_oth_pk_region)
            overworld_screen = pyautogui.locateCenterOnScreen("not_battle.png", region=battlecheck_region)

            # Check if battle finished
            if overworld_screen is not None:
                in_battle = False
                break

            # Check if current pk dead
            if current_pk_dead is not None:  # select a pokemon screen is visible
                pyautogui.click(choose_other_pk_btn_x, choose_other_pk_btn_y)
                time.sleep(5)

                # Try to run
                run_away()
                overworld_screen = pyautogui.locateCenterOnScreen("not_battle.png", region=battlecheck_region)
                while overworld_screen is None:
                    run_away()
                    overworld_screen = pyautogui.locateCenterOnScreen("not_battle.png", region=battlecheck_region)
                pyautogui.moveTo(cursor_away, cursor_away)
                in_battle = False
