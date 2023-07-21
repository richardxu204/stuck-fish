# app.py
from flask import Flask, send_file, render_template
import os

app = Flask(__name__)

# Function to get the absolute path of the "images" directory
def get_image_path(filename):
    image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
    return os.path.join(image_dir, filename)

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve the images
@app.route('/image/<filename>')
def serve_image(filename):
    # Get the absolute path of the image file
    image_path = get_image_path(filename)
    
    # Check if the image file exists
    if os.path.exists(image_path):
        # Use Flask's send_file function to send the image file to the browser
        return send_file(image_path, mimetype='image/jpeg')  # You can adjust the mimetype based on your image type (e.g., 'image/png')

    # Return a 404 Not Found error if the image file does not exist
    return "Image not found", 404

if __name__ == '__main__':
    app.run(debug=True)