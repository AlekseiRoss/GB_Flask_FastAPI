from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/main/')
def main():
    context = {'title': 'Главная'}
    return render_template('main.html', **context)


@app.route('/shoes/')
def shoes():
    context = {'title': 'Обувь'}
    return render_template('shoes.html', **context)


@app.route('/coats/')
def coats():
    context = {'title': 'Куртки'}
    return render_template('coats.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
