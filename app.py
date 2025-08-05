from flask import Flask, render_template

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


@app.get('/status')
def status():
    return {'damaged_system': SYSTEM}


@app.get('/repair-bay')
def repair_bay():
    return render_template('repair-bay.html', code=CODE)


@app.post('/teapot')
def teapot():
    return "I'm a teapot!", 418
