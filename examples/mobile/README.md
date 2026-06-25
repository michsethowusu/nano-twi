# Mobile (Android / iOS) — nano-twi via sherpa-onnx

sherpa-onnx has native, offline TTS on Android (Kotlin/Java) and iOS (Swift), plus Flutter/React-Native bindings. You drop the nano-twi model files into the sample app's assets and point the config at them.

## Model assets (from `model/sherpa-onnx/`)
- `twi_ep045_steps4.onnx`  (acoustic)
- `vocos-22khz-univ.onnx`   (vocoder)
- `tokens.txt`
- `espeak-ng-data/`         (whole folder)

## Android
1. Start from the official offline-TTS sample:
   https://github.com/k2-fsa/sherpa-onnx/tree/master/android/SherpaOnnxTts
2. Copy the four assets above into `app/src/main/assets/` (keep `espeak-ng-data/` as a folder).
3. Configure a **Matcha** offline TTS in `MainActivity.kt` / the helper:
   ```kotlin
   val config = OfflineTtsConfig(
       model = OfflineTtsModelConfig(
           matcha = OfflineTtsMatchaModelConfig(
               acousticModel = "twi_ep045_steps4.onnx",
               vocoder = "vocos-22khz-univ.onnx",
               tokens = "tokens.txt",
               dataDir = "espeak-ng-data",
               noiseScale = 0.667f,
               lengthScale = 1.0f,
           ),
           numThreads = 2,
       ),
   )
   val tts = OfflineTts(assetManager = assets, config = config)
   val audio = tts.generate(text = "Awurade ne me hwɛfoɔ.", sid = 0, speed = 1.0f)
   audio.save(filename = "/sdcard/twi.wav")
   ```
   Docs: https://k2-fsa.github.io/sherpa/onnx/tts/android.html

## iOS
1. Sample: https://github.com/k2-fsa/sherpa-onnx/tree/master/ios-swift/SherpaOnnxTts
2. Add the assets to the app bundle and build a `SherpaOnnxOfflineTtsMatchaModelConfig`
   (acoustic_model / vocoder / tokens / data_dir) the same way.
   Docs: https://k2-fsa.github.io/sherpa/onnx/tts/ios.html

## Flutter / React Native / others
sherpa-onnx provides bindings (Dart, JS/Node, C, Go, Kotlin, Swift, …) — the same Matcha config
fields apply. See https://k2-fsa.github.io/sherpa/onnx/tts/

> For phones, prefer **int8-quantized** acoustic models and **fewer ODE steps** for smaller app
> size and faster synthesis (see the model repo for variants).
