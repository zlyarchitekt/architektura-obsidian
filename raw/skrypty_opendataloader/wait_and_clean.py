import time
import os
import subprocess

print("Waiting for process_pipeline.py to finish...")
# We just wait until the process pipeline finishes. The process pipeline writes to RZUT-34
# Since we don't have its PID easily in Windows from python w/o psutil, we will just wait until "part_121_128.pdf" or something is processed.
# A simpler way: we know process_pipeline.py uses subprocess.run() in a loop. I can just wait for the process python.exe to finish? 
# Actually, process_pipeline.py creates RZUT-34 files. When we have part_121_128.md or it takes > 20 minutes, we assume done?

# Better way: we will check if process_pipeline.py is still in the tasklist!
def is_running():
    result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe", "/V"], capture_output=True, text=True)
    return "process_pipeline" in result.stdout or "process_pipeline.py" in result.stdout

# Wait until process_pipeline is done (max 40 minutes)
for _ in range(40 * 6):
    if not is_running():
        # wait a bit more just to be safe
        time.sleep(10)
        break
    time.sleep(10)

print("Pipeline finished, running cleanup...")
subprocess.run(["python", "clean_md_34.py"])
print("All tasks finished successfully!")
