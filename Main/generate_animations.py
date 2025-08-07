import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
import os
import mediapipe as mp
from PIL import Image
import sys

SEQUENCE_LENGTH = 20

class PoseExtractor:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.8)
        self.position = {
            'head': range(7, 9),
            'neck': range(11, 13),
            'left_elbow': [13],
            'right_elbow': [14],
            'left_wrist': range(15, 23, 2),
            'right_wrist': range(16, 23, 2),
            'hip': range(23, 25),
            'left_knee': [25],
            'right_knee': [26],
            'left_ankle': range(27, 33, 2),
            'right_ankle': range(28, 33, 2)
        }

    def extract(self, frame):
        temp = []
        frame_rgb = np.array(frame) 
        results = self.pose.process(frame_rgb)

        if results.pose_landmarks:
            keypoints = np.array([(lmk.x, lmk.y, lmk.visibility) for lmk in results.pose_landmarks.landmark])
            keypoints[:, 1] = (1 - keypoints[:, 1]) * 0.8 

        for indices in self.position.values():
            temp_ = [keypoints[i, :2] for i in indices]
            temp.append(np.mean(temp_, axis=0))

        if len(temp) < 11:
            temp.extend([np.zeros(2)] * (11 - len(temp)))
        elif len(temp) > 11:
            temp = temp[:11]

        return temp

class PosePredictor:
    def __init__(self, model_path, sequence_length=20):
        self.sequence_length = sequence_length
        self.model_path = model_path
        self.model = self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            print("Loading existing RNN model...")
            return load_model(self.model_path, custom_objects={'pointwise_mse': self.pointwise_mse})
        else:
            print("RNN model not found.")
            sys.exit()

    def pointwise_mse(self, y_true, y_pred):
        error = tf.square(y_true - y_pred)
        return tf.reduce_mean(error, axis=-1)

    def generate_points(self, initial_pose, num_iterations=100):
        input_sequence = np.concatenate([np.random.rand(self.sequence_length - 1, 11, 2), initial_pose], axis=0).reshape(1, self.sequence_length, 11, 2)
        generated_points = np.zeros((num_iterations, 11, 2))

        for i in range(num_iterations):
            output_sequence = self.model.predict(input_sequence)
            predicted_pose = output_sequence[0, -1, :, :]
            generated_points[i] = predicted_pose
            input_sequence = np.concatenate((input_sequence[:, 1:, :, :], predicted_pose.reshape(1, 1, 11, 2)), axis=1)

        return generated_points

def main():
    image_path = 'uploads/input_1.jpg'
    save_path = 'data/gen_points.npy'

    pose_extractor = PoseExtractor()
    image = Image.open(image_path)
    initial_pose = np.array(pose_extractor.extract(image)).reshape(1, 11, 2)

    initial_pose = (initial_pose - initial_pose.min()) / (initial_pose.max() - initial_pose.min())

    pose_predictor = PosePredictor(model_path='models/rnn_model.h5')
    generated_points = pose_predictor.generate_points(initial_pose)

    np.save(save_path, generated_points)
    #print(generated_points)

if __name__ == "__main__":
    main()
