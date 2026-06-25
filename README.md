# nano-twi

Fast, **offline** Asante Twi text-to-speech that runs anywhere — Python, web (WASM), and mobile (Android/iOS) — powered by [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx).

- **Acoustic model:** [Matcha-TTS](https://github.com/shivammehta25/Matcha-TTS) (epoch 45), finetuned from English LJSpeech, phonemized with the espeak-ng `lfn` voice.
- **Vocoder:** Vocos universal (≈26× faster than HiFi-GAN on CPU).
- **Runtime:** sherpa-onnx — CPU, ~2× realtime, no PyTorch. Single voice (no cloning).

**Live demo:** https://huggingface.co/spaces/michsethowusu/nano-twi
**Model files:** https://huggingface.co/michsethowusu/matcha-twi (folder `sherpa-onnx/`)

## What's in the model bundle
| File | Role |
|------|------|
| `twi_ep045_steps4.onnx` | Matcha acoustic model — **default**, 4 ODE steps (~4× realtime on CPU), best quality |
| `twi_ep045_steps2.onnx` | Matcha acoustic model — **fast** option, 2 ODE steps (~11× realtime), *some quality loss* |
| `vocos-22khz-univ.onnx` | Vocos vocoder (mel → audio) |
| `tokens.txt` | phoneme → id table |
| `espeak-ng-data/` | espeak-ng data incl. the `lfn` voice (phonemization) |

**Which acoustic model?** Use `twi_ep045_steps4.onnx` by default. Switch to `twi_ep045_steps2.onnx`
when you need maximum speed / lowest latency (e.g. on weak devices) and can accept a small drop in
clarity. Everything else (vocoder, tokens, espeak data) is shared — just swap the `--matcha-acoustic-model`.


## Quick start (no clone needed)

One model + one script — that's all.

```bash
# 1. install
pip install -U sherpa-onnx soundfile "huggingface_hub[cli]"

# 2. download the model bundle into ./model
hf download michsethowusu/matcha-twi --include "sherpa-onnx/*" --local-dir ./model

# 3. grab the one-file synthesizer and speak
curl -O https://raw.githubusercontent.com/michsethowusu/nano-twi/main/examples/python/synthesize.py

# default = 4-step model (best quality):
python3 synthesize.py --model-dir ./model/sherpa-onnx \
  --text "Awurade ne me hwɛfoɔ, biribiara renhia me." --out twi.wav

# fast = 2-step model (lower quality) — pick the model with --acoustic:
python3 synthesize.py --model-dir ./model/sherpa-onnx --acoustic twi_ep045_steps2.onnx \
  --text "Awurade ne me hwɛfoɔ, biribiara renhia me." --out twi_fast.wav
```

The acoustic model is chosen with **`--acoustic`** (default `twi_ep045_steps4.onnx`); everything else (vocoder, tokens, espeak data) is shared.

> Uses the sherpa-onnx **Python API** (stable across versions). The standalone
> `sherpa-onnx-offline-tts` command-line tool was removed from the pip package in
> sherpa-onnx ≥ 1.13, so the one-file script above is the simplest reliable path.

## Integration examples
- **Python** — [`examples/python/`](./examples/python)
- **Web (browser, WASM)** — [`examples/web/`](./examples/web)
- **Mobile (Android / iOS)** — [`examples/mobile/`](./examples/mobile)

## Compatibility (important for mobile / web / any runtime)
The phonemizer is **espeak-ng**, which is **embedded inside sherpa-onnx** (you never install it
separately — it's compiled into the desktop wheel, the Android/iOS native libs, and the WASM build).
The only espeak asset you ship is the small **`espeak-ng-data/`** folder included in this bundle.

- **Always use the `espeak-ng-data/` that ships in this bundle.** It was produced with
  **eSpeak NG 1.52.0** and the model was trained against those exact phonemes. Substituting a
  different `espeak-ng-data` (e.g. your system one) can change pronunciation.
- **Verified with sherpa-onnx 1.12.x and 1.13.x** (Python API). Use a sherpa-onnx **≥ 1.12** build
  on any platform — desktop (pip), Android/iOS (native), or Web (WASM). They all embed a compatible
  espeak-ng, so the same `espeak-ng-data/` works everywhere; just ship it as an app/web asset.
- If a future sherpa-onnx ever phonemizes oddly, regenerate `espeak-ng-data/` from *that* release's
  espeak-ng (same prune: keep `phondata`, `phonindex`, `phontab`, `phondata-manifest`, `intonations`,
  `lfn_dict`, `lang/art/lfn`).

## Notes
- Input is **Asante Twi text** in normal orthography (incl. `ɛ ɔ`); phonemization to IPA happens automatically via espeak-ng `lfn`.
- `noise_scale=0.667`, `length_scale=1.0` are good defaults; raise `length_scale` to slow speech.
- Two acoustic models ship in the bundle: `twi_ep045_steps4.onnx` (default) and `twi_ep045_steps2.onnx` (faster, lower quality).

## License
MIT (this repo). The model and its dependencies (Matcha-TTS, Vocos, sherpa-onnx, espeak-ng) retain their respective licenses.
