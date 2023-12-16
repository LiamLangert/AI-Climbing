from ultralytics import YOLO
import cv2
from ultralytics import YOLO
import pathlib
import platform
from roboflow import Roboflow
from PIL import Image

model = YOLO('yolov8n-cls.pt')
results = model.train(data='../Difficulty Classifier Data', epochs=100, imgsz=64)



plt = platform.system()
# if plt != 'Windows': pathlib.WindowsPath = pathlib.PosixPath
# Load a pretrained YOLOv8n model
model = YOLO('../runs/classify/train4/weights/best.pt')
# Gets the image at the specified path as a numpy array
def getImage(path):
    img = cv2.imread(path)
    return img

# Displays the results of model(image)
def getResults(results):
    for r in results:
        guesses = r.probs.data
        if guesses[0] == max(guesses):
            return "bolt"
        if guesses[9] == max(guesses):
            return "tag"
        aggregate = (8 * guesses[2] + 5 * guesses[3] + 4 * guesses[4] + 9 * guesses[5] + 
                     1 * guesses[6] + 7 * guesses[7] + 6 * guesses[8] + 10 * guesses[10] + 3 * guesses[11] + 2 * guesses[12]) 
        return float(aggregate)
def getConfidence(results):
    for r in results:
        guesses = r.probs.data
        squares = 0
        for guess in guesses:
            squares += guess ** 2
    return float(squares)

def saveImage(image):
    im = Image.fromarray(image[..., ::-1])
    im.save('../images/results.jpg')
    
def rotateImage(mat, angle):
    height, width = mat.shape[:2] # image shape has 3 dimensions
    image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
    
    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)
    
    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0]) 
    abs_sin = abs(rotation_mat[0,1])
    
    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)
    
    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]
    
    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat

def getIdealRotation(image):
    best = (0, 0)
    for i in range(8):
        rot = rotateImage(image, i * 45)
        res = model.predict(rot)
        conf = getConfidence(res)
        if conf > best[1]:
            best = (i * 45, conf)
    return best[0]


img = getImage("../images/redtag.png")
print(getResults(model.predict(img)))
print(getIdealRotation(img))
