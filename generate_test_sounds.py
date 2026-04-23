import wave
import struct
import math
import os

sample_rate = 44100.0

def save_wav(filename, samples):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(sample_rate)
        for sample in samples:
            # clip to 16-bit int
            sample = max(-32768, min(32767, int(sample)))
            wav_file.writeframes(struct.pack('h', sample))

# 1. Ascending tone (boot.wav) 0.5s
samples_boot = []
for i in range(int(sample_rate * 0.5)):
    t = float(i) / sample_rate
    freq = 440 + 880 * t  # Ascends
    val = 16000 * math.sin(2.0 * math.pi * freq * t)
    samples_boot.append(val)
save_wav('sounds_computer/greeting_sounds/boot.wav', samples_boot)

# 2. Short beep (beep.wav) 0.1s
samples_beep = []
for i in range(int(sample_rate * 0.1)):
    t = float(i) / sample_rate
    val = 16000 * math.sin(2.0 * math.pi * 1000 * t)
    samples_beep.append(val)
save_wav('sounds_computer/ack_sounds/beep.wav', samples_beep)

# 3. Soft hum (hum.wav) 1.0s
samples_hum = []
for i in range(int(sample_rate * 1.0)):
    t = float(i) / sample_rate
    val = 6000 * math.sin(2.0 * math.pi * 150 * t)  # quieter
    samples_hum.append(val)
save_wav('sounds_computer/thinking_sounds/hum.wav', samples_hum)

# 4. Low buzz (alert.wav) 0.3s
samples_alert = []
for i in range(int(sample_rate * 0.3)):
    t = float(i) / sample_rate
    # mix 300Hz and 315Hz for discordance
    val = 10000 * (math.sin(2.0 * math.pi * 300 * t) + math.sin(2.0 * math.pi * 315 * t))
    samples_alert.append(val)
save_wav('sounds_computer/error_sounds/alert.wav', samples_alert)

print("Generated test sounds in sounds_computer/")
