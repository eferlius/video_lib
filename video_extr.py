import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from . import general
from . import __utils__
"""
date: 2023-10-02 18:01:31
note: 
use save_video if the output is None but saves a video
use save_frames if the output is None but saves a series of frames
use get_frame if the output is a frame
"""



def save_video_write_frame_num_and_time(video_source_path_or_cap, video_dest_path, 
                                    fps = -1, 
                                    timestamp_list = None, 
                                    string_format = 'frame: {:05d} time: {:03.3f}',
                                    origin = (20, 20),
                                    font = cv2.FONT_HERSHEY_SIMPLEX,
                                    fontScale = 1, 
                                    color = (255, 255, 255),
                                    thickness = 1):
    cap = general.get_cap(video_source_path_or_cap)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if timestamp_list:
        assert len(timestamp_list) == total_frames, (
            'len(timestamp_list) is {} while video has {} frames'.format(len(timestamp_list), total_frames))
        
    if fps == -1:
        fps = cap.get(cv2.CAP_PROP_FPS)

    video_writer_initialized = False
    for i in range(total_frames):
        ret, frame = cap.read()
        if ret == True:
            if not video_writer_initialized:
                    h, w = frame.shape[:2]
                    # fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
                    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
                    videoWriter = cv2.VideoWriter(video_dest_path, fourcc, fps, (w,h))
                    video_writer_initialized = True
            try:
                if timestamp_list:
                    timestamp = timestamp_list[i]
                else:
                    timestamp = i / fps 
                stringForImage =  string_format.format(i, timestamp)
                imgForVideo = cv2.putText(frame, stringForImage, origin, font, fontScale, color, thickness, cv2.LINE_AA)
                videoWriter.write(imgForVideo)
            except:
                print('error occurred in the loop at iteration {}'.format(i))
                pass
        else:
            print('not recognized frame at iteration {}'.format(i))
            break
    cap.release()
    videoWriter.release()

def save_video_from_start_frame_to_end_frame(video_source_path_or_cap, video_dest_path, 
                                             start_frame = 0, end_frame = -1,
                                             fps = -1):
    # .mov format for fourcc = cv2.VideoWriter_fourcc('M','J','P','G') 
    cap = general.get_cap(video_source_path_or_cap)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps == -1:
        fps = cap.get(cv2.CAP_PROP_FPS)

    video_writer_initialized = False

    if end_frame == -1:
        end_frame = total_frames
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    for i in range(end_frame-start_frame+1):
        ret, frame = cap.read()
        if ret == True:
            if not video_writer_initialized:
                    h, w = frame.shape[:2]
                    # fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
                    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
                    videoWriter = cv2.VideoWriter(video_dest_path, fourcc, fps, (w,h))
                    video_writer_initialized = True
            try:
                timestamp = i / fps 
                videoWriter.write(frame)
            except:
                print('error occurred in the loop at frame {}'.format(i+start_frame))
                pass
        else:
            print('not recognized frame {}'.format(i+start_frame))
            break
    cap.release()
    videoWriter.release()
    
def save_video_from_folder_of_frames(dir_complete_path, video_dest_path, fps, write_on_frame = False,
                                     string_format = 'frame: {:05d} time: {:03.3f}',
                                     origin = (20, 20),
                                     font = cv2.FONT_HERSHEY_SIMPLEX,
                                     fontScale = 1, 
                                     color = (255, 255, 255),
                                     thickness = 1):
    files_list = __utils__.list_files_in_this_dir(dir_complete_path)

    video_writer_initialized = False

    for f in files_list:
        file_name = os.path.split(f)[1]
            
        frame = cv2.imread(f)
            
        if not video_writer_initialized:
            h, w = frame.shape[:2]
            # fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
            fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
            videoWriter = cv2.VideoWriter(video_dest_path, fourcc, fps, (w,h))
            video_writer_initialized = True
        try:
            if write_on_frame:
                frame = cv2.putText(frame, file_name, origin, font, fontScale, color, thickness, cv2.LINE_AA)
            videoWriter.write(frame)
        except:
            print('error occurred in the loop with file {}'.format(file_name))
            pass
    videoWriter.release()

def save_frames_from_start_frame_to_end_frame(video_source_path_or_cap, folder_dest_path, start_frame = 0, end_frame = -1, fmt = None):
    cap = general.get_cap(video_source_path_or_cap)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if end_frame == -1:
        end_frame = total_frames
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    if not fmt:
        fmt = 'f{'+':0{}'.format(len(str(end_frame)))+'d}'

    for i in range(end_frame-start_frame):
        ret, frame = cap.read()
        if ret == True:
            try: 
                cv2.imwrite(os.path.join(folder_dest_path,fmt.format(i+start_frame)+'.png'), frame)
            except:
                print('error occurred in the loop at frame {}'.format(i+start_frame))
                pass
        else:
            print('not recognized frame {}'.format(i+start_frame))
            break
    cap.release()


def get_frame_at_index(video_source_path_or_cap, frame_num):
    cap = general.get_cap(video_source_path_or_cap)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    assert frame_num < 0 or frame_num > total_frames, (
            'frame {} was required but only frames from 0 to {} are available'.format(frame_num, total_frames))
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    if ret == True:
        return frame
    else:
        return None
    
    
def function_copy_paste_save_video_with_operations_on_frames(video_source_path_or_cap, video_dest_path, fps = -1, OTHER_PARAMETERS_FOR_YOUR_FUNCTION = None):
    cap = general.get_cap(video_source_path_or_cap)
    # cap = video_lib.general.get_cap(video_source_path_or_cap)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
    if fps == -1:
        fps = cap.get(cv2.CAP_PROP_FPS)

    video_writer_initialized = False
    for i in range(total_frames):
        ret, frame = cap.read()
        if ret == True:
            if not video_writer_initialized:
                    h, w = frame.shape[:2]
                    # fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
                    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
                    videoWriter = cv2.VideoWriter(video_dest_path, fourcc, fps, (w,h))
                    video_writer_initialized = True
            try:
                # write here all the operations on the image
                # imgForVideo = foo(frame)
                imgForVideo = frame # cancel this line
                videoWriter.write(imgForVideo)
            except:
                print('error occurred in the loop at iteration {}'.format(i))
                pass
        else:
            print('not recognized frame at iteration {}'.format(i))
            break
    cap.release()
    videoWriter.release()

def function_copy_paste_play_video_with_operations_on_frames(video_source_path_or_cap, video_dest_path, fps = -1, OTHER_PARAMETERS_FOR_YOUR_FUNCTION = None):
    cap = general.get_cap(video_source_path_or_cap)
    # cap = video_lib.general.get_cap(video_source_path_or_cap)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
    if fps == -1:
        fps = cap.get(cv2.CAP_PROP_FPS)
        
    for i in range(total_frames):
        ret, frame = cap.read()
        if ret == True:
            try:
                # write here all the operations on the image
                # imgForVideo = foo(frame)
                imgForVideo = frame # cancel this line
            except:
                print('error occurred in the loop at iteration {}'.format(i))
                pass
        else:
            print('not recognized frame at iteration {}'.format(i))
            break
    cap.release()


def record_video(saving_path, source = 0, video_freq = 30, max_frames = 1800, 
                max_duration = 60, save_csv = True, display_video = True, 
                print_execution = True, write_on_frame = True,
                string_format = 'frame: {:05d} time: {:03.3f}',
                origin = (20, 20), font = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale = 1, color = (255, 255, 255), thickness = 1):
    # initialize capture
    capture = cv2.VideoCapture(source)
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    # fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

    saving_path_folder = os.path.join(saving_path,  __utils__.this_moment())
    os.makedirs(saving_path_folder, exist_ok = True)

    # initialize video writer
    video_saving_path = os.path.join(saving_path_folder, 'video.mp4')
    video_writer = cv2.VideoWriter(video_saving_path, fourcc, video_freq, (frame_width, frame_height))  
    
    # initialize csv header
    if save_csv:
        csv_raw = os.path.join(saving_path_folder, 'times.csv')
        init = ['frame', 'time']
        __utils__.write_row_csv(csv_raw, init)
    
    counter = -1
    elapsed = 0
    t = __utils__.Timer()
    
    while (elapsed <= max_duration and counter <= max_frames) :
        counter+=1
        ret, orig_frame = capture.read()
        orig_frame = cv2.flip(orig_frame, 1)
        elapsed = t.elap(printTime=False)
        elapsed = np.around(elapsed, 3)

        if ret:
            if write_on_frame:
                stringForImage =  string_format.format(counter, elapsed)
                frame = cv2.putText(orig_frame, stringForImage, origin, font, fontScale, color, thickness, cv2.LINE_AA)
            else:
                frame = orig_frame

            video_writer.write(frame)
            if display_video:    
                cv2.imshow('press esc to terminate', frame)
            if save_csv:
                __utils__.write_row_csv(csv_raw, [counter, elapsed])
            if print_execution:
                print(string_format.format(counter, elapsed))
        # press esc to exit
        if cv2.waitKey(1) == 27:
            break

    elapsed = t.stop()
    print('{c:.0f} frames in {e:.2f} seconds'.format(c=counter, e=elapsed))
    print('{f:.2f} Hz'.format(f=(counter/elapsed)))

    capture.release()
    video_writer.release()
    cv2.destroyAllWindows()

    
    

    


