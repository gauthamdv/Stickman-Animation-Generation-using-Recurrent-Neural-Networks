import mediapipe as mp
import numpy as np
import imageio

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

video_path = 'Vid_5.mp4' 
save_path = 'points.npy'
    
Position= {
    'head' : range(7,9),
    'neck' : range(11,13),
    'left_elbow' : [13],
    'right_elbow' : [14],
    'left_wrist' : range(15,23,2),
    'right_wrist' : range(16,23,2),
    'hip' : range(23,25),
    'left_knee' : [25],
    'right_knee' : [26],
    'left_ankle' : range(27,33,2),
    'right_ankle' : range(28,33,2)}


def extract_frames(video_path):
    frames = []
    with imageio.get_reader(video_path) as reader:
        for i in reader:
            frames.append(i)
    print(f'Extracted {len(frames)} frames.')
    return frames


def extract_pose(frame):
    temp = []
        
    frame_rgb = np.array(frame) 
    results = pose.process(frame_rgb)
    
    if results.pose_landmarks:
        keypoints = np.array([(lmk.x, lmk.y, lmk.visibility) for lmk in results.pose_landmarks.landmark])
        keypoints[:,1] = (1 - keypoints[:,1])*0.8
    

    for i in Position.values():
        temp_ = []
        for j in i:
            temp_.append(keypoints[j,:2])
        temp.append(np.mean(temp_, axis = 0))  
    
    return temp


def main():
    List = []
    
    frames = extract_frames(video_path)
    for i in frames:
        List.append(extract_pose(i))          
    points = np.array(List)
    points = points - points.min()
    points = points / points.max()

    np.save(save_path, points)
    
    print('Successfully saved points')
    
    
if __name__ == "__main__":
    main()
    
    
