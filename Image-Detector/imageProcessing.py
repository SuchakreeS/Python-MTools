import cv2 as cv
import numpy as np
import time
import zmq
import math

MIN_MATCH_COUNT = 7
FLANN_INDEX_KDTREE = 0
SENSITIVE_LENGTH = 0.5
flannParam = dict(algorithm = FLANN_INDEX_KDTREE, tree = 5)
flann = cv.FlannBasedMatcher(flannParam, {})
detector = cv.xfeatures2d.SIFT_create()

targetImg = cv.imread("Images/nfc_50x50.jpg", 0)
trainKP, trainDecs = detector.detectAndCompute(targetImg, None)


def WristbandDetection(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    queryKP, queryDesc = detector.detectAndCompute(gray, None)
    matches = flann.knnMatch(queryDesc, trainDecs, k = 2)
    json = {"Detected": False, "Color": {}}
    goodMatch = []
    for m, n in matches:
        if(m.distance < 0.75 * n.distance):
            goodMatch.append(m)

    if(len(goodMatch) > MIN_MATCH_COUNT):
        tp = []
        qp = []
        for m in goodMatch:
            tp.append(trainKP[m.trainIdx].pt)
            qp.append(queryKP[m.queryIdx].pt)
        tp, qp = np.float32((tp, qp))
        H, status = cv.findHomography(tp, qp, cv.RANSAC, 3.0)
        h, w = targetImg.shape
        traindBorder = np.float32([[[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]])
        
        height, width, _ = img.shape
        try:
            queryBorder = cv.perspectiveTransform(traindBorder, H)

            # Find Color near Logo 
            points = queryBorder[0]
            distance = (GetDistance(points[0], points[1]) + GetDistance(points[2], points[3])) / 2
            
            left, right = GetPointsNearLogo(points)
            target1 = GetMiddlePoint(points[0], points[1])
            target2 = GetMiddlePoint(points[2], points[3])

            if CheckGoodMatch(GetDistance(target1, left), GetDistance(target2, right)):
                colorLeft = GetColorFromImage(img, left[0], left[1])
                colorRight = GetColorFromImage(img, right[0], right[1])
                json["Color"]["Left"] = colorLeft
                json["Color"]["Right"] = colorRight
                json["Detected"] = True

                # draw near logo
                cv.line(img, target1, left, (255,0,0), 2)
                cv.line(img, target2, right, (255,0,0), 2)
                cv.line(img, (0, 0), left, colorLeft, 2)
                cv.line(img, (width - 1, 0), right, colorRight, 2)
                cv.line(img, (0, height - 1), left, colorLeft, 2)
                cv.line(img, (width - 1, height - 1), right, colorRight, 2)
                # draw polyLines
                cv.polylines(img, [np.int32(queryBorder)], True, (0, 255, 0), 2)
                return json
        except:
            json["Detected"] = False
            return json
    else:
        # return "Not enough mathes - %d/%d" % (len(goodMatch), MIN_MATCH_COUNT)
        json["Detected"] = False
        return json

def GetDistance(p1, p2):
    return int(math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2))

def GetMiddlePoint(p1, p2):
    return (int(((p2[0] - p1[0]) / 2) + p1[0]), int(((p2[1] - p1[1]) / 2) + p1[1]))

def GetPointsNearLogo(polyPoints):
    middleLeft = GetMiddlePoint(polyPoints[0], polyPoints[1])
    middleRight = GetMiddlePoint(polyPoints[2], polyPoints[3])
    # Left
    p1 = [polyPoints[0][0], polyPoints[0][1], 1]
    p2 = [polyPoints[1][0], polyPoints[1][1], 1]
    cross = np.cross(p1, p2)
    left = (int(cross[0]*0.2 + middleLeft[0]), int(cross[1]*0.2 + middleLeft[1]))

    # Right
    p1 = [polyPoints[2][0], polyPoints[2][1], 1]
    p2 = [polyPoints[3][0], polyPoints[3][1], 1]
    cross = np.cross(p1, p2)
    right = (int(cross[0] * 0.2 + middleRight[0]), int(cross[1] * 0.2 + middleRight[1]))

    return left, right

def GetColorFromImage(img, x, y):
    h, w = img.shape[:2]
    if(x < w and y < h):
        red = int(img[y, x][2])
        green = int(img[y, x][1])
        blue = int(img[y, x][0])
        return (red, green, blue)

def CheckGoodMatch(left, right):
    minValue = left if left < right else right
    if abs(right - left) < minValue * SENSITIVE_LENGTH:
        return True
    else:
        return False

