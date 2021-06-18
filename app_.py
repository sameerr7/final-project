#Import necessary libraries
from flask import Flask, render_template, request
 
import numpy as np
import os

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from tensorflow.keras.applications.densenet import preprocess_input

#load model

model =load_model(r"C:\Users\maitr\Downloads\model256_densenet201.h5")
print('@@ Model loaded')
 
 
def pred_cot_dieas(cott_plant):
  test_image = load_img(cott_plant, target_size = (256, 256)) # load image 
  print("@@ Got Image for prediction")
   
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
  img_data=preprocess_input(test_image)
  result = model.predict(img_data) # predict diseased plant or not
  print('@@ Raw result = ', result)
   
  pred = np.argmax(result,axis=1) # get the index of max value
  print (pred)
 # pred =2
  #return 'Diseased Okra Leaf', 'Disease_Okra_leaf.html'
  
  if pred == 0:
     # print ("d cotton leaf")
      return "Diseased Cotton Leaf", 'disease_plant_leaf.html' # if index 0 burned leaf
  elif pred == 1:
      #print("d cotton plant")
      return 'Diseased Cotton Plant', 'disease_plant.html' # # if index 1
  elif pred == 2:
      #print("d okra leaf")
      return 'Diseased Okra Leaf', 'Disease_Okra_leaf.html'  # if index 2  fresh leaf
  elif pred== 3:
      #print ("f cotton leaf")
      return 'Fresh Cotton Leaf', 'healthy_plant.html'
  elif pred ==4:
      #print ("f cotton plant")
      return 'Fresh Cotton Plant', 'healthy_plant.html'
  elif pred==5:
      #print ("f okra leaf")    
      return 'Fresh Okra Leaf', 'Healthy_Okra_leaf.html'
  
  
 
#------------>>pred_cot_dieas<<--end
     
 
# Create flask instance
app = Flask(__name__)
 
# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')
     
  
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
         
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)
 
        print("@@ Predicting class......")
        pred, output_page = pred_cot_dieas(cott_plant=file_path)
               
        return render_template(output_page, pred_output = pred, user_image = file_path)
     
# For local system & cloud
if __name__ == "__main__":
    app.run(threaded=False) 
