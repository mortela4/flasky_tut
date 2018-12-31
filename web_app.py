from flask import Flask, render_template


app = Flask(__name__)


B = ["Ten", "Pearl Jam", "Grunge"]


@app.route('/')
def main():
    return render_template('tut_1.html', my_list=B)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

