from monster_flask.app import db


#   COLOR MODELS


#   Monster color, represents elemental 'type' and is used to determine damage modifiers such as
#   SCAB (Same Color Attack Bonus) and 'effectiveness' modifiers

class Color(db.Model):
    __tablename__ = "color"
    id_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    species = db.relationship('Species', backref="color", lazy=True)
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


class Species(db.Model):
    __tablename__ = "species"
    id_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id_no'), nullable=False)

    #   base stats
    base_life = db.Column(db.Integer, nullable=False)
    base_energy = db.Column(db.Integer, nullable=False)
    base_defense = db.Column(db.Integer, nullable=False)
    base_special = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Species({}: '{}', color: '{}')".format(self.id_no, self.name, self.color_id)


#
#   STAT MODELS


class Stat(db.Model):
    __tablename__ = "stat"
    id_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    default = db.Column(db.Integer, nullable=False)
    increment = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Stat({}: '{}'. default value: {}, increment: {})".format(
            self.id_no, self.name, self.default * self.increment, self.increment
        )
