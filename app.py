
from flask import Flask, request, jsonify, send_from_directory
import os
import urllib.request
import json

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/api/notify", methods=["POST"])
def notify():

    webhook = os.environ.get("DISCORD_WEBHOOK_URL")

    if not webhook:
        return jsonify({"error": "Webhook not configured"}), 500

    try:
        payload = json.dumps({
            "content": "Someone submitted the Wi-Fi form."
        }).encode("utf-8")

        req = urllib.request.Request(
            webhook,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        urllib.request.urlopen(req, timeout=10)

        return jsonify({"success": True}), 200

    except Exception:
        return jsonify({"error": "Notification failed"}), 500


if __name__ == "__main__":
    app.run()
