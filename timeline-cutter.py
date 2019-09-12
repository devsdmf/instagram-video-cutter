
import ffmpeg
import math
import pprint

dd = pprint.PrettyPrinter(indent=4)

INPUT_FILE = 'burn-in-hell.mp4'
OUTPUT_FILE = 'burn-in-hell-insta.mp4'
CHUNK_DURATION = 57 # seconds

probe = ffmpeg.probe(INPUT_FILE)
video_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
dd.pprint(video_info)

total_frames = int(video_info['nb_frames'])
print('Total Frames: {}'.format(total_frames))

frame_rate = eval(video_info['r_frame_rate'])
print('Frame Rate: {}'.format(frame_rate))

frames_per_chunk = math.ceil(CHUNK_DURATION * frame_rate) 
print('Frames per Chunk: {}'.format(frames_per_chunk))

n_chunks = math.ceil(total_frames / frames_per_chunk)
print('Total Chunks: {}'.format(n_chunks))

for i in range(n_chunks):
    start_frame = i * frames_per_chunk
    end_frame = (start_frame + frames_per_chunk) - 1
    end_frame = end_frame if end_frame <= total_frames else total_frames
    print('Chunk #{} starts at {}, ends at {}, size {}'.format(i,start_frame,end_frame,end_frame - start_frame))

