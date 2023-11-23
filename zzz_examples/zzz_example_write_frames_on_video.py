import pandas as pd
import os
import sys
sys.path.insert(1, os.path.split(os.path.split(os.getcwd())[0])[0])
sys.path.insert(2, os.path.split(os.getcwd())[0])
import video_lib

FOLDER = r'2023-11-23 13-10-09'
VIDEO_NAME = 'video.mov'
CSV_NAME = 'times.csv'


video_file = os.path.join(os.getcwd(), FOLDER, VIDEO_NAME)
video_file_dest = os.path.join(os.getcwd(), FOLDER, VIDEO_NAME.replace('video', 'video_write'))
video_file_dest2 = os.path.join(os.getcwd(), FOLDER, VIDEO_NAME.replace('video', 'video_write2'))
csv_file = os.path.join(os.getcwd(), FOLDER, CSV_NAME)

df_timestamp = pd.read_csv(csv_file)

video_lib.video_extr.save_video_write_frame_num_and_time(video_file, video_file_dest, timestamp_list = df_timestamp['time'].values, origin = (20, 50))
video_lib.video_extr.save_video_write_frame_num_and_time(video_file_dest, video_file_dest2, timestamp_list = None, origin = (20, 80))