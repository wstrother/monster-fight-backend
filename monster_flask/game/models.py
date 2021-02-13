from monster_flask import db


#   COLOR MODELS


#   Monster color, represents elemental 'type' and is used to determine damage modifiers such as
#   SCAB (Same Color Attack Bonus) and 'effectiveness' modifiers (ColorMod table)

class Color(db.Model):
    __tablename__ = "color"
    id_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    species = db.relationship('Species', backref="color", lazy=True)

    dice = db.relationship('Dice', backref="dice_color", lazy=True,
                           foreign_keys="Dice.color_id")
    moves = db.relationship('Moves', backref="move_color", lazy=True,
                            foreign_keys="Moves.color_id")

    attack_mods = db.relationship('ColorMod', backref="attacker_color",
                                  lazy=True, foreign_keys="ColorMod.attacker_id")
    target_mods = db.relationship('ColorMod', backref="target_color",
                                  lazy=True, foreign_keys="ColorMod.target_id")

    def __repr__(self):
        return "Color({}: '{}')".format(self.id_no, self.name)


#   The floating point value used as a multiple factor in calculating damage where relevant colors
#   give an effectiveness modifier. These modifier values have a 'multiplier' value and an 'ordinal'
#   position value that can either be positive (for multipliers bigger than 1) or negative (for
#   multipliers smaller than 1)

class ColorModValue(db.Model):
    __tablename__ = "color_mod_value"
    id_no = db.Column(db.Integer, primary_key=True)
    multiple = db.Column(db.Float, nullable=False)
    ordinal = db.Column(db.Integer, nullable=False, unique=True)
    mods = db.relationship('ColorMod', backref="mod_value", lazy=True)

    def __repr__(self):
        return "ColorModValue(ordinal {}: {})".format(self.ordinal, self.multiple)


#   The relationship between two colors such that an effectiveness modifier is used in calculating the applicable
#   damage. Applies where the damage roll's color.id == 'attacker_id' and the
#   monster taking damage has a color.id == 'target.id'
#   The relevant multiple value is determined from the ColorModValue table by the corresponding 'ordinal' value

class ColorMod(db.Model):
    __tablename__ = "color_mod"
    id_no = db.Column(db.Integer, primary_key=True)
    attacker_id = db.Column(db.Integer, db.ForeignKey('color.id_no'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('color.id_no'), nullable=False)
    ordinal = db.Column(db.Integer, db.ForeignKey('color_mod_value.ordinal'), nullable=False)

    def __repr__(self):
        return "ColorMod({}: '{}' on '{}' ({}))".format(self.id_no, self.attacker_id, self.target_id, self.ordinal)


#
#   SPECIES MODELS

# A monster species defines the color of that monster and a set of base values for four stats --
#   life, energy, defense, and special
# which are stored as integer values representing "deviation values". The species ID is also referenced
# by the char_creator.py module to provide hardcoded data with regards to Move Pool selection at the
# time of character creation

class Species(db.Model):
    __tablename__ = "species"
    id_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id_no'), nullable=False)
    monsters = db.relationship('Monster', backref='species_type', lazy=True)

    #   base stats
    base_life = db.Column(db.Integer, nullable=False)
    base_energy = db.Column(db.Integer, nullable=False)
    base_defense = db.Column(db.Integer, nullable=False)
    base_special = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Species({}: '{}', color: '{}')".format(self.id_no, self.name, self.color_id)


# The Monster table records instances of monsters with a given species who have also had certain
# character creation choices applied, such as addition "deviation values" applied at character
# creations and move pool selections used to create a move set

class Monster(db.Model):
    __tablename__ = "monsters"
    id_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    species_id = db.Column(db.Integer, db.ForeignKey('species.id_no'), nullable=False)

#
#   STAT MODELS


# The BaseStat model records the name of the four base stats as well as their respective
# 'increment' values, which are used in calculation for battle interactions, as well as the
# 'default' value which defines the standard number of 'deviation values' for that stat which
# is unique across all species. The calculated value of a stat is equal to it's 'increment'
# value multiplied by the total number of 'deviation values'

class BaseStat(db.Model):
    __tablename__ = "base_stat"
    id_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    default = db.Column(db.Integer, nullable=False)
    increment = db.Column(db.Integer, nullable=False)
    applied_stats = db.relationship('AppliedStat', backref="stat_type", lazy=True)

    def __repr__(self):
        return "Stat({}: '{}', default value: {}, increment: {})".format(
            self.id_no, self.name, self.default * self.increment, self.increment
        )


# The AppliedStat table records instances of BaseStat associations for a given Monster after it's
# additional 'deviation values' are applied based on the Species base stat values and character creation

class AppliedStat(db.Model):
    __tablename__ = "applied_stat"
    id_no = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    base_stat = db.Column(db.Integer, db.ForeignKey('base_stat.id_no'), nullable=False)

    def __repr__(self):
        return "Stat({}: '{}', dv: {}, applied value: {})".format(
            self.id_no, self.stat.name, self.value, self.base_stat.increment * (self.base_stat.default * self.value)
        )


#
#   MOVE MODELS


# DiceValues represent the standard damage values that a Move can use in its damage calculation formula

class DiceValues(db.Model):
    __tablename__ = "dice_value"
    id_no = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    dice = db.relationship('Dice', backref="damage", lazy=True)

    def __repr__(self):
        return "DiceValue({}: {})".format(self.id_no, self.value)


# The Moves table represents an association between a move with a given name and a primary Color (which is
# used to organize Move Pool selections for the character creation process) as well as a number of Dice
# which are used for calculating damage

class Moves(db.Model):
    __tablename__ = "move"
    id_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id_no'), nullable=False)

    dice = db.relationship('Dice', backref="value", lazy=True)

    def __repr__(self):
        return "Move({}: '{}')".format(self.id_no, self.name)


# The Dice table represents an association between a damage value and a particular Color. Multiple dice
# can belong to a given move and are used for damage calculation

class Dice(db.Model):
    __tablename__ = "die"
    id_no = db.Column(db.Integer, primary_key=True)
    value_id = db.Column(db.Integer, db.ForeignKey('dice_value.id_no'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id_no'), nullable=False)
    move_id = db.Column(db.Integer, db.ForeignKey('move.id_no'), nullable=False)

    def __repr__(self):
        return "Die({}: {}, color id: {}, move: {})".format(
            self.id_no, self.value_id, self.color_id, self.move_id
        )
