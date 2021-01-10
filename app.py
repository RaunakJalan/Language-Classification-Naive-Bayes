from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
from LanguageClassification import predict_language
import os

app = Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict', methods = ['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        inputText = request.form['content']
        inputText = inputText.strip()
        language = predict_language(inputText)
        return render_template('index.html', result=[inputText, language])
    else:
        return render_template('index.html')

if __name__ == "__main__":
    # app.run(port=8001, debug=True)
    port = int(os.environ.get('PORT','5000'))
    app.run(debug=True, port = port)

