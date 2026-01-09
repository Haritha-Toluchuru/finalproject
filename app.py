# Importing the required libraries
from flask import Flask,render_template,request,redirect, url_for
import mysql.connector

import os


app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='fruits'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/prediction', methods=["POST", "GET"])
def prediction():
    return render_template("prediction.html")

@app.route('/prediction1', methods=["POST", "GET"])
def prediction1():
    return render_template("prediction1.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT UPPER(email) FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email.upper() in email_data_list:
            
            query = "SELECT UPPER(password) FROM users WHERE email = %s"
            values = (email,)
            password__data = retrivequery1(query, values)
            if password.upper() == password__data[0][0]:
                
                global user_email
                user_email = email

                return render_template('home.html')
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']  

        if password != c_password:
            return render_template('register.html', message="Confirm password does not match!")

        
        query = "SELECT UPPER(email) FROM users"
        email_data = retrivequery2(query)
        email_data_list = [i[0] for i in email_data]

        if email.upper() in email_data_list:
            return render_template('register.html', message="This email ID already exists!")

        
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        values = (name, email, password)
        executionquery(query, values)

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home():
    return render_template('home.html')

#================================================= Fruits Image Dection Code =============================================

from flask import Flask, render_template, request
import os
import cv2
import numpy as np
from ultralytics import YOLO
from werkzeug.utils import secure_filename

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the YOLO model
model = YOLO('fruits_and_vegetable.pt')

# Static information for each class (calories per 100g, avg weight per unit, description)
FRUIT_VEG_INFO = {
    'Bitter melon': {'calories': 17, 'weight': 100, 'description': 'A bitter, green vegetable used in Asian cuisine, known for its health benefits.'},
    'Brinjal': {'calories': 25, 'weight': 200, 'description': 'Also known as eggplant, a versatile vegetable used in various dishes.'},
    'Cabbage': {'calories': 25, 'weight': 1000, 'description': 'A leafy green vegetable rich in fiber and vitamins.'},
    'Calabash': {'calories': 14, 'weight': 500, 'description': 'A bottle-shaped gourd often used in soups or as a container.'},
    'Capsicum': {'calories': 20, 'weight': 150, 'description': 'Bell peppers, available in various colors, rich in vitamin C.'},
    'Cauliflower': {'calories': 25, 'weight': 800, 'description': 'A cruciferous vegetable high in fiber and nutrients.'},
    'Cherry': {'calories': 50, 'weight': 5, 'description': 'Small, sweet fruits rich in antioxidants.'},
    'Garlic': {'calories': 149, 'weight': 3, 'description': 'A pungent bulb used for flavoring and medicinal purposes.'},
    'Ginger': {'calories': 80, 'weight': 50, 'description': 'A spicy root used in cooking and for its anti-inflammatory properties.'},
    'Green Chili': {'calories': 40, 'weight': 10, 'description': 'Spicy peppers used to add heat to dishes.'},
    'Kiwi': {'calories': 61, 'weight': 70, 'description': 'A small fruit with a fuzzy skin, rich in vitamin C.'},
    'Lady finger': {'calories': 33, 'weight': 15, 'description': 'Also known as okra, a green vegetable used in stews.'},
    'Onion': {'calories': 40, 'weight': 150, 'description': 'A staple vegetable used for flavoring in many cuisines.'},
    'Potato': {'calories': 77, 'weight': 200, 'description': 'A starchy tuber used in a wide variety of dishes.'},
    'Sponge Gourd': {'calories': 20, 'weight': 200, 'description': 'A mild-flavored gourd used in Asian cooking.'},
    'Tomato': {'calories': 18, 'weight': 100, 'description': 'A juicy fruit often used as a vegetable in cooking.'},
    'apple': {'calories': 52, 'weight': 180, 'description': 'A crisp fruit available in many varieties, rich in fiber.'},
    'avocado': {'calories': 160, 'weight': 140, 'description': 'A creamy fruit high in healthy fats and potassium.'},
    'banana': {'calories': 89, 'weight': 120, 'description': 'A sweet, elongated fruit rich in potassium.'},
    'cucumber': {'calories': 16, 'weight': 300, 'description': 'A refreshing vegetable high in water content.'},
    'dragon fruit': {'calories': 60, 'weight': 300, 'description': 'A vibrant fruit with mild sweetness and tiny seeds.'},
    'egg': {'calories': 68, 'weight': 50, 'description': 'A protein-rich food, typically from chickens.'},
    'guava': {'calories': 68, 'weight': 150, 'description': 'A tropical fruit high in vitamin C and fiber.'},
    'mango': {'calories': 60, 'weight': 200, 'description': 'A juicy tropical fruit known as the king of fruits.'},
    'orange': {'calories': 47, 'weight': 130, 'description': 'A citrus fruit rich in vitamin C.'},
    'oren': {'calories': 47, 'weight': 130, 'description': 'Likely a typo for orange, a citrus fruit rich in vitamin C.'},
    'peach': {'calories': 39, 'weight': 150, 'description': 'A juicy fruit with a fuzzy skin, rich in vitamins.'},
    'pear': {'calories': 57, 'weight': 180, 'description': 'A sweet, juicy fruit with a smooth texture.'},
    'pineapple': {'calories': 50, 'weight': 1000, 'description': 'A tropical fruit with a sweet-tart flavor.'},
    'strawberry': {'calories': 32, 'weight': 15, 'description': 'A sweet, red berry rich in antioxidants.'},
    'sugar apple': {'calories': 94, 'weight': 250, 'description': 'Also known as custard apple, a sweet tropical fruit.'},
    'watermelon': {'calories': 30, 'weight': 5000, 'description': 'A large, juicy fruit high in water content.'}
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/image_upload', methods=['GET', 'POST'])
def image_upload():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('image_upload.html', error='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('image_upload.html', error='No selected file')
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Make predictions using YOLO
            results = model.predict(filepath, conf=0.25, iou=0.45, save=False, show=False)
            
            # Get class names and their static info
            class_names = results[0].names
            detected_items = [
                {
                    'class_name': class_names[int(cls)],
                    'calories': FRUIT_VEG_INFO.get(class_names[int(cls)], {}).get('calories', 'Unknown'),
                    'weight': FRUIT_VEG_INFO.get(class_names[int(cls)], {}).get('weight', 'Unknown'),
                    'description': FRUIT_VEG_INFO.get(class_names[int(cls)], {}).get('description', 'No description available')
                }
                for cls in results[0].boxes.cls
            ]

            # Generate and save image with bounding boxes
            img_with_predictions = results[0].plot()  # Plot includes bounding boxes and labels
            output_filename = f'processed_{filename}'
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            cv2.imwrite(output_filepath, img_with_predictions)

            # Pass the detected items and image path to the template
            return render_template('image_upload.html', 
                                 image_path=output_filename, 
                                 detected_items=detected_items,
                                 success=True)
        else:
            return render_template('image_upload.html', error='Invalid file type')
    return render_template('image_upload.html')


#================================================================================================================================

#============================================================ Fruits LIVE Detection =================================================================

import os
import cv2
from flask import Flask, render_template
from ultralytics import YOLO

import subprocess
@app.route('/image_live',methods=['POST','GET'])
def image_live():
    if request.method == 'POST':
        subprocess.Popen(['python', 'live.py'])

    return render_template("image_live.html")

#=============================================================================================================================

#======================================================= Fruit Rippen Detection (Live) ==============================================

import os
import cv2
from flask import Flask, render_template
from ultralytics import YOLO

import subprocess
@app.route('/image_live1',methods=['POST','GET'])
def image_live1():
    if request.method == 'POST':
        subprocess.Popen(['python', 'live1.py'])

    return render_template("image_live1.html")

#======================================================= Fruit Rippen Detection (upload) ==============================================

from flask import Flask, request, render_template
import cv2
import numpy as np
from ultralytics import YOLO
import io
import base64
from PIL import Image


# Load the trained YOLO model once at startup
model12 = YOLO('Fruits_rippen_detection.pt')

# Classes your model predicts
classes = [
    'Apple Overripe', 'Apple Ripe', 'Apple Rotten', 'Apple Unripe',
    'Banana Overripe', 'Banana Ripe', 'Banana Rotten', 'Banana Unripe',
    'Grape Overripe', 'Grape Ripe', 'Grape Rotten', 'Grape Unripe',
    'Mango Overripe', 'Mango Ripe', 'Mango Rotten', 'Mango Unripe',
    'Melon Overripe', 'Melon Ripe', 'Melon Rotten', 'Melon Unripe',
    'Orange Overripe', 'Orange Ripe', 'Orange Rotten', 'Orange Unripe',
    'Peach Overripe', 'Peach Ripe', 'Peach Rotten', 'Peach Unripe',
    'Pear Overripe', 'Pear Ripe', 'Pear Rotten', 'Pear Unripe'
]

@app.route('/image_upload1', methods=['GET', 'POST'])
def image_upload1():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No image part", 400
        file = request.files['image']
        if file.filename == '':
            return "No selected file", 400
        
        # Read image file bytes, convert to OpenCV image
        img_bytes = file.read()
        npimg = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Run model prediction on the image
        results = model12.predict(img, conf=0.25, iou=0.45, save=False, show=False)

        # Get image with annotated predictions (with bounding boxes & labels)
        img_with_predictions = results[0].plot()

        # Convert BGR (OpenCV) image to RGB (PIL)
        img_rgb = cv2.cvtColor(img_with_predictions, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)

        # Convert PIL image to base64 string for embedding in HTML
        buffered = io.BytesIO()
        pil_img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Render template and pass the base64 image string
        return render_template("image_upload1.html", img_data=img_str)
    
    # GET request - just render upload form
    return render_template("image_upload1.html")


if __name__ == "__main__":
    app.run(debug=True)