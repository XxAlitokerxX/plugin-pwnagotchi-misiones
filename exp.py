import logging
import os
import random
import json
import pwnagotchi
import pwnagotchi.agent
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK

# Static Variables
MULTIPLIER_ASSOCIATION = 1
MULTIPLIER_DEAUTH = 2
MULTIPLIER_HANDSHAKE = 3
MULTIPLIER_AI_BEST_REWARD = 5
TAG = "[EXP Plugin]"
FACE_LEVELUP = '(≧◡◡≦)'
FILE_SAVE = "exp_stats"
JSON_KEY_LEVEL = "level"
JSON_KEY_EXP = "exp"
JSON_KEY_EXP_TOT = "exp_tot"


class Mission:
    def __init__(self, description, target, reward, max_target):
        self.description = description
        self.target = target
        self.progress = 0
        self.completed = False
        self.reward = reward
        self.max_target = max_target

    def update_progress(self, value):
        if not self.completed:
            self.progress += value
            if self.progress >= self.target:
                self.progress = self.target
                self.completed = True
                return True
        return False

    def reset(self):
        if self.target < self.max_target:
            self.target = int(self.target * 1.5)
            if self.target > self.max_target:
                self.target = self.max_target
        self.progress = 0
        self.completed = False


class EXP(plugins.Plugin):
    __author__ = 'GaelicThunder'
    __version__ = '1.0.6'
    __license__ = 'GPL3'
    __description__ = 'Get exp every time a handshake get captured.'

    def __init__(self):
        self.percent = 0
        self.exp = 0
        self.lv = 1
        self.exp_tot = 0
        self.missions = []
        self.initialize_missions()
        self.save_file = self.getSaveFileName()
        self.log = logging.getLogger(TAG)
        if not os.path.exists(self.save_file):
            self.save()
        else:
            self.load()

    def initialize_missions(self):
        self.missions.append(Mission("Handshakes", 20, 30, 100))
        self.missions.append(Mission("Deauths", 20, 100, 300))
        self.missions.append(Mission("Associations", 15, 75, 225))
        self.missions.append(Mission("AI", 2, 5, 15))

    def save(self):
        data = {
            JSON_KEY_LEVEL: self.lv,
            JSON_KEY_EXP: self.exp,
            JSON_KEY_EXP_TOT: self.exp_tot
        }
        with open(self.save_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self):
        with open(self.save_file, 'r') as f:
            data = json.load(f)
            self.lv = data[JSON_KEY_LEVEL]
            self.exp = data[JSON_KEY_EXP]
            self.exp_tot = data[JSON_KEY_EXP_TOT]

    def getSaveFileName(self):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), FILE_SAVE + ".json")

    def calcExpNeeded(self, level):
        return 5 if level == 1 else int((level ** 3) / 2)

    def exp_check(self, agent):
        if self.exp >= self.calcExpNeeded(self.lv):
            self.exp = 0
            self.lv += 1
            self.log.info(f"Level Up! New Level: {self.lv}")
            self.save()
            self.displayLevelUp(agent)

    def check_mission_completion(self, event_type, value=1):
        """
        Actualiza el progreso de la misión asociada con el tipo de evento dado.
        """
        for mission in self.missions:
            # Verifica que la descripción de la misión coincida con el evento
            if mission.description.lower() == event_type.lower() and not mission.completed:
                self.log.info(f"Updating mission '{mission.description}' with progress: {value}")
                completed = mission.update_progress(value)
                if completed:
                    self.log.info(f"Mission completed: {mission.description}")
                    self.exp += mission.reward
                    self.exp_tot += mission.reward
                    self.save()
                    mission.reset()
                    self.log.info(f"Mission reset: {mission.description} New target: {mission.target}")
                    return

    def displayLevelUp(self, agent):
        view = agent.view()
        view.set('face', FACE_LEVELUP)
        view.set('status', "Level Up!")
        view.update(force=True)

    def on_ui_setup(self, ui):
        ui.add_element('Lv', LabeledValue(
            color=BLACK, label='Lv', value=0,
            position=(int(self.options["lvl_x_coord"]), int(self.options["lvl_y_coord"])),
            label_font=fonts.Bold, text_font=fonts.Medium
        ))
        ui.add_element('Exp', LabeledValue(
            color=BLACK, label='Exp', value=0,
            position=(int(self.options["exp_x_coord"]), int(self.options["exp_y_coord"])),
            label_font=fonts.Bold, text_font=fonts.Medium
        ))
        ui.add_element('Missions', LabeledValue(
            color=BLACK, label='', value="",
            position=(int(self.options["missions_x_coord"]), int(self.options["missions_y_coord"])),
            label_font=fonts.Bold, text_font=fonts.Small
        ))

    def on_ui_update(self, ui):
        self.percent = int((self.exp / self.calcExpNeeded(self.lv)) * 100)
        symbols_count = int(self.options["bar_symbols_count"])
        bar = self.barString(symbols_count, self.percent)
        ui.set('Lv', f"{self.lv}")
        ui.set('Exp', f"{bar}")

        current_mission = self.missions[random.randint(0, len(self.missions) - 1)]
        status = f"{current_mission.description} {current_mission.progress}/{current_mission.target}"
        ui.set('Missions', status)

    def barString(self, symbols_count, percent):
        if percent > 100:
            percent = 100
        bar_length = int((symbols_count / 100) * percent)
        blank_length = symbols_count - bar_length
        return "|" + "▥" * bar_length + " " * blank_length + "|"

    def on_association(self, agent, access_point):
        """
        Evento: Asociación detectada.
        """
        self.exp += MULTIPLIER_ASSOCIATION
        self.exp_tot += MULTIPLIER_ASSOCIATION
        self.exp_check(agent)
        self.check_mission_completion("associations", 1)  # Exact match
        self.save()

    def on_deauthentication(self, agent, access_point, client_station):
        """
        Evento: Deautenticación detectada.
        """
        self.exp += MULTIPLIER_DEAUTH
        self.exp_tot += MULTIPLIER_DEAUTH
        self.exp_check(agent)
        self.check_mission_completion("deauths", 1)  # Exact match
        self.save()

    def on_handshake(self, agent, filename, access_point, client_station):
        """
        Evento: Handshake capturado.
        """
        self.exp += MULTIPLIER_HANDSHAKE
        self.exp_tot += MULTIPLIER_HANDSHAKE
        self.exp_check(agent)
        self.check_mission_completion("handshakes", 1)  # Exact match
        self.save()

    def on_ai_best_reward(self, agent, reward):
        """
        Evento: La IA alcanza su mejor recompensa.
        """
        self.exp += MULTIPLIER_AI_BEST_REWARD
        self.exp_tot += MULTIPLIER_AI_BEST_REWARD
        self.exp_check(agent)
        self.check_mission_completion("ai", 1)  # Exact match
        self.save()
