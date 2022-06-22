from flask import Flask, render_template, request, url_for, redirect, flash
import urllib.request
import os
from werkzeug.utils import secure_filename
import numpy as np
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from gevent.pywsgi import WSGIServer


model = load_model('6Classes_model_transfar_learning3.h5')

code = {'buildings':0, 'forest':1, 'glacier':2, 'mountain':3, 'sea':4, 'street':5}
def getcode(n) : 
    for x , y in code.items() : 
        if n == y : 
            return x 

        
app= Flask(__name__)
app.secret_key= "nooormamdouh65"
UPLOAD_FOLDER= 'static/uploads/'
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER

ALLOWED_EXTENSIONS= set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return filename.split('.')[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def homepage():
    return render_template("index3.html")

@app.route('/', methods= ['POST'])    # دي معمول كده route زي ما ال methods= ['POST']  بتاعها لازم يكون '/' وال action اللي ال template اللي في ال form يعني الفانكشن دي هتشتغل مع ال POST أنا هنا هشتغل
def upload_image():
    if 'file' not in request.files:   # مش أسم تاني 'file' اللي أسمه type من نوع input فأنت كده في المكان الغلط او الفانكشن الغلط لأن الفانكشن دي بتشتغل علي التاج 'file' بتاعه مأسمهوش name ده لو ال file اللي نوعه input لو التاج ال    
        flash('No File Part')
        return redirect(request.url)

    file= request.files['file']       # request template اللي في ال name="file" الفايل او الصوره اللي هتتبعت هتبقي اللي جت من التاج اللي ال
    if file.filename == '':           # فلو الفايل اللي اتبعت ماليهوش اسم يعني لو اسمه فاضي فمعني كده ان مافيش جاجه اتبعتت يعني مافيش صوره اتبعتت فبعد ازنك مافيش صوره اترفعت لينا وارجع تاني للصفحه الرأيسيه ارفعلي صوره تانيه
        flash('No Image Selected For Uploading')
        return redirect(request.url)  # فأرجعلي عليالصفحه الرأيسيه هاتلي صوره تانيه
    
    if file and allowed_file(file.filename):         # ALLOWED_EXTENSIONS بتوع extensions بتاع الصوره من ضمن ال extension موجود فيه صور فعلاً وكمان اسم ال file تب لو ال
      
        filename= secure_filename(file.filename)     # بتاع الصوره secure_filename يبقي اسم الصوره هو ال 
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))     # ['static/uploads/أسم الصوره'] واحفظلي الصوره في المسار ده
        flash('Image Succuessfully Uploaded & Displayed Below')            # render_template وقتها بقي قولي أن الصوره فعلاً اترفعت وسيتم عرضها في الاسفل مباشراً وفعلا هروح اعرضها ب
    

        img_array= plt.imread(file)        # read image as array
        s= 100
        img_resize= cv2.resize(img_array, (s, s))
        img_gray= cv2.cvtColor(img_resize, cv2.COLOR_RGB2GRAY) 
        image_shape = (s, s, 1)
        img_gray = img_gray.reshape(1, *image_shape)
        test_img= img_gray.repeat(3, axis=-1)                # I will convert the images channel from 1 to 3 to be suitable with the vgg16 (pre-trained model) channels because the pre-trained model take only the (RGB 3 channels images)
        # print(test_img.shape)
        test_img= test_img / 255        # to normalize image
        y_pred = model.predict(test_img)
        # labels= ['buildings', 'forest', 'glacier', 'mountain', 'sea', 'street']
        # arg_max= np.argmax(y_pred, axis=1)
        # print(arg_max)
        # pred_result= labels[arg_max[0]]
        pred_result= getcode(np.argmax(y_pred, axis=1))
    
        return render_template('index3.html', filename= filename, pred_result= pred_result)
    
    else:
        flash('The uploaded image not in this types:  ["png", "jpg", "jpeg", "gif"]')       # ALLOWED_EXTENSIONS بتوع extensions موجود فيه صور فعلاً ولكن الصور مش من ضمن ال file تب لو ال
        return redirect(request.url)        # فأرجعلي تاني علي الصفحه الرأيسيه حملي صوره تانيه تكون من الأنواع المذكورة
    

# @app.route('/display/<filename>')
@app.route('/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename= 'uploads/' + filename))


if __name__ == '__main__':
    app.run(port =5997)
