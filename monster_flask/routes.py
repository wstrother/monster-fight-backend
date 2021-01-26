from monster_flask.app import app, db
from flask import jsonify, request

from monster_flask.controllers import ColorController, SpeciesController, MovesController, StatController
from monster_flask import models

COLORS = ColorController(db, models.Color, models.ColorMod, models.ColorModValue)
SPECIES = SpeciesController(db, models.Species, models.BaseStat)
MOVES = MovesController(db, models.DiceValues, models.Moves, models.Dice)


def prepare_response(data):
    res = jsonify(data)
    res.headers.add('Access-Control-Allow-Origin', '*')
    status = 200

    if "error" in data:
        data.update({"request": request.args})
        status = 400

    return res, status

#
# def error(e):
#     e.update({"request": request.args})
#     # res = prepare_response({
#     #     "error": msg,
#     #     "request": request.args
#     # })
#     return prepare_response(e), 400


@app.route('/color/', methods=['GET'])
def color():
    if "color" in request.args:
        color_id = int(request.args["color"])

        # c = COLORS.query.get(color_id)
        # if c is None:
        #     return error("'id' value: '{}' not found".format(color_id))
        #
        # color_data = ColorController.get_color_data(c)
        # return prepare_response(color_data)

        return prepare_response(COLORS.get_color_by_id(color_id))

    else:
        return prepare_response({"error": "select a color by id"})


@app.route('/species/', methods=['GET'])
def species():
    if "species" in request.args:
        species_id = int(request.args["species"])

        # s = Species.query.get(species_id)
        # if s is None:
        #     return error("'id' value: '{}' not found".format(species_id))
        #
        # species_data = SpeciesController.get_species_data(s)
        # return prepare_response(species_data)

        return prepare_response(SPECIES.get_species_by_id(species_id))

    else:
        # species_list = [
        #     SpeciesController.get_species_data(s) for s in Species.query.all()
        # ]
        return prepare_response(SPECIES.get_all())


@app.route('/monster/', methods=['GET'])
def monster():
    if "species" in request.args:
        species_id = int(request.args["species"])

        # s = Species.query.get(species_id)
        # if s is None:
        #     return error("'id' value: '{}' not found".format(species_id))
        #
        # stats = BaseStat.query.all()
        #
        # monster_data = SpeciesController.get_monster_data(s, stats)
        # return prepare_response(monster_data)

        return SPECIES.get_monster_by_species_id(species_id)

    else:
        return prepare_response({"error": "select a species by id"})


@app.route('/moves/', methods=['GET'])
def moves():
    if "species" in request.args:
        pass

    elif "move" in request.args:
        return prepare_response(MOVES.get_move_by_id(request.args["move"]))

    else:
        return prepare_response(MOVES.get_all())


@app.route('/new_character/', methods=['GET'])
def new_char():
    return prepare_response({
        "dv_max": 5
    })
