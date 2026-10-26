import cv2
import numpy
import os
import sys


def loadimage(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    return img


def hsvfilter(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    white = cv2.inRange(hsv, (0, 0, 200), (179, 40, 255))
    yellow = cv2.inRange(hsv, (15, 80, 100), (35, 255, 255))
    return cv2.bitwise_or(white, yellow)


def blur(mask):
    return cv2.GaussianBlur(mask, (5, 5), 0)


def detectedges(blurred):
    return cv2.Canny(blurred, 50, 150)


def roi(edge):
    h,w= edge.shape
    roimask=numpy.zeros_like(edge)
    
    trapezoid=numpy.array([[ (0,h), # bottom-left
                            (w, h), # bottom-right
        (int(0.55 * w), int(0.6 * h)),  # top-right
        (int(0.45 * w), int(0.6 * h)),  # top-left
    ]])
    
    cv2.fillPoly(roimask, trapezoid, 255)
    roiresult=cv2.bitwise_or(edge,roimask)
    return roiresult

def trapezoid(shape):
    h, w = shape[:2]
    return numpy.array([[
        (0, h),  # bottom-left
        (w, h),  # bottom-right
        (int(0.55 * w), int(0.6 * h)),  # top-right
        (int(0.45 * w), int(0.6 * h)),  # top-left
         ]])

def debugroad(img):
    """Original image with the green trapezoid drawn on it."""
    debug = img.copy()
    cv2.polylines(debug,trapezoid(img.shape), True, (0, 255, 0), 3)
    return debug

def highlight(img, mask, color=(0, 0, 255), alpha=0.6):
    overlay = img.copy()
    overlay[mask > 0] = color
    return cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)


def process(path, dir="output"):
    name = os.path.splitext(os.path.basename(path))[0]

    img = loadimage(path)
    mask = hsvfilter(img)
    blurred = blur(mask)
    edges = detectedges(blurred)
    roiresult = roi(edges)
    highlighted = highlight(img, detectedges(mask))
    debug = debugroad(img)

    os.makedirs(dir, exist_ok=True)
    cv2.imwrite(os.path.join(dir, f"{name}_img.jpg"), img)
    cv2.imwrite(os.path.join(dir, f"{name}_mask.jpg"), mask)
    cv2.imwrite(os.path.join(dir, f"{name}_blur.jpg"), blurred)
    cv2.imwrite(os.path.join(dir, f"{name}_edge.jpg"), edges)
    cv2.imwrite(os.path.join(dir, f"{name}_roiresult.jpg"), roiresult)
    cv2.imwrite(os.path.join(dir, f"{name}_debug.jpg"), debug)
    cv2.imwrite(os.path.join(dir, f"{name}_highlighted.jpg"), highlighted)

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # user gave image path(s) when running the script
        for path in sys.argv[1:]:
            process(path)
            print("Processed", path)
    else:
        # no path given: ask for one
        path = input("Enter the path to a road image: ").strip().strip('"')
        process(path)
        print("Processed", path)
