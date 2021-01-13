from monster_flask.app import app
from flask import jsonify, request
from monster_flask.models import Color


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/color/', methods=['GET'])
def color():
    if "color" in request.args:
        color_id = int(request.args["color"])
        color_data = get_color_data(Color.query.get(color_id))
        return jsonify(color_data)

    else:
        return "error: select a color"


def get_color_data(color):
    mods = []
    for m in color.attack_mods:
        mods.append(get_color_mod_data(m))

    return {
        "id": color.id_no,
        "name": color.name,
        "mods": mods
    }


def get_color_mod_data(mod):
    return {
        "attacker": mod.attacker_color.name,
        "target": mod.target_color.name,
        "multiple": mod.mod_value.multiple
    }
