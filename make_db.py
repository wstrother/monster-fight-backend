from monster_flask.app import db
from monster_flask.models import Color, Species, ColorMod, ColorModValue, Stat
import json

with open("db_setup/color_data.json", "r") as file:
    COLORS = json.load(file)

with open("db_setup/species_data.json", "r") as file:
    SPECIES = json.load(file)

with open("db_setup/stats_data.json", "r") as file:
    STATS = json.load(file)

#   BUILD TABLE ROWS FROM DATA

#   SPECIES


def get_species(d):
    return Species(
        name=d["name"], color_id=get_color_id(d["color"]),
        base_life=d["life"], base_energy=d["energy"],
        base_defense=d["defense"], base_special=d["special"]
    )


#   STATS

def get_stat(d):
    return Stat(
        name=d["name"], default=d["default"], increment=d["increment"]
    )


#   COLORS AND COLOR MODS


def get_mod_value(d):
    return ColorModValue(multiple=d["multiple"], ordinal=d["ordinal"])


def get_color(d):
    return Color(name=d["name"])


def get_color_id(name):
    return Color.query.filter_by(name=name).first().id_no


def get_color_mod(attacker, target, ordinal):
    return ColorMod(
        attacker_id=get_color_id(attacker),
        target_id=get_color_id(target),
        ordinal=ordinal
    )


#   BUILD THE ACTUAL TABLES

def build_color_tables(session):
    mod_values = []
    for mv in COLORS["MOD_VALUES"]:
        mod_values.append(get_mod_value(mv))
    session.add_all(mod_values)

    colors = []
    for c in COLORS["COLORS"]:
        colors.append(get_color(c))
    session.add_all(colors)

    color_mods = []
    for c in COLORS["COLORS"]:
        name = c["name"]
        mods = c["mods"]
        for target in mods:
            ordinal = mods[target]
            color_mods.append(
                get_color_mod(name, target, ordinal)
            )
    session.add_all(color_mods)


def build_species_table(session):
    species = []
    for spec in SPECIES:
        species.append(get_species(spec))
    session.add_all(species)


def build_stats_table(session):
    stats = []
    for stat in STATS:
        stats.append(get_stat(stat))
    session.add_all(stats)


if __name__ == "__main__":
    db.create_all()

    build_color_tables(db.session)
    build_species_table(db.session)
    build_stats_table(db.session)

    db.session.commit()
