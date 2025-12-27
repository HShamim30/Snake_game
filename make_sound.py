import wave
import struct
import math

def generate_sound(filename, freq, duration=0.2, volume=0.5):
    framerate = 44100
    samples = int(framerate * duration)

    wav_file = wave.open(filename, 'w')
    wav_file.setparams((1, 2, framerate, samples, 'NONE', 'not compressed'))

    for i in range(samples):
        value = int(volume * 32767 * math.sin(2 * math.pi * freq * i / framerate))
        data = struct.pack('<h', value)
        wav_file.writeframesraw(data)

    wav_file.close()

# Eat sound (short high pitch)
generate_sound("eat.wav", freq=900, duration=0.12)

# Game over sound (low pitch)
generate_sound("gameover.wav", freq=200, duration=0.4)

print("✅ eat.wav & gameover.wav created successfully")
