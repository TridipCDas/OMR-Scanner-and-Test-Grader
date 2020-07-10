from scipy.spatial import distance
import numpy as np
import cv2

def order_points(pts):
    """
    Returns a list transforming the coordinates in ordered way.
    
    Arguments:
    pts: A list of 4 tuples containing the coordinates of the corner points of the rectangle
    
    Return:
    A list of tuples containing the coordinates in ordered way(TL,TR,BR,BL)
	 """
    
    xsorted = pts[np.argsort(pts[:, 0]),:]
        
    leftmost = xsorted[:2, :]
    rightmost = xsorted[2:, :]
    	
    leftmost = leftmost[np.argsort(leftmost[:, 1]), :]
    (tl, bl) = leftmost
    	
    D = distance.cdist(tl[np.newaxis], rightmost, "euclidean")[0]
    (br, tr) = rightmost[np.argsort(D)[::-1], :]
    	
    return np.array([tl, tr, br, bl], dtype="float32")
    
    
     
    	                      
def four_point_transform(image,pts):
    
    """
    Perform a 4 point transform of the object in the image
    
    Arguments:
    image: Source image containing the object
    pts:A list of 4 tuples containing the coordinates of the corner points of the rectangle
    
    Return:
    
    Apply the perspective transform matrix on the object in the image
    """
    
    rect = order_points(pts)
    (tl,tr,br,bl)=rect
    
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
    
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    return warped
                    
                                                            