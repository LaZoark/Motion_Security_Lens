import cv2, pandas
import numpy as np
from datetime import datetime

# List when any moving object appear
motion_list = [None, None]
# Time of movement
time = []
# Initializing DataFrame, one column is start 
# time and other column is end time
df = pandas.DataFrame(columns=["Start", "End"])

DETECT_AREA = 2400
DAMPING_RATE = 0.008
cap = cv2.VideoCapture(1)
# cap = cv2.VideoCapture("http://192.168.1.8:81")
win_name = "frame_"

# 取得影像的尺寸大小 and fps
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) + 5

# 初始化平均影像
ret, frame = cap.read()
avg = cv2.blur(frame, (4, 4))
avg_float = np.float32(avg)
output_name = datetime.now().strftime("%Y%m%d_%H%M%S")
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用 XVID 編碼
# 建立 VideoWriter 物件，輸出影片至 output.avi
out = cv2.VideoWriter("video\\" + output_name + ".avi", fourcc, fps, (width, height))
print("FPS: ", fps)
# on_top = True
i = 0


def on_mouse_event(event, x, y, flags, param):
    global DAMPING_RATE, output_name, i
    # print("EVENT:", event, '\n', flags)
    if event == 10:  # mousewheel event code is 10
        if flags > 0:  # scroll up
            DAMPING_RATE += 0.0005
        else:  # scroll down
            DAMPING_RATE -= 0.0005
    if event == cv2.EVENT_LBUTTONDOWN:  # 1
        if flags == cv2.EVENT_FLAG_LBUTTON:
            later_st = datetime.now().strftime("%Y%m%d_%H%M%S")
            if output_name == later_st:
                i += 1
                cv2.imwrite("img\\" + later_st + '_' + str(i) + ".jpg", frame)
                print("saved image : ", later_st + '_' + str(i) + ".jpg")
            else:
                i = 0
                cv2.imwrite("img\\" + later_st + ".jpg", frame)
                print("saved image : ", later_st + ".jpg")
            output_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    elif event == cv2.EVENT_LBUTTONDOWN and flags == cv2.EVENT_FLAG_CTRLKEY:
        cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)


while cap.isOpened():
    # 讀取一幅影格
    ret, frame = cap.read()
    # 若讀取至影片結尾，則跳出
    if ret == False:
        break
    # Initializing motion = 0(no motion)
    motion = 0
    # 模糊處理
    blur = cv2.blur(frame, (4, 4))

    # 計算目前影格與平均影像的差異值
    diff = cv2.absdiff(avg, blur)

    # 將圖片轉為灰階
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # 篩選出變動程度大於門檻值的區域
    ret, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

    # 使用型態轉換函數去除雜訊
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # 產生等高線
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
        # 忽略太小的區域
        if cv2.contourArea(c) < DETECT_AREA:
            continue
        motion = 1
        # 偵測到物體，可以自己加上處理的程式碼在這裡...
        out.write(frame)

        # 計算等高線的外框範圍
        (x, y, w, h) = cv2.boundingRect(c)

        # 畫出外框
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

    # 畫出等高線（除錯用）
    cv2.drawContours(frame, cnts, -1, (0, 255, 255), 1)

    # 顯示偵測結果影像
    cv2.setMouseCallback(win_name, on_mouse_event)
    cv2.imshow(win_name, frame)
    # 錄影整段
    # out.write(frame)
    key = cv2.waitKey(1) & 0xFF

    if key == 27 or key == 113:
        # if something is movingthen it append the end time of movement
        if motion == 1:
            time.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4])
        break
    elif key == 43:
        DETECT_AREA += 100
    elif key == 45:
        DETECT_AREA -= 100
    # elif key == ord('t'):   # stay on top
    #         if on_top:
    #             cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)
    #         on_top = not on_top
    elif key == 115 or key == 83:  # press 's' or 'S' to save the video
        out.release()
        output_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = cv2.VideoWriter("video\\" + output_name + ".avi", fourcc, fps, (width, height))

    # 更新平均影像
    cv2.accumulateWeighted(blur, avg_float, DAMPING_RATE)
    avg = cv2.convertScaleAbs(avg_float)

# Appending time of motion in DataFrame
for i in range(0, len(time), 2):
    df = df.append({"Start": time[i], "End": time[i + 1]}, ignore_index=True)

# Creating a CSV file in which time of movements will be saved
df.to_csv("video\\" + output_name + ".csv")
print("log has been saved.")

out.release()
cap.release()
cv2.destroyAllWindows()
