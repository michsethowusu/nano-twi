#!/usr/bin/env python3
"""Offline Asante Twi TTS with sherpa-onnx (Matcha + Vocos).

Usage:
    python synthesize.py --model-dir ./model/sherpa-onnx \
        --text "Awurade ne me hwɛfoɔ." --out twi.wav
"""
import argparse

import sherpa_onnx
import soundfile as sf


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model-dir", required=True, help="folder with the sherpa-onnx bundle")
    p.add_argument("--text", required=True)
    p.add_argument("--out", default="twi.wav")
    p.add_argument("--acoustic", default="twi_ep045_steps4.onnx")
    p.add_argument("--speed", type=float, default=1.0, help="1.0 = normal; >1 faster")
    p.add_argument("--noise-scale", type=float, default=0.667)
    p.add_argument("--num-threads", type=int, default=2)
    a = p.parse_args()

    d = a.model_dir.rstrip("/")
    tts = sherpa_onnx.OfflineTts(
        sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                matcha=sherpa_onnx.OfflineTtsMatchaModelConfig(
                    acoustic_model=f"{d}/{a.acoustic}",
                    vocoder=f"{d}/vocos-22khz-univ.onnx",
                    lexicon="",
                    tokens=f"{d}/tokens.txt",
                    data_dir=f"{d}/espeak-ng-data",
                    noise_scale=a.noise_scale,
                    length_scale=1.0,
                ),
                num_threads=a.num_threads,
                provider="cpu",
            ),
            max_num_sentences=1,
        )
    )
    audio = tts.generate(a.text, sid=0, speed=a.speed)
    sf.write(a.out, audio.samples, audio.sample_rate)
    print(f"Wrote {a.out}  ({len(audio.samples) / audio.sample_rate:.2f}s @ {audio.sample_rate} Hz)")


if __name__ == "__main__":
    main()
