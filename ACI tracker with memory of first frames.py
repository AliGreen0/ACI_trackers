# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 16:41:14 2019

@author: Ali Sekhavati

ACI tracker with memory of first frames
"""

import cv2
import sys

if __name__ == '__main__' :
    
    
    def are_other_2_close (bound0 , bound1):
        are_other_2_close_flag = True
        for i in range (0,4):
            if abs (bound0[i] - bound1[i]) > 30 or bound0[i] < 0.01 or bound1[i] < 0.01:
                are_other_2_close_flag = False
        return are_other_2_close_flag
            

    tracker_type = 'ACI with memory of first frames'

    tracker1 = cv2.TrackerMOSSE_create()
    tracker = cv2.TrackerKCF_create()

    tracker0 = cv2.TrackerCSRT_create()
    
    #First memory
    tracker1m = cv2.TrackerMOSSE_create()
    trackerm = cv2.TrackerKCF_create()
    tracker0m = cv2.TrackerCSRT_create()

    # Read video
    video = cv2.VideoCapture("videos/nascar_01.mp4")

    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()

    # Read first frame
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
    
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)

    # Uncomment the line below to select a different bounding box
    bbox0m = bboxm = bbox1m = bbox0 = bbox1 = bbox = bbox_average = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    ok0 = tracker0.init(frame, bbox0)
    ok1 = tracker1.init(frame, bbox1)
    ok = tracker.init(frame, bbox)
    
    ok0m = tracker0m.init(frame, bbox0m)
    ok1m = tracker1m.init(frame, bbox1m)
    okm = trackerm.init(frame, bboxm)
    
    flag = flag0 = flag1 = True
    
    nf = 0
    lfps = []
    total_fps = 0
    k = 0
    counter = 0
    flag_learn = True
    h,w,_ = frame.shape
    counter_learn = 0
    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (w,h))

    while k!= 27:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        
        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)
        ok0, bbox0 = tracker0.update(frame)
        ok1, bbox1 = tracker1.update(frame)
        
        if flag_learn:
            okm, bboxm = trackerm.update(frame)
            ok0m, bbox0m = tracker0m.update(frame)
            ok1m, bbox1m = tracker1m.update(frame)
        
        flag = True
        flag0 = True
        flag1 = True
        for i in range (0,4):
            if abs (bbox[i]-bbox_average[i])>30 or not ok or bbox [i]<0.001:
                flag = False
                
            if abs (bbox0[i]-bbox_average[i])>30 or not ok0 or bbox0 [i]<0.001:
                flag0 = False
                
            if abs (bbox1[i]-bbox_average[i])>30 or not ok1 or bbox1 [i]<0.001:
                flag1 = False
            
        if not flag:
            flag_use_memory = True
            okm = trackerm.init(frame, bboxm)
            okm, bboxm = trackerm.update(frame)
            for i in range (4):
                if not okm or bboxm [i]<0.001:
                    flag_use_memory = False
            if flag_use_memory:
                del tracker
                bbox = bboxm
                tracker = cv2.TrackerKCF_create()
                ok = tracker.init(frame, bbox)
                
        if not flag0:
            flag_use_memory0 = True
            ok0m = tracker0m.init(frame, bbox0m)
            ok0m, bbox0m = tracker0m.update(frame)
            for i in range (4):
                if not ok0m or bbox0m [i]<0.001:
                    flag_use_memory0 = False
            if flag_use_memory0:
                del tracker0
                bbox0 = bbox0m
                tracker0 = cv2.TrackerCSRT_create()
                ok0 = tracker0.init(frame, bbox0)
                
        if not flag1:
            flag_use_memory1 = True
            ok1m = tracker1m.init(frame, bbox1m)
            ok1m, bbox1m = tracker1m.update(frame)
            for i in range (4):
                if not ok1m or bbox1m [i]<0.001:
                    flag_use_memory1 = False            
            if flag_use_memory1:
                del tracker1
                bbox1 = bbox1m
                tracker1 = cv2.TrackerMOSSE_create()
                ok1 = tracker1.init(frame, bbox1)
        
        if flag and flag0 and flag1:
            del bbox_average
            bbox_average=((bbox[0]+bbox0[0]+bbox1[0])/3,(bbox[1]+bbox0[1]+bbox1[1])/3,(bbox[2]+bbox0[2]+bbox1[2])/3,(bbox[3]+bbox0[3]+bbox1[3])/3)
        elif flag0 and flag1:
            del bbox_average
            del bbox
            del tracker
            bbox_average= ((bbox0[0]+bbox1[0])/2,(bbox0[1]+bbox1[1])/2,(bbox0[2]+bbox1[2])/2,(bbox0[3]+bbox1[3])/2)
            bbox=bbox_average
            tracker = cv2.TrackerKCF_create()
            ok = tracker.init(frame, bbox)
            if counter_learn <= 20:
                counter_learn += 1
                del bboxm
                bboxm = bbox
                okm = trackerm.init(frame, bboxm)
            else:
                flag_learn = False
                
        elif flag and flag0:
            del bbox_average
            del bbox1
            bbox_average= ((bbox[0]+bbox0[0])/2,(bbox[1]+bbox0[1])/2,(bbox[2]+bbox0[2])/2,(bbox[3]+bbox0[3])/2)
            bbox1=bbox_average
            del tracker1
            tracker1 = cv2.TrackerMOSSE_create()
            ok1 = tracker1.init(frame, bbox1)
            if counter_learn <= 20:
                counter_learn += 1
                del bbox1m
                bbox1m = bbox1
                ok1m = tracker1m.init(frame, bbox1m)
            else:
                flag_learn = False
            
        elif flag and flag1:
            del bbox_average
            del bbox0
            del tracker0
            bbox_average= ((bbox[0]+bbox1[0])/2,(bbox[1]+bbox1[1])/2,(bbox[2]+bbox1[2])/2,(bbox[3]+bbox1[3])/2)
            bbox0=bbox_average
            tracker0 = cv2.TrackerCSRT_create()
            ok0 = tracker0.init(frame, bbox0)
            if counter_learn <= 20:
                counter_learn += 1
                del bbox0m
                bbox0m = bbox0
                ok0m = tracker0m.init(frame, bbox0m)
            else:
                flag_learn = False
        
        elif ok0:
            del bbox_average 
            counter += 1
            bbox_average=bbox0
            if are_other_2_close(bbox , bbox1):
                bbox_average = ((bbox[0]+bbox1[0])/2,(bbox[1]+bbox1[1])/2,(bbox[2]+bbox1[2])/2,(bbox[3]+bbox1[3])/2)
            if counter == 100:
                del tracker , tracker1
                bbox1 = bbox_average
                bbox = bbox_average
                tracker1 = cv2.TrackerMOSSE_create()
                ok1 = tracker1.init(frame, bbox1)
                tracker = cv2.TrackerKCF_create()
                ok = tracker.init(frame, bbox)
        elif ok1:
            del bbox_average
            bbox_average=bbox1
            if are_other_2_close (bbox , bbox0):
                bbox_average= ((bbox[0]+bbox0[0])/2,(bbox[1]+bbox0[1])/2,(bbox[2]+bbox0[2])/2,(bbox[3]+bbox0[3])/2)
        elif ok:
            del bbox_average
            bbox_average=bbox
            if are_other_2_close (bbox0 , bbox1):   
                bbox_average= ((bbox0[0]+bbox1[0])/2,(bbox0[1]+bbox1[1])/2,(bbox0[2]+bbox1[2])/2,(bbox0[3]+bbox1[3]))
        else:
            bbox_average=bbox0
        
        
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            counter = 0
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,0,0),2)
            bbox=bbox_average
            #ok=True
            #frm.append(frame)
        
        if ok0:
            # Tracking success
            p10 = (int(bbox0[0]), int(bbox0[1]))
            p20 = (int(bbox0[0] + bbox0[2]), int(bbox0[1] + bbox0[3]))
            cv2.rectangle(frame, p10, p20, (0,255,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking CSRT failure detected", (100,110), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,0),2)
            bbox0=bbox_average
            #frm0.append(frame)
        
        if ok1:
            # Tracking success
            p11 = (int(bbox1[0]), int(bbox1[1]))
            p21 = (int(bbox1[0] + bbox1[2]), int(bbox1[1] + bbox1[3]))
            cv2.rectangle(frame, p11, p21, (0,0,255), 2, 1)
            counter = 0
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking 1 failure detected", (100,140), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            bbox1=bbox_average
            #frm1.append(frame)
            
        p1_average = (int(bbox_average[0]), int(bbox_average[1]))
        p2_average = (int(bbox_average[0] + bbox_average[2]), int(bbox_average[1] + bbox_average[3]))
        cv2.rectangle(frame, p1_average, p2_average, (0,0,0), 2, 1)
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
        
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);


        # Display result
        cv2.imshow("Tracking", frame)
        #nf += 1
        lfps.append(fps)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        out.write (frame)
        #if k == 27 : break
    
    cv2.destroyAllWindows()
    
    for i in range (len(lfps)):
        total_fps += lfps [i]
    average_fps = total_fps / len(lfps)    
    out.release()