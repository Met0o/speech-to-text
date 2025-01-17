from pydub import AudioSegment

def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

convert_mp3_to_wav("4min.mp3", "output.wav")