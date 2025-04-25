from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio
import os
os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"

# download and load all models
preload_models()
voice_preset = "v2/hi_speaker_0"

# generate audio from text
text_prompt = """
     नमस्ते, मेरा नाम सोम्या है और मैं भारत के मुंबई शहर में रहती हूँ। मैं एक इंजीनियरिंग छात्रा हूँ और मुझे कंप्यूटर साइंस में रुचि है। अपने खाली समय में, मुझे किताबें पढ़ना, संगीत सुनना और दोस्तों के साथ घूमना पसंद है। मैं हिंदी के अलावा अंग्रेजी भी बोल सकती हूँ।
"""
# audio_array = generate_audio(text_prompt, history_prompt=voice_preset)
audio_array = generate_audio(text_prompt)

# save audio to disk
write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
  
# play text in notebook
#Audio(audio_array, rate=SAMPLE_RATE)