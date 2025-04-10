# Endpoints
# `/api/v1/details`
# `/api/v1/healthz`

# Link to Code
# https://www.geeksforgeeks.org/flask-creating-first-simple-application/


from flask import Flask

app = Flask(__name__)

@app.route('/api/v1/details')
def details():
    return '<h1>Hello World</h1>'

if __name__ == '__main__':
    app.run()

