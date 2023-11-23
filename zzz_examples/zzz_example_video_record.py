import os
import sys
sys.path.insert(1, os.path.split(os.path.split(os.getcwd())[0])[0])
sys.path.insert(2, os.path.split(os.getcwd())[0])
import video_lib

video_lib.video_extr.record_video(os.getcwd(), source = 1, max_duration = 10, ext = '.mov')