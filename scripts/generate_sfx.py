import math
import os
import random
import wave
import struct

SAMPLE_RATE = 44100
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, "Assets", "Audio", "Generated")
os.makedirs(OUT_DIR, exist_ok=True)


def clamp(v, lo=-1.0, hi=1.0):
    return max(lo, min(hi, v))


def env_exp(t, dur, attack=0.002, curve=6.0):
    if t < attack:
        return t / attack
    p = (t - attack) / max(1e-6, (dur - attack))
    return math.exp(-curve * p)


def write_wav(path, samples):
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for s in samples:
            iv = int(clamp(s) * 32767)
            frames += struct.pack('<h', iv)
        wf.writeframes(frames)


def tone(freq, dur, wave_type="sine", amp=0.5, env=True, sweep_to=None):
    n = int(dur * SAMPLE_RATE)
    out = []
    phase = 0.0
    for i in range(n):
        t = i / SAMPLE_RATE
        if sweep_to is not None:
            f = freq + (sweep_to - freq) * (t / dur)
        else:
            f = freq
        phase += 2 * math.pi * f / SAMPLE_RATE
        if wave_type == "sine":
            s = math.sin(phase)
        elif wave_type == "square":
            s = 1.0 if math.sin(phase) >= 0 else -1.0
        elif wave_type == "saw":
            s = 2.0 * ((phase / (2 * math.pi)) % 1.0) - 1.0
        else:
            s = math.sin(phase)
        e = env_exp(t, dur) if env else 1.0
        out.append(s * amp * e)
    return out


def white_noise(dur, amp=0.4):
    n = int(dur * SAMPLE_RATE)
    out = []
    for i in range(n):
        t = i / SAMPLE_RATE
        out.append((random.random() * 2.0 - 1.0) * amp * env_exp(t, dur))
    return out


def bandpass_noise(dur, center=2000.0, q=0.6, amp=0.45):
    x = white_noise(dur, amp=amp)
    n = len(x)
    y = [0.0] * n

    w0 = 2 * math.pi * center / SAMPLE_RATE
    alpha = math.sin(w0) / (2 * q)
    b0 = q * alpha
    b1 = 0.0
    b2 = -q * alpha
    a0 = 1 + alpha
    a1 = -2 * math.cos(w0)
    a2 = 1 - alpha

    b0 /= a0
    b1 /= a0
    b2 /= a0
    a1 /= a0
    a2 /= a0

    x1 = x2 = y1 = y2 = 0.0
    for i in range(n):
        yi = b0 * x[i] + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        y[i] = yi
        x2, x1 = x1, x[i]
        y2, y1 = y1, yi
    return y


def mix(*tracks):
    max_len = max(len(t) for t in tracks)
    out = [0.0] * max_len
    for t in tracks:
        for i, s in enumerate(t):
            out[i] += s
    peak = max(1e-9, max(abs(v) for v in out))
    if peak > 0.95:
        scale = 0.95 / peak
        out = [v * scale for v in out]
    return out


def sequence(notes):
    out = []
    for freq, dur, wt, amp in notes:
        out.extend(tone(freq, dur, wt, amp=amp, env=True))
    return out


def dual_pulse(freq, dur, gap):
    p1 = tone(freq, dur, "sine", amp=0.65)
    gap_s = [0.0] * int(gap * SAMPLE_RATE)
    p2 = tone(freq, dur, "sine", amp=0.65)
    return p1 + gap_s + p2


def sweep_noise(dur, start=200.0, end=8000.0, amp=0.5):
    n = int(dur * SAMPLE_RATE)
    out = [0.0] * n
    phase = 0.0
    for i in range(n):
        t = i / SAMPLE_RATE
        f = start + (end - start) * (t / dur)
        phase += 2 * math.pi * f / SAMPLE_RATE
        carrier = math.sin(phase)
        noise = (random.random() * 2.0 - 1.0)
        out[i] = (0.45 * carrier + 0.55 * noise) * amp * env_exp(t, dur, attack=0.001, curve=4.0)
    return out


def write(name, samples):
    path = os.path.join(OUT_DIR, name)
    write_wav(path, samples)
    print(f"Generated: {path}")


def main():
    random.seed(42)

    write("sfx_move_tap_v1.wav", tone(440, 0.05, "square", amp=0.38))

    write("sfx_land_thump_v1.wav", mix(
        tone(80, 0.15, "sine", amp=0.7),
        tone(160, 0.12, "sine", amp=0.22),
    ))

    write("sfx_rotate_swish_v1.wav", bandpass_noise(0.10, center=2200, q=0.7, amp=0.52))

    write("sfx_flip_rise_v1.wav", tone(200, 0.30, "sine", amp=0.58, sweep_to=600))

    write("sfx_flip_clack_v1.wav", mix(
        tone(100, 0.08, "square", amp=0.42),
        bandpass_noise(0.08, center=1600, q=0.8, amp=0.22),
    ))

    write("sfx_clear_1_ping_v1.wav", tone(880, 0.20, "sine", amp=0.52))

    write("sfx_clear_2_pump_v1.wav", dual_pulse(60, 0.08, 0.10))

    write("sfx_clear_3_bass_v1.wav", mix(
        tone(40, 0.50, "saw", amp=0.62),
        tone(120, 0.45, "sine", amp=0.22),
    ))

    write("sfx_clear_4_blast_v1.wav", mix(
        sweep_noise(0.80, start=120, end=9000, amp=0.58),
        bandpass_noise(0.75, center=2600, q=0.6, amp=0.28),
    ))

    write("sfx_level_clear_arp_v1.wav", sequence([
        (261.63, 0.14, "sine", 0.5),
        (329.63, 0.14, "sine", 0.5),
        (392.00, 0.22, "sine", 0.55),
    ]))

    write("sfx_game_over_low_v1.wav", mix(
        tone(60, 2.0, "sine", amp=0.45),
        tone(120, 1.8, "sine", amp=0.13),
    ))

    write("sfx_cat_meow_v1.wav", tone(500, 0.20, "sine", amp=0.45, sweep_to=300))


if __name__ == "__main__":
    main()
