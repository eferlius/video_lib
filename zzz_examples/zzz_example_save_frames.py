import os
import sys
sys.path.insert(1, os.path.split(os.path.split(os.getcwd())[0])[0])
sys.path.insert(2, os.path.split(os.getcwd())[0])
import video_lib

video_source_path_or_cap = r'G:\Shared drives\TableTennis\Tests\20230928\02_preprocessing\mp_pose mc1_mdc0.5_mtc0.3\t01_side_ID8_pose.mp4'
folder_dest_path = r'G:\Shared drives\TableTennis\Tests\20230928\02_preprocessing\frames\mp_pose mc1_mdc0.5_mtc0.3\t01_side_ID8_pose'

start_frame = 8575
end_frame = 8580
video_lib.video_extr.save_frames_from_start_frame_to_end_frame(video_source_path_or_cap, folder_dest_path, start_frame, end_frame, fmt = None)

start_frame = 8400
end_frame = 9000
video_dest_path = r'G:\Shared drives\TableTennis\Tests\20230928\02_preprocessing\frames\mp_pose mc1_mdc0.5_mtc0.3\t01_side_ID8_pose\from{}to{}.mov'.format(start_frame, end_frame)
video_lib.video_extr.save_video_from_start_frame_to_end_frame(video_source_path_or_cap, video_dest_path, 
                                             start_frame, end_frame, fps = -1)

print('done')