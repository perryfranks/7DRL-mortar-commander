import pytest

from components.ai import DudAi
from components.equipment import Equipment
from components.equippable_fantasy import Dagger, LeatherArmor
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

hp = 10
base_defense = 10
base_power = 10


@pytest.fixture
def fighter():
    return Fighter(
        hp=hp,
        base_defense=base_defense,
        base_power=base_power
    )


@pytest.fixture
def player_no_equipment():
    """
    An actor with basic inventory and fighter component
    """
    test = Actor(
        char="o",
        color=(63, 127, 63),
        name="Test actor",
        ai_cls=DudAi,
        equipment=Equipment(),
        fighter=Fighter(hp=10, base_defense=0, base_power=3),
        inventory=Inventory(capacity=26),
        level=Level(level_up_factor=200),
    )
    return test


@pytest.fixture
def player_equipment():
    """
    An actor with basic inventory and fighter component
    """
    weapon = Item(
        char="/",
        color=(0, 191, 255),
        name="Dagger",
        equippable=Dagger()
    )

    armor = Item(
        char="[",
        color=(139, 69, 19),
        name="Leather Armor",
        equippable=LeatherArmor(),
    )

    test = Actor(
        char="o",
        color=(63, 127, 63),
        name="Test actor",
        ai_cls=DudAi,
        equipment=Equipment(weapon=weapon, armor=armor),
        fighter=Fighter(hp=10, base_defense=base_defense, base_power=base_power),
        inventory=Inventory(capacity=26),
        level=Level(level_up_factor=200),
    )
    return test


def test_hp_getter(fighter):
    assert fighter.hp == hp


def test_hp_setter(fighter):
    fighter.hp = 5
    assert fighter.hp == 5
    fighter.hp = -1  # Lets hope the parent call dosen't crash the system
    assert fighter.hp == 5


def test_defense(player_equipment):
    assert player_equipment.fighter.defense == base_defense + 1


def test_power(player_equipment):
    assert player_equipment.fighter.power == base_power + 2


def test_defense_bonus_no_bonus(player_no_equipment):
    assert player_no_equipment.fighter.defense_bonus == 0


def test_defense_bonus(player_equipment):
    assert player_equipment.fighter.defense_bonus == 1


def test_power_bonus_no_bonus(player_no_equipment):
    assert player_no_equipment.fighter.power_bonus == 0


def test_power_bonus(player_equipment):
    assert player_equipment.fighter.power_bonus == 2


def test_heal_max_health(fighter):
    assert fighter.hp == fighter.max_hp
    assert fighter.heal(10) == 0
    assert fighter.hp == fighter.max_hp


def test_heal_normal(fighter):
    fighter.take_damage(6)
    assert fighter.hp == 4
    assert fighter.heal(1) == 1
    assert fighter.hp == 5


def test_heal_over_heal(fighter):
    fighter.take_damage(6)
    assert fighter.hp == 4
    assert fighter.heal(9) == 6
    assert fighter.hp == 10


def test_take_damage_normal(fighter):
    fighter.take_damage(1)
    assert fighter.hp == 9


def test_die():
    assert False
