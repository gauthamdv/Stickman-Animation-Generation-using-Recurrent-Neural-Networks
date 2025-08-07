# 🕴️ Stickman Animation Generation using Recurrent Neural Networks

This project generates stickman pose animations using Recurrent Neural Networks (RNNs) trained on simplified pose data extracted from videos using [MediaPipe](https://google.github.io/mediapipe/). The model learns to predict future human poses from sequences of past poses, enabling frame-by-frame animation generation.

---

## 📽️ Overview

- **Pose Extraction:** 33 landmark points are extracted using MediaPipe.
- **Point Reduction:** The 33 points are reduced to 11 meaningful body joints (e.g., head, elbows, ankles) using mean/median-based averaging.
- **Sequence Preparation:** The dataset is split into overlapping sequences of 20 frames for training.
- **Model Training:** An RNN model is trained to predict the next frame given the current sequence.
- **Pose Generation:** Starting from a single frame, the model can recursively generate future frames.

---

## 📊 11-Point Mapping

The following body parts are extracted from the 33 MediaPipe landmarks:

1.	head      
2.	neck       
3.	left_elbow 
4.	right_elbow 
5.	left_wrist  
6.	right_wrist 
7.	hip         
8.	left_knee   
9.	right_knee  
10.	left_ankle  
11.	right_ankle


---

## 🧠 Model Architecture

- Input shape: `(20, 11, 2)`
- Layers:
  - Reshape → `(20, 22)`
  - LSTM layer (128 units)
  - TimeDistributed Dense layers: 64 → 32 → 22
  - Reshape back to `(20, 11, 2)`
- Loss: Custom point-wise MSE for pose accuracy

---

## 🏃 Usage

### Installation

```bash
git clone https://github.com/gauthamdv/Stickman-Animation-Generation-using-Recurrent-Neural-Networks
cd Stickman-Animation-Generation-using-Recurrent-Neural-Networks
pip install -r requirements.txt
```

### Run Training

```bash
python Codes/train_model.py
```

### Generate Animations

```bash
python Codes/generate_animation.py
```

---

### 📦 Requirements

Install the required packages:

```bash
pip install tensorflow numpy mediapipe opencv-python
```

### 🔁 Preprocessing

1. Extract frames from a video.
2. Use MediaPipe to extract 33 pose keypoints per frame.
3. Reduce to 11 keypoints and save the data as `points.npy`.


### 🔮 Inference

After training, the model can predict future frames using a single starting pose:

```python
# Example:
start_pose = data[0:20]
predicted_sequence = model.predict(start_pose)
```

---

## 🗂️ Project Structure

```
📁 Stickman-Animation-Generation
├── points.npy              # Preprocessed 11-point pose dataset
├── rnn_model.py            # RNN class with model definition, training, and saving
├── main.py                 # Main script to load data, train, and save model
├── utils/                  # (optional) Helper scripts for pose extraction, animation
└── README.md               # Project documentation
```

---

## 🧠 Model Overview

- Type: RNN-based sequence generator
- Input: 11 pose keypoints from the previous frame
- Output: 11 keypoints for the next frame
- Training: Sequences of pose frames from MediaPipe output
- Feedback: Output of one timestep is fed into the next

---

## 🎯 Output

- 2D keypoints that can be mapped onto any animation model
- Can be visualized as stick figures or converted for use in animation software

---

## 📈 Evaluation

- Custom point-wise loss function
- Visual comparisons across predicted and real sequences
- Metrics tracked across epochs (loss, accuracy)

---

## 🎞️ Animation Notes

To visualize the output as animation:
- Feed the generated 11 keypoints into any animation or rendering tool.
- Map these 11 keypoints to your character's joints (e.g., head, elbows, knees).
- Stickman visualization is **not included** in this repository, but the pose coordinates are ready for use in animation software or custom renderers.

---

## 📈 Future Work

- Add a Transformer baseline for performance comparison
- Introduce noise scheduling to improve long-sequence generation
- Integrate output into tools like Blender/Unity
- JSON export for skeletal mapping

---

## 🙌 Acknowledgements

- [MediaPipe](https://google.github.io/mediapipe/) for pose extraction
- TensorFlow/Keras for RNN model implementation

---

## 📬 Contact

Created by [Gautham DV](https://github.com/gauthamdv)  
Open to suggestions and contributions!
