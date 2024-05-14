from chalice import Chalice, Response
import os

app = Chalice(app_name='mylambdaapp')

@app.route('/')
def index():
    # Specify the path to your HTML file
    html_file_path = os.path.join(os.path.dirname(__file__), 'chalicelib', 'index.html')

    # Read the HTML file content
    with open(html_file_path, 'r') as html_file:
        html_content = html_file.read()

    # Return the HTML content as a response
    return Response(body=html_content, status_code=200, headers={'Content-Type': 'text/html'})

