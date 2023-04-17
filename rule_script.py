class game_rule():
    rule_dict = {
        "p1_is_human": {
            "index": 0,
            "meta-name": "p1_is_human",
            "rule": True,
            "display name": "PLAYER 1: HUMAN"
        },
        "p1_is_easy_ai": {
            "index": 1,
            "meta-name": "p1_is_easy_ai",
            "rule": False,
            "display name": "PLAYER 1: EASY AI"
        },
        "p1_is_normal_ai": {
            "index": 2,
            "meta-name": "p1_is_normal_ai",
            "rule": False,
            "display name": "PLAYER 1: NORMAL AI"
        },
        "p1_is_advanced_ai": {
            "index": 3,
            "meta-name": "p1_is_advanced_ai",
            "rule": False,
            "display name": "PLAYER 1: ADVANCED AI"
        },
        "p2_is_human": {
            "index": 4,
            "meta-name": "p2_is_human",
            "rule": False,
            "display name": "PLAYER 2: HUMAN"
        },
        "p2_is_easy_ai": {
            "index": 5,
            "meta-name": "p2_is_easy_ai",
            "rule": False,
            "display name": "PLAYER 2: EASY AI"
        },
        "p2_is_normal_ai": {
            "index": 6,
            "meta-name": "p2_is_normal_ai",
            "rule": False,
            "display name": "PLAYER 2: NORMAL AI"
        },
        "p2_is_advanced_ai": {
            "index": 7,
            "meta-name": "p2_is_advanced_ai",
            "rule": True,
            "display name": "PLAYER 2: ADVANCED AI"
        },
        "ball_count": {
            "index": 8,
            "meta-name": "ball_count",
            "rule": 1,
            "display name": "BALL COUNT: "
        },
        "ball_speed_snail": {
            "index": 9,
            "meta-name": "ball_speed_snail",
            "rule": False,
            "display name": "BALL SPEED: SNAIL"
        },
        "ball_speed_slow": {
            "index": 10,
            "meta-name": "ball_speed_slow",
            "rule": False,
            "display name": "BALL SPEED: SLOW"
        },
        "ball_speed_normal": {
            "index": 11,
            "meta-name": "ball_speed_normal",
            "rule": True,
            "display name": "BALL SPEED: NORMAL"
        },
        "ball_speed_fast": {
            "index": 12,
            "meta-name": "ball_speed_fast",
            "rule": False,
            "display name": "BALL SPEED: FAST"
        },
        "ball_speed_hyper": {
            "index": 13,
            "meta-name": "ball_speed_hyper",
            "rule": False,
            "display name": "BALL SPEED: HYPER"
        },
        "ball_normalization_normal": {
            "index": 14,
            "meta-name": "ball_normalization_normal",
            "rule": True,
            "display name": "BALL NORMALIZATION: NORMAL"
        },
        "ball_normalization_straightened": {
            "index": 15,
            "meta-name": "ball_normalization_straightened",
            "rule": False,
            "display name": "BALL NORMALIZATION: STRAIGHTENED"
        },
        "ball_normalization_curved": {
            "index": 16,
            "meta-name": "ball_normalization_curved",
            "rule": False,
            "display name": "BALL NORMALIZATION: CURVED"
        },
        "ball_normalization_constant_acceleration": {
            "index": 17,
            "meta-name": "ball_normalization_constant_acceleration",
            "rule": False,
            "display name": "BALL NORMALIZATION: CONSTANT ACCELERATION"
        },
        "ball_normalization_none": {
            "index": 18,
            "meta-name": "ball_normalization_none",
            "rule": False,
            "display name": "BALL NORMALIZATION: NONE"
        },
        "ball_bounce_absorbant": {
            "index": 19,
            "meta-name": "ball_bounce_absorbant",
            "rule": False,
            "display name": "BALL BOUNCE: ABSORBANT"
        },
        "ball_bounce_normal": {
            "index": 20,
            "meta-name": "ball_bounce_normal",
            "rule": True,
            "display name": "BALL BOUNCE: NORMAL"
        },
        "ball_bounce_intense": {
            "index": 21,
            "meta-name": "ball_bounce_intense",
            "rule": False,
            "display name": "BALL BOUNCE: INTENSE"
        },
        "ball_bounce_burst": {
            "index": 22,
            "meta-name": "ball_bounce_burst",
            "rule": False,
            "display name": "BALL BOUNCE: BURST"
        },
        "ball_bounce_none": {
            "index": 23,
            "meta-name": "ball_bounce_none",
            "rule": False,
            "display name": "BALL BOUNCE: NONE"
        },
        "ball_fade_normal": {
            "index": 24,
            "meta-name": "ball_fade_normal",
            "rule": True,
            "display name": "BALL FADE: NORMAL"
        },
        "ball_fade_low_res": {
            "index": 25,
            "meta-name": "ball_fade_low_res",
            "rule": False,
            "display name": "BALL FADE: LOW-RES"
        },
        "ball_fade_high_res": {
            "index": 26,
            "meta-name": "ball_fade_high_res",
            "rule": False,
            "display name": "BALL FADE: HIGH-RES"
        },
        "ball_fade_high_res_long": {
            "index": 27,
            "meta-name": "ball_fade_high_res_long",
            "rule": False,
            "display name": "BALL FADE: HIGH-RES LONG"
        },
        "ball_fade_none": {
            "index": 28,
            "meta-name": "ball_fade_none",
            "rule": False,
            "display name": "BALL FADE: NONE"
        },
        "ball_color": {
            "index": 29,
            "meta-name": "ball_color",
            "rule": "RED",
            "display name": "BALL COLOR: "
        },
        "paddle_speed_snail": {
            "index": 30,
            "meta-name": "paddle_speed_snail",
            "rule": False,
            "display name": "PADDLE SPEED: SNAIL"
        },
        "paddle_speed_slow": {
            "index": 31,
            "meta-name": "paddle_speed_slow",
            "rule": False,
            "display name": "PADDLE SPEED: SLOW"
        },
        "paddle_speed_noraml": {
            "index": 32,
            "meta-name": "paddle_speed_noraml",
            "rule": True,
            "display name": "PADDLE SPEED: NORMAL"
        },
        "paddle_speed_fast": {
            "index": 33,
            "meta-name": "paddle_speed_fast",
            "rule": False,
            "display name": "PADDLE SPEED: FAST"
        },
        "paddle_speed_hyper": {
            "index": 34,
            "meta-name": "paddle_speed_hyper",
            "rule": False,
            "display name": "PADDLE SPEED: HYPER"
        },
        "paddle_acceleration_snail": {
            "index": 35,
            "meta-name": "paddle_acceleration_snail",
            "rule": False,
            "display name": "PADDLE ACCELERATION: SNAIL"
        },
        "paddle_acceleration_slow": {
            "index": 36,
            "meta-name": "paddle_acceleration_slow",
            "rule": False,
            "display name": "PADDLE ACCELERATION: SLOW"
        },
        "paddle_acceleration_normal": {
            "index": 37,
            "meta-name": "paddle_acceleration_normal",
            "rule": True,
            "display name": "PADDLE ACCELERATION: NORMAL"
        },
        "paddle_acceleration_fast": {
            "index": 38,
            "meta-name": "paddle_acceleration_fast",
            "rule": False,
            "display name": "PADDLE ACCELERATION: FAST"
        },
        "paddle_acceleration_hyper": {
            "index": 39,
            "meta-name": "paddle_acceleration_hyper",
            "rule": False,
            "display name": "PADDLE ACCELERATION: HYPER"
        },
        "paddle_fade_normal": {
            "index": 40,
            "meta-name": "paddle_fade_normal",
            "rule": True,
            "display name": "PADDLE FADE: NORMAL"
        },
        "paddle_fade_low_res": {
            "index": 41,
            "meta-name": "paddle_fade_low_res",
            "rule": False,
            "display name": "PADDLE FADE: LOW RES"
        },
        "paddle_fade_high_res": {
            "index": 42,
            "meta-name": "paddle_fade_high_res",
            "rule": False,
            "display name": "PADDLE FADE: HIGH RES"
        },
        "paddle_fade_high_res_long": {
            "index": 43,
            "meta-name": "paddle_fade_high_res_long",
            "rule": False,
            "display name": "PADDLE FADE: HIGH RES LONG"
        },
        "paddle_fade_none": {
            "index": 44,
            "meta-name": "paddle_fade_none",
            "rule": False,
            "display name": "PADDLE FADE: NONE"
        },
        "paddle_color_p1": {
            "index": 45,
            "meta-name": "paddle_color_p1",
            "rule": "WHITE",
            "display name": "PADDLE COLOR P1: "
        },
        "paddle_color_p2": {
            "index": 46,
            "meta-name": "paddle_color_p2",
            "rule": "WHITE",
            "display name": "PADDLE COLOR P2: "
        },
        "ball_to_ball_collisions_on": {
            "index": 47,
            "meta-name": "ball_to_ball_collisions_on",
            "rule": True,
            "display name": "BALL-TO-BALL COLLISIONS: ON"
        },
        "ball_to_ball_collisions_off": {
            "index": 48,
            "meta-name": "ball_to_ball_collisions_off",
            "rule": False,
            "display name": "BALL-TO-BALL COLLISIONS: OFF"
        },
        "ball_size_normal": {
            "index": 49,
            "meta-name": "ball_size_normal",
            "rule": True,
            "display name": "BALL SIZE: NORMAL"
        },
        "ball_size_large": {
            "index": 50,
            "meta-name": "ball_size_large",
            "rule": False,
            "display name": "BALL SIZE: LARGE"
        },
        "ball_size_random": {
            "index": 51,
            "meta-name": "ball_size_random",
            "rule": False,
            "display name": "BALL SIZE: RANDOM"
        },
        "ball_size_small": {
            "index": 52,
            "meta-name": "ball_size_small",
            "rule": False,
            "display name": "BALL SIZE: SMALL"
        },
        "portals_none": {
            "index": 53,
            "meta-name": "portals_none",
            "rule": True,
            "display name": "PORTALS: NONE"
        },
        "portals_gate": {
            "index": 54,
            "meta-name": "portals_gate",
            "rule": False,
            "display name": "PORTALS: GATE"
        },
        "portals_double_gate": {
            "index": 55,
            "meta-name": "portals_double_gate",
            "rule": False,
            "display name": "PORTALS: DOUBLE GATE"
        },
        "portals_close_1": {
            "index": 56,
            "meta-name": "portals_close_1",
            "rule": False,
            "display name": "PORTALS: CLOSE 1"
        },
        "portals_close_2": {
            "index": 57,
            "meta-name": "portals_close_2",
            "rule": False,
            "display name": "PORTALS: CLOSE 2"
        },
        "portals_double_close": {
            "index": 58,
            "meta-name": "portals_double_close",
            "rule": False,
            "display name": "PORTALS: DOUBLE CLOSE"
        },
        "portals_central": {
            "index": 59,
            "meta-name": "portals_central",
            "rule": False,
            "display name": "PORTALS: CENTRAL"
        },
        "portals_double_central": {
            "index": 60,
            "meta-name": "portals_double_central",
            "rule": False,
            "display name": "PORTALS: DOUBLE CENTRAL"
        },
        "portals_barriers": {
            "index": 61,
            "meta-name": "portals_barriers",
            "rule": False,
            "display name": "PORTALS: BARRIERS"
        },
        "shield_off": {
            "index": 62,
            "meta-name": "shield_off",
            "rule": True,
            "display name": "SHIELD: OFF"
        },
        "shield_charge_slow": {
            "index": 63,
            "meta-name": "shield_charge_slow",
            "rule": False,
            "display name": "SHIELD: CHARGE SLOW"
        },
        "shield_charge_normal": {
            "index": 64,
            "meta-name": "shield_charge_normal",
            "rule": False,
            "display name": "SHIELD: CHARGE NORMAL"
        },
        "shield_charge_fast": {
            "index": 65,
            "meta-name": "shield_charge_fast",
            "rule": False,
            "display name": "SHIELD: CHARGE FAST"
        }
    }
    ball_color_list = ["MAROON", "RED", "ORANGE", "DARKORANGE", "GOLD",
                       "YELLOW", "GREEN", "MAGENTA", "DARKVIOLET", "BLUE", "NAVY"]
    paddle_color_list = ["WHITE", "YELLOW", "MAGENTA"]

    rule_list = {}
    rule_change = False

    def compare_nested_dicts(dict1, dict2):

        for item in dict1:
            try:
                if dict1[item]["rule"] == dict2[item]["rule"]:
                    pass
                else:
                    return False
            except:
                return False
        return True

    def load_rule_list():
        game_rule.rule_list = game_rule.rule_dict.copy()

        # Below is AUTO LOAD SAVE DATA / NOTATE FILE ERRORS. Any errors should resolve after opening and closing after updating settings
        try:
            # This trys to access the save file in the same folder as this program. Error is expected when the save file doesn't exist, and will auto-resolve on the next save (occurs when settings are adjusted).
            save_data = open('game_rules.txt', 'r')
            saved_rules = save_data.readlines()
            try:
                # If the file is opened, this bit of code reads it and updates the rules. Error is expected when the save file is bad/formatted improperly. Will auto resolve by resetting to the default rules.
                for rule in game_rule.rule_dict:
                    try:
                        try:
                            game_rule.rule_list[rule]["rule"] = eval(
                                saved_rules[game_rule.rule_list[rule]["index"]].strip("\n"))
                        except:
                            game_rule.rule_list[rule]["rule"] = saved_rules[game_rule.rule_list[rule]
                                                                            ["index"].strip("\n")]
                    except:
                        game_rule.rule_list[rule]["rule"] = '"' + str(saved_rules[game_rule.rule_list[rule]
                                                                                  ["index"].strip("\n")]) + '"'
            except:
                print("LOAD ERROR")
                game_rule.rule_list = game_rule.rule_dict.copy()
        except:
            print("FILE ERROR")
            game_rule.rule_list = game_rule.rule_dict.copy()

    def save_rule_list():  # Creates the save file by copying the rule_list
        try:
            game_rule.rule_change = False
            save_data = open('game_rules.txt', 'w')
            for item in game_rule.rule_list:
                if game_rule.rule_list[item]["rule"].__class__ is str:
                    save_data.writelines('"' +
                                         str(game_rule.rule_list[item]["rule"]) + '"' + "\n")
                else:
                    save_data.writelines(
                        str(game_rule.rule_list[item]["rule"]) + "\n")
            save_data.close()
        except:
            print("SAVE ERROR")

    # General use function for switching between game rules. Pass in all the game rule dictionaries to cycle through.
    def cycle_game_rules_dict(*args):
        rules = args
        for index in range(len(rules)):
            try:
                game_rule.rule_change = True
                try:
                    if rules[index]["rule"] == True:
                        if rules[index+1]["rule"] == False:
                            rules[index]["rule"] = False
                            rules[index+1]["rule"] = True

                            return rules, game_rule.rule_list
                except IndexError:
                    if rules[index]["rule"] == True:
                        rules[index]["rule"] = False
                        rules[0]["rule"] = True

                        return rules
            except:
                print("RULE CYCLE ERROR")
                return args

    def cycle_game_rules_list(rule, list1):
        try:
            index = list1.index(rule["rule"])
            rule["rule"] = list1[index+1]
        except:
            rule["rule"] = list1[0]
