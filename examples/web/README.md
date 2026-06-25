# Web (browser) — nano-twi via sherpa-onnx WASM

sherpa-onnx ships a WebAssembly TTS build that runs **entirely in the browser** (no server, fully offline once loaded). You bundle the nano-twi model files with it.

## Steps

1. **Get the model** (see repo root `download_model.sh`) — you need from `model/sherpa-onnx/`:
   `twi_ep045_steps10.onnx`, `vocos-22khz-univ.onnx`, `tokens.txt`, and `espeak-ng-data/`.

2. **Build the sherpa-onnx WASM TTS app.** Follow the official guide:
   https://k2-fsa.github.io/sherpa/onnx/tts/wasm/index.html
   Clone sherpa-onnx and use the TTS WASM template:
   ```bash
   git clone https://github.com/k2-fsa/sherpa-onnx
   cd sherpa-onnx
   # copy the nano-twi model into the wasm tts assets dir:
   cp -r /path/to/model/sherpa-onnx/* wasm/tts/assets/
   ```

3. **Point the build at a Matcha model.** In `wasm/tts/assets/` the build script expects model
   filenames; set them to ours (acoustic = `twi_ep045_steps10.onnx`, vocoder = `vocos-22khz-univ.onnx`,
   tokens = `tokens.txt`, and the `espeak-ng-data/` dir). Edit `build-wasm-simd-tts.sh` /
   `sherpa-onnx-wasm-main-tts.js` model paths accordingly (matcha acoustic + vocoder + data-dir).

4. **Build & serve:**
   ```bash
   ./build-wasm-simd-tts.sh
   cd build-wasm-simd-tts/install/bin/wasm/tts
   python3 -m http.server 8080   # open http://localhost:8080
   ```

The page gives a text box → audio, running the exact same Matcha+Vocos pipeline as the Python example, compiled to WASM.

> Tip: for a smaller download over the web, use int8-quantized + fewer-ODE-step model variants (see the model repo). espeak-ng-data is the biggest asset; you can prune unused voices but keep `lang/` + the `lfn` voice.

Reference: https://github.com/k2-fsa/sherpa-onnx/tree/master/wasm/tts
