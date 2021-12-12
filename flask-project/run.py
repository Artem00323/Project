from flask import Flask, render_template, url_for
from python_files import jupyter_1 as jp

app = Flask(__name__)

@app.route('/')
def main():
    tables, titles = jp.tables, jp.titles
    return render_template('index.html', tables=tables, titles=titles)

@app.route('/task1')
def task1():
    tables1, titles1 = jp.tables1, jp.titles1
    tables2, titles2 = jp.tables2, jp.titles2
    tables3, titles3 = jp.tables3, jp.titles3
    tables4, titles4 = jp.tables4, jp.titles4
    return render_template('task1.html', tables=tables1, titles=titles1, \
        tables2=tables2, titles2=titles2, \
            tables3=tables3, titles3=titles3, \
                tables4=tables4, titles4=titles4)
@app.route('/task2')
def task2():
    return render_template('task2.html')
@app.route('/task3')
def task3():
    return render_template('task3.html')
@app.route('/task4')
def task4():
    return render_template('task4.html')
@app.route('/task5')
def task5():
    return render_template('task5.html')

if __name__ == "__main__":
    app.run(debug=True)




# FLASK_DEBUG=1  FLASK_APP=run.py flask run