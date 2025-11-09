from flask import Flask, request, jsonify, render_template
from main import processCommand
import webbrowser

main = Flask(__name__)

@main.route("/")
def index():
    return render_template("interface.html")

@main.route("/run", methods=["POST"])
def run_command():
    try:
        cmd = request.form.get("command", "")

        if not cmd:
            return jsonify({"message": "No command received"})

        output = processCommand(cmd)

        if isinstance(output, dict):
            text = output.get("message", "Processed")
            url = output.get("url", None)
        else:
            text = str(output)
            url = None

        return jsonify({"message": text, "url": url})

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})


if __name__ == "__main__":
    main.run(debug=True)
