# pong2 by Grievous667 4/16/2023
# This is a pygame game that I wrote to practice object-oriented programming. As with most everything I've ever done, this program is incomplete, and it's a disaster in several places, but it's currently in a playable state.
#
# The general layout of the code is as follows:
#
# imports
# key Variables
# constants
# classes
# ---status_variable
# ---game_rule
# ---input_info
# ---game_states
# ---portal
# ---force_field
# ---scores
# ---button
# ---graphics
# ---sound
# ---paddle
# ---ball
# ---ai
# logic functions (mother nodes that call other functions)
# game loop
#
# The ball class handles collisions.
# Note: the statistics screen isn't implemented, in addition the the advanced settings menu and presets.


import pygame
import time
import random
from pygame.constants import K_w, K_s, K_a, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE

pygame.display.set_caption("Space Paddle")
screen_x = 1500
screen_y = 750
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
mouse_pos = pygame.mouse.get_pos()
rule_list = []
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.3)

# This is wired up to be variable, though low frame rates currently phase the ball through the paddles (increments per frame are greater than the paddle width). 300 is reccomended, don't go lower than 240, and make sure the fps is divisible by 60
FRAMES_PS = 300
MENU_FONT = pygame.font.SysFont('Bauhaus 93', 35, False, False)
OPTIONS_FONT = pygame.font.SysFont('Bauhaus 93', 25, False, False)
GAME_FONT = pygame.font.SysFont('Bauhaus 93', 20, False, False)
SCORE_FONT = pygame.font.SysFont('Sans-Serif', 50, False, False)
try:
    MENU_BACKGROUND = pygame.image.load(
        'images/menu_background.png').convert_alpha()
except:
    MENU_BACKGROUND = pygame.Surface((screen_x, screen_y))
    print("'images/menu_background.png' not found")
try:
    GAME_BACKGROUND = pygame.image.load(
        'images/game_background.png').convert_alpha()
except:
    GAME_BACKGROUND = pygame.Surface((screen_x, screen_y))
    print("'images/game_background.png' not found")


class status_variable():
    current_frame = 0
    music_avaliable = True
    sounds_avaliable = True


try:
    BONK_SOUND = 'sounds/bonk.wav'
    SCORE_SOUND = 'sounds/score.wav'
except:
    status_variable.sounds_avaliable = False
    print("''sounds/bonk.wav' and/or 'sounds/score.wav' not found")
try:
    TRACK_1 = 'game_music.mp3'
except:
    status_variable.music_avaliable = False
    print("'game_music.mp3' not found")


class game_rule():
    rule_dict = [    # "rule_dict" is a list of conditions (mostly booleans) that gets saved to an external txt file, and loaded on opening the game. The comments below list rules by their index and by their name/effect.
        True,  # 0 p1_is_human
        False,  # 1 p1_is_easy_ai
        False,  # 2 p1_is_normal_ai
        False,  # 3 p1_is_advanced_ai

        True,   # 4 p2_is_human
        False,  # 5 p2_is_easy_ai
        False,  # 6 p2_is_normal_ai
        False,  # 7 p2_is_advanced_ai

        1,  # 8 ball_count

        False,  # 9 ball_speed_snail
        False,  # 10 ball_speed_slow
        True,   # 11 ball_speed_noraml
        False,  # 12 ball_speed_fast
        False,  # 13 ball_speed_hyper

        True,   # 14 ball_normalization_normal
        False,  # 15 ball_normalization_straightened
        False,  # 16 ball_normalization_curved
        False,  # 17 ball_normalization_constant_acceleration
        False,  # 18 ball_normalization_none

        False,  # 19 ball_bounce_absorbant
        True,   # 20 ball_bounce_noraml
        False,  # 21 ball_bounce_intense
        False,  # 22 ball_bounce_burst
        False,  # 23 ball_bounce_none

        True,   # 24 ball_fade_normal
        False,  # 25 ball_fade_low_res
        False,  # 26 ball_fade_high_res
        False,  # 27 ball_fade_high_res_long
        False,  # 28 ball_fade_none

        "RED",  # 29 ball_color

        False,  # 30 paddle_speed_snail
        False,  # 31 paddle_speed_slow
        True,   # 32 paddle_speed_noraml
        False,  # 33 paddle_speed_fast
        False,  # 34 paddle_speed_hyper

        False,  # 35 paddle_acceleration_snail
        True,   # 36 paddle_acceleration_slow
        False,  # 37 paddle_acceleration_normal
        False,  # 38 paddle_acceleration_fast
        False,  # 39 paddle_acceleration_hyper

        True,   # 40 paddle_fade_normal
        False,  # 41 paddle_fade_low_res
        False,  # 42 paddle_fade_high_res
        False,  # 43 paddle_fade_high_res_long
        False,  # 44 paddle_fade_none
        "WHITE",  # 45 paddle_color_p1
        "WHITE",  # 46 paddle_color_p2

        True,    # 47 Ball-to-Ball Collisions_On
        False,   # 48 Ball-to-Ball Collisions_Off

        True,    # 49 ball_size_normal
        False,   # 50 ball_size_large
        False,   # 51 ball_size_random
        False,   # 52 ball_size_small

        True,    # 53 portals_none
        False,   # 54 portals_gate
        False,   # 55 portals_double_gate
        False,   # 56 portals_close_1
        False,   # 57 portals_close_2
        False,   # 58 portals_double_close
        False,   # 59 portals_central
        False,   # 60 portals_double_central
        False,   # 61 portals_barriers

        True,    # 62 shield_off
        False,   # 63 shield_charge_slow
        False,   # 64 shield_charge_normal
        False    # 65 shield_charge_fast

    ]
    rule_list_save_check = []

    # Below is AUTO LOAD SAVE DATA / NOTATE FILE ERRORS. Any errors should resolve after opening and closing after updating settings
    try:
        # This trys to access the save file in the same folder as this program. Error is expected when the save file doesn't exist, and will auto-resolve on the next save (occurs when settings are adjusted).
        save_data = open('game_rules.txt', 'r')
        saved_rules = save_data.readlines()
        try:
            # If the file is opened, this bit of code reads it and updates the rules. Error is expected when the save file is bad/formatted improperly. Will auto resolve by resetting to the default rules.
            rule_list = rule_dict.copy()
            for index in range(len(saved_rules)):
                try:
                    rule_list[index] = eval(saved_rules[index].strip("\n"))
                except:
                    rule_list[index] = saved_rules[index].strip("\n")
        except:
            print("LOAD ERROR")
            rule_list = rule_dict.copy()
    except:
        print("FILE ERROR")
        rule_list = rule_dict.copy()

    def save_rule_list():  # Creates the save file by copying the rule_list
        try:
            save_data = open('game_rules.txt', 'w')
            for items in game_rule.rule_list:
                save_data.writelines(str(items) + "\n")
            save_data.close()
        except:
            print("SAVE ERROR")

    # General use function for switching between game rules. Pass in all the game rules to cycle through.
    def cycle_game_rules(*args):
        rules = list(args)
        for index in range(len(rules)):
            try:
                try:
                    if rules[index] == True:
                        if rules[index + 1] == False:
                            rules[index] = False
                            rules[index + 1] = True
                            return rules
                except IndexError:
                    if rules[index] == True:
                        rules[index] = False
                        rules[0] = True
                        return rules
            except:
                print("RULE CYCLE ERROR")
                return args


class input_info():
    def mouse_position():
        pos = pygame.mouse.get_pos()
        return pos

    def key_input():
        keys = pygame.key.get_pressed()
        return keys
    can_press_esc = True


# Boolean values to control what game state (menu, options, playing) is active.
class game_states():
    menu_screen = True
    game_screen = False
    options_screen = False
    statistics_screen = False
    pause_screen = False

    ball_settings = False
    paddle_settings = False
    arena_settings = False

    advanced_settings = False
    preset_settings = False

    def new_game():
        game_states.set_game_state_play()

        force_field.reset_force_fields()

        portal.reset_portals()
        paddle.reset_paddles()
        scores.reset_scores()
        ball.reset_balls()

        scores.initialize_scores()

        sound.music()

    def falsify_states():  # Set all game states to false. Follow up with what to change to
        game_states.menu_screen = False
        game_states.game_screen = False
        game_states.options_screen = False
        game_states.pause_screen = False
        game_states.statistics_screen = False

        game_states.ball_settings = False
        game_states.paddle_settings = False
        game_states.arena_settings = False

        game_states.advanced_settings = False
        game_states.preset_settings = False

    def set_game_state_play():
        game_states.falsify_states()
        game_states.game_screen = True

    def set_game_state_menu():
        game_states.falsify_states()
        game_states.menu_screen = True

        sound.stop_music()

    def set_game_state_pause():
        game_states.falsify_states()
        game_states.pause_screen = True

    def set_game_state_options():
        game_states.falsify_states()
        game_states.options_screen = True

        for buttons in buttons_list:
            button.update_button_text(buttons)

    def set_game_state_stats():
        game_states.falsify_states()
        game_states.statistics_screen = True

    def set_game_state_ball_settings():
        game_states.falsify_states()
        game_states.options_screen = True
        game_states.ball_settings = True

    def set_game_state_paddle_settings():
        game_states.falsify_states()
        game_states.options_screen = True
        game_states.paddle_settings = True

    def set_game_state_arena_settings():
        game_states.falsify_states()
        game_states.options_screen = True
        game_states.arena_settings = True

    def set_game_state_advanced_settings():
        game_states.falsify_states()
        game_states.options_screen = True
        game_states.advanced_settings = True

    def set_game_state_preset_settings():
        game_states.falsify_states()
        game_states.options_screen = True
        game_states.preset_settings = True


class portal():
    portal_list = []

    portal_width = 10
    portal_height = 200

    def __init__(self, start_x, start_y, color):

        self.color = color

        self.x = start_x
        self.y = start_y

        self.width = portal.portal_width
        self.height = portal.portal_height

        self.position_tuple = self.x, self.y
        self.vibration_vector = pygame.math.Vector2(self.position_tuple)
        self.position_vector = pygame.math.Vector2(self.position_tuple)

        self.img = pygame.Surface((self.width, self.height))
        self.img.fill(self.color)
        self.hitbox = self.img.get_rect(topleft=(self.position_vector))

        self.speed_x = 0
        self.speed_y = 0

        self.vibrate_positions = []
        self.trail_density = 10
        self.trail_length = 10
        self.trail_base_opacity = 60
        self.trail_fade = 4

        self.displacement = 4

        portal.portal_list.append(self)

    # This spawns portals at the game's start depending on the game rules.
    def initialize_portals():
        if game_rule.rule_list[53] == True:
            pass
        elif game_rule.rule_list[54] == True:
            portal_1 = portal(screen_x/2 + 100, screen_y/2 -
                              portal.portal_height/2, (15, 200, 255))
            portal_2 = portal(screen_x/2 - 100 -
                              portal.portal_width, screen_y/2 -
                              portal.portal_height/2, (15, 200, 255))
        elif game_rule.rule_list[55] == True:
            portal_1 = portal(screen_x/2 + 100, screen_y -
                              portal.portal_height, (15, 200, 255))
            portal_2 = portal(screen_x/2 - 100 -
                              portal.portal_width, 0, (15, 200, 255))

            portal_3 = portal(screen_x/2 + 100, -1, (255, 0, 100))
            portal_4 = portal(screen_x/2 - 100 -
                              portal.portal_width, screen_y -
                              portal.portal_height, (255, 0, 100))
        elif game_rule.rule_list[56] == True:
            portal_1 = portal(500, 200 - portal.portal_height, (15, 200, 255))
            portal_2 = portal(1000 - portal.portal_width,
                              screen_y - 200, (15, 200, 255))
        elif game_rule.rule_list[57] == True:
            portal_1 = portal(1000, 200 - portal.portal_height, (15, 200, 255))
            portal_2 = portal(500 - portal.portal_width,
                              screen_y - 200, (15, 200, 255))
        elif game_rule.rule_list[58] == True:
            portal_1 = portal(1000, 200 - portal.portal_height, (15, 200, 255))
            portal_2 = portal(500 - portal.portal_width,
                              screen_y - 200, (15, 200, 255))
            portal_3 = portal(500, 200 - portal.portal_height, (255, 0, 100))
            portal_4 = portal(1000 - portal.portal_width,
                              screen_y - 200, (255, 0, 100))
        elif game_rule.rule_list[59] == True:
            portal_1 = portal(screen_x/2 - portal.portal_width/2,
                              200 - portal.portal_height, (15, 200, 255))
            portal_2 = portal(screen_x/2 - portal.portal_width /
                              2, screen_y - 200, (15, 200, 255))
        elif game_rule.rule_list[60] == True:
            portal_1 = portal(screen_x/2 - portal.portal_width/2,
                              200 - portal.portal_height, (15, 200, 255))
            portal_2 = portal(screen_x/2 - portal.portal_width /
                              2, screen_y - 200, (15, 200, 255))
            portal_3 = portal(screen_x/2 + 30,
                              400 - portal.portal_height, (255, 0, 100))
            portal_4 = portal(screen_x/2 - 30 - portal.portal_width,
                              screen_y - 400, (255, 0, 100))
        elif game_rule.rule_list[61] == True:
            portal_1 = portal(0,
                              0, (15, 200, 255))
            portal_2 = portal(screen_x - portal.portal_width,
                              screen_y - portal.portal_height, (15, 200, 255))
            portal_3 = portal(0,
                              screen_y - portal.portal_height, (255, 0, 100))
            portal_4 = portal(screen_x - portal.portal_width,
                              0, (255, 0, 100))

    def reset_portals():
        portal.portal_list.clear()
        portal.initialize_portals()

    def update_portals(self):  # Constantly called to move the portals
        self.position_vector[0] += self.speed_x
        self.position_vector[1] += self.speed_y
        self.hitbox.topleft = self.position_vector

    # Handles ball/portal interactions depending on which side of the portal/ball collides. Somehow it works, but don't ask me to explain it to you.
    def portal_logic():
        for portal_set in range(int(len(portal.portal_list))):
            if portal_set % 2 == 0:
                for balls in balls_list:
                    if balls.hitbox.colliderect(portal.portal_list[portal_set].hitbox):
                        if balls.speed_x < 0:
                            if balls.hitbox.left <= portal.portal_list[portal_set].hitbox.right:
                                balls.position_vector.x = portal.portal_list[portal_set+1].x - \
                                    balls.width - \
                                    portal.portal_list[portal_set +
                                                       1].displacement
                        elif balls.speed_x > 0:
                            if balls.hitbox.right >= portal.portal_list[portal_set].hitbox.left:
                                balls.position_vector.x = portal.portal_list[portal_set+1].x + \
                                    portal.portal_list[portal_set+1].width + \
                                    portal.portal_list[portal_set +
                                                       1].displacement
                        from_portal_top = portal.portal_list[portal_set].y - \
                            balls.position_vector.y
                        balls.position_vector.y = portal.portal_list[portal_set+1].y - \
                            from_portal_top
                        if balls.speed_x > 0:
                            balls.speed_x += .001
                        else:
                            balls.speed_x -= .001
                        if balls.speed_y > 0:
                            balls.speed_y += .01

                    if balls.hitbox.colliderect(portal.portal_list[portal_set+1].hitbox):
                        if balls.speed_x < 0:
                            if balls.hitbox.left <= portal.portal_list[portal_set+1].hitbox.right:
                                balls.position_vector.x = portal.portal_list[portal_set].x - \
                                    balls.width - \
                                    portal.portal_list[portal_set].displacement
                        elif balls.speed_x > 0:
                            if balls.hitbox.right >= portal.portal_list[portal_set+1].hitbox.left:
                                balls.position_vector.x = portal.portal_list[portal_set].x + \
                                    portal.portal_list[portal_set].width + \
                                    portal.portal_list[portal_set].displacement
                        from_portal_top = portal.portal_list[portal_set+1].y - \
                            balls.position_vector.y
                        balls.position_vector.y = portal.portal_list[portal_set].y - \
                            from_portal_top
                        if balls.speed_x > 0:
                            balls.speed_x += .001
                        else:
                            balls.speed_x -= .001
                        if balls.speed_y > 0:
                            balls.speed_y += .01

        for portals in portal.portal_list:

            # Vibration
            if portals.vibration_vector.x >= portals.position_vector.x:
                portals.vibration_vector.x -= portals.displacement * 1.8
            elif portals.vibration_vector.x < portals.position_vector.x:
                portals.vibration_vector.x += portals.displacement * 1.9
            if portals.vibration_vector.y >= portals.position_vector.y:
                portals.vibration_vector.y -= portals.displacement * 1.2
            elif portals.vibration_vector.y < portals.position_vector.y:
                portals.vibration_vector.y += portals.displacement * 1.21


class force_field():

    force_field_ready_p1 = False
    force_field_frame_p1 = 0

    force_field_ready_p2 = False
    force_field_frame_p2 = 0

    force_field_list = []

    def __init__(self, x, recharge_rate):

        self.recharge_rate = recharge_rate

        self.width = 10
        self.height = screen_y

        self.x = x
        self.y = 0

        self.img = pygame.Surface((self.width, self.height))
        self.img.fill("CYAN")
        self.rect = self.img.get_rect()

    def force_field_logic():
        if force_field.force_field_ready_p1 == False:
            if force_field.force_field_frame_p1 + force_field.force_field_list[0].recharge_rate < status_variable.current_frame:
                force_field.force_field_ready_p1 = True
        if force_field.force_field_ready_p2 == False:
            if force_field.force_field_frame_p2 + force_field.force_field_list[1].recharge_rate < status_variable.current_frame:
                force_field.force_field_ready_p2 = True

    def initialize_force_fields():
        if game_rule.rule_list[62] != True:
            if game_rule.rule_list[63] == True:
                p1_shield = force_field(0, 6000)
                p2_shield = force_field(screen_x - 10, 6000)
            if game_rule.rule_list[64] == True:
                p1_shield = force_field(0, 3000)
                p2_shield = force_field(screen_x - 10, 3000)
            if game_rule.rule_list[65] == True:
                p1_shield = force_field(0, 1000)
                p2_shield = force_field(screen_x - 10, 1000)

            force_field.force_field_list.append(p1_shield)
            force_field.force_field_list.append(p2_shield)

    def reset_force_fields():
        force_field.force_field_list.clear()
        force_field.initialize_force_fields()


class scores():
    p1_score = 0
    p2_score = 0

    def __init__(self, x, y, readout):
        self.x = x
        self.y = y
        self.image = readout
        self.box = self.image.get_rect(center=(self.x, self.y))

        score_list.append(self)

    def initialize_scores():
        p1_score_readout = scores(
            50, screen_y - 40, SCORE_FONT.render(str(scores.p1_score), True, "Cyan"))
        score_list.append(p1_score_readout)

        p2_score_readout = scores(screen_x - 50, screen_y -
                                  40, SCORE_FONT.render(str(scores.p2_score), True, "Cyan"))

    def point_p1(balls):

        ball.p1_score_reset_ball(balls)
        sound.score_sound_fx()
        if game_rule.rule_list[8] == 1:
            scores.score_time_freeze()
            paddle.reset_paddles()

        scores.p1_score += 1
        score_list.clear()
        p1_score_readout = scores(
            50, screen_y - 40, SCORE_FONT.render(str(scores.p1_score), True, "Cyan"))
        p2_score_readout = scores(screen_x - 50, screen_y -
                                  40, SCORE_FONT.render(str(scores.p2_score), True, "Cyan"))

        return p1_score_readout, p2_score_readout

    def point_p2(balls):

        ball.p2_score_reset_ball(balls)
        # sound.score_sound_fx()
        sound.score_sound_fx()
        if game_rule.rule_list[8] == 1:
            scores.score_time_freeze()
            paddle.reset_paddles()

        scores.p2_score += 1
        score_list.clear()
        p1_score_readout = scores(
            50, screen_y - 40, SCORE_FONT.render(str(scores.p1_score), True, "Cyan"))
        p2_score_readout = scores(screen_x - 50, screen_y -
                                  40, SCORE_FONT.render(str(scores.p2_score), True, "Cyan"))

        return p1_score_readout, p2_score_readout

    def point_p1_reset():
        paddle.reset_paddles()
        ball.reset_balls()

    def point_p2_reset():
        paddle.reset_paddles()
        ball.reset_balls()

    def score_time_freeze():
        time.sleep(.5)

    def reset_scores():
        scores.p1_score = 0
        scores.p2_score = 0
        score_list.clear()
        p1_score_readout = scores(
            50, screen_y - 40, SCORE_FONT.render(str(scores.p1_score), True, "Cyan"))
        p2_score_readout = scores(screen_x - 50, screen_y -
                                  40, SCORE_FONT.render(str(scores.p2_score), True, "Cyan"))
        return p1_score_readout, p2_score_readout


class button():

    def __init__(self, x, y, pic, hover_pic, buttons, index):
        self.x = x
        self.y = y
        self.pos = x, y
        self.width = 100
        self.height = 50
        self.dimensions = self.width, self.height
        self.image = pic
        self.backup_image = pic
        self.hover_image = hover_pic
        self.box = self.image.get_rect(topleft=(self.x, self.y))
        self.index = index
        self.can_click = True
        buttons.insert(self.index, self)

    def draw_buttons(self):
        global mouse_pos
        screen.blit(self.image, self.box)

        if self.box.collidepoint(mouse_pos):
            self.image = self.hover_image
            screen.blit(self.image, self.box)

            if pygame.mouse.get_pressed()[0] and buttons_list[self.index].can_click == True:
                buttons_list[self.index].can_click = False

                if self.index == 0:
                    # Play Button
                    game_states.new_game()

                elif self.index == 1:
                    # Options Button
                    game_states.set_game_state_options()
                elif self.index == 2:
                    # Exit Button
                    pygame.quit()
                    exit()
                elif self.index == 3:
                    # Pause Button
                    game_states.set_game_state_pause()
                elif self.index == 4:
                    game_states.set_game_state_play()
                elif self.index == 5:
                    game_states.set_game_state_menu()
                elif self.index == 6:
                    game_states.set_game_state_stats()
                elif self.index == 7:
                    game_rule.rule_list[0], game_rule.rule_list[1], game_rule.rule_list[2], game_rule.rule_list[3] = game_rule.cycle_game_rules(
                        game_rule.rule_list[0], game_rule.rule_list[1], game_rule.rule_list[2], game_rule.rule_list[3])
                    button.update_button_text(self)
                elif self.index == 8:
                    game_rule.rule_list[4], game_rule.rule_list[5], game_rule.rule_list[6], game_rule.rule_list[7] = game_rule.cycle_game_rules(
                        game_rule.rule_list[4], game_rule.rule_list[5], game_rule.rule_list[6], game_rule.rule_list[7])
                    button.update_button_text(self)
                elif self.index == 9:
                    if game_states.ball_settings == True:
                        game_states.set_game_state_options()
                    else:
                        game_states.set_game_state_ball_settings()
                elif self.index == 10:
                    if game_states.paddle_settings == True:
                        game_states.set_game_state_options()
                    else:
                        game_states.set_game_state_paddle_settings()
                elif self.index == 11:
                    if game_states.arena_settings == True:
                        game_states.set_game_state_options()
                    else:
                        game_states.set_game_state_arena_settings()
                elif self.index == 12:
                    if game_states.advanced_settings == True:
                        game_states.set_game_state_options()
                    else:
                        game_states.set_game_state_advanced_settings()
                elif self.index == 13:
                    if game_states.preset_settings == True:
                        game_states.set_game_state_options()
                    else:
                        game_states.set_game_state_preset_settings()
                elif self.index == 14:
                    if game_rule.rule_list[8] < 10:
                        game_rule.rule_list[8] += 1
                    elif game_rule.rule_list[8] == 10:
                        game_rule.rule_list[8] = 1
                    button.update_button_text(self)
                elif self.index == 15:
                    game_rule.rule_list[9], game_rule.rule_list[10], game_rule.rule_list[11], game_rule.rule_list[12], game_rule.rule_list[13] = game_rule.cycle_game_rules(
                        game_rule.rule_list[9], game_rule.rule_list[10], game_rule.rule_list[11], game_rule.rule_list[12], game_rule.rule_list[13])
                    button.update_button_text(self)
                elif self.index == 16:
                    game_rule.rule_list[14], game_rule.rule_list[15], game_rule.rule_list[16], game_rule.rule_list[17], game_rule.rule_list[18] = game_rule.cycle_game_rules(
                        game_rule.rule_list[14], game_rule.rule_list[15], game_rule.rule_list[16], game_rule.rule_list[17], game_rule.rule_list[18])
                    button.update_button_text(self)
                elif self.index == 17:
                    game_rule.rule_list[19], game_rule.rule_list[20], game_rule.rule_list[21], game_rule.rule_list[22], game_rule.rule_list[23] = game_rule.cycle_game_rules(
                        game_rule.rule_list[19], game_rule.rule_list[20], game_rule.rule_list[21], game_rule.rule_list[22], game_rule.rule_list[23])
                    button.update_button_text(self)
                elif self.index == 18:
                    game_rule.rule_list[24], game_rule.rule_list[25], game_rule.rule_list[26], game_rule.rule_list[27], game_rule.rule_list[28] = game_rule.cycle_game_rules(
                        game_rule.rule_list[24], game_rule.rule_list[25], game_rule.rule_list[26], game_rule.rule_list[27], game_rule.rule_list[28])
                    button.update_button_text(self)
                elif self.index == 19:
                    if game_rule.rule_list[29] == "MAROON":
                        game_rule.rule_list[29] = "RED"
                    elif game_rule.rule_list[29] == "RED":
                        game_rule.rule_list[29] = "ORANGE"
                    elif game_rule.rule_list[29] == "ORANGE":
                        game_rule.rule_list[29] = "DARKORANGE"
                    elif game_rule.rule_list[29] == "DARKORANGE":
                        game_rule.rule_list[29] = "GOLD"
                    elif game_rule.rule_list[29] == "GOLD":
                        game_rule.rule_list[29] = "YELLOW"
                    elif game_rule.rule_list[29] == "YELLOW":
                        game_rule.rule_list[29] = "GREEN"
                    elif game_rule.rule_list[29] == "GREEN":
                        game_rule.rule_list[29] = "MAGENTA"
                    elif game_rule.rule_list[29] == "MAGENTA":
                        game_rule.rule_list[29] = "DARKVIOLET"
                    elif game_rule.rule_list[29] == "DARKVIOLET":
                        game_rule.rule_list[29] = "BLUE"
                    elif game_rule.rule_list[29] == "BLUE":
                        game_rule.rule_list[29] = "NAVY"
                    elif game_rule.rule_list[29] == "NAVY":
                        game_rule.rule_list[29] = "MAROON"

                    button.update_button_text(self)
                elif self.index == 20:
                    game_rule.rule_list[30], game_rule.rule_list[31], game_rule.rule_list[32], game_rule.rule_list[33], game_rule.rule_list[34] = game_rule.cycle_game_rules(
                        game_rule.rule_list[30], game_rule.rule_list[31], game_rule.rule_list[32], game_rule.rule_list[33], game_rule.rule_list[34])
                    button.update_button_text(self)
                elif self.index == 21:
                    game_rule.rule_list[35], game_rule.rule_list[36], game_rule.rule_list[37], game_rule.rule_list[38], game_rule.rule_list[39] = game_rule.cycle_game_rules(
                        game_rule.rule_list[35], game_rule.rule_list[36], game_rule.rule_list[37], game_rule.rule_list[38], game_rule.rule_list[39])
                    button.update_button_text(self)
                elif self.index == 22:
                    game_rule.rule_list[40], game_rule.rule_list[41], game_rule.rule_list[42], game_rule.rule_list[43], game_rule.rule_list[44] = game_rule.cycle_game_rules(
                        game_rule.rule_list[40], game_rule.rule_list[41], game_rule.rule_list[42], game_rule.rule_list[43], game_rule.rule_list[44])
                    button.update_button_text(self)
                elif self.index == 23:
                    if game_rule.rule_list[45] == "WHITE":
                        game_rule.rule_list[45] = "YELLOW"
                    elif game_rule.rule_list[45] == "YELLOW":
                        game_rule.rule_list[45] = "MAGENTA"
                    elif game_rule.rule_list[45] == "MAGENTA":
                        game_rule.rule_list[45] = "WHITE"
                    button.update_button_text(self)
                elif self.index == 24:
                    if game_rule.rule_list[46] == "WHITE":
                        game_rule.rule_list[46] = "YELLOW"
                    elif game_rule.rule_list[46] == "YELLOW":
                        game_rule.rule_list[46] = "MAGENTA"
                    elif game_rule.rule_list[46] == "MAGENTA":
                        game_rule.rule_list[46] = "WHITE"
                    button.update_button_text(self)
                elif self.index == 25:
                    game_rule.rule_list[47], game_rule.rule_list[48] = game_rule.cycle_game_rules(
                        game_rule.rule_list[47], game_rule.rule_list[48])
                    button.update_button_text(self)
                elif self.index == 26:
                    game_rule.rule_list[49], game_rule.rule_list[50], game_rule.rule_list[51], game_rule.rule_list[52] = game_rule.cycle_game_rules(
                        game_rule.rule_list[49], game_rule.rule_list[50], game_rule.rule_list[51], game_rule.rule_list[52])
                    button.update_button_text(self)
                elif self.index == 27:
                    game_states.set_game_state_menu()
                elif self.index == 28:
                    game_rule.save_rule_list()
                    game_rule.rule_list_save_check = game_rule.rule_list.copy()
                elif self.index == 29:
                    game_rule.rule_list[53], game_rule.rule_list[54], game_rule.rule_list[55], game_rule.rule_list[56], game_rule.rule_list[57], game_rule.rule_list[58], game_rule.rule_list[59], game_rule.rule_list[60], game_rule.rule_list[61] = game_rule.cycle_game_rules(
                        game_rule.rule_list[53], game_rule.rule_list[54], game_rule.rule_list[55], game_rule.rule_list[56], game_rule.rule_list[57], game_rule.rule_list[58], game_rule.rule_list[59], game_rule.rule_list[60], game_rule.rule_list[61])
                    button.update_button_text(self)
                elif self.index == 30:
                    game_rule.rule_list[62], game_rule.rule_list[63], game_rule.rule_list[64], game_rule.rule_list[65] = game_rule.cycle_game_rules(
                        game_rule.rule_list[62], game_rule.rule_list[63], game_rule.rule_list[64], game_rule.rule_list[65])
                    button.update_button_text(self)
                else:
                    print("Error: Unhandled Button")
        else:
            self.image = self.backup_image
            screen.blit(self.image, self.box)

    def change_button_text(button, new_text):
        button.image = OPTIONS_FONT.render(str(new_text), True, "White")
        button.backup_image = OPTIONS_FONT.render(
            str(new_text), True, "White")
        button.hover_image = OPTIONS_FONT.render(
            str(new_text), True, "Cyan")
        button.box = button.image.get_rect(topleft=(button.x, button.y))

    def update_button_text(self):
        if self.index == 7:
            if game_rule.rule_list[0] == True:
                button.change_button_text(
                    buttons_list[self.index], "P1: HUMAN")
            if game_rule.rule_list[1] == True:
                button.change_button_text(
                    buttons_list[self.index], "P1: EASY AI")
            if game_rule.rule_list[2] == True:
                button.change_button_text(
                    buttons_list[self.index], "P1: NORMAL AI")
            if game_rule.rule_list[3] == True:
                button.change_button_text(
                    buttons_list[self.index], "P1: ADVANCED AI")
        elif self.index == 8:
            if game_rule.rule_list[4] == True:
                button.change_button_text(
                    buttons_list[self.index], "P2: HUMAN")
            if game_rule.rule_list[5] == True:
                button.change_button_text(
                    buttons_list[self.index], "P2: EASY AI")
            if game_rule.rule_list[6] == True:
                button.change_button_text(
                    buttons_list[self.index], "P2: NORMAL AI")
            if game_rule.rule_list[7] == True:
                button.change_button_text(
                    buttons_list[self.index], "P2: ADVANCED AI")
        elif self.index == 14:
            button.change_button_text(
                buttons_list[self.index], "BALL COUNT: " + str(game_rule.rule_list[8]))
        elif self.index == 15:
            if game_rule.rule_list[9] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL SPEED: SNAIL")
            if game_rule.rule_list[10] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL SPEED: SLOW")
            if game_rule.rule_list[11] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL SPEED: NORMAL")
            if game_rule.rule_list[12] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL SPEED: FAST")
            if game_rule.rule_list[13] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL SPEED: HYPER")
        elif self.index == 16:
            if game_rule.rule_list[14] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL NORMALIZATION: NORMAL")
            if game_rule.rule_list[15] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL NORMALIZATION: STRAIGHTENED")
            if game_rule.rule_list[16] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL NORMALIZATION: CURVED")
            if game_rule.rule_list[17] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL NORMALIZATION: CONSTANT ACCELERATION")
            if game_rule.rule_list[18] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL NORMALIZATION: NONE")
        elif self.index == 17:
            if game_rule.rule_list[19] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL BOUNCE: ABSORBANT")
            if game_rule.rule_list[20] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL BOUNCE: NORMAL")
            if game_rule.rule_list[21] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL BOUNCE: INTENSE")
            if game_rule.rule_list[22] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL BOUNCE: BURST")
            if game_rule.rule_list[23] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL BOUNCE: NONE")
        elif self.index == 18:
            if game_rule.rule_list[24] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL FADE: NORMAL")
            if game_rule.rule_list[25] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL FADE: LOW-RES")
            if game_rule.rule_list[26] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL FADE: HIGH-RES")
            if game_rule.rule_list[27] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL FADE: HIGH-RES LONG")
            if game_rule.rule_list[28] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL FADE: NONE")
        elif self.index == 19:
            try:
                button.change_button_text(
                    buttons_list[self.index], "BALL COLOR: " + str(game_rule.rule_list[29]))
            except:
                button.change_button_text(
                    buttons_list[self.index], "BALL COLOR: NULL")
        elif self.index == 20:
            if game_rule.rule_list[30] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE SPEED: SNAIL")
            if game_rule.rule_list[31] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE SPEED: SLOW")
            if game_rule.rule_list[32] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE SPEED: NORMAL")
            if game_rule.rule_list[33] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE SPEED: FAST")
            if game_rule.rule_list[34] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE SPEED: HYPER")
        elif self.index == 21:
            if game_rule.rule_list[35] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE ACCELERATION: SNAIL")
            if game_rule.rule_list[36] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE ACCELERATION: SLOW")
            if game_rule.rule_list[37] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE ACCELERATION: NORMAL")
            if game_rule.rule_list[38] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE ACCELERATION: FAST")
            if game_rule.rule_list[39] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE ACCELERATION: HYPER")
        elif self.index == 22:
            if game_rule.rule_list[40] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE FADE: NORMAL")
            if game_rule.rule_list[41] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE FADE: LOW-RES")
            if game_rule.rule_list[42] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE FADE: HIGH-RES")
            if game_rule.rule_list[43] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE FADE: HIGH-RES LONG")
            if game_rule.rule_list[44] == True:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE FADE: NONE")
        elif self.index == 23:
            try:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE COLOR P1: " + str(game_rule.rule_list[45]))
            except:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE COLOR: NULL")
        elif self.index == 24:
            try:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE COLOR P2: " + str(game_rule.rule_list[46]))
            except:
                button.change_button_text(
                    buttons_list[self.index], "PADDLE COLOR: NULL")
        elif self.index == 25:
            if game_rule.rule_list[47] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL-TO-BALL COLLISIONS: ON")
            if game_rule.rule_list[48] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL-TO-BALL COLLISIONS: OFF")
        elif self.index == 26:
            if game_rule.rule_list[49] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL SIZE: NORMAL")
            if game_rule.rule_list[50] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL SIZE: LARGE")
            if game_rule.rule_list[51] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL SIZE: RANDOM")
            if game_rule.rule_list[52] == True:
                button.change_button_text(
                    buttons_list[self.index], "BALL SIZE: SMALL")
        elif self.index == 29:
            if game_rule.rule_list[53] == True:
                button.change_button_text(
                    buttons_list[self.index], "PORTALS: NONE")
            if game_rule.rule_list[54] == True:
                button.change_button_text(
                    buttons_list[self.index], "PORTALS: GATE CONFIGURATION")
            if game_rule.rule_list[55] == True:
                button.change_button_text(
                    buttons_list[self.index], "PORTALS: TWIN GATE CONFIGURATION")
            if game_rule.rule_list[56] == True:
                button.change_button_text(
                    buttons_list[self.index], "PORTALS: CLOSE CONFIGURATION 1")
            if game_rule.rule_list[57] == True:
                button.change_button_text(
                    buttons_list[self.index], "PORTALS: CLOSE CONFIGURATION 2")
            if game_rule.rule_list[58] == True:
                button.change_button_text(
                    buttons_list[self.index], "PORTALS: TWIN CLOSE CONFIGURATION")
            if game_rule.rule_list[59] == True:
                button.change_button_text(
                    buttons_list[self.index], "PORTALS: CENTRAL CONFIGURATION")
            if game_rule.rule_list[60] == True:
                button.change_button_text(
                    buttons_list[self.index], "PORTALS: TWIN CENTRAL CONFIGURATION")
            if game_rule.rule_list[61] == True:
                button.change_button_text(
                    buttons_list[self.index], "PORTALS: BARRIER CONFIGURATION")
        elif self.index == 30:
            if game_rule.rule_list[62] == True:
                button.change_button_text(
                    buttons_list[self.index], "SHIELDS: OFF")
            if game_rule.rule_list[63] == True:
                button.change_button_text(
                    buttons_list[self.index], "SHIELDS: SLOW_CHARGE")
            if game_rule.rule_list[64] == True:
                button.change_button_text(
                    buttons_list[self.index], "SHIELDS: NORMAL_CHARGE")
            if game_rule.rule_list[65] == True:
                button.change_button_text(
                    buttons_list[self.index], "SHIELDS: FAST_CHARGE")

    def initialize_buttons(buttons_list):
        play_button = button(20, 20, MENU_FONT.render(
            "Play", True, "White"), MENU_FONT.render("Play", True, "Cyan"), buttons_list, 0)

        options_button = button(20, 100, MENU_FONT.render(
            "Options", True, "White"), MENU_FONT.render("Options", True, "Cyan"), buttons_list, 1)
        exit_button = button(20, 140, MENU_FONT.render(
            "Exit", True, "White"), MENU_FONT.render("Exit", True, "Cyan"), buttons_list, 2)

        pause_button = button(screen_x/2, screen_y - 30, GAME_FONT.render(
            "Pause", True, "White"), GAME_FONT.render("Pause", True, "Cyan"), buttons_list, 3)
        unpause_button = button(screen_x/2 - 10, screen_y - 30, GAME_FONT.render(
            "Unpause", True, "White"), GAME_FONT.render("Unpause", True, "Cyan"), buttons_list, 4)
        pause_to_menu_button = button(screen_x/2 - 20, screen_y - 55, GAME_FONT.render(
            "Main Menu", True, "White"), GAME_FONT.render("Main Menu", True, "Cyan"), buttons_list, 5)
        statistics_button = button(20, 60, MENU_FONT.render(
            "Statistics", True, "White"), MENU_FONT.render("Statistics", True, "Cyan"), buttons_list, 6)

        # Options Buttons

        p1_ai_button = button(20, 20, OPTIONS_FONT.render(
            "P1: HUMAN", True, "White"), OPTIONS_FONT.render("P1: HUMAN", True, "Cyan"), buttons_list, 7)
        p2_ai_button = button(20, 50, OPTIONS_FONT.render(
            "P2: HUMAN", True, "White"), OPTIONS_FONT.render("P2: HUMAN", True, "Cyan"), buttons_list, 8)

        ball_settings_button = button(20, 100, OPTIONS_FONT.render(
            "BALL SETTINGS", True, "White"), OPTIONS_FONT.render("BALL SETTINGS", True, "Cyan"), buttons_list, 9)
        paddle_settings_button = button(20, 130, OPTIONS_FONT.render(
            "PADDLE SETTINGS", True, "White"), OPTIONS_FONT.render("PADDLE SETTINGS", True, "Cyan"), buttons_list, 10)
        arena_settings_button = button(20, 160, OPTIONS_FONT.render(
            "ARENA SETTINGS", True, "White"), OPTIONS_FONT.render("ARENA SETTINGS", True, "Cyan"), buttons_list, 11)
        advanced_settings_button = button(20, 210, OPTIONS_FONT.render(
            "ADVANCED SETTINGS", True, "White"), OPTIONS_FONT.render("ADVANCED SETTINGS", True, "Cyan"), buttons_list, 12)
        presets_button = button(20, 240, OPTIONS_FONT.render(
            "PRESETS", True, "White"), OPTIONS_FONT.render("PRESETS", True, "Cyan"), buttons_list, 13)

        ball_count_button = button(300, 20, OPTIONS_FONT.render(
            "BALL COUNT: " + str(game_rule.rule_list[8]), True, "White"), OPTIONS_FONT.render("BALL COUNT: " + str(game_rule.rule_list[8]), True, "Cyan"), buttons_list, 14)
        ball_speed_button = button(300, 50, OPTIONS_FONT.render(
            "BALL SPEED: NORMAL", True, "White"), OPTIONS_FONT.render("BALL SPEED: NORMAL", True, "Cyan"), buttons_list, 15)
        ball_normalization_button = button(300, 80, OPTIONS_FONT.render(
            "BALL NORMALIZATION: NORMAL", True, "White"), OPTIONS_FONT.render("BALL NORMALIZATION: NORMAL", True, "Cyan"), buttons_list, 16)
        ball_bounce_button = button(300, 110, OPTIONS_FONT.render(
            "BALL BOUNCE: NORMAL", True, "White"), OPTIONS_FONT.render("BALL BOUNCE: NORMAL", True, "Cyan"), buttons_list, 17)
        ball_fade_button = button(300, 140, OPTIONS_FONT.render(
            "BALL FADE: NORMAL", True, "White"), OPTIONS_FONT.render("BALL FADE: NORMAL", True, "Cyan"), buttons_list, 18)
        ball_color_button = button(300, 190, OPTIONS_FONT.render(
            "BALL COLOR: RED", True, "White"), OPTIONS_FONT.render("BALL COLOR: RED", True, "Cyan"), buttons_list, 19)
        ball_to_ball_collisions_button = button(300, 240, OPTIONS_FONT.render(
            "BALL-TO-BALL COLLISIONS: ON", True, "White"), OPTIONS_FONT.render("BALL-TO-BALL COLLISIONS: ON", True, "Cyan"), buttons_list, 25)
        ball_size_button = button(300, 290, OPTIONS_FONT.render(
            "BALL SIZE: NORMAL", True, "White"), OPTIONS_FONT.render("BALL SIZE: NORMAL", True, "Cyan"), buttons_list, 26)

        paddle_speed_button = button(300, 20, OPTIONS_FONT.render(
            "PADDLE SPEED: NORMAL", True, "White"), OPTIONS_FONT.render("PADDLE SPEED: NORMAL", True, "Cyan"), buttons_list, 20)
        paddle_bounce_button = button(300, 50, OPTIONS_FONT.render(
            "PADDLE ACCELERATION: NORMAL", True, "White"), OPTIONS_FONT.render("PADDLE ACCELERATION: NORMAL", True, "Cyan"), buttons_list, 21)
        paddle_fade_button = button(300, 80, OPTIONS_FONT.render(
            "PADDLE FADE: NORMAL", True, "White"), OPTIONS_FONT.render("PADDLE FADE: NORMAL", True, "Cyan"), buttons_list, 22)
        paddle_color_p1_button = button(300, 130, OPTIONS_FONT.render(
            "PADDLE COLOR P1: " + game_rule.rule_list[45], True, "White"), OPTIONS_FONT.render("PADDLE COLOR P1: " + game_rule.rule_list[45], True, "Cyan"), buttons_list, 23)
        paddle_color_p2_button = button(300, 160, OPTIONS_FONT.render(
            "PADDLE COLOR P2: " + game_rule.rule_list[46], True, "White"), OPTIONS_FONT.render("PADDLE COLOR P2: " + game_rule.rule_list[46], True, "Cyan"), buttons_list, 24)
        back_button = button(20, screen_y - 40, OPTIONS_FONT.render(
            "BACK", True, "White"), OPTIONS_FONT.render("BACK", True, "Cyan"), buttons_list, 27)
        save_button = button(120, screen_y - 40, OPTIONS_FONT.render(
            "SAVE", True, "White"), OPTIONS_FONT.render("SAVE", True, "Cyan"), buttons_list, 28)

        portals_button = button(300, 20, OPTIONS_FONT.render(
            "PORTALS: NONE", True, "White"), OPTIONS_FONT.render("PORTALS: NONE", True, "Cyan"), buttons_list, 29)
        shield_button = button(300, 50, OPTIONS_FONT.render(
            "PORTALS: NONE", True, "White"), OPTIONS_FONT.render("PORTALS: NONE", True, "Cyan"), buttons_list, 30)


class graphics():
    angle = 0

    def draw_backgrounds():
        if game_states.menu_screen == True or game_states.options_screen == True:
            screen.blit(MENU_BACKGROUND, (0, 0))
        elif game_states.game_screen == True:
            screen.blit(GAME_BACKGROUND, (0, 0))

        elif game_states.pause_screen == True:
            screen.blit(GAME_BACKGROUND, (0, 0))
        else:
            screen.blit(MENU_BACKGROUND, (0, 0))

    def draw_buttons():
        if game_states.menu_screen == True:
            button.draw_buttons(buttons_list[0])
            button.draw_buttons(buttons_list[1])
            button.draw_buttons(buttons_list[2])
            button.draw_buttons(buttons_list[6])
        elif game_states.game_screen == True:
            button.draw_buttons(buttons_list[3])
        elif game_states.pause_screen == True:
            button.draw_buttons(buttons_list[4])
            button.draw_buttons(buttons_list[5])
        elif game_states.options_screen == True:
            button.draw_buttons(buttons_list[7])
            button.draw_buttons(buttons_list[8])
            button.draw_buttons(buttons_list[9])
            button.draw_buttons(buttons_list[10])
            button.draw_buttons(buttons_list[11])
            button.draw_buttons(buttons_list[12])
            button.draw_buttons(buttons_list[13])
            button.draw_buttons(buttons_list[27])
            if game_rule.rule_list != game_rule.rule_list_save_check:
                button.draw_buttons(buttons_list[28])
            if game_states.ball_settings == True:
                button.draw_buttons(buttons_list[14])
                button.draw_buttons(buttons_list[15])
                button.draw_buttons(buttons_list[16])
                button.draw_buttons(buttons_list[17])
                button.draw_buttons(buttons_list[18])
                button.draw_buttons(buttons_list[19])
                button.draw_buttons(buttons_list[25])
                button.draw_buttons(buttons_list[26])
            elif game_states.paddle_settings == True:
                button.draw_buttons(buttons_list[20])
                button.draw_buttons(buttons_list[21])
                button.draw_buttons(buttons_list[22])
                button.draw_buttons(buttons_list[23])
                button.draw_buttons(buttons_list[24])
            elif game_states.arena_settings == True:
                button.draw_buttons(buttons_list[29])
                button.draw_buttons(buttons_list[30])
        elif game_states.statistics_screen == True:
            button.draw_buttons(buttons_list[27])
        else:
            print("Error: Unhandled Button Information for Current Game State")

    def draw_paddles():
        local_index = 0
        for id in paddles_list:
            paddles_list[local_index].hitbox = paddles_list[local_index].image.get_rect(
                topleft=(paddles_list[local_index].position_vector))
            screen.blit(paddles_list[local_index].image,
                        paddles_list[local_index].hitbox)
            local_index += 1

    def paddle_trails():
        if game_rule.rule_list[44] != True:
            for paddles in paddles_list:
                if game_states.game_screen == True:
                    if status_variable.current_frame % paddles.trail_density == 0:
                        paddles.previous_positions.append(paddles.hitbox)
                if len(paddles.previous_positions) > paddles.trail_length:
                    paddles.previous_positions.pop(0)
                img = pygame.Surface((paddles.width, paddles.height))
                img.fill(paddles.color)
                alpha = paddles.trail_base_opacity
                for pos in paddles.previous_positions[::-1]:
                    alpha -= paddles.trail_fade
                    img.set_alpha(alpha)
                    screen.blit(img, pos)

    def draw_balls():
        for balls in balls_list:
            balls.hitbox = balls.image.get_rect(
                topleft=(balls.position_vector.x, balls.position_vector.y))
            screen.blit(balls.image, balls.hitbox)

    def ball_trails():
        if game_rule.rule_list[28] != True:
            for balls in balls_list:
                if game_states.game_screen == True:
                    if status_variable.current_frame % balls.trail_density == 0:
                        balls.previous_positions.append(balls.hitbox)
                if len(balls.previous_positions) > balls.trail_length:
                    balls.previous_positions.pop(0)
                img = pygame.Surface((balls.width, balls.height))
                img.fill(balls.color)
                alpha = balls.trail_base_opacity
                for pos in balls.previous_positions[::-1]:
                    alpha -= balls.trail_fade
                    img.set_alpha(alpha)
                    screen.blit(img, pos)

    def draw_scores():
        for score in score_list:
            screen.blit(score.image, score.box)

    def draw_force_field():
        if force_field.force_field_ready_p1 == True:
            screen.blit(
                force_field.force_field_list[0].img, (force_field.force_field_list[0].x, force_field.force_field_list[0].y))
        if force_field.force_field_ready_p2 == True:
            screen.blit(
                force_field.force_field_list[1].img, (force_field.force_field_list[1].x, force_field.force_field_list[1].y))

    def draw_portals():
        for portals in portal.portal_list:
            screen.blit(portals.img,
                        portals.position_vector)

    def portal_vibrations():
        for portals in portal.portal_list:
            if game_states.game_screen == True:
                if status_variable.current_frame % portals.trail_density == 0:
                    portals.vibrate_positions.append(portals.vibration_vector)
            if len(portals.vibrate_positions) > portals.trail_length:
                portals.vibrate_positions.pop(0)
            img = pygame.Surface((portals.width, portals.height))
            img.fill(portals.color)
            alpha = portals.trail_base_opacity
            for pos in portals.vibrate_positions[::-1]:
                alpha -= portals.trail_fade
                img.set_alpha(alpha)
                screen.blit(img, pos)


class sound():

    def music():
        if status_variable.music_avaliable == True:
            try:
                pygame.mixer.music.load(TRACK_1)
                pygame.mixer.music.play(-1)
            except:
                pass
        else:
            pass

    def stop_music():
        pygame.mixer.music.stop()

    def ball_sound_fx():
        if status_variable.sounds_avaliable == True:
            try:
                audio = pygame.mixer.Sound(BONK_SOUND)
                audio.play()
            except:
                pass
        else:
            pass

    def score_sound_fx():
        if status_variable.sounds_avaliable == True:
            try:
                audio = pygame.mixer.Sound(SCORE_SOUND)
                audio.play()
            except:
                pass
        else:
            pass


class paddle():

    def __init__(self, x, y, color_input):

        self.color = color_input

        self.width = 20
        self.height = 200

        self.x = x - self.width/2
        self.y = y - self.height/2

        self.position_tuple = self.x, self.y
        self.position_vector = pygame.math.Vector2(self.position_tuple)

        self.speed_x = 0
        self.speed_y = 0

        self.top_speed_x = 20 / (FRAMES_PS / 60)
        self.top_speed_y = 20 / (FRAMES_PS / 60)

        self.normal_acceleration = .65 / (FRAMES_PS / 60)
        self.normal_deaccerlaration_factor = .9

        self.collision_paddle_bounce_factor = .2 / (FRAMES_PS / 60)
        self.border_bounce_factor = .7 / (FRAMES_PS / 60)

        self.free_zone = 500
        self.extra_y = 90

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.hitbox = self.image.get_rect(topleft=(self.x, self.y))

        if game_rule.rule_list[35] == True:
            self.acceleration_modifier = .1
            self.deacceleration_modifier = 1.005
        elif game_rule.rule_list[36] == True:
            self.acceleration_modifier = .4
            self.deacceleration_modifier = 1.002
        elif game_rule.rule_list[37] == True:
            self.acceleration_modifier = 1
            self.deacceleration_modifier = 1
        elif game_rule.rule_list[38] == True:
            self.acceleration_modifier = 5
            self.deacceleration_modifier = 1
        elif game_rule.rule_list[39] == True:
            self.acceleration_modifier = 10
            self.deacceleration_modifier = 1

        # Trail
        self.previous_positions = []
        if game_rule.rule_list[40] == True:
            self.trail_density = .2 * (FRAMES_PS / 60)
            self.trail_length = 10
            self.trail_base_opacity = 60
            self.trail_fade = 4
        elif game_rule.rule_list[41] == True:
            self.trail_density = .5 * (FRAMES_PS / 60)
            self.trail_length = 10
            self.trail_base_opacity = 60
            self.trail_fade = 4
        elif game_rule.rule_list[42] == True:
            self.trail_density = .1 * (FRAMES_PS / 60)
            self.trail_length = 25
            self.trail_base_opacity = 60
            self.trail_fade = 5
        elif game_rule.rule_list[43] == True:
            self.trail_density = .1 * (FRAMES_PS / 60)
            self.trail_length = 25
            self.trail_base_opacity = 60
            self.trail_fade = 2

        paddles_list.append(self)

    def initialize_paddles():
        p1_paddle = paddle(50, screen_y/2, game_rule.rule_list[45])
        p2_paddle = paddle(screen_x - 50, screen_y/2, game_rule.rule_list[46])

    def handle_paddle_input():
        if game_rule.rule_list[0] == True:
            if pygame.key.get_pressed()[K_w]:
                paddle.paddle_up_input_p1()
            if pygame.key.get_pressed()[K_s]:
                paddle.paddle_down_input_p1()
            if pygame.key.get_pressed()[K_a]:
                paddle.paddle_left_input_p1()
            if pygame.key.get_pressed()[K_d]:
                paddle.paddle_right_input_p1()

        if game_rule.rule_list[4] == True:
            if pygame.key.get_pressed()[K_UP]:
                paddle.paddle_up_input_p2()
            if pygame.key.get_pressed()[K_DOWN]:
                paddle.paddle_down_input_p2()
            if pygame.key.get_pressed()[K_LEFT]:
                paddle.paddle_left_input_p2()
            if pygame.key.get_pressed()[K_RIGHT]:
                paddle.paddle_right_input_p2()

    #
    # P1
    #
    def paddle_up_input_p1():
        # Control input by framerate because speed is relative to how many inputs are received
        if status_variable.current_frame % (FRAMES_PS / 60) == 0:
            if paddles_list[0].speed_y > -paddles_list[0].top_speed_y:
                paddles_list[0].speed_y -= paddles_list[0].normal_acceleration * \
                    paddles_list[0].acceleration_modifier

    def paddle_down_input_p1():
        if status_variable.current_frame % (FRAMES_PS / 60) == 0:
            if paddles_list[0].speed_y < paddles_list[0].top_speed_y:
                paddles_list[0].speed_y += paddles_list[0].normal_acceleration * \
                    paddles_list[0].acceleration_modifier

    def paddle_left_input_p1():
        if status_variable.current_frame % (FRAMES_PS / 60) == 0:
            if paddles_list[0].speed_x > -paddles_list[0].top_speed_x:
                paddles_list[0].speed_x -= paddles_list[0].normal_acceleration * \
                    paddles_list[0].acceleration_modifier

    def paddle_right_input_p1():
        if status_variable.current_frame % (FRAMES_PS / 60) == 0:
            if paddles_list[0].speed_x < paddles_list[0].top_speed_x:
                paddles_list[0].speed_x += paddles_list[0].normal_acceleration * \
                    paddles_list[0].acceleration_modifier

    def stop_paddle_p1():
        if status_variable.current_frame % (FRAMES_PS / 60) == 0:
            if paddles_list[0].speed_y > 0:
                paddle.paddle_up_input_p1()
            if paddles_list[0].speed_y < 0:
                paddle.paddle_down_input_p1()

    def paddle_movement_p1():
        # Acceleration
        if game_rule.rule_list[30] == True:
            paddles_list[0].x += paddles_list[0].speed_x * .5
            paddles_list[0].y += paddles_list[0].speed_y * .5
        elif game_rule.rule_list[31] == True:
            paddles_list[0].x += paddles_list[0].speed_x * .75
            paddles_list[0].y += paddles_list[0].speed_y * .75
        elif game_rule.rule_list[32] == True:
            paddles_list[0].x += paddles_list[0].speed_x * 1
            paddles_list[0].y += paddles_list[0].speed_y * 1
        elif game_rule.rule_list[33] == True:
            paddles_list[0].x += paddles_list[0].speed_x * \
                1.25
            paddles_list[0].y += paddles_list[0].speed_y * \
                1.25
        elif game_rule.rule_list[34] == True:
            paddles_list[0].x += paddles_list[0].speed_x * \
                1.5
            paddles_list[0].y += paddles_list[0].speed_y * \
                1.5

        paddles_list[0].position_tuple = paddles_list[0].x, paddles_list[0].y
        paddles_list[0].position_vector = pygame.math.Vector2(
            paddles_list[0].position_tuple)

        # Deacceleration
        if not pygame.key.get_pressed()[K_a] and not pygame.key.get_pressed()[K_d]:
            if status_variable.current_frame % (FRAMES_PS / 60) == 0:
                paddles_list[0].speed_x *= paddles_list[0].normal_deaccerlaration_factor * \
                    paddles_list[0].deacceleration_modifier
        if not pygame.key.get_pressed()[K_w] and not pygame.key.get_pressed()[K_s]:
            if status_variable.current_frame % (FRAMES_PS / 60) == 0:
                paddles_list[0].speed_y *= paddles_list[0].normal_deaccerlaration_factor * \
                    paddles_list[0].deacceleration_modifier
        else:
            pass

        # Kill tiny floats so that the paddle stops eventually
        if abs(paddles_list[0].speed_x) < .0001:
            paddles_list[0].speed_x = 0
        if abs(paddles_list[0].speed_y) < .0001:
            paddles_list[0].speed_y = 0
    #
    # P2
    #

    def paddle_up_input_p2():
        if status_variable.current_frame % (FRAMES_PS / 60) == 0:
            if paddles_list[1].speed_y > -paddles_list[1].top_speed_y:
                paddles_list[1].speed_y -= paddles_list[1].normal_acceleration * \
                    paddles_list[1].acceleration_modifier

    def paddle_down_input_p2():
        if status_variable.current_frame % (FRAMES_PS / 60) == 0:
            if paddles_list[1].speed_y < paddles_list[1].top_speed_y:
                paddles_list[1].speed_y += paddles_list[1].normal_acceleration * \
                    paddles_list[1].acceleration_modifier

    def paddle_left_input_p2():
        if status_variable.current_frame % (FRAMES_PS / 60) == 0:
            if paddles_list[1].speed_x > -paddles_list[1].top_speed_x:
                paddles_list[1].speed_x -= paddles_list[1].normal_acceleration * \
                    paddles_list[1].acceleration_modifier

    def paddle_right_input_p2():
        if status_variable.current_frame % (FRAMES_PS / 60) == 0:
            if paddles_list[1].speed_x < paddles_list[1].top_speed_x:
                paddles_list[1].speed_x += paddles_list[1].normal_acceleration * \
                    paddles_list[1].acceleration_modifier

    def stop_paddle_p2():
        if status_variable.current_frame % (FRAMES_PS / 60) == 0:
            if paddles_list[1].speed_y > 0:
                paddle.paddle_up_input_p2()
            if paddles_list[1].speed_y < 0:
                paddle.paddle_down_input_p2()

    def paddle_movement_p2():
        # Acceleration
        if game_rule.rule_list[30] == True:
            paddles_list[1].x += paddles_list[1].speed_x * .5
            paddles_list[1].y += paddles_list[1].speed_y * .5
        elif game_rule.rule_list[31] == True:
            paddles_list[1].x += paddles_list[1].speed_x * .75
            paddles_list[1].y += paddles_list[1].speed_y * .75
        elif game_rule.rule_list[32] == True:
            paddles_list[1].x += paddles_list[1].speed_x * 1
            paddles_list[1].y += paddles_list[1].speed_y * 1
        elif game_rule.rule_list[33] == True:
            paddles_list[1].x += paddles_list[1].speed_x * \
                1.25
            paddles_list[1].y += paddles_list[1].speed_y * \
                1.25
        elif game_rule.rule_list[34] == True:
            paddles_list[1].x += paddles_list[1].speed_x * \
                1.5
            paddles_list[1].y += paddles_list[1].speed_y * \
                1.5

        paddles_list[1].position_tuple = paddles_list[1].x, paddles_list[1].y
        paddles_list[1].position_vector = pygame.math.Vector2(
            paddles_list[1].position_tuple)

        # Deacceleration
        if not pygame.key.get_pressed()[K_LEFT] and not pygame.key.get_pressed()[K_RIGHT]:
            if status_variable.current_frame % (FRAMES_PS / 60) == 0:
                paddles_list[1].speed_x *= paddles_list[1].normal_deaccerlaration_factor * \
                    paddles_list[1].deacceleration_modifier
        if not pygame.key.get_pressed()[K_UP] and not pygame.key.get_pressed()[K_DOWN]:
            if status_variable.current_frame % (FRAMES_PS / 60) == 0:
                paddles_list[1].speed_y *= paddles_list[1].normal_deaccerlaration_factor * \
                    paddles_list[1].deacceleration_modifier
        else:
            pass

        # Kill tiny floats so that the paddle stops eventually
        if abs(paddles_list[1].speed_x) < .0001:
            paddles_list[1].speed_x = 0
        if abs(paddles_list[1].speed_y) < .0001:
            paddles_list[1].speed_y = 0

    def restrict_paddles():  # Kepp the paddles inbounds/in their assigned areas
        for paddles in paddles_list:
            if paddles.x + paddles.width > screen_x:
                paddles.x = screen_x - paddles.width
                paddles.speed_x = - \
                    abs(paddles.speed_x *
                        paddles.border_bounce_factor)
            if paddles.x < 0:
                paddles.x = 0
                paddles.speed_x =  \
                    abs(paddles.speed_x *
                        paddles.border_bounce_factor)

            if paddles.y + paddles.height > screen_y + paddles.extra_y:
                paddles.y = screen_y + paddles.extra_y - paddles.height
                paddles.speed_y = - \
                    abs(paddles.speed_y * paddles.border_bounce_factor)
            if paddles.y < -paddles.extra_y:
                paddles.y = -paddles.extra_y
                paddles.speed_y = abs(
                    paddles.speed_y * paddles.border_bounce_factor)
        if paddles_list[0].x + paddles_list[0].width > paddles_list[0].free_zone:
            paddles_list[0].x = paddles_list[0].free_zone - \
                paddles_list[0].width
            paddles_list[0].speed_x = - \
                abs(paddles_list[0].speed_x *
                    paddles_list[0].border_bounce_factor)
        if paddles_list[1].x < screen_x - paddles_list[1].free_zone:
            paddles_list[1].x = screen_x - paddles_list[1].free_zone
            paddles_list[1].speed_x = abs(
                paddles_list[1].speed_y * paddles_list[1].border_bounce_factor)

    def reset_paddles():
        paddles_list.clear()
        paddle.initialize_paddles()


class ball():

    def __init__(self, x, y, speed_x, speed_y):
        try:
            self.color = game_rule.rule_list[29]
        except:
            self.color = "RED"

        if game_rule.rule_list[49] == True:
            self.scale = 50
            self.width = self.scale
            self.height = self.scale
        elif game_rule.rule_list[50] == True:
            self.scale = 100
            self.width = self.scale
            self.height = self.scale
        elif game_rule.rule_list[51] == True:
            self.scale = random.randint(10, 150)
            self.width = self.scale
            self.height = self.scale
        elif game_rule.rule_list[52] == True:
            self.scale = 20
            self.width = self.scale
            self.height = self.scale
        else:
            self.width = 10
            self.height = screen_y

        self.start_x = x - self.width/2
        self.start_y = y - self.height/2

        self.position_tuple = self.start_x, self.start_y
        self.position_vector = pygame.math.Vector2(self.position_tuple)

        self.speed_x = speed_x
        self.speed_y = speed_y

        self.collision_paddle_bounce_factor = .2 / (FRAMES_PS / 60)

        self.collision_frame = 0

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.hitbox = self.image.get_rect(topleft=(self.position_vector))

        if game_rule.rule_list[14] == True:
            self.top_speed_x = 25
            self.top_speed_y = 12.5

            self.slow_to_top_speed_factor_x = .999
            self.slow_to_top_speed_factor_y = .999

            # When the ball is over max speed by a large margin, slow it down quickly
            self.slow_to_top_speed_factor_x_fast = .990
            self.slow_to_top_speed_factor_y_fast = .990

            # How large that margin is, multiplied by the top speed
            self.speed_x_soft_cap_factor = 2.5
            self.speed_y_soft_cap_factor = 2.5

        # 15 ball_normalization_straightened
        elif game_rule.rule_list[15] == True:
            self.top_speed_x = 10
            self.top_speed_y = .1

            self.speed_x_soft_cap_factor = 2.5
            self.speed_y_soft_cap_factor = 1.0

            self.slow_to_top_speed_factor_x = .9995
            self.slow_to_top_speed_factor_y = .995

            self.slow_to_top_speed_factor_x_fast = .990
            self.slow_to_top_speed_factor_y_fast = self.slow_to_top_speed_factor_y

        elif game_rule.rule_list[16] == True:  # 16 ball_normalization_curved
            self.top_speed_x = .75
            self.top_speed_y = 1.5

            self.speed_x_soft_cap_factor = 5
            self.speed_y_soft_cap_factor = 1

            self.slow_to_top_speed_factor_x = .998
            self.slow_to_top_speed_factor_y = .9995

            self.slow_to_top_speed_factor_x_fast = self.slow_to_top_speed_factor_x
            self.slow_to_top_speed_factor_y_fast = .990

        # 17 ball_normalization_constant_acceleration
        elif game_rule.rule_list[17] == True:
            self.top_speed_x = 0
            self.top_speed_y = 2.5

            self.speed_x_soft_cap_factor = 1
            self.speed_y_soft_cap_factor = 4

            self.slow_to_top_speed_factor_x = 1.0001
            self.slow_to_top_speed_factor_y = .999

            self.slow_to_top_speed_factor_x_fast = self.slow_to_top_speed_factor_x
            self.slow_to_top_speed_factor_y_fast = .995

        elif game_rule.rule_list[18] == True:  # 18 ball_normalization_none
            self.top_speed_x = 10000
            self.top_speed_y = 10000

            self.speed_x_soft_cap_factor = 1
            self.speed_y_soft_cap_factor = 1

            self.slow_to_top_speed_factor_x = 1
            self.slow_to_top_speed_factor_y = 1

            self.slow_to_top_speed_factor_x_fast = self.slow_to_top_speed_factor_x
            self.slow_to_top_speed_factor_y_fast = self.slow_to_top_speed_factor_y

        if game_rule.rule_list[19] == True:  # 19 ball_bounce_absorbant
            self.bounce_factor_x = .8
            self.bounce_factor_y = .5
        elif game_rule.rule_list[20] == True:  # 20 ball_bounce_noraml
            self.bounce_factor_x = 1.1
            self.bounce_factor_y = .9
        elif game_rule.rule_list[21] == True:  # 21 ball_bounce_intense
            self.bounce_factor_x = 1.5
            self.bounce_factor_y = .8
        elif game_rule.rule_list[22] == True:  # 22 ball_bounce_burst
            self.bounce_factor_x = 2
            self.bounce_factor_y = 1
        # 23 ball_bounce_none (simply reflects off the paddle with no extra speed added)
        elif game_rule.rule_list[23] == True:
            self.bounce_factor_x = 1
            self.bounce_factor_y = 1

        try:
            if game_rule.rule_list[9] == True:  # 9 ball_speed_snail
                self.top_speed_x *= .5
                self.top_speed_y *= .5
            elif game_rule.rule_list[10] == True:  # 10 ball_speed_slow
                self.top_speed_x *= .75
                self.top_speed_y *= .75
            elif game_rule.rule_list[11] == True:  # 11 ball_speed_noraml
                self.top_speed_x *= 1
                self.top_speed_y *= 1
            elif game_rule.rule_list[12] == True:  # 12 ball_speed_fast
                self.top_speed_x *= 1.25
                self.top_speed_y *= 1.25
            elif game_rule.rule_list[13] == True:  # 13 ball_speed_hyper
                self.top_speed_x *= 1.75
                self.top_speed_y *= 1.75
        except:
            pass

        # Trail
        self.previous_positions = []
        if game_rule.rule_list[24] == True:  # 24 ball_fade_normal
            self.trail_density = .5 * (FRAMES_PS / 60)
            self.trail_length = 25
            self.trail_base_opacity = 100
            self.trail_fade = 5
        elif game_rule.rule_list[25] == True:  # 25 ball_fade_low_res
            self.trail_density = 1 * (FRAMES_PS / 60)
            self.trail_length = 2.0
            self.trail_base_opacity = 100
            self.trail_fade = 5
        elif game_rule.rule_list[26] == True:  # 26 ball_fade_high_res
            self.trail_density = 2 * (FRAMES_PS / 60)
            self.trail_length = 5.0
            self.trail_base_opacity = 100
            self.trail_fade = 2
        elif game_rule.rule_list[27] == True:  # 27 ball_fade_high_res_long
            self.trail_density = .2 * (FRAMES_PS / 60)
            self.trail_length = 100
            self.trail_base_opacity = 100
            self.trail_fade = 1

        balls_list.append(self)

    def ball_update(self):
        try:
            if game_rule.rule_list[9] == True:  # 9 ball_speed_snail
                self.position_vector[0] += self.speed_x * .5 / (FRAMES_PS / 60)
                self.position_vector[1] += self.speed_y * .5 / (FRAMES_PS / 60)
            elif game_rule.rule_list[10] == True:  # 10 ball_speed_slow
                self.position_vector[0] += self.speed_x * .75 / \
                    (FRAMES_PS / 60)
                self.position_vector[1] += self.speed_y * .75 / \
                    (FRAMES_PS / 60)
            elif game_rule.rule_list[11] == True:  # 11 ball_speed_noraml
                self.position_vector[0] += self.speed_x * 1 / (FRAMES_PS / 60)
                self.position_vector[1] += self.speed_y * 1 / (FRAMES_PS / 60)
            elif game_rule.rule_list[12] == True:  # 12 ball_speed_fast
                self.position_vector[0] += self.speed_x * \
                    1.5 / (FRAMES_PS / 60)
                self.position_vector[1] += self.speed_y * \
                    1.5 / (FRAMES_PS / 60)
            elif game_rule.rule_list[13] == True:  # 13 ball_speed_hyper
                self.position_vector[0] += self.speed_x * 2 / (FRAMES_PS / 60)
                self.position_vector[1] += self.speed_y * 2 / (FRAMES_PS / 60)
        except:
            self.position_vector[0] += self.speed_x / (FRAMES_PS / 60)
            self.position_vector[1] += self.speed_y / (FRAMES_PS / 60)

        # Apply soft cap to top speed
        if abs(self.speed_x) > self.top_speed_x * self.speed_x_soft_cap_factor:
            self.speed_x *= self.slow_to_top_speed_factor_x_fast
        elif abs(self.speed_x) > self.top_speed_x:
            self.speed_x *= self.slow_to_top_speed_factor_x

        if abs(self.speed_y) > self.top_speed_y * self.speed_y_soft_cap_factor:
            self.speed_y *= self.slow_to_top_speed_factor_y_fast
        elif abs(self.speed_y) > self.top_speed_y:
            self.speed_y *= self.slow_to_top_speed_factor_y

    def initialize_balls(speed_x, speed_y):
        ball(screen_x/2, screen_y/2, speed_x, speed_y)

    def ball_collision_borders():
        for balls in balls_list:
            if balls.hitbox.top <= 0:
                balls.speed_y = abs(balls.speed_y)
                balls.position_vector.y = 1
            elif balls.hitbox.bottom >= screen_y:
                balls.speed_y = -abs(balls.speed_y)
                balls.position_vector.y = screen_y - balls.height - 1

            if balls.hitbox.left <= 0:
                if force_field.force_field_ready_p1 == True:
                    balls.speed_x = -balls.speed_x
                    force_field.force_field_ready_p1 = False
                    force_field.force_field_frame_p1 = status_variable.current_frame
                elif balls.hitbox.right <= 0:
                    scores.point_p2(balls)

            if balls.hitbox.right >= screen_x:
                if force_field.force_field_ready_p2 == True:
                    balls.speed_x = -balls.speed_x
                    force_field.force_field_ready_p2 = False
                    force_field.force_field_frame_p2 = status_variable.current_frame
                elif balls.hitbox.left >= screen_x:
                    scores.point_p1(balls)

    def identify_ball_to_ball_collisions(ball_1):
        for ball_2 in balls_list:
            if ball_1.collision_frame + 150 < status_variable.current_frame:
                if ball_1.hitbox.colliderect(ball_2.hitbox) and ball_1 != ball_2:
                    ball.ball_to_ball_collision(ball_1, ball_2)

                    ball_1.collision_frame = status_variable.current_frame

    def ball_to_ball_collision(ball_1, ball_2):
        sound.ball_sound_fx()

        # determine which ball was hit
        if ball_1.position_vector.y > ball_2.position_vector.y:
            if ball_1.speed_y < ball_2.speed_y:
                ball_2.speed_y += ball_1.speed_y
                ball_1.speed_y *= .5
            else:
                ball_1.speed_y += ball_2.speed_y
                ball_2.speed_y *= .5
            ball_1.position_vector.y += abs(ball_2.speed_y)
            ball_2.position_vector.y += -abs(ball_1.speed_y)

        elif ball_1.position_vector.y < ball_2.position_vector.y:
            if ball_1.speed_y > ball_2.speed_y:
                ball_2.speed_y += ball_1.speed_y
                ball_1.speed_y *= .5
            else:
                ball_1.speed_y += ball_2.speed_y
                ball_2.speed_y *= .5
            ball_1.position_vector.y += -abs(ball_2.speed_y)
            ball_2.position_vector.y += abs(ball_1.speed_y)

        if ball_1.position_vector.x > ball_2.position_vector.x:
            if ball_1.speed_x < ball_2.speed_x:
                ball_2.speed_x += ball_1.speed_x
                ball_1.speed_x *= .5
            else:
                ball_1.speed_x += ball_2.speed_x
                ball_2.speed_x *= .5
            ball_1.position_vector.x += abs(ball_2.speed_x)
            ball_2.position_vector.x += -abs(ball_1.speed_x)

        else:
            if ball_1.speed_x > ball_2.speed_x:
                ball_2.speed_x += ball_1.speed_x
                ball_1.speed_x *= .5
            else:
                ball_1.speed_x += ball_2.speed_x
                ball_2.speed_x *= .5
            ball_1.position_vector.x += -abs(ball_2.speed_x)
            ball_2.position_vector.x += abs(ball_1.speed_x)

    def ball_to_paddle_collision(balls):
        for paddles in paddles_list:
            if balls.hitbox.colliderect(paddles.hitbox):
                sound.ball_sound_fx()
                if balls.hitbox.bottom - 5 <= paddles.hitbox.top:
                    paddles.speed_x += balls.speed_x * balls.collision_paddle_bounce_factor
                    if balls.hitbox.top <= 5:
                        balls.speed_y *= .5
                        balls.speed_x *= .2
                        paddles.speed_y = abs(paddles.speed_y)
                    else:
                        balls.position_vector.y = paddles.hitbox.top - \
                            3 - balls.height
                        balls.speed_y = -abs(balls.speed_y)

                        if game_rule.rule_list[17] != True:
                            balls.speed_x += paddles.speed_x * balls.bounce_factor_x
                        balls.speed_y += paddles.speed_y * balls.bounce_factor_y
                        paddles.speed_y = - \
                            abs(paddles.speed_y * paddles.collision_paddle_bounce_factor) - \
                            (balls.speed_y * balls.collision_paddle_bounce_factor)

                elif balls.hitbox.top + 5 >= paddles.hitbox.bottom:
                    paddles.speed_x += balls.speed_x * balls.collision_paddle_bounce_factor
                    if balls.hitbox.bottom >= screen_y - 5:
                        balls.speed_y *= .5
                        balls.speed_x *= .2
                        paddles.speed_y = -abs(paddles.speed_y)
                    else:
                        balls.position_vector.y = paddles.hitbox.bottom + 3
                        balls.speed_y = abs(balls.speed_y)

                        if game_rule.rule_list[17] != True:
                            balls.speed_x += paddles.speed_x * balls.bounce_factor_x
                        balls.speed_y += paddles.speed_y * balls.bounce_factor_y
                        paddles.speed_y = abs(
                            paddles.speed_y * paddles.collision_paddle_bounce_factor) - (balls.speed_y * balls.collision_paddle_bounce_factor)

                else:
                    paddles.speed_y += balls.speed_y * balls.collision_paddle_bounce_factor
                    if balls.position_vector.x > paddles.x:
                        balls.position_vector.x = paddles.hitbox.right + 3
                        balls.speed_x = abs(balls.speed_x)

                        if game_rule.rule_list[17] != True:
                            balls.speed_x += paddles.speed_x * balls.bounce_factor_x
                        balls.speed_y += paddles.speed_y * balls.bounce_factor_y

                        paddles.speed_x = - \
                            abs(paddles.speed_x * paddles.collision_paddle_bounce_factor) - \
                            (balls.speed_x * balls.collision_paddle_bounce_factor)

                    elif balls.position_vector.x < paddles.x:
                        balls.position_vector.x = paddles.hitbox.left - \
                            3 - balls.width
                        balls.speed_x = -abs(balls.speed_x)

                        if game_rule.rule_list[17] != True:
                            balls.speed_x += paddles.speed_x * balls.bounce_factor_x
                        balls.speed_y += paddles.speed_y * balls.bounce_factor_y

                        paddles.speed_x = abs(
                            paddles.speed_x * paddles.collision_paddle_bounce_factor) - (balls.speed_x * balls.collision_paddle_bounce_factor)
                    paddles.speed_y /= 2

    def reset_balls():
        balls_list.clear()
        if game_rule.rule_list[8] == 1:
            y = random.randint(-1.0, 1.0)
            if y == 0:
                y = random.randint(1, 100)
                if y > 50:
                    y = .50
                else:
                    y = -.50
            ball.initialize_balls(-10, y)
        else:
            for x in range(game_rule.rule_list[8]):
                x = random.randint(1, 100)
                if x > 50:
                    x = 10
                else:
                    x = -10
                y = random.randint(-10, 10)
                if y == 0:
                    y = random.randint(1, 100)
                    if y > 50:
                        y = .50
                    else:
                        y = -.50
                ball.initialize_balls(x, y)

    def p1_score_reset_ball(balls):
        balls_list.remove(balls)
        y = random.randint(1, 100)
        if y > 50:
            y = .5
        else:
            y = -.5
        ball(screen_x/2, screen_y/2, 10, y)

    def p2_score_reset_ball(balls):
        balls_list.remove(balls)
        y = random.randint(1, 100)
        if y > 50:
            y = .5
        else:
            y = -.5
        ball(screen_x/2, screen_y/2, -10, y)


class ai():
    y_intercept_location_p1 = screen_x/2
    y_intercept_location_p2 = screen_x/2

    def ai_mother_node_p1():  # Note: for some reason, the p1 AI is worse than the p2 one.
        if game_rule.rule_list[1] == True:
            ai.easy_ai_p1()
        elif game_rule.rule_list[2] == True:
            ai.normal_ai_p1()
        elif game_rule.rule_list[3] == True:
            ai.advanced_ai_p1()

    def ai_mother_node_p2():
        if game_rule.rule_list[5] == True:
            ai.easy_ai_p2()
        elif game_rule.rule_list[6] == True:
            ai.normal_ai_p2()
        elif game_rule.rule_list[7] == True:
            ai.advanced_ai_p2()

    def get_ball_trajectory_p1():
        for balls in balls_list:

            try:

                frames_till_x_intersect = (
                    balls.position_vector.x - 100) / balls.speed_x
                ai.y_intercept_location_p1 = balls.position_vector.y + \
                    frames_till_x_intersect * balls.speed_y

                pos_x = balls.position_vector.x
                pos_y = balls.position_vector.y
                spd_x = balls.speed_x
                spd_y = balls.speed_y
                for x in range(int(balls.position_vector.x - 100)):
                    if pos_y >= screen_y - balls.height:
                        spd_y = -abs(spd_y)
                    elif pos_y <= 0:
                        spd_y = abs(spd_y)

                    if pos_x > 0:
                        pos_x += spd_x
                        pos_y += spd_y
                    elif pos_x <= 0:
                        pass
                    try:
                        for portal_set in range(int(len(portal.portal_list))):
                            if portal_set % 2 == 0:
                                if portal.portal_list[portal_set].hitbox.collidepoint((pos_x, pos_y)):
                                    if spd_x > 0:
                                        if pos_x + balls.width >= portal.portal_list[portal_set].hitbox.left:
                                            pos_x = portal.portal_list[portal_set+1].x - \
                                                balls.width - \
                                                portal.portal_list[portal_set +
                                                                   1].displacement
                                    elif spd_x < 0:
                                        if pos_x <= portal.portal_list[portal_set].hitbox.right:
                                            pos_x = portal.portal_list[portal_set+1].x + \
                                                portal.portal_list[portal_set+1].width + \
                                                portal.portal_list[portal_set +
                                                                   1].displacement
                                    from_portal_top = portal.portal_list[portal_set].y - \
                                        pos_y
                                    pos_y = portal.portal_list[portal_set+1].y - \
                                        from_portal_top
                                    if spd_x > 0:
                                        spd_x += .001
                                    else:
                                        spd_x -= .001
                                    if spd_y > 0:
                                        spd_y += .01

                                if portal.portal_list[portal_set+1].hitbox.collidepoint((pos_x, pos_y)):
                                    if spd_x < 0:
                                        if pos_x <= portal.portal_list[portal_set+1].hitbox.right:
                                            pos_x = portal.portal_list[portal_set].x - \
                                                balls.width - \
                                                portal.portal_list[portal_set].displacement
                                    elif spd_x > 0:
                                        if pos_x + balls.width >= portal.portal_list[portal_set+1].hitbox.left:
                                            pos_x = portal.portal_list[portal_set].x + \
                                                portal.portal_list[portal_set].width + \
                                                portal.portal_list[portal_set].displacement
                                    from_portal_top = portal.portal_list[portal_set+1].y - \
                                        pos_y
                                    pos_y = portal.portal_list[portal_set].y - \
                                        from_portal_top
                                    if spd_x > 0:
                                        spd_x += .001
                                    else:
                                        spd_x -= .001
                                    if spd_y > 0:
                                        spd_y += .01
                    except IndexError:
                        pass
                    ai.y_intercept_location_p1 = pos_y
            except ZeroDivisionError:
                ai.y_intercept_location_p1 = pos_y

            return ai.y_intercept_location_p1

    def get_ball_trajectory_p2():
        for balls in balls_list:

            try:

                frames_till_x_intersect = (
                    ((screen_x - 100) - balls.position_vector.x) / balls.speed_x)
                ai.y_intercept_location_p2 = balls.position_vector.y + \
                    frames_till_x_intersect * balls.speed_y

                pos_x = balls.position_vector.x
                pos_y = balls.position_vector.y
                spd_x = balls.speed_x
                spd_y = balls.speed_y
                for x in range(int(screen_x-100 - balls.position_vector.x)):
                    if pos_y >= screen_y - balls.height:
                        spd_y = -abs(spd_y)
                    elif pos_y <= 0:
                        spd_y = abs(spd_y)

                    if pos_x < screen_x:
                        pos_x += spd_x
                        pos_y += spd_y
                    elif pos_x >= screen_x:
                        pass
                    try:
                        for portal_set in range(int(len(portal.portal_list))):
                            if portal_set % 2 == 0:
                                if portal.portal_list[portal_set].hitbox.collidepoint((pos_x, pos_y)):
                                    if spd_x < 0:
                                        if pos_x <= portal.portal_list[portal_set].hitbox.right:
                                            pos_x = portal.portal_list[portal_set+1].x - \
                                                balls.width - \
                                                portal.portal_list[portal_set +
                                                                   1].displacement
                                    elif spd_x > 0:
                                        if pos_x + balls.width >= portal.portal_list[portal_set].hitbox.left:
                                            pos_x = portal.portal_list[portal_set+1].x + \
                                                portal.portal_list[portal_set+1].width + \
                                                portal.portal_list[portal_set +
                                                                   1].displacement
                                    from_portal_top = portal.portal_list[portal_set].y - \
                                        pos_y
                                    pos_y = portal.portal_list[portal_set+1].y - \
                                        from_portal_top
                                    if spd_x > 0:
                                        spd_x += .001
                                    else:
                                        spd_x -= .001
                                    if spd_y > 0:
                                        spd_y += .01

                                if portal.portal_list[portal_set+1].hitbox.collidepoint((pos_x, pos_y)):
                                    if spd_x < 0:
                                        if pos_x <= portal.portal_list[portal_set+1].hitbox.right:
                                            pos_x = portal.portal_list[portal_set].x - \
                                                balls.width - \
                                                portal.portal_list[portal_set].displacement
                                    elif spd_x > 0:
                                        if pos_x + balls.width >= portal.portal_list[portal_set+1].hitbox.left:
                                            pos_x = portal.portal_list[portal_set].x + \
                                                portal.portal_list[portal_set].width + \
                                                portal.portal_list[portal_set].displacement
                                    from_portal_top = portal.portal_list[portal_set+1].y - \
                                        pos_y
                                    pos_y = portal.portal_list[portal_set].y - \
                                        from_portal_top
                                    if spd_x > 0:
                                        spd_x += .001
                                    else:
                                        spd_x -= .001
                                    if spd_y > 0:
                                        spd_y += .01
                    except IndexError:
                        pass
                    ai.y_intercept_location_p2 = pos_y
            except ZeroDivisionError:
                ai.y_intercept_location_p2 = pos_y

            return ai.y_intercept_location_p2

    def execute_path_p1():
        if ai.y_intercept_location_p1 + balls_list[0].height > paddles_list[0].y + paddles_list[0].height/2 + 10:
            paddle.paddle_down_input_p1()

        if ai.y_intercept_location_p1 < paddles_list[0].y + paddles_list[0].height/2 - 10:
            paddle.paddle_up_input_p1()

        if ai.y_intercept_location_p1 < paddles_list[0].y + paddles_list[0].height/2 + 10 and ai.y_intercept_location_p1 + balls_list[0].height > paddles_list[0].y + paddles_list[0].height/2 - 10:
            paddle.stop_paddle_p1()

    def execute_path_p2():

        if ai.y_intercept_location_p2 + balls_list[0].height > paddles_list[1].y + paddles_list[1].height/2 + 10:
            paddle.paddle_down_input_p2()

        if ai.y_intercept_location_p2 < paddles_list[1].y + paddles_list[1].height/2 - 10:
            paddle.paddle_up_input_p2()

        if ai.y_intercept_location_p2 < paddles_list[1].y + paddles_list[1].height/2 + 10 and ai.y_intercept_location_p2 + balls_list[0].height > paddles_list[1].y + paddles_list[1].height/2 - 10:
            paddle.stop_paddle_p2()

    def return_to_center_p1():
        if game_rule.rule_list[56] == True:
            ai.y_intercept_location_p1 = screen_y * .30
        elif game_rule.rule_list[57] == True:
            ai.y_intercept_location_p1 = screen_y * .70
        else:
            ai.y_intercept_location_p1 = screen_y / 2
        return ai.y_intercept_location_p1

    def return_to_center_p2():
        if game_rule.rule_list[56] == True:
            ai.y_intercept_location_p2 = screen_y * .70
        elif game_rule.rule_list[57] == True:
            ai.y_intercept_location_p2 = screen_y * .30
        else:
            ai.y_intercept_location_p2 = screen_y / 2
        return ai.y_intercept_location_p2

    def execute_offensive_logic_p1():
        if balls_list[0].position_vector.x < paddles_list[0].x:
            paddle.paddle_left_input_p1()
            paddle.paddle_left_input_p1()
            paddle.paddle_left_input_p1()
            if balls_list[0].position_vector.y > paddles_list[0].y + paddles_list[0].height/2:
                paddle.paddle_down_input_p1()
            elif balls_list[0].position_vector.y < paddles_list[0].y + paddles_list[0].height/2:
                paddle.paddle_up_input_p1()

        elif balls_list[0].speed_y > 0.2 and balls_list[0].position_vector.x < paddles_list[0].x + 300:
            paddle.paddle_down_input_p1()
            if balls_list[0].position_vector.y > paddles_list[0].y + paddles_list[0].height/2 - 40 and balls_list[0].position_vector.y < paddles_list[0].y + paddles_list[0].height/2 + 40:
                paddle.paddle_right_input_p1()
        elif balls_list[0].speed_y < -0.2 and balls_list[0].position_vector.x < paddles_list[0].x + 300:
            paddle.paddle_up_input_p1()
            if balls_list[0].position_vector.y > paddles_list[0].y + paddles_list[0].height/2 - 40 and balls_list[0].position_vector.y < paddles_list[0].y + paddles_list[0].height/2 + 40:
                paddle.paddle_right_input_p1()
        elif balls_list[0].position_vector.x < paddles_list[0].x + 300 and balls_list[0].position_vector.y > paddles_list[0].y + paddles_list[0].height/2 - 40 and balls_list[0].position_vector.y < paddles_list[0].y + paddles_list[0].height/2 + 40:
            paddle.paddle_left_input_p1()
            paddle.paddle_left_input_p1()
        else:
            paddle.paddle_left_input_p1()

    def execute_offensive_logic_p2():
        if balls_list[0].position_vector.x > paddles_list[1].x:
            paddle.paddle_right_input_p2()
            paddle.paddle_right_input_p2()
            paddle.paddle_right_input_p2()
            if balls_list[0].position_vector.y > paddles_list[1].y + paddles_list[1].height/2:
                paddle.paddle_down_input_p2()
            elif balls_list[0].position_vector.y < paddles_list[1].y + paddles_list[1].height/2:
                paddle.paddle_up_input_p2()

        elif balls_list[0].speed_y > 0.2 and balls_list[0].position_vector.x > paddles_list[1].x - 300:
            paddle.paddle_down_input_p2()
            if balls_list[0].position_vector.y > paddles_list[1].y + paddles_list[1].height/2 - 40 and balls_list[0].position_vector.y < paddles_list[1].y + paddles_list[1].height/2 + 40:
                paddle.paddle_left_input_p2()
        elif balls_list[0].speed_y < -0.2 and balls_list[0].position_vector.x > paddles_list[1].x - 300:
            paddle.paddle_up_input_p2()
            if balls_list[0].position_vector.y > paddles_list[1].y + paddles_list[1].height/2 - 40 and balls_list[0].position_vector.y < paddles_list[1].y + paddles_list[1].height/2 + 40:
                paddle.paddle_left_input_p2()
        elif balls_list[0].position_vector.x > paddles_list[1].x - 300 and balls_list[0].position_vector.y > paddles_list[1].y + paddles_list[1].height/2 - 40 and balls_list[0].position_vector.y < paddles_list[1].y + paddles_list[1].height/2 + 40:
            paddle.paddle_left_input_p2()
            paddle.paddle_left_input_p2()
        else:
            paddle.paddle_right_input_p2()

    def easy_ai_p1():
        if balls_list[0].position_vector.y + balls_list[0].height/2 > paddles_list[0].y + paddles_list[0].height/2:
            paddle.paddle_down_input_p1()
        if balls_list[0].position_vector.y + balls_list[0].height/2 < paddles_list[0].y + paddles_list[0].height/2:
            paddle.paddle_up_input_p1()

    def normal_ai_p1():
        if balls_list[0].speed_x < 0:
            ai.y_intercept_location_p1 = ai.get_ball_trajectory_p1()
        if balls_list[0].speed_x > 0:
            ai.return_to_center_p1()
        ai.execute_path_p1()

    def advanced_ai_p1():
        if balls_list[0].speed_x < 0:
            ai.y_intercept_location_p1 = ai.get_ball_trajectory_p1()
        if balls_list[0].speed_x > 0:
            ai.return_to_center_p1()
        ai.execute_path_p1()
        ai.execute_offensive_logic_p1()

    def easy_ai_p2():
        if balls_list[0].position_vector.y + balls_list[0].height/2 > paddles_list[1].y + paddles_list[1].height/2:
            paddle.paddle_down_input_p2()
        if balls_list[0].position_vector.y + balls_list[0].height/2 < paddles_list[1].y + paddles_list[1].height/2:
            paddle.paddle_up_input_p2()

    def normal_ai_p2():
        if balls_list[0].speed_x > 0:
            ai.y_intercept_location_p2 = ai.get_ball_trajectory_p2()
        if balls_list[0].speed_x < 0:
            ai.return_to_center_p2()
        ai.execute_path_p2()

    def advanced_ai_p2():
        if balls_list[0].speed_x > 0:
            ai.y_intercept_location_p2 = ai.get_ball_trajectory_p2()
        if balls_list[0].speed_x < 0:
            ai.return_to_center_p2()
        ai.execute_path_p2()
        ai.execute_offensive_logic_p2()


balls_list = []
buttons_list = []
paddles_list = []
score_list = []

button.initialize_buttons(buttons_list)
game_rule.rule_list_save_check = game_rule.rule_list.copy()


def game_logic():
    if game_states.game_screen == True:
        if game_rule.rule_list[62] != True:
            force_field.force_field_logic()

        if game_rule.rule_list[53] != True:
            portal.portal_logic()
            for portals in portal.portal_list:
                portal.update_portals(portals)

        paddle.handle_paddle_input()
        paddle.restrict_paddles()
        paddle.paddle_movement_p1()
        paddle.paddle_movement_p2()

        if game_rule.rule_list[4] != True:
            ai.ai_mother_node_p2()
        if game_rule.rule_list[0] != True:
            ai.ai_mother_node_p1()

        ball.ball_collision_borders()
        for balls in balls_list:
            ball.ball_to_paddle_collision(balls)
            if game_rule.rule_list[47] == True:
                ball.identify_ball_to_ball_collisions(balls)
            ball.ball_update(balls)


def handle_graphics():
    graphics.draw_backgrounds()

    if game_states.game_screen == True or game_states.pause_screen == True:

        if game_rule.rule_list[44] != True:
            graphics.paddle_trails()
        graphics.draw_paddles()

        graphics.draw_balls()
        if game_rule.rule_list[28] != True:
            graphics.ball_trails()
        if game_rule.rule_list[62] != True:
            graphics.draw_force_field()

        if game_rule.rule_list[53] != True:
            graphics.draw_portals()
            graphics.portal_vibrations()

        graphics.draw_scores()
    else:
        pass

    graphics.draw_buttons()


def handle_general_input():
    if pygame.key.get_pressed()[K_ESCAPE] and input_info.can_press_esc == True:
        if game_states.game_screen == True:
            game_states.set_game_state_pause()
        elif game_states.pause_screen == True:
            game_states.set_game_state_play()
        elif game_states.options_screen == True:
            game_states.set_game_state_menu()
        elif game_states.statistics_screen == True:
            game_states.set_game_state_menu()
        elif game_states.menu_screen == True:
            pass
        else:
            exit()


def game_loop():
    global mouse_pos
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        clock.tick(FRAMES_PS)
        status_variable.current_frame += 1
        mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()
        input_info.key_input()

        handle_graphics()
        game_logic()
        handle_general_input()

        # Reset/Restrict Left Mouse Button Input
        if pygame.mouse.get_pressed()[0] == False:
            for id in buttons_list:
                id.can_click = True
        else:
            for id in buttons_list:
                id.can_click = False

        if pygame.key.get_pressed()[K_ESCAPE]:
            input_info.can_press_esc = False
        else:
            input_info.can_press_esc = True


game_loop()
