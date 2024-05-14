from chalice import Chalice

app = Chalice(app_name='mylambdaapp')

@app.route('/')
def index():
    return {'message': 'Hello from AWS Lambda using Chalice!'}

