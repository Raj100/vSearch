import os
import cv2
import numpy as np
from typing import List

def process_video(
    video_path: str,
    output_dir: str,
    interval: int = 1 
) -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)
    frame_paths = []
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            frame_file = f"{output_dir}/frame_{frame_count}.jpg"
            cv2.imwrite(frame_file, frame)
            frame_paths.append(frame_file)
        
        frame_count += 1
    
    cap.release()
    return frame_paths

def compute_histogram(image_path: str, bins: int = 16) -> list:
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    hist = cv2.calcHist(
        [hsv], [0, 1], None,
        [bins, bins], [0, 180, 0, 256]
    )
    cv2.normalize(hist, hist)
    return hist.flatten().tolist()