from tkinter import *
import os
from PIL import Image, ImageTk
from tkinter import filedialog 
from PIL import Image, ImageDraw, ImageFont
import boto3
import base64
import json
import os



client=boto3.client('rekognition')

client = boto3.client("rekognition",aws_access_key_id='ASIAZX6VTHS6I5BBZJ4X',
aws_secret_access_key='f9BzD+dVWPEp09syPkiqvH1TeJK7ZmhOw5Fnpsvc',aws_session_token='FwoGZXIvYXdzEGwaDEx6fT5eKva/el+1SSLbAVNts85EEyTpVwePcKwFBpi07MClJpLXVk/hyKwrae89Hyfs6r2sekoGKa1Jissrtpkc1qSRmizPdvw89SemTaRtem34UvLdpmY0U6HipvATFNkbqGXjumOJ/JwpR2/5tSH+fsU0Nnd8KJJ2hocAmyXyRhYLULI0OGcnEnuswpJN+Vwi84Nhp/gm1Uxol0C05Xynb6BXK+VhyTXP6APz6Iu7AVg9wSUVr8V5oYnLWyGywledsEUPafwX+UxC//e9/UlfBmDFOXSxOBLv0z9Cmy4lGWHhqO5pBe5lByiQr9r7BTItX/751jBQqCLO2cNVqE6ivFIus9koWTV49Q23DyeewlmID7JJyGM9IyToUx5Q')


window = Tk()
window.title("AWS Analytics")
window.geometry("900x640") #Width x Height

head_label = Label(text = "AWS Analytics")
head_label.config(font=("Courier", 44))
head_label.grid(row= 1, column=1, columnspan=2)


filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File", filetypes = (("Image Files","*.jpg*"),("all files","*.*")))    

file = open(filename, 'rb').read()


try:
	file = open(filename, 'rb').read()


	response = client.detect_faces(
    Image={'Bytes': file
    },
    Attributes=['ALL']
	)
	for face in response['FaceDetails']:
		Gender = str(face['Gender']['Value'])
		gender = Label(window, text = "Gender = " + Gender, fg="Green", font=("Helvetica", 18))
		gender.grid(row = 2, column= 2)

		print('Gender : '+ Gender)
		if Gender == 'Male':
			pronoun = 'He'
			Mustache = str(face['Mustache']['Value'])
			if Mustache == 'True':
				mustache = Label(window, text = "Has Mustache", fg="Green", font=("Helvetica", 18))
				mustache.grid(row = 3, column= 2)
				print('Has Mustache')
			else:
				mustache = Label(window, text = "Does not have Mustache", fg="Green", font=("Helvetica", 18))
				mustache.grid(row = 3, column= 2)
				print('Does not have Mustache')
		else:
			pronoun = 'She'
		Age = Label(window, text = 'The Detected face is between age ' + str(face['AgeRange']['Low']) + ' and ' + str(face['AgeRange']['High']), fg="Green", font=("Helvetica", 18))
		Age.grid(row = 4, column= 2)
		print('The Detected face is between ' + str(face['AgeRange']['Low']) + ' and ' + str(face['AgeRange']['High']))
		
		face_emotion_confidence = 0
		face_emotion = 'None'
		for emotion in face.get('Emotions'):
			if emotion.get('Confidence') >= face_emotion_confidence:
				face_emotion_confidence = emotion['Confidence']
				face_emotion = emotion.get('Type')
		Smile = str(face['Smile']['Value'])
		if Smile == 'True':
			exp = 'Smiling'
		else:
			exp = "not Smiling"

		mustache = Label(window, text = pronoun + ' is ' + face_emotion + ' and is ' + exp, fg="Green", font=("Helvetica", 18))
		mustache.grid(row = 5, column= 2)
		print(pronoun + ' is ' + face_emotion + ' and is ' + exp)

		Sunglass = str(face['Sunglasses']['Value'])
		if Sunglass == 'True':
			mustache = Label(window, text = pronoun + " is wearing Sunglass", fg="Green", font=("Helvetica", 18))
			mustache.grid(row = 6, column= 2)
			print(pronoun + " is wearing Sunglass" )
		else:
			mustache = Label(window, text = pronoun + " is not wearing Sunglass", fg="Green", font=("Helvetica", 18))
			mustache.grid(row = 6, column= 2)
			print(pronoun + " is not wearing Sunglass")


	img = Image.open(filename)
	w, h = img.size
	width = 400
	height = h/w * 400
	height = int(height)
	img_file = img.resize((width,height), Image.ANTIALIAS)
	img_file = ImageTk.PhotoImage(img_file)
	orig_img = Label(window, text = "Exit", image = img_file)
	orig_img.grid(row = 2, column= 1, rowspan = 9)


	orig_text = Label(window, text = "Original Image", fg="Red", font=("Helvetica", 18))
	orig_text.grid(row = 12, column= 1)

except:
	error = Label(window, text = "Image Doesnot Contains Any Faces. Retry:", fg="Red", font=("Helvetica", 23))
	error.grid(row = 2, column= 1)

	def try_again():
		os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

	try_btn = Button(window, text = "Try Again", fg="Green", font=("Helvetica", 16), command= try_again)
	try_btn.grid(row = 3, column= 1)




window.mainloop()

