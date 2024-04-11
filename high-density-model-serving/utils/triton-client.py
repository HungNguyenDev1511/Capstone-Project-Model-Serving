import cv2
import numpy as np
import tritonclient.http as httpclient
from process import draw_image, postprocess, preprocess

IMAGE_PATH = "/home/hungnguyen/Capstone-Project-Model-Serving/high-density-model-serving/images/car_1.jpg"
DRAWED_PATH = "images/drawed.jpg"
ENDPOINT = "localhost:8008"
INPUT_SHAPE = (640, 640)  # height, width

MODEL_NAME = "onnx"

def main():
    # Define the client to interact with the endpoint
    client = httpclient.InferenceServerClient(url=ENDPOINT)

    # Read the image
    image = cv2.imread(IMAGE_PATH)
    resized = preprocess(image, INPUT_SHAPE).astype(np.float32)

    # Define some arguments
    detection_input = httpclient.InferInput("images", resized.shape, datatype="FP32")
    detection_input.set_data_from_numpy(resized, binary_data=True)

    # Get the response
    detection_output = httpclient.InferRequestedOutput("output0", binary_data=True)
    detection = client.infer(
        model_name=MODEL_NAME, inputs=[detection_input], outputs=[detection_output]
    )
    result = detection.as_numpy("output0")
    print(f"Received result buffer of size {result.shape}")

    # Post process the result
    bboxes, scores, class_ids = postprocess(result, image.shape)
    draw_image(image, bboxes, scores, class_ids, DRAWED_PATH)


if __name__ == "__main__":
    main()