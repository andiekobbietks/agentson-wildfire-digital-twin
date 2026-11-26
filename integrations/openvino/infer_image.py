"""Generic OpenVINO image inference; no wildfire-specific interpretation."""

import argparse
import json
import time
from pathlib import Path

import cv2
import numpy as np
from openvino import Core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Path to OpenVINO IR .xml model")
    parser.add_argument("--image", required=True, help="Path to an input image")
    args = parser.parse_args()

    model_path = Path(args.model).resolve()
    image_path = Path(args.image).resolve()
    if not model_path.is_file() or not image_path.is_file():
        parser.error("Model XML and image must both exist.")

    image = cv2.imread(str(image_path))
    if image is None:
        parser.error(f"Could not decode image: {image_path}")

    core = Core()
    model = core.read_model(str(model_path))
    compiled = core.compile_model(model, "AUTO")
    input_port = compiled.input(0)
    shape = list(input_port.shape)

    # Generic NCHW/NHWC image preprocessing. Model-specific normalisation,
    # colour order and dynamic shapes must be configured for the chosen model.
    if len(shape) != 4 or any(not isinstance(dim, int) for dim in shape):
        parser.error(f"Expected a static 4D image input; model input shape is {shape}")

    if shape[1] in (1, 3, 4):  # NCHW
        height, width = shape[2], shape[3]
        resized = cv2.resize(image, (width, height))
        if shape[1] == 1:
            resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)[..., None]
        else:
            resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        tensor = np.transpose(resized, (2, 0, 1))[None, ...]
    else:  # Assume NHWC
        height, width = shape[1], shape[2]
        resized = cv2.resize(image, (width, height))
        resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        tensor = resized[None, ...]

    tensor = tensor.astype(np.float32)
    started = time.perf_counter()
    outputs = compiled({input_port: tensor})
    latency_ms = (time.perf_counter() - started) * 1000

    report = {
        "status": "inference_completed",
        "semantic_interpretation": "not_performed",
        "model": str(model_path),
        "image": str(image_path),
        "input_shape": shape,
        "output_shapes": [list(value.shape) for value in outputs.values()],
        "latency_ms": round(latency_ms, 3),
        "preprocessing_note": "Generic resize/RGB conversion only; validate model-specific preprocessing.",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
