import imagiz
import cv2
import multiprocessing
import os
import signal

def get_webcam(port,sv_op):
  #(' -- Activated -- ')
  
  server=imagiz.TCP_Server(port)
  server.start()
  
  
  if sv_op:
      vid_cod = cv2.VideoWriter_fourcc(*'XVID')
      output = cv2.VideoWriter("E:/FYP_web/Employee/Server/Images/Monitoring.avi", vid_cod, 10.0, (640,480))

  while True:
      message=server.receive()
      message = cv2.imdecode(message.image,1)
      # frame=cv2.imdecode(message.image,1)

      width = int(message.shape[1] / 0.6)
      height = int(message.shape[0] / 0.6)
      dim = (width, height)
        
      # resize image
      resized = cv2.resize(message, dim, interpolation = cv2.INTER_AREA) 
      cv2.imshow("WebMonitoring Video",resized)

      if sv_op:
        output.write(resized)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  try:
    output.release()
  except:
    pass      
  cv2.destroyAllWindows()
  current_id = multiprocessing.current_process().pid
  #(current_id)
  #('Killed_Process')
  os.kill(current_id,signal.SIGTERM)