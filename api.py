from flask import Flask, Response, jsonify

app = Flask(__name__)
filename = "simulation.log"
@app.route("/api/ping", methods=["GET"])
def ping():
    return Response(status=200)

@app.route("/api/traffic/info", methods=["GET"])
def info():
    data = {
        "vehicles": []
    }
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            mode, module, idx, x, y = map(lambda s: s.strip(), line.split(":"))
            data["vehicles"].append({ "mode": mode, "module":module, "idx": idx, "x": x, "y": y })
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
