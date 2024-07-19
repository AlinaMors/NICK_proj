from flask import Flask, render_template, jsonify, request
import requests
from ya_gpt_client import get_client
import prompts


app = Flask(__name__)
BASE_URL = '/neurones'
app.config['BASE_URL'] = BASE_URL
GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"


@app.context_processor
def inject_base_url():
    return dict(base_url=app.config['BASE_URL'])


@app.route(f'/api/gen_task_by_location', methods=['GET'])
def get_parks():
    try:
        location = request.args.get('location')
        task_type = request.args.get('task_type', None)
        client = get_client()
        if task_type:
            task_text = client.chat(
                prompts.task_system_prompt, prompts.task_user_prompt_with_type %(location, task_type))
        else:
            task_text = client.chat(
                prompts.task_system_prompt, prompts.task_user_prompt %(location))
        response = {"location": location, "task": task_text}
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5002)
