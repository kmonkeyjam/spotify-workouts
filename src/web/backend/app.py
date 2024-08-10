from chalice import Chalice, Response
import os
import mimetypes

app = Chalice(app_name='spotify-workouts-web')

@app.route('/')
def index():
    # Path to the build directory of your React app
    html_file_path = os.path.join(os.path.dirname(__file__), 'chalicelib', 'build', 'index.html')

    # Read the HTML file content
    with open(html_file_path, 'r') as html_file:
        html_content = html_file.read()

    # Return the HTML content as a response
    return Response(body=html_content, status_code=200, headers={'Content-Type': 'text/html'})

@app.route('/static/{path+}')
def serve_static_files(path):
    static_file_path = os.path.join(os.path.dirname(__file__), 'chalicelib', 'build', 'static', path)

    if os.path.exists(static_file_path):
        content_type, _ = mimetypes.guess_type(static_file_path)
        with open(static_file_path, 'rb') as static_file:
            return Response(body=static_file.read(), status_code=200, headers={'Content-Type': content_type or 'application/octet-stream'})
    else:
        return Response(body='File not found', status_code=404)
