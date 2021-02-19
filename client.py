import imagiz
import cv2
import os
import multiprocessing
import signal
import mss
import time
import numpy

def send_webcam(port):
    vid=cv2.VideoCapture(0)
    client=imagiz.TCP_Client(server_port=port,client_name="cc1",server_ip='192.168.1.17') # IP of your server
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    # t_end = time.time() + int(time_)
    frame_rate = 10
    prev = 0
    while True:
        time_elapsed = time.time() - prev
        r,frame=vid.read()
        print('Original Dimension', frame.shape)

        if time_elapsed > 1./frame_rate:
            prev = time.time()
            scale_percent = 60 # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            
            # resize image
            resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

            if r:
                try:
                    r,image=cv2.imencode('.jpg',resized, encode_param)
                    response=client.send(image)
                    print(response)
                except:
                    break

    vid.release()
    cv2.destroyAllWindows()
    current_id = multiprocessing.current_process().pid
    print('Webcam Process:',current_id)
    os.kill(current_id,signal.SIGTERM)
    print('Killed_Process')


def client_screenshare(port):
    sct =mss.mss()
    monitor = sct.monitors[1]  
    client=imagiz.TCP_Client(server_port=port,client_name="cc1",server_ip='192.168.1.17') # Ip of your server
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    frame_rate = 10
    prev = 0

    while True:
        try:
            time_elapsed = time.time() - prev

            if time_elapsed > 1./frame_rate:
                prev = time.time()
                pic =sct.grab(monitor)
                img = numpy.array(pic)
                scale_percent = 60 # percent of original size
                width = int(img.shape[1] * scale_percent / 100)
                height = int(img.shape[0] * scale_percent / 100)
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                _,image=cv2.imencode('.jpg',resized, encode_param)
                response = client.send(image)
                print(response)
        except:
            break

    current_id = multiprocessing.current_process().pid
    print(current_id)
    os.kill(current_id,signal.SIGTERM)
    print('Killed_Process')
