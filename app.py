import os
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, Response, jsonify
from object_detection.utils import config_util
from object_detection.builders import model_builder
from object_detection.utils import label_map_util, visualization_utils as viz_utils

app = Flask(__name__)

# Paths to the model and label map
MODEL_DIR = r'C:\ml\Tensorflow\workspace\models\my_ssd_n'
LABELMAP_PATH = r'C:\ml\Tensorflow\workspace\annotations\label_map.pbtxt'
CHECKPOINT_PATH = os.path.join(MODEL_DIR)

# Load the pipeline configuration file for the model
pipeline_config = os.path.join(MODEL_DIR, 'pipeline.config')
configs = config_util.get_configs_from_pipeline_file(pipeline_config)

# Build the detection model using the configuration file
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(CHECKPOINT_PATH, 'ckpt-11')).expect_partial()

# Load the label map
category_index = label_map_util.create_category_index_from_labelmap(LABELMAP_PATH, use_display_name=True)

# Set up the video capture (from your webcam or any other source)
cap = cv2.VideoCapture(0)

# List to keep track of detected classes for logging
detection_log = []

@tf.function
def detect_fn(image):
    """Detect function using the detection model"""
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/get_detections')
def get_detections():
    """Fetch the current detections from the webcam stream."""
    ret, frame = cap.read()
    if not ret:
        return jsonify({'current_detection': "No detection", 'detection_log': []})

    # Convert the frame to a numpy array
    image_np = np.array(frame)

    # Model prediction
    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)

    # Process detections
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections['num_detections'] = num_detections
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    detected_classes = []
    current_detection = "No detection"  # Initialize as "No detection"
    max_score = 0.0

    for i in range(num_detections):
        class_id = detections['detection_classes'][i]
        score = detections['detection_scores'][i]
        class_id += 1
        
        if class_id in category_index and score >= 0.70:  # Adjust threshold if needed
            class_name = category_index[class_id]['name']
            detected_classes.append(class_name)
            
            # Update current detection if this detection is more confident
            if score > max_score:
                max_score = score
                current_detection = class_name

    if current_detection != "No detection":
        detection_log.append(current_detection)  # Log the current detection

    return jsonify({'current_detection': current_detection, 'detection_log': detection_log})

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to a numpy array
        image_np = np.array(frame)

        # Model prediction
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)

        # Process detections
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        # Visualize detections on the frame
        label_id_offset = 1
        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'] + label_id_offset,
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=6,
            min_score_thresh=.76,
            agnostic_mode=False)

        # Encode the processed image back to a video frame
        ret, buffer = cv2.imencode('.jpg', image_np_with_detections)
        frame = buffer.tobytes()

        # Yield the frame to be used in the video feed
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
