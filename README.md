# LabelUs
my customized label tool for my research

```python main.py``` to start the app.

### Top Dependencies
```
PyQt5==5.15.3, opencv-python==4.1.2.30, numpy==1.21.4, pycocotools==2.0.0.1
```
Note that the pycocotools installation process is a little bit complicated.
I'll demonstrate the process for Windows OS

```pip install pycocotools-windows```  
or  
Visit the https://pypi.tuna.tsinghua.edu.cn/simple/pycocotools-windows/ and install the appropriate wheel file.  
Go to download file folder and pip install wheel file name.  

I also had exported the requirements.txt which you can refer to.

### Notice
![image](https://user-images.githubusercontent.com/67520151/231901292-d254b7b4-d322-4b2b-91f4-93439d548c54.png)


There's may have the area which is not closed (first image).
Since algo behind is computing the convex hull of multiple area, thus we can select the most of the interested area (second image) to approximately achieve the result (third image).


### Mouse Function
* Wheel for zoom-in / out image
* Left-click and not released can drag the image
* Right-click to draw temp mask

### Hot Key
* <kbd>A</kbd> for undo
* <kbd>S</kbd> for turning temp mask to final mask
* <kbd>Ctrl</kbd> + <kbd>S</kbd> for exporting json file
* <kbd>Ctrl</kbd> + <kbd>Z</kbd> is same as A

### Basic Usage Flow
1. open image through Open Image button or open a floder through Open Folder button and double-click the filename in the lower right corner.
2. adjust image through wheel and left-click, right-click the area you want to fill, the light yellow represent the area you want.
3. the light yellow mask is tentative, press <kbd>S</kbd> to accept the final mask.
4. after finish, press <kbd>Ctrl</kbd> + <kbd>S</kbd> or Save button in the left to store json file.

### Advanced Feature
1. hover mouse with right-click can also draw temp mask
