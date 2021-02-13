from flask import Blueprint, request

from monster_flask import char_creator, db
from monster_flask.game.controllers import ColorController, SpeciesController, MovesController
from monster_flask.utils import prepare_response

game = Blueprint('game', __name__)


COLORS = ColorController(db)
SPECIES = SpeciesController(db)
MOVES = MovesController(db)


@game.route('/color', methods=['GET'])
def color():
    if "color" in request.args:
        color_id = int(request.args["color"])

        return prepare_response(COLORS.get_color_by_id(color_id))

    else:
        return prepare_response(COLORS.get_all())


@game.route('/species', methods=['GET'])
def species():
    if "species" in request.args:
        species_id = int(request.args["species"])

        return prepare_response(SPECIES.get_species_by_id(species_id))

    else:
        return prepare_response(SPECIES.get_all())


@game.route('/monster', methods=['GET'])
def monster():
    if "species" in request.args:
        species_id = int(request.args["species"])

        return prepare_response(SPECIES.get_monster_by_species_id(species_id))

    else:
        return prepare_response({"error": "select a species by id"})


@game.route('/moves', methods=['GET'])
def moves():
    if "species" in request.args:
        return prepare_response(char_creator.get_species_moves(
            MOVES, SPECIES, request.args["species"]
        ))

    elif "move" in request.args:
        return prepare_response(MOVES.get_move_by_id(request.args["move"]))

    elif "color" in request.args:
        return prepare_response(MOVES.get_moves_by_color(request.args["color"]))

    else:
        return prepare_response(MOVES.get_all())


@game.route('/new_character', methods=['GET'])
def new_char():
    if "move_pool" in request.args:
        first, second = char_creator.get_move_pool(
            MOVES, COLORS, request.args["move_pool"]
        )

        return prepare_response({
            "first": first,
            "second": second
        })

    else:
        return prepare_response({
            "dv_max": char_creator.DV_MAX
        })
