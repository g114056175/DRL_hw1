from flask import Flask, render_template, request, jsonify
from policy_eval import value_iteration_steps, policy_iteration_steps, generate_random_policy

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/iterate", methods=["POST"])
def iterate():
    """
    接收 Grid 設定，執行 Value Iteration，回傳完整步驟歷史供前端逐步視覺化。
    Request JSON : { n, start:[r,c], end:[r,c], obstacles:[[r,c],...] }
    Response JSON: { steps:[...], total:int, converged_at:int|null }
    """
    data           = request.get_json()
    n              = int(data["n"])
    start          = data["start"]
    end            = data["end"]
    obstacles      = data["obstacles"]
    initial_values = data.get("initial_values")   # None for fresh run, dict for hot-edit branch

    steps = value_iteration_steps(n, obstacles, start, end,
                                   initial_V=initial_values)

    # 找出首次收斂的步驟索引
    converged_at = next(
        (s["iteration"] for s in steps if s["converged"]), None
    )

    return jsonify({
        "steps":        steps,
        "total":        len(steps),
        "converged_at": converged_at,
    })


@app.route("/policy_iterate", methods=["POST"])
def policy_iterate():
    """
    執行 Policy Iteration 並回傳步驟快照。
    """
    data      = request.get_json()
    n         = int(data["n"])
    start     = data["start"]
    end       = data["end"]
    obstacles = data["obstacles"]

    steps = policy_iteration_steps(n, obstacles, start, end)

    converged_at = next(
        (s["iteration"] for s in steps if s["converged"]), None
    )

    return jsonify({
        "steps":        steps,
        "total":        len(steps),
        "converged_at": converged_at,
    })


@app.route("/reset_policy", methods=["POST"])
def reset_policy():
    """
    隨機重新生成初始策略。
    """
    data      = request.get_json()
    n         = int(data["n"])
    start     = data["start"]
    end       = data["end"]
    obstacles = data["obstacles"]

    policy = generate_random_policy(n, obstacles, start, end)
    return jsonify({"policy": policy})


if __name__ == "__main__":
    app.run(debug=True)
