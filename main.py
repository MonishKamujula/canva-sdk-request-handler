from openai import OpenAI
from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
from canva_rag import handle_rag
import openai
from pydantic import BaseModel
from pprint import pprint
import requests
import re
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

class StepBreakdown(BaseModel):
    steps: list[str]
    rag_query : list[str]

# class CanvaRequest(BaseModel):
#     function : dict
# class CanvaReturnFormat(BaseModel):
#     functions : list(CanvaRequest)

@app.route("/canvarequest" , methods=['POST'])
def canvarequest():
    user_input = request.get_json()['user_input']
    page_dimensions = request.get_json()['page_dimensions']["dimensions"]
    print("User Input is : " , user_input)
    step_client = OpenAI()
    step_prompt = f'''
    #Break down the given input into smaller technical step commands seperated by comma to generate a document.
    - Example : 
    if given input is "Add information about animal on the page" then output should be :
    Add heading about animal on the page, Add image about animal at center of the page, Add paragraph about animal at bottom of the page
    Also according to command provide the list of rag query required for steps. Here is the list of rag query:
    - An element that renders image.
    - An element that renders image content and has positional properties.
    - An element that renders video content.
    - An element that renders video content and has positional properties.
    - An element that renders text content.
    - An element that renders text content and has positional properties.
    - An element that renders rich text content.
    - An element that renders rich text content and has positional properties.
    - An element that renders rich media, such as a YouTube video.
    - An element that renders rich media, such as a YouTube video, and has positional properties.
    - An element that renders a vector shape.
    - An element that renders a vector shape and has positional properties.
    - An element that renders a table.
    - An element that renders a table and has positional properties.
    - An element that renders a vector shape.
    - An element that renders a vector shape and has positional properties.
    - An element that renders a table.
    - An element that renders a table and has positional properties.
    '''

    response = step_client.responses.parse(
        model="gpt-4.1",
        input=[
        {
            "role": "system",
            "content": step_prompt,
        },
        {"role": "user", "content": user_input},
    ],
        text_format=StepBreakdown,
    )

    print("Step Breakdown : " , response)
    print("STEP BREAKDOWN WITH OUTPUT PRASED : " , response.output_parsed)

    def search_pexels_image(query):
        headers = {"Authorization": "xwjeCY8K2Lz6sYAAwVlUvMEC2rt4cJ2hDVjlEfUdwCTsgyv2jh2MmKQZ"}
        params = {"query": query, "per_page": 1}
        response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
        try: 
            return response.json()['photos'][0]['src']['medium']
        except IndexError as e:
            return "https://i.postimg.cc/jSYRBQWR/image-not-found.png"
        
    
    all_steps = response.output_parsed

    return_type_format = handle_rag(all_steps.rag_query)

    prompt = f'''
    You are an Ai which can design a canva page, with great astehetics.
    Return array of json value in the following format according for given input steps :
    {return_type_format} 
    Follow the postional properties given in the steps and generate the canva commands accordingly. This Should look asthetically pleasing. And try to keep content inside the page dimensions
    the output should be only a list of json objects, where each json object is a canva function format as given above. No extra tags, no extra lines, no extra spaces. Should start with [ and end with ], don't add any comments.
    page_dimensions : {page_dimensions}. Everything is in pixels, This width and height are different from the width and height of an element in the page.
    The top left corrner is (top 0, left 0), top right corner is (left {page_dimensions["width"]}, top 0), bottom left corner is (left 0, top {page_dimensions["height"]}), and the bottom right corner is (left {page_dimensions["width"]}, top {page_dimensions["height"]}). 
    All the elements should be inside the page dimensions. Some params for some elements have a spefic set of values to choose from, so choose from only those values, for example if you are dealing with textalign, choose only "start", "center", "end", "justify".
    '''

    user_steps = ",".join(all_steps.steps)
    
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1",
        instructions=prompt,
        input=user_steps,
    )
    
    print("Response is : " , response.output_text)
    edited_response = json.loads(response.output_text)

    for item in edited_response:
        print("Item is : " , item)
        if "ref" in item:
            old = item["ref"]
            print("Old is : " , old)
            print("New is : " , search_pexels_image(old))
            print("__________________________________________________________________________")
            item["ref"] = search_pexels_image(old)
    print(page_dimensions)
    print("Edited Response : " , json.dumps(edited_response, indent=2))
    return json.dumps(edited_response, indent=2)


if __name__ == "__main__":
    app.run()


