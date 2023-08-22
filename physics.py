"""This file represents the laws of physics and shall not be modified"""
from random import randint

from config import Config


def warp(location):
    """Warping impacts the Ontarian Manifold and the location of The Rascal"""

    with open(Config.Location.path, "a") as location_file:
        location_file.write(f"{location}\n")

    with open(Config.OntarianManifold.path, "a") as ontarian_manifold_file:
        ontarian_manifold_file.write(f"{randint(40001, 50000)}\n")


def cool():
    """Cooling resets the Ontarian Manifold for 40000 KPGs"""

    with open(Config.OntarianManifold.path, "a") as ontarian_manifold_file:
        ontarian_manifold_file.write("40000\n")
