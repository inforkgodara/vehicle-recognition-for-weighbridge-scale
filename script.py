import cv2
import time
from twilio.rest import Client
from datetime import datetime
import os

account_sid = 'YOUR_TWILIO_SID'
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
client = Client(account_sid, auth_token)

car_cascade = cv2.CascadeClassifier("haar-cascade-for-truck.xml")

cap = cv2.VideoCapture(r'Demo-1.mp4')
 
while True:
    respose, color_img = cap.read()
    print(color_img)
    if respose == False:
        break
    gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    faces = car_cascade.detectMultiScale(gray_img, 1.1, 2)
    i=0
    for (x, y, w, h) in faces:
        if i%2==0:
            cv2.rectangle(color_img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            i +=1
            print('No, Could not find.')
        else:
            cv2.rectangle(color_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            i +=1
            print('Yes, Vehicle found and sent image on whatsapp.');

            now = datetime.now()
            timestamp = datetime.timestamp(now)
            directory = str(timestamp)
            parent_dir = "C:/inetpub/wwwroot/temp"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            cv2.imwrite(parent_dir +'/' + str(timestamp) + '/image.png', color_img)

            message = client.messages.create(
                from_='whatsapp:+TWILIO_PHONE_NUMBER',
                body=str(datetime.now()),
                to='whatsapp:TO_WHOME_YOU_NEED_TO_SEND_IMAGE_PHONE_NUMBER',
                media_url='NGROK_URL' + str(timestamp) + '/image.png'
            )
            time.sleep(10000);
            exit(0);
        cv2.imshow('Image', color_img)
             
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()