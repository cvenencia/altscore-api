from flask import Flask, render_template, request

app = Flask(__name__)

SYSTEMS = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

SYSTEM = 'life_support'
CODE = SYSTEMS[SYSTEM]

P_LIQUID, V_LIQUID = 0.05, 0.00105
PC, VC = 10, 0.0035
P_VAPOR, V_VAPOR = 0.05, 30

Point = tuple[float, float]


def get_linear_function(xy1: Point, xy2: Point):
    x1, y1 = xy1
    x2, y2 = xy2

    slope = (y2 - y1) / (x2 - x1)
    intercept = slope * (-x1) + y1

    def f(x):
        return round(slope * x + intercept, 8)

    return f


fp_liquid = get_linear_function((P_LIQUID, V_LIQUID), (PC, VC))
fp_vapor = get_linear_function((PC, VC), (P_VAPOR, V_VAPOR))


@app.get('/status')
def status():
    return {'damaged_system': SYSTEM}


@app.get('/repair-bay')
def repair_bay():
    return render_template('repair-bay.html', code=CODE)


@app.post('/teapot')
def teapot():
    return "I'm a teapot!", 418


@app.get('/phase-change-diagram')
def phase_change_diagram():
    pressure = request.args.get('pressure')
    if pressure is None:
        return {'error': 'Missing pressure parameter'}, 400
    try:
        pressure = float(pressure)
    except ValueError:
        return {'error': 'Value type not correct. Expected int/float'}, 400

    if not (P_LIQUID <= pressure <= PC):
        return {'error': 'Pressure is outside of temperature range'}, 400

    return {
        'specific_volume_liquid': fp_liquid(pressure),
        'specific_volume_vapor': fp_vapor(pressure),
    }
