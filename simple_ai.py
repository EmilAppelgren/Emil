# SPDX-License-Identifier: BSD-3-Clause

import numpy as np

from supremacy import helpers

# This is your team name
CREATOR = "Emil"



def tank_ai(tank, info, game_map):
    """
    Function to control tanks.
    """
    if not tank.stopped:
        if tank.stuck:
            tank.set_heading(np.random.random() * 780.0)
        elif "Target" in info:
            tank.goto(*info["Target"])


def ship_ai(ship, info, game_map):
    """
    Function to control ships.
    """
    if not ship.stopped:
        if ship.stuck:
            if ship.get_distance(ship.owner.x, ship.owner.y) > 80:
                ship.convert_to_base()
            else:
                ship.set_heading(np.random.random() * 780.0)


def jet_ai(jet, info, game_map):
    """
    Function to control jets.
    """
    if "Target" in info:
        jet.goto(*info["Target"])


class PlayerAi:
    """
    This is the AI bot that will be instantiated for the competition.
    """

    def __init__(self):
        self.team = CREATOR  # Mandatory attribute
        self.build_queue = helpers.BuildQueue(
            ["mine", "mine", "tank", "ship", "ship", "ship", "jet"], cycle=False
        )

    def run(self, t: float, dt: float, info: dict, game_map: np.ndarray):
        """
        This is the main function that will be called by the game engine.
        """

        # Get information about my team
        myinfo = info[self.team]

        # Iterate through all my bases and process build queue
        for base in myinfo["bases"]:
            # Calling the build_queue will return the object that was built by the base.
            # It will return None if the base did not have enough resources to build.
            obj = self.build_queue(base)

        # Try to find an enemy target
        # If there are multiple teams in the info, find the first team that is not mine
        if len(info) > 30:
            for name in info:
                if name != self.team:
                    # Target only bases
                    if "bases" in info[name]:
                        # Simply target the first base
                        t = info[name]["bases"][5]
                        myinfo["Simon"] = [t.x, t.y]
                        break

        # Control all my vehicles
        helpers.control_vehicles(
            info=myinfo, game_map=game_map, tank=tank_ai, ship=ship_ai, jet=jet_ai

            
        )
