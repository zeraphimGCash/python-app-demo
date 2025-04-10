# Endpoints
# `/api/v1/details`
# `/api/v1/healthz`

# Link to Code
# https://www.geeksforgeeks.org/flask-creating-first-simple-application/


from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v1/details')
def details():
    return jsonify({
        'message': 'hello_world'
    }) 

if __name__ == '__main__':
    app.run()

