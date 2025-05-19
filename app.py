from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Halo, Flask berjalan dengan baik!"

if __name__ == "__main__":
    app.run(debug=True)
