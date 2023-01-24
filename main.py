import numpy as np
import heapq
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for
import os
from colorthief import ColorThief
import webcolors


app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    image.save(os.path.join('static/uploads', image.filename))
    file_name = f'static/uploads/{image.filename}'
    my_img = Image.open(file_name)
    # Convert the image to a numpy array
    im_array = np.array(my_img)
    # Flatten the array and convert to list
    pixels = im_array.flatten().tolist()

    # Create a dictionary to store the frequency of each color
    color_count = {}

    # Iterate through the list of pixels and count the frequency of each color
    for color in pixels:
        if color in color_count:
            color_count[color] += 1
        else:
            color_count[color] = 1

    # Find the 10 colors with the highest frequency
    most_used_colors = heapq.nlargest(10, color_count, key=color_count.get)

# Open the image
    color_thief = ColorThief(file_name)

    # Get the palette of the image with 10 colors
    palette = color_thief.get_palette(color_count=10)

    # Print the 10 most used colors as color codes

    var = []
    print("10 most used colors:")
    for color in palette:
        color_code = webcolors.rgb_to_hex(color)
        print(color_code, 'color_code')
        var.append(color_code)

    return render_template('index.html', filename=image.filename, most_used_colors=var)


if __name__ == '__main__':
    app.run(debug=True)
