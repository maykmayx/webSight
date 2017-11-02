from flask import Flask
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def homepage():
    the_time = "Hello world"

    return """
    <h1>האתר המגניב של רון ועומר</h1>
    <p>עוד מעט יהיה אפשר להעלות תמונות, בינתיים.. הינה חתול</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time=the_time)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)