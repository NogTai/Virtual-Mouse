import os
from cv2 import waitKey
from Hand_Tracking_Module_cvzone_custom import HandDetector
import cv2
import matplotlib.pyplot as plt

def CaptureImage(name_gesture, folder_name, instance_bonus, delay_count):
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    count = 0
    number_Image = 0
    while True:
        # Get image frame
        success, img_cam = cap.read()
        
        # img = cv2.flip(img_cam, 1)
        img = img_cam
        # Find the hand and its landmarks
        hands, drawed_img = detector.findHands(img.copy(), flipType=True)  # with draw
        # hands = detector.findHands(img, draw=False)  # without draw

        if hands:
            # Hand 1
            hand1 = hands[0]
            # lmList1 = hand1["lmList"]  # List of 21 Landmark points
            bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
            centerPoint1 = hand1['center']  # center of the hand cx,cy
            # handType1 = hand1["type"]  # Handtype Left or Right

            # fingers1 = detector.fingersUp(hand1)


            #Save croped image
            if count == delay_count:
                while os.path.exists(folder_name + '/' + name_gesture + '/' + str(number_Image) + ".jpg"): number_Image += 1
                img_crop = img[bbox1[1]-instance_bonus:bbox1[1]+bbox1[3]+instance_bonus, bbox1[0]-instance_bonus:bbox1[0]+bbox1[2]+instance_bonus]
                try:
                    cv2.imwrite(folder_name + '/' + name_gesture + '/' + str(number_Image) + ".jpg", img_crop)
                    number_Image += 1
                except:
                    print("Your action is so fast!")
                count = 0
            count += 1
            
            cv2.circle(drawed_img, (centerPoint1[0], centerPoint1[1]), 8, (255, 0, 255), cv2.FILLED) # draw center point
            # if len(hands) == 2:
            #     # Hand 2
            #     hand2 = hands[1]
            #     lmList2 = hand2["lmList"]  # List of 21 Landmark points
            #     bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
            #     centerPoint2 = hand2['center']  # center of the hand cx,cy
            #     handType2 = hand2["type"]  # Hand Type "Left" or "Right"

            #     fingers2 = detector.fingersUp(hand2)
                
            #     cv2.circle(img, (centerPoint2[0], centerPoint2[1]), 8, (255, 0, 255), cv2.FILLED) # draw center point

            #     # Find Distance between two Landmarks. Could be same hand or different hands
            #     # length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)  # with draw
            #     # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw
        # Display
        cv2.imshow("Image (Press q to quit)", drawed_img)

        if waitKey(1) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__': 
    directory = "Scroll_mouse"

    parent_dir = "C:/Users/theta/OneDrive - nogdev/Desktop/Work/Python/Product_HIT/Datasets/Hand_Gestures/train/"

    path = os.path.join(parent_dir, directory)

    try:
        os.makedirs(path, exist_ok = True)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)

    CaptureImage(directory, parent_dir, 50, delay_count=10)