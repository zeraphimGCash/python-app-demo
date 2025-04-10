# Endpoints
# `/api/v1/details`
# `/api/v1/healthz`

# Link to Code
# https://www.geeksforgeeks.org/flask-creating-first-simple-application/


from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route('/api/v1/healthz')
def healthz():
    return jsonify({
        'status': 'up'
    }), 200


@app.route('/api/v1/details')
def details():
    return jsonify({
        'time': datetime.datetime.now().strftime("%I:%M%p %S on %B %d, %Y"),
        'hostname': 'here'
    }) 

if __name__ == '__main__':
    app.run()

