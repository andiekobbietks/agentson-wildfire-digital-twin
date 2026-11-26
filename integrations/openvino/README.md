# OpenVINO inference adapter

This adapter runs a user-supplied OpenVINO IR model against one image. It is a generic inference harness, not a supplied wildfire detector.

## Install

Use a dedicated Python environment:

```bash
python -m venv .venv
# Activate the environment for your platform
pip install -r requirements.txt
```

## Run

```bash
python infer_image.py --model path/to/model.xml --image path/to/frame.jpg
```

The adapter reports the model path, input path, output tensor shapes and inference latency. It does not assign semantic labels or claim that a tensor represents fire. Add a model-specific postprocessor only after documenting the model card, classes, training/evaluation data, licence and known failure modes.

For video or ROS 2 integration, define a bounded queue, timestamp propagation, back-pressure and stale-frame policy before adding a subscriber.
