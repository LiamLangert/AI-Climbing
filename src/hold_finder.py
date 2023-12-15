import pathlib
import platform
from PIL import Image
import numpy as np
from ultralytics import YOLO
from ultralytics.engine.results import Boxes
import cv2
import os

plt = platform.system()
if plt != 'Windows': pathlib.WindowsPath = pathlib.PosixPath

# Load a pretrained YOLOv8n model
model = YOLO('../runs/detect/yolov8n_v8_50e22/weights/best.pt')

def predictHolds(path):
    return model.predict(path)

# Gets the image at the specified path as a numpy array
def getImage(path):
    img = cv2.imread(path)
    return img

# Displays the results of model(image)
def dispResults(results):
    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        im.show()  # show image
        im.save('results.jpg')  # save image

# Removes all bounding boxes in the results of model(image)
# that may be cut off by the sides
def removeEdges(results):
    for r in results:
        boxes_coords = np.array(r.boxes.xyxy)
        boxes_last = np.array(r.boxes.data[:, 4:])
        i=0
        while i < (len(boxes_coords)):
            x1, y1, x2, y2 = boxes_coords[i]
            imh = r.boxes.orig_shape[0]
            imw = r.boxes.orig_shape[1]
            if (x1 < imw / 100.0) or (y1 < imh / 100) or (x2 > imw - imw / 100.0) or (y2 > imh - imh / 100.0):
                boxes_coords = np.delete(boxes_coords, i, 0)
                boxes_last = np.delete(boxes_last, i, 0)
                i -= 1
            i += 1
        new_data = np.concatenate((boxes_coords, boxes_last), axis=1)
        newboxes = Boxes(new_data, r.boxes.orig_shape)
        r.boxes = newboxes
    return results


def getBoxAsImage(results, index):
    r = results[0]
    x1, y1, x2, y2 = np.array(r.boxes.xyxy)[index]
    im_array = np.array(r.orig_img)
    cropped = im_array[round(y1):round(y2), round(x1):round(x2)]
    return cropped
        
def individualHolds(model, img_path, hold_path):
    try:
        os.rmdir(hold_path)
    except:
        pass
    os.mkdir(hold_path)
    for img_name in os.listdir(img_path):   
        img = getImage(f"{img_path}/{img_name}")
        results = model(img)
        results = removeEdges(results)
        r = results[0]
        for i in range(len(r.boxes)):
            im_array = getBoxAsImage(results, i)
            im = Image.fromarray(im_array)
            im.save(f"{hold_path}/{str(i) + '-'}{img_name}")
def colorDifference (color1, color2):
    c1hsv = cv2.cvtColor(color1, cv2.COLOR_RGB2HSV)
    c2hsv = cv2.cvtColor(color1, cv2.COLOR_RGB2HSV)
    return abs(c1hsv[0] - c2hsv[0])


def getDomColor(img):
    #Use K-means clustering to find the 2 dominant colors
    #https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
    
    average = img.mean(axis=0).mean(axis=0)
    pixels = np.float32(img.reshape(-1, 3))
    n_colors = 2
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    hsv_palette = []
    for i in range(len(palette)):
        hsv_palette.append(cv2.cvtColor(np.array([[palette[i]]]), cv2.COLOR_BGR2HSV)[0][0])
        hsv_palette[i] = np.array([hsv_palette[i][0], hsv_palette[i][1] * 100, hsv_palette[i][2] * 100 / 255.0])
    #compares the saturations of the two colors (to filter for the wall)
    sats = np.array([col[1] for col in hsv_palette])
    return(hsv_palette[np.argmax(sats)])
def closeEnough(color2, color1, close):
    if color1[1] == 0:
        if color2[1] < 20:
            if color2[2] < 50 and color1[2] < 50:
                return True
            elif color2[2] > 50 and color1[2] > 50:
                return True
            else:
                return False
        return False
    else:
        if color2[1] >= color1[1] and color2[2] >= color1[2]:
            diff = abs(color1[0] - color2[0])
            colcheck = min(diff, 360 - diff) < close
            return colcheck
    return False
def getHoldsNearColor(results, color, close):
    for r in results:
        boxes_data = np.array(r.boxes.data)
        new_data = np.array([])
        for i in range(len(boxes_data)):
            img = getBoxAsImage(results, i)
            dom = getDomColor(img)
            if closeEnough(dom, color, close): 
                if len(new_data) == 0:
                    new_data = np.array([boxes_data[i]])
                else:
                    new_data = np.append(new_data, [boxes_data[i]], axis=0)
        newboxes = Boxes(new_data, r.boxes.orig_shape)
        r.boxes = newboxes
    return results