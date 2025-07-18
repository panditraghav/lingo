import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
import struct
from uuid import uuid4
import os
import mimetypes

load_dotenv("../.env")

def save_binary_file(file_name: str, data: bytes | None):
    f = open(file_name, "wb")
    f.write(data or bytes())
    f.close()
    print(f"File saved to to: {file_name}")


def generate():
    client = genai.Client(
            api_key=os.environ.get("GOOGLE_AI_STUDIO_KEY"),
        )

    prompt = """Rise and shine, let's make today awesome!"""

    model = "gemini-2.5-flash-preview-tts"
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=[
            "audio",
        ],
        speech_config= types.SpeechConfig(
            voice_config = types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Zephyr"))
        )
    )

    chunk = client.models.generate_content(model = model, contents = prompt, config = generate_content_config)

    if (
        chunk.candidates is None
        or chunk.candidates[0].content is None
        or chunk.candidates[0].content.parts is None
    ):
        print("No audio")
        return
    
    if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
        file_name = f"{int(time.time())}-{uuid4()}"

        inline_data = chunk.candidates[0].content.parts[0].inline_data

        data_buffer = inline_data.data
        file_extension = mimetypes.guess_extension(inline_data.mime_type or "")

        if file_extension is None:
            file_extension = ".wav"
            data_buffer = convert_to_wav(inline_data.data or bytes(), inline_data.mime_type or "")

        print("Saving ", file_name)
        save_binary_file(f"{file_name}{file_extension}", data_buffer)


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Generates a WAV file header for the given audio data and parameters.

    Args:
        audio_data: The raw audio data as a bytes object.
        mime_type: Mime type of the audio data.

    Returns:
        A bytes object representing the WAV file header.
    """
    print("Converting to wav")
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample or 0 // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate or 0 * block_align
    chunk_size = 36 + data_size  # 36 bytes for header fields before data chunk size

    print(
        "parameters: ", parameters,
        "bits_per_sample: ", bits_per_sample,
        "sample_rate: ", sample_rate,
        "num_channels: ", num_channels,
        "data_size: ", data_size,
        "bytes_per_sample: ", bytes_per_sample,
        "block_align: ", block_align,
        "byte_rate: ", byte_rate,
        "chunk_size: ", chunk_size,
    )

    # http://soundfile.sapp.org/doc/WaveFormat/

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",          # ChunkID
        chunk_size,       # ChunkSize (total file size - 8 bytes)
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size (16 for PCM)
        1,                # AudioFormat (1 for PCM)
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size (size of audio data)
    )
    return header + audio_data

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    """Parses bits per sample and rate from an audio MIME type string.

    Assumes bits per sample is encoded like "L16" and rate as "rate=xxxxx".

    Args:
        mime_type: The audio MIME type string (e.g., "audio/L16;rate=24000").

    Returns:
        A dictionary with "bits_per_sample" and "rate" keys. Values will be
        integers if found, otherwise None.
    """
    bits_per_sample = 16
    rate = 24000

    # Extract rate from parameters
    parts = mime_type.split(";")
    for param in parts: # Skip the main type part
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                # Handle cases like "rate=" with no value or non-integer value
                pass # Keep rate as default
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass # Keep bits_per_sample as default if conversion fails

    return {"bits_per_sample": bits_per_sample, "rate": rate}

if __name__ == "__main__":
    generate()
