import cv2, pandas
import numpy as np
from datetime import datetime
import multiprocessing as mp

# Manager to create shared object.
# manager = mp.Manager()  # could shared across computers
i = mp.Value('i', 0)
# on_top = mp.Value('i', True)
# your ESP32-CAM's ip
url_list=[
    "http://192.168.1.8:81",
    "http://192.168.1.6:81",
    "http://192.168.1.17:81"]

def cctv(url_):
    # global DAMPING_RATE, output_name
    global DAMPING_RATE, DETECT_AREA, output_name, i
    # List when any moving object appear
    motion_list = [ None, None ]
    # Time of movement
    time = []
    # Initializing DataFrame, one column is start 
    # time and other column is end time
    df = pandas.DataFrame(columns = ["Start", "End"])
    
    DETECT_AREA = 2400
    DAMPING_RATE = 0.01
    
    cap = cv2.VideoCapture(url_)
    win_name = "Streaming_" + url_[7:]
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) + 5
    
    # init the avg_background
    ret, frame = cap.read()
    avg = cv2.blur(frame, (4, 4))
    avg_float = np.float32(avg)
    output_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("video\\" + url_[17:-3] + "_" + output_name + ".avi", fourcc, fps, (width, height))
    print(url_ + "_FPS: ", fps)

    def on_mouse_event(event, x, y, flags, param):
        global DAMPING_RATE, DETECT_AREA, output_name, i
        # if not event == cv2.EVENT_MOUSEMOVE:
        #     print("EVENT:", event, '\n', flags)
        if event == cv2.EVENT_RBUTTONDOWN and flags == 9:
            print("# ctrl+Rm")
        if event == 10:     # mousewheel event code is 10
            if flags>0 and flags%120 == 8:   # scroll up+ctrl
                DETECT_AREA += 100
            elif flags<0 and flags%120 == 8 and DAMPING_RATE > 100: # scroll down+ctrl
                DETECT_AREA -= 100
            elif flags > 0:   # scroll up
                DAMPING_RATE += 0.0005
            elif flags < 0 and DAMPING_RATE > 0.0005:           # scroll down
                DAMPING_RATE -= 0.0005
        if event == cv2.EVENT_LBUTTONDOWN and flags == 9:  # ctrl+Lm to keep on top
            cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)
            print("ON TOP!")
        # elif flags == cv2.EVENT_FLAG_LBUTTON:   # Lm to save img
        #     later_st = datetime.now().strftime("%Y%m%d_%H%M%S")
        #     if output_name == later_st:
        #         i += 1
        #         cv2.imwrite("img\\" + later_st + '_' + str(i) + ".jpg", frame)
        #         print("saved image : ", later_st + '_' + str(i) + ".jpg")
        #     else:
        #         i = 0
        #         cv2.imwrite("img\\" + later_st + ".jpg", frame)
        #         print("saved image : ", later_st + ".jpg")
        #     output_name = datetime.now().strftime("%Y%m%d_%H%M%S")
            
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            break
        # Initializing motion = 0(no motion)
        motion = 0
        blur = cv2.blur(frame, (4, 4))
        diff = cv2.absdiff(avg, blur)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    
        # Generate contour lines
        cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detect_area = "DETECT_AREA: {}".format(DETECT_AREA)
        damping_rate = "DAMPING_RATE: {:.4f}".format(DAMPING_RATE)
        cv2.putText(frame, detect_area, (9, 19), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (150, 0, 0), 1)
        cv2.putText(frame, detect_area, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 255), 1)
        cv2.putText(frame, damping_rate, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (150, 0, 0), 1)
        cv2.putText(frame, damping_rate, (9, 39), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 0, 255), 1)
        cv2.putText(frame, datetime.now().strftime("%Y%m%d %A %p%I:%M:%S"),
                    (8, frame.shape[0] - 8), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (200, 50, 0), 2)
        cv2.putText(frame, datetime.now().strftime("%Y%m%d %A %p%I:%M:%S"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (50, 200, 255), 2)
    
        for c in cnts:
            if cv2.contourArea(c) < DETECT_AREA:
                continue
            motion = 1
            
            out.write(frame)
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Appending status of motion
        motion_list.append(motion)
        motion_list = motion_list[-2:]
      
        # Appending Start time of motion
        if motion_list[-1] == 1 and motion_list[-2] == 0:
            time.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4])
      
        # Appending End time of motion
        if motion_list[-1] == 0 and motion_list[-2] == 1:
            time.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4])
        
        # Draw the contour line(for DEBUG)
        cv2.drawContours(frame, cnts, -1, (0, 255, 255), 1)

        cv2.setMouseCallback(win_name, on_mouse_event)
        cv2.imshow(win_name, frame)
        
        key = cv2.waitKey(1) & 0xFF
    
        if key == 27 or key == 113:
             # if something is movingthen it append the end time of movement
            if motion == 1:
                time.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4])
            break
        # elif key == 43:
        #     DETECT_AREA += 100
        # elif key == 45:
        #     DETECT_AREA -= 100
        # elif key == ord('t'):   # stay on top
        #         if on_top:
        #             cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)
        #         on_top = not on_top
        elif key == 115 or key == 83:   # press 's' or 'S' to save the video
            out.release()
            output_name = datetime.now().strftime("%Y%m%d_%H%M%S")
            out = cv2.VideoWriter("video\\" + url_[17:-3] + "_" + output_name + ".avi", fourcc, fps, (width, height))
            
    
        # update the avg background
        cv2.accumulateWeighted(blur, avg_float, DAMPING_RATE)
        avg = cv2.convertScaleAbs(avg_float)
        
    # Appending time of motion in DataFrame
    for i in range(0, len(time), 2):
        df = df.append({"Start":time[i], "End":time[i + 1]}, ignore_index = True)
      
    # Creating a CSV file in which time of movements will be saved
    df.to_csv("video\\" + url_[17:-3] + "_" + output_name + ".csv")
    print("log has been saved.")

    out.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    p_list = []
    for j in url_list:
        p_list.append(mp.Process(target=cctv, args=(j,)))
        
    for p in p_list:
        p.start()
        
    # Main Process 繼續執行自己的工作
    proc = mp.current_process()
    print(proc.name, proc.pid)
    
    # 等待所有Process執行結束
    for p in p_list:
        p.join()
    
    print("End saftly.")