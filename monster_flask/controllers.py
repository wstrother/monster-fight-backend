from monster_flask import models

#
# Format models as JSON for API responses


class ModelController:
    def __init__(self, db):
        self.db = db

    def add(self, item):
        self.db.session.add(item)

    def add_all(self, items):
        self.db.session.add_all(items)

    def commit(self):
        self.db.commit()


class ColorController(ModelController):
    # def __init__(self, db, color, mod, cmv):
    #     super(ColorController, self).__init__(db)
    #     self.color_model = color
    #     self.mod_model = mod
    #     self.cmv_model = cmv

    # color model

    @staticmethod
    def get_color_id(name):
        return models.Color.query.filter_by(name=name).first().id_no

    def add_color(self, name):
        self.add(models.Color(
            name=name
        ))

    # color_mod_value model

    def add_mod_value(self, multiple, ordinal):
        self.add(models.ColorModValue(multiple=multiple, ordinal=ordinal))

    # color_mod model

    def add_mod(self, attacker, target, ordinal):
        self.add(models.ColorMod(
            attacker_id=self.get_color_id(attacker),
            target_id=self.get_color_id(target),
            ordinal=ordinal
        ))

    # API methods

    def get_all(self):
        return [self.get_color_data(c) for c in models.Color.query.all()]

    def get_color_by_id(self, color_id):
        color = models.Color.query.get(color_id)

        if color is None:
            return {"error": "No color found with id {}".format(color_id)}

        return self.get_color_data(color)

    @staticmethod
    def get_color_data(color):
        mods = []
        for m in color.attack_mods:
            mods.append(ColorController.get_color_mod_data(m))

        return {
            "id": color.id_no,
            "name": color.name,
            "mods": mods
        }

    @staticmethod
    def get_color_mod_data(mod):
        return {
            "attacker": mod.attacker_color.name,
            "target": mod.target_color.name,
            "multiple": mod.mod_value.multiple
        }


class StatController(ModelController):
    # def __init__(self, db, stats):
    #     super(StatController, self).__init__(db)
    #     self.stat_model = stats

    def add_stat(self, name, default, increment):
        self.add(models.BaseStat(
            name=name, default=default, increment=increment
        ))

    # API methods

    def get_all(self):
        return [self.get_stat_data(s) for s in models.BaseStat.query.all()]

    def get_stat_by_id(self, stat_id):
        stat = models.BaseStat.query.get(stat_id)

        if stat is None:
            return {"error": "No stat found with id {}".format(stat_id)}

        return self.get_stat_data(stat)

    @staticmethod
    def get_stat_data(stat):
        return {
            "name": stat.name,
            "base": stat.default,
            "increment": stat.increment
        }


class SpeciesController(ModelController):
    # def __init__(self, db, species, stats):
    #     super(SpeciesController, self).__init__(db, stats)
    #     self.species_model = species

    def add_species(self, name, color_id, life, energy, defense, special):
        self.add(models.Species(
            name=name, color_id=color_id,
            base_life=life, base_energy=energy,
            base_defense=defense, base_special=special
        ))

    # API methods

    def get_all(self):
        return [self.get_species_data(s) for s in models.Species.query.all()]

    def get_species_by_id(self, species_id):
        species = models.Species.query.get(species_id)

        if species is None:
            return {"error": "No species found with id {}".format(species_id)}

        return self.get_species_data(species)

    def get_monster_by_species_id(self, species_id):
        species = models.Species.query.get(species_id)

        if species is None:
            return {"error": "No species found with id {}".format(species_id)}

        stats = models.BaseStat.query.all()
        return self.get_monster_data(species, stats)

    @staticmethod
    def get_species_data(species):
        return {
            "id": species.id_no,
            "name": species.name,
            "color": ColorController.get_color_data(species.color),
            "base_life": species.base_life,
            "base_energy": species.base_energy,
            "base_defense": species.base_defense,
            "base_special": species.base_special
        }

    @staticmethod
    def get_monster_data(species, stats):
        return {
            "species": SpeciesController.get_species_data(species),
            "stats": [StatController.get_stat_data(s) for s in stats]
        }


class MovesController(ModelController):
    # def __init__(self, db, dice_values, moves, dice):
    #     super(MovesController, self).__init__(db)
    #     self.values_model = dice_values
    #     self.moves_model = moves
    #     self.dice_model = dice

    # dice_values model

    @staticmethod
    def get_value_id(value):
        return models.DiceValues.query.filter_by(value=value).first().id_no

    def add_dice_value(self, value):
        self.add(models.DiceValues(
            value=value
        ))

    # moves model

    @staticmethod
    def get_move_id(name):
        return models.Moves.query.filter_by(name=name).first().id_no

    def add_move(self, name, color_id):
        self.add(models.Moves(
            name=name, color_id=color_id
        ))

    # dice model

    def add_die(self, value_id, color_id, move_id):
        self.add(models.Dice(
            value_id=value_id, color_id=color_id, move_id=move_id
        ))

    # API methods

    def get_all(self):
        return [self.get_move_data(m) for m in models.Moves.query.all()]

    def get_move_by_id(self, move_id):
        move = models.Moves.query.get(move_id)

        if move is None:
            return {"error": "No move found with id {}".format(move_id)}

        return self.get_move_data(move)

    def get_moves_by_color(self, color_id):
        return [self.get_move_data(m) for m in models.Moves.query.filter_by(color_id=color_id)]

    def get_move_by_color_index(self, color_id, index):
        move = models.Moves.query.filter_by(color_id=color_id)[int(index)]

        return self.get_move_data(move)

    @staticmethod
    def get_move_data(move):
        dice = [MovesController.get_die_data(d) for d in move.dice]
        return {
            "name": move.name,
            "color": ColorController.get_color_data(move.move_color),
            "dice": dice,
            "id": move.id_no
        }

    @staticmethod
    def get_die_data(die):
        return {
            "value": die.damage.value,
            "color": ColorController.get_color_data(die.dice_color)
        }
