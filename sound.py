# wavファイルを読み込む
with wave.open("./src/move.wav", "r") as wav_file:
    # wavファイルのフォーマット情報を取得
    sample_width = wav_file.getsampwidth()
    channels = wav_file.getnchannels()
    framerate = wav_file.getframerate()
    samples = wav_file.readframes(wav_file.getnframes())

# pyxelのsoundeditor用に変換
result = []
for i in range(0, len(samples), sample_width * channels):
    data = samples[i:i+sample_width*channels]
    if sample_width == 2:
        # 16bit の wav
        if channels == 2:
            # stereo
            left = struct.unpack("<h", data[0:2])[0]
            right = struct.unpack("<h", data[2:4])[0]
            value = (left + right) // 2
        else:
            # mono
            value = struct.unpack("<h", data)[0]
    else:
        # 8bit の wav
        if channels == 2:
            # stereo
            left = data[0]
            right = data[1]
            value = (left + right) // 2
        else:
            # mono
            value = data[0]
    result.append(value)

# pyxelのsoundeditor用のフォーマットに変換したデータを書き出す
with open("sample.pysnd", "wb") as f:
    f.write(struct.pack("<3i", framerate, sample_width*8, len(result)))
    for value in result:
        f.write(struct.pack("<h", value))

pyxel.play(0, 0)