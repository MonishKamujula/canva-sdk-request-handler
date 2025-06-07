from openai import OpenAI
from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
from controllers import create_canva_functions, create_steps, create_cards_from_user_input

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



# class CanvaRequest(BaseModel):
#     function : dict
# class CanvaReturnFormat(BaseModel):
#     functions : list(CanvaRequest)

@app.route("/canvarequest" , methods=['POST'])
def canvarequest():
    user_input = request.get_json()['user_input']
    page_dimensions = request.get_json()['page_dimensions']["dimensions"]
    current_page = request.get_json()['current_page']

    functions = create_canva_functions(create_steps(user_input), page_dimensions)
    
    return functions


@app.route("/create_cards", methods=["POST"])
def create_cards():
    user_input = request.get_json()["user_input"]
    n_cards = request.get_json()["n_cards"]

    return create_cards_from_user_input(user_input, n_cards)


if __name__ == "__main__":
    app.run()


