import tensorflow as tf
import cv2
import numpy as np
from http.server import BaseHTTPRequestHandler, HTTPServer

# Load the sign language model
model = tf.keras.models.load_model('keras_model.h5')


# Define the HTTP request handler class
class MyRequestHandler(BaseHTTPRequestHandler):

    # Handle GET requests
    def do_GET(self):
        if self.path == '/':
            # Serve the index.html file
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path.endswith('.js'):
            # Serve the JavaScript file
            self.send_response(200)
            self.send_header('Content-type', 'text/javascript')
            self.end_headers()
            with open('static/script.js', 'rb') as f:
                self.wfile.write(f.read())
        else:
            # Serve other files (such as CSS)
            self.send_response(200)
            self.send_header('Content-type', 'text/css' if self.path.endswith('.css') else 'application/octet-stream')
            self.end_headers()
            with open(self.path[1:], 'rb') as f:
                self.wfile.write(f.read())

    # Handle POST requests
    def do_POST(self):
        if self.path == '/predict':
            # Read the uploaded image
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            # Convert the image to a Numpy array
            nparr = np.frombuffer(post_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # Preprocess the image for the model
            img = cv2.resize(img, (224, 224))
            img = img / 255.0
            img = np.expand_dims(img, axis=0)
            # Make a prediction using the model
            pred = model.predict(img)
            # Get the predicted label
            label = np.argmax(pred)
            # Return the predicted label to the webpage
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(label).encode())
        else:
            self.send_error(404)


# Define the main function
def main():
    # Create an HTTP server and serve requests indefinitely
    server = HTTPServer(('', 8080), MyRequestHandler)
    print('Server started on http://localhost:8080')
    server.serve_forever()


if __name__ == '__main__':
    main()