from flask import Flask, render_template, request, jsonify
from policy_eval import generate_random_policy, policy_evaluation

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    n = int(data["n"])
    start = tuple(data["start"])   # [row, col]
    end = tuple(data["end"])       # [row, col]
    obstacles = [tuple(o) for o in data["obstacles"]]

    policy = generate_random_policy(n, obstacles, start, end)
    values = policy_evaluation(n, policy, obstacles, start, end)

    return jsonify({"policy": policy, "values": values})


if __name__ == "__main__":
    app.run(debug=True)
