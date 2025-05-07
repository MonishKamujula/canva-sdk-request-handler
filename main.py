from openai import OpenAI
from flask import Flask
from flask import request
from canva_rag import handle_rag
import openai

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/canvarequest" , methods=['POST'])
def canvarequest():

    user_input = request.get_json()['user_input']

    return_type_format = handle_rag(user_input)

    prompt = f'''
    Return json value in the following format according to given input :
    {return_type_format} 
    '''

    
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1",
        instructions=prompt,
        input=user_input,
    )

    return response.output_text


if __name__ == "__main__":
    app.run()


