import sequencer as sq
import time
import signal
import sonic_api as sapi

keep_listening = True
sequencer = sq.Sequencer()
sequencer.start()

def handler(signum, frame):
    msg = "Ctrl-c was pressed. Closing the app ..."
    print(msg, end="", flush=True)
    keep_listening = False
    sequencer.stop()
    exit()
 
signal.signal(signal.SIGINT, handler)

# sequencer.set_bpm(120)
# sequencer.set_note(0, 3)
# sequencer.set_note(1, 5)
# sequencer.set_note(2, 7)
# sequencer.set_note(3, 2)

sonicApi = sapi.SonicApi("mqtt.devbit.be", "sonic")
sonicApi.connect()

while keep_listening:
  time.sleep(0.1)
  sonicApi.request_next_device_update()
  print(sonicApi.get_registered_devices())

  devices = sonicApi.get_registered_devices()
  notes = sq.notes
  noteIndices = []
  for device in devices:
    if device.distance > 0:
      distance = min([device.distance, 100])
      index = int(len(notes) * distance / 100.0)
      noteIndices.append(index)
  
  sequencer.set_sequence(noteIndices)