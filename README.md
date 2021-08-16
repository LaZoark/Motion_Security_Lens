# Motion_Security_Lens
Detecting and record the motion via (multiple) streaming sourse by openCV4.

> | :warning: **The project is still under development.**|
> |---|

It was obviously that I got tons of stuff to improve. and I made this project just for fun! (also for the sake of security of my lab)


## Features

1. **Motion Detector** : It will film automatically whenever the moving event occur. 
* NOTICE that it only capture the frame around the movement.
* This might lead to *JUMPING FRAME*.
2. **Adjustable monitor** : Adjust the size of the window with your mouse. Whenever you want to recover to the default window size, just press `keyboard "r"`.
3. **Quick Save** : `Mouse Left click` will save the image.
4. **Quick Adjust** : `Mouse Wheel` can increase/decrease the value (motion threshold) on the frame.
5. **Stay An Top** : `Mouse Left click + Ctrl` will keep the window on top. (press 'X' to reset the window.)
6. **Clip that now** : `keyboard "s"` can save the clip right away. (the target need to be focused.)
7. **Multiprocessing** : not really sure whether this is an advantage or not :confused:.   Maybe someone can give me some advice, will be appreciated a lot!

## Any Problem?
- How to end the program?  
Same as usual, simply press `'q'` or `'Esc'` to stop the process.  
(If there are more then one process, please quit separately.)   

- How to change the streaming sourse?  
Just change the content of `url_list` to whatever you want.   
It is able to read *webcam* by setting the index of them.   
(i.g. `cap = cv2.VideoCapture(0)`. `0` stand for your first webcam)  
Get more info about the [valid type](https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html#ga288b8b3da0892bd651fce07b3bbd3a56) on official website.

- Still somehow not gonna work?   
Feel free to Issue the problem or fork/pull the project!

## TODO
- [X] Auto reconnect to the video source
- [ ] Integral the frames as a single monitor.
- [ ] Find out all stream source automatically.
- [ ] ....No inspiration yet
