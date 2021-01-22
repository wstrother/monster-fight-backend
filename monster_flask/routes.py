from monster_flask.app import app
from flask import jsonify, request

from monster_flask.controllers import get_color_data, get_species_data, get_monster_data
from monster_flask.models import Color, Species, BaseStat


def prepare_response(data):
    res = jsonify(data)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res


def error(msg):
    res = prepare_response({
        "error": msg,
        "request": request.args
    })
    return res, 400


@app.route('/color/', methods=['GET'])
def color():
    if "color" in request.args:
        color_id = int(request.args["color"])

        c = Color.query.get(color_id)
        if c is None:
            return error("'id' value: '{}' not found".format(color_id))

        color_data = get_color_data(c)
        return prepare_response(color_data)

    else:
        return error("select a color by id")


@app.route('/species/', methods=['GET'])
def species():
    if "species" in request.args:
        species_id = int(request.args["species"])

        s = Species.query.get(species_id)
        if s is None:
            return error("'id' value: '{}' not found".format(species_id))

        species_data = get_species_data(s)
        return prepare_response(species_data)

    else:
        species_list = [
            get_species_data(s) for s in Species.query.all()
        ]
        return prepare_response(species_list)


@app.route('/monster/', methods=['GET'])
def monster():
    if "species" in request.args:
        species_id = int(request.args["species"])

        s = Species.query.get(species_id)
        if s is None:
            return error("'id' value: '{}' not found".format(species_id))

        stats = BaseStat.query.all()

        monster_data = get_monster_data(s, stats)
        return prepare_response(monster_data)

    else:
        return error("select a species by id")


@app.route('/new_character/', methods=['GET'])
def new_char():
    return prepare_response({
        "dv_max": 5
    })
