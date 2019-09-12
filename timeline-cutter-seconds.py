
import ffmpeg
import math
import pprint
import threading

dd = pprint.PrettyPrinter(indent=4)

INPUT_FILE = 'burn-in-hell.mp4'
OUTPUT_FILE = 'burn-in-hell_{}.mp4'
CHUNK_DURATION = 57 # seconds

probe = ffmpeg.probe(INPUT_FILE)
video_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
dd.pprint(video_info)

total_duration = float(video_info['duration'])
print('Total Duration: {} seconds'.format(total_duration))

n_chunks = math.ceil(total_duration / CHUNK_DURATION)
print('Total Chunks: {}'.format(n_chunks))

def chunk_video(src, start, time, out):
    ffmpeg.input(src, ss=start, t=time).output(out).overwrite_output().run()

threads = list()
for i in range(n_chunks):
    start_time = i * CHUNK_DURATION
    start_time = start_time + 1 if start_time > 0 else start_time

    end_time = start_time + CHUNK_DURATION
    end_time = end_time if end_time <= total_duration else total_duration
    print('Chunk #{} starts at {}, ends at {}, size {}'.format(i,start_time,end_time,end_time - start_time))
    
    x = threading.Thread(target=chunk_video, args=(INPUT_FILE,start_time,CHUNK_DURATION,OUTPUT_FILE.format(i),))
    threads.append(x)
    x.start()

    #ffmpeg.input(INPUT_FILE,ss=start_time,t=CHUNK_DURATION).output(OUTPUT_FILE.format(i)).overwrite_output().run()

for index, thread in enumerate(threads):
    thread.join()

