from flask import Flask, request, jsonify
from score import score, load_model

app = Flask(__name__)
model = load_model()

@app.route("/score", methods=["POST"])
def score_endpoint():
    try:
        data = request.get_json(force=True)
        print("✅ Received data:", data)

        text = data.get("text", "")
        threshold = float(data.get("threshold", 0.5))
        print(f"✅ Parsed text: '{text}', threshold: {threshold}")

        prediction, propensity = score(text, model, threshold)
        print("✅ Score output:", prediction, propensity)

        return jsonify({
            "prediction": prediction,
            "propensity": propensity
        })
    
    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": "Invalid request", "message": str(e)}), 400

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify({"error": "Bad Request", "message": str(e)}), 400

# ✅ THIS BLOCK STARTS THE FLASK SERVER CORRECTLY
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
