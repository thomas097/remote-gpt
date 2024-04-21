import time
import threading
from pyngrok import ngrok
from flask import Flask, request, jsonify
from hosting import authenticate, Config, pprint, ask_confirm


app = Flask(__name__)
llm = None

@app.route('/text', methods=['POST'])
def POST_request_handler():
    text = request.get_json()['text']

    response = {
        "success": True,
        "response": "this is my response!"
    }

    return jsonify(response)


def main(config: Config):
    authenticate(auth_token=config.authtoken)

    # Use ngrok to open tunnel to the HTTP server
    public_url = ngrok.connect(config.port).public_url
    pprint(f"Exposing 'http://127.0.0.1:{config.port}' as '{public_url}'")

    # Set Flask's URL to the public ngrok URL
    app.config["BASE_URL"] = public_url

    # TODO: initialize LLM

    # Start Flask server in a new thread
    pprint(f"Booting up '{app.name}'", rule=True)
    threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()

    time.sleep(1)
    pprint("Running!", rule=True)

    # Close connection
    while not ask_confirm("\n To close connection, press 'Y'"):
        pass

    ngrok.disconnect(public_url)


if __name__ == '__main__':
    config = Config("config.toml")
    main(config=config)