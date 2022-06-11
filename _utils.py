from numpy import newaxis, arange, uint8, int16, sqrt, max


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
    rNormal = r / max(r)

    cos = (xRange - xCenter) / r
    sin = (yRange - yCenter) / r

    intensityArange = arange(0, 1, 1 / (seperNum))
    intensityArange = (sqrt(intensityArange) * intensity).astype(int16)

    rEffect = r[:,:,newaxis] - intensityArange
    rEffect[rEffect < 0] = 0

    xEffect = (rEffect * cos[:,:,newaxis] + xCenter).astype(int16)
    yEffect = (rEffect * sin[:,:,newaxis] + yCenter).astype(int16)

    xEffect[xEffect > xShape - 1] = xShape - 1
    xEffect[xEffect < 0] = 0
    yEffect[yEffect < 0] = 0
    yEffect[yEffect > yShape -1] = yShape -1

    step = (rNormal**0.1)[:,:,newaxis] * ((seperNum - arange(seperNum)) / seperNum)[::-1]

    imgBlur = ((img[yEffect,xEffect]*step).sum(2) / seperNum).astype(uint8)

    return imgBlur