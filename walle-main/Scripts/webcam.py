#Importer les librairies necessaires
from flask import Flask, render_template, Response
import cv2

#Initialisation de l'application Flask
app = Flask(__name__)

#Associer la camera de l'index 0 a l'attribut camera
camera = cv2.VideoCapture(0)

def gen_frames():
    #Si la camera ne peut pas etre lus, on sort de la fonction
    while True:
        success, frame = camera.read()  #Lis la camera
        if not success:
            break
        else:
            frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_LINEAR)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                   
#Accede le template du fichier index.html                   
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
