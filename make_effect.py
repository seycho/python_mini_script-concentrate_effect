from numpy import newaxis, arange, uint8, int16, sqrt

def RadialBlur(img, xCenterRatio=0.5, yCenterRatio=0.5, intensity=100, seperNum=10):

    shape = img.shape
    if len(img.shape) == 3:
        yShape, xShape, _ = shape
    else:
        yShape, xShape = shape

    xRange = arange(xShape) 
    yRange = arange(yShape)[:,newaxis]

    yCenter = (yShape - 1) * yCenterRatio
    xCenter = (xShape - 1) * xCenterRatio

    r = sqrt((xRange - xCenter)**2 + (yRange - yCenter)**2)
    rNormal = r / np.max(r)

    cos = (xRange - xCenter) / r
    sin = (yRange - yCenter) / r

    intensityArange = arange(0, 1, 1 / (seperNum))
    intensityArange = (np.sqrt(intensityArange) * intensity).astype(int16)

    rEffect = r[:,:,newaxis] - intensityArange
    rEffect[rEffect < 0] = 0

    xEffect = (rEffect * cos[:,:,newaxis] + xCenter).astype(int16)
    yEffect = (rEffect * sin[:,:,newaxis] + yCenter).astype(int16)

    xEffect[xEffect > xShape - 1] = xShape - 1
    xEffect[xEffect < 0] = 0
    yEffect[yEffect < 0] = 0
    yEffect[yEffect > yShape -1] = yShape -1

    step = (rNormal**0.1)[:,:,newaxis] * ((seperNum - np.arange(seperNum)) / seperNum)[::-1]

    imgBlur = ((img[yEffect,xEffect]*step).sum(2) / seperNum).astype(uint8)

    return imgBlur

import numpy as np
import argparse, cv2


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=str, help="variable saved csv file")
    args = parser.parse_args()

    csvPath = args.csv

    inputDic = {}
    for inputValue in np.loadtxt(csvPath, delimiter=',', dtype=str):
        inputDic[inputValue[0]] = inputValue[1]

    pathInput = inputDic["pathInput"]
    pathOutput = inputDic["pathOutput"]
    xLocationRatio = float(inputDic["xLocationRatio"])
    yLocationRatio = 1 - float(inputDic["yLocationRatio"])
    rIntensity = int(inputDic["rIntensity"])
    noiseDivide = int(inputDic["noiseDivide"])

    img = cv2.imread(pathInput, 0)

    yShape, xShape = img.shape

    noise = np.random.rand(yShape // noiseDivide, xShape // noiseDivide)

    noise = cv2.resize(noise, dsize=(xShape, yShape))
    noise = cv2.GaussianBlur(noise, (21, 21), 15)

    imgEdge = cv2.Laplacian(img, cv2.CV_8U, ksize=3)
    imgEdge[imgEdge > 64] = 255

    imgEdgeBlur = RadialBlur(imgEdge * noise, xCenterRatio=xLocationRatio, yCenterRatio=yLocationRatio, intensity=rIntensity, seperNum=noiseDivide)
    threshold = np.mean(imgEdgeBlur)
    imgEdgeBlur[imgEdgeBlur > threshold] = 255
    imgEdgeBlur[imgEdgeBlur < threshold] = 0

    cv2.imwrite(pathOutput, imgEdgeBlur)

    return None

if __name__ == "__main__":
    main()