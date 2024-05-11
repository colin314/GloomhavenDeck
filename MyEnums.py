from enum import Enum


class Effect(Enum):
    NONE = 0
    CRITICAL = 1
    MISS = 2
    WOUND = 3
    BRITTLE = 4
    BANE = 5
    POISON = 6
    IMMOBILIZE = 7
    DISARM = 8
    INJURE = 9
    STUN = 10
    MUDDLE = 11
    CURSE = 12
    REGENERATE = 13
    WARD = 14
    INVISIBLE = 15
    STRENGTHEN = 16
    BLESS = 17
    PUSH = 18
    PULL = 19
    PIERCE = 20
    SHIELD = 21
    RETALIATE = 22
    HEAL = 23
    GEN_FIRE = 24
    GEN_ICE = 25
    GEN_EARTH = 26
    GEN_AIR = 27
    GEN_LIGHT = 28
    GEN_DARK = 29
    GEN_ANY = 30
    CUSTOM_1 = 31
    CUSTOM_2 = 32
    CUSTOM_3 = 33
    REMOVE = 34
    SHUFFLE = 35
