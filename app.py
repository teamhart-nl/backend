from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/print/', methods=['POST'])
def test():
    if request.method == 'POST':
        print(request.form['text'])
        return('200')

if __name__ == '__main__':
    app.run(debug=True)
