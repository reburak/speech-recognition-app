import json
import pyaudio
from vosk import Model, KaldiRecognizer
import asyncio
import websockets

async def recognize_speech(websocket, path):
    # VOSK modelini yükle
    model = Model("vosk-model-small-tr")
    recognizer = KaldiRecognizer(model, 16000)

    # PyAudio ayarları
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Ses tanıma sistemi başlatıldı. Konuşmaya başlayabilirsiniz...")

    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_json = json.loads(result)
                recognized_text = result_json.get("text", "")
                print(f"Tanınan metin: {recognized_text}")
                if recognized_text.strip() != "":
                    await websocket.send(json.dumps({"type": "final", "text": recognized_text + " "}))
                    break  # Tanınan metin sonrası döngüyü sonlandır

            else:
                partial_result = recognizer.PartialResult()
                partial_result_json = json.loads(partial_result)
                partial_text = partial_result_json.get("partial", "")
                print(f"Geçici metin: {partial_text}")

    except Exception as e:
        print(f"Exception: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

start_server = websockets.serve(recognize_speech, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
