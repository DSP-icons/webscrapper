from flask import Flask, request, jsonify
import json
from bs4 import BeautifulSoup
import requests
import os

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/api/news', methods=['POST'])
def get_news():
    url = request.json['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news = soup.get_text()
    prompt = f"""
        Toma la siguiente noticia que está delimitada por guiones tripes (---).
        Verifica que la noticia tenga relación con un desastre natural.
        De esta información extrae la información más relevante y retorna un json con la siguiente información:
        - title: El título de la noticia
        - type: tipo de desastre natural como terremoto, inundación, etc.
        - country: país donde ocurrió el desastre natural
        - city: ciudad donde ocurrió el desastre natural si esta información está disponible, si no es null
        - continent: continente donde ocurrió el desastre natural
        - date: fecha en que ocurrió el desastre natural en formato iso 8601
        - description: descripción del desastre natural
        - source: la fuente de la noticia -> {url}
        ---{news}---
        """
    openai_url = 'https://api.openai.com/v1/engines/davinci-codex/completions'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}'}
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"user", "content": prompt}
        ],
    )

    print(response.choices[0])

    # result = response.json()['choices'][0]['text']
    return jsonify(json.loads(response.choices[0].message.content))

if __name__ == '__main__':
    app.run(debug=True)