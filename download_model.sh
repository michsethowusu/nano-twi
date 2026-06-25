#!/usr/bin/env bash
# Download the nano-twi sherpa-onnx model bundle from Hugging Face into ./model
set -e
pip install -U "huggingface_hub[cli]" >/dev/null
hf download michsethowusu/matcha-twi --include "sherpa-onnx/*" --local-dir ./model
echo "Model ready at ./model/sherpa-onnx/"
