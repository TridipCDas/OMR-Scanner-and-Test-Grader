import numpy as np
import cv2
import imutils
from fpt import four_point_transform
from imutils import contours


ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}


image=cv2.imread("test_04.png")
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blurred=cv2.GaussianBlur(gray,(5,5),0)
med_val=np.median(blurred)
th1=int(max(0,0.7*med_val))
th2=int(min(255,1.3*med_val))
edged=cv2.Canny(blurred,th1,th2)



img,cnts,hierarchies=cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cnts=sorted(cnts,key=cv2.contourArea,reverse=True)
for c in cnts:
    peri=cv2.arcLength(c,True)
    approx=cv2.approxPolyDP(c,0.02*peri,True)
    
    if len(approx)==4:
        exam_page=approx
        break
    

paper=four_point_transform(image,exam_page.reshape(4,2))
warped=four_point_transform(gray,exam_page.reshape(4,2))

ret,thresh=cv2.threshold(warped,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

cnts2=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts2=imutils.grab_contours(cnts2)

qstn_cnts=[]
for c in cnts2:
    (x,y,w,h)=cv2.boundingRect(c)
    ar=w/float(h)
    
    if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
        qstn_cnts.append(c)
        
qstn_cnts_sorted=contours.sort_contours(qstn_cnts,method="top-to-bottom")[0]
correct=0

for (q,i) in enumerate(np.arange(0,len(qstn_cnts_sorted),5)):
    cnts=contours.sort_contours(qstn_cnts_sorted[i:i+5])[0]
    bubbled=None
    marked=0
    for(j,c) in enumerate(cnts):
        mask=np.zeros(thresh.shape,dtype="uint8")
        cv2.drawContours(mask,[c],-1,255,-1)
        
        mask=cv2.bitwise_and(thresh,thresh,mask=mask)
        total=cv2.countNonZero(mask)
        if total >500:
            marked=1
            print("Question:{}, Answer={}, Value={} \n".format(q+1,j+1,total))
            if bubbled is None or total > bubbled[0]:
                bubbled = (total, j)
    
    color=(0,0,255)
    answer=ANSWER_KEY[q]
    if marked!=0:
        if answer==bubbled[1]:
            color=(0,255,0)
            correct=correct+1
    
    cv2.drawContours(paper, [cnts[answer]], -1, color, 3)

score = (correct / 5.0) * 100
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper, "{:.2f}%".format(score), (10, 30),
	cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
cv2.imshow("Original", image)
cv2.imshow("Exam", paper)
cv2.waitKey(0)


        