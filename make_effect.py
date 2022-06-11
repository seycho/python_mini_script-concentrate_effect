from ._utils import RadialBlur

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