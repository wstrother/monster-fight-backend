from monster_flask.app import app, db
from flask import jsonify, request

from monster_flask import char_creator
from monster_flask.controllers import ColorController, SpeciesController, MovesController

COLORS = ColorController(db)
SPECIES = SpeciesController(db)
MOVES = MovesController(db)


def prepare_response(data):
    res = jsonify(data)
    res.headers.add('Access-Control-Allow-Origin', '*')
    status = 200

    if "error" in data:
        data.update({"request": request.args})
        status = 400

    return res, status


@app.route('/color/', methods=['GET'])
def color():
    if "color" in request.args:
        color_id = int(request.args["color"])

        return prepare_response(COLORS.get_color_by_id(color_id))

    else:
        return prepare_response(COLORS.get_all())


@app.route('/species/', methods=['GET'])
def species():
    if "species" in request.args:
        species_id = int(request.args["species"])

        return prepare_response(SPECIES.get_species_by_id(species_id))

    else:
        return prepare_response(SPECIES.get_all())


@app.route('/monster/', methods=['GET'])
def monster():
    if "species" in request.args:
        species_id = int(request.args["species"])

        return prepare_response(SPECIES.get_monster_by_species_id(species_id))

    else:
        return prepare_response({"error": "select a species by id"})


@app.route('/moves/', methods=['GET'])
def moves():
    # if "move" in request.args and "color" in request.args:
    #     return prepare_response(MOVES.get_move_by_color_index(
    #         request.args["color"], request.args["move"]
    #     ))
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


@app.route('/new_character/', methods=['GET'])
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
