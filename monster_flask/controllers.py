#
# Format models as JSON for API responses


def get_color_data(color):
    mods = []
    for m in color.attack_mods:
        mods.append(get_color_mod_data(m))

    return {
        "id": color.id_no,
        "name": color.name,
        "mods": mods
    }


def get_species_data(species):
    return {
        "id": species.id_no,
        "name": species.name,
        "color": get_color_data(species.color),
        "base_life": species.base_life,
        "base_energy": species.base_energy,
        "base_defense": species.base_defense,
        "base_special": species.base_special
    }


def get_monster_data(species, stats):
    return {
        "species": get_species_data(species),
        "stats": [get_stat_data(s) for s in stats]
    }


def get_color_mod_data(mod):
    return {
        "attacker": mod.attacker_color.name,
        "target": mod.target_color.name,
        "multiple": mod.mod_value.multiple
    }


def get_stat_data(stat):
    return {
        "name": stat.name,
        "base": stat.default,
        "increment": stat.increment
    }
