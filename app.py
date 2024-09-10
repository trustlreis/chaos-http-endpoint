from flask import Flask, request

app = Flask(__name__)

# Catch-all route to handle any path and any HTTP method
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def catch_all(path):
    print(f"Received request on {path}")
    print(f"Headers: {request.headers}")
    print(f"Body: {request.get_data(as_text=True)}")
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
