import whisper
from pathlib import Path
#from whisper.utils import write_srt

model = whisper.load_model("small")
result = model.transcribe("[episode pathname]", language="en")

#audio_basename = Path("/Users/ebarry/Desktop/Regen_Eps/01_Tenth_Planet_4.mp4").stem
#with open(Path("/Users/ebarry/Desktop/Regen_Eps") / (audio_basename + ".srt"), "w", encoding="utf-8") as srt:
#    write_srt(result["segments"], file=srt)

lines = result["text"]

with open(Path("[transcription file pathname]"), "w") as f:
    f.write(lines)