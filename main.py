from flask import Flask

app = Flask(__name__)


@app.route("/")
def main():
    return "Test vercel app"

if (__name__) == "__main__":
    app.run(debug=False)