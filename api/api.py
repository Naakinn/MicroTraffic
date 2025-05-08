from flask import Flask, Response, jsonify, render_template

app = Flask(__name__)
filename = "simulation.log"


@app.route("/api/ping", methods=["GET"])
def ping():
    return Response(status=200)


@app.route("/api/traffic/info", methods=["GET"])
def info():
    data = {"vehicles": [], "traffic_light": str}
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            logline = list(map(lambda s: s.strip(), line.split(":")))
            if logline[2] == "v":
                mode, module, _, idx, x, y, dir = logline
                data["vehicles"].append(
                    {
                        "mode": mode,
                        "module": module,
                        "idx": idx,
                        "x": x,
                        "y": y,
                        "dir": dir,
                    }
                )
            elif logline[2] == "l":
                light_state = logline[3]
                data["traffic_light"] = light_state
            else:
                raise ValueError("Unrecognized log type")
    return render_template("traffic.html", data=data)


if __name__ == "__main__":
    app.run(port=8000)
