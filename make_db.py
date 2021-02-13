import json

from monster_flask import db, create_app
from monster_flask.game.controllers import ColorController, SpeciesController, MovesController, StatController

with open("db_setup/color_data.json", "r") as file:
    COLORS = json.load(file)

with open("db_setup/species_data.json", "r") as file:
    SPECIES = json.load(file)

with open("db_setup/stats_data.json", "r") as file:
    STATS = json.load(file)

with open("db_setup/move_data.json", "r") as file:
    MOVES = json.load(file)


def build_color_tables(controller):
    for mv in COLORS["MOD_VALUES"]:
        controller.add_mod_value(mv["multiple"], mv["ordinal"])

    for c in COLORS["COLORS"]:
        controller.add_color(c["name"])

    for c in COLORS["COLORS"]:
        attacker = c["name"]
        mods = c["mods"]
        for target in mods:
            ordinal = mods[target]
            controller.add_mod(attacker, target, ordinal)


def build_species_table(species_controller, color_controller):
    for spec in SPECIES:
        species_controller.add_species(
            spec["name"], color_controller.get_color_id(spec["color"]),
            spec["life"], spec["energy"], spec["defense"], spec["special"]
        )


def build_stats_table(controller):
    for stat in STATS:
        controller.add_stat(stat["name"], stat["default"], stat["increment"])


def build_move_tables(move_controller, color_controller):
    for v in MOVES["DICE_VALUES"]:
        move_controller.add_dice_value(v)

    for c in MOVES["MOVES"]:
        for m in MOVES["MOVES"][c]:
            move_controller.add_move(
                m["NAME"], color_controller.get_color_id(c)
            )

            for d in m["DICE"]:
                color, value = d
                move_controller.add_die(
                    move_controller.get_value_id(value),
                    color_controller.get_color_id(color),
                    move_controller.get_move_id(m["NAME"])
                )


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()

        color_cont = ColorController(db)
        species_cont = SpeciesController(db)
        move_cont = MovesController(db)
        stat_cont = StatController(db)

        build_color_tables(color_cont)
        build_species_table(species_cont, color_cont)
        build_stats_table(stat_cont)
        build_move_tables(move_cont, color_cont)

        db.session.commit()
