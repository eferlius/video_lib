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

# .mov format for fourcc = cv2.VideoWriter_fourcc('M','J','P','G') 
"""

def save_video_write_frame_num_and_time(video_source_path_or_cap, video_dest_path, 
                                    fps = -1, 
                                    timestamp_list = None, 
                                    string_fmt = 'frame: {:05d} time: {:03.3f}',
                                    origin = (20, 20),
                                    font = cv2.FONT_HERSHEY_SIMPLEX,
                                    fontScale = 1, 
                                    color = (255, 255, 255),
                                    thickness = 1):
    '''
    Save a video in a given path writing on each frame information 
    about the number of frame and the elapsed time

    Parameters
    ----------
    video_source_path_or_cap : string (path to the video) or capture object
        where to find the video
    video_dest_path : string (path to the video)
        where to save the video
    fps : int, optional
        fps to record the output video.
        By default -1, which means the fps of the original video are used
    timestamp_list : list, optional
        list containing the elapsed time with respect to time 0 of each frame.
        By default None, which means the elapsed time is taken from fps and not from the list
    string_fmt : str, optional
        format of the string that is written on the frames, by default 'frame: {:05d} time: {:03.3f}'
    origin : tuple of 2 int, optional
        position of the origin (x, y) of the text, by default (20, 20)
    font : _type_, optional
        _description_, by default cv2.FONT_HERSHEY_SIMPLEX
    fontScale : int, optional
        _description_, by default 1
    color : tuple, optional
        _description_, by default (255, 255, 255)
    thickness : int, optional
        _description_, by default 1
    '''
    cap = general.get_cap(video_source_path_or_cap)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if not timestamp_list is None:
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
                    fourcc = general.get_correct_fourcc(os.path.splitext(video_dest_path)[1])
                    videoWriter = cv2.VideoWriter(video_dest_path, fourcc, fps, (w,h))
                    video_writer_initialized = True
            try:
                if not timestamp_list is None:
                    timestamp = timestamp_list[i]
                else:
                    timestamp = i / fps 
                stringForImage =  string_fmt.format(i, timestamp)
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
    '''
    Save video in a given path from start frame to end frame

    Parameters
    ----------
    video_source_path_or_cap : string (path to the video) or capture object
        where to find the video
    video_dest_path : string (path to the video)
        where to save the video
    start_frame : int, optional
        by default 0
    end_frame : int, optional
        by default -1, corresponds to the last frame
    fps : int, optional
        fps to record the output video.
        By default -1, which means the fps of the original video are used
    '''
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
                    fourcc = general.get_correct_fourcc(ext)
                    videoWriter = cv2.VideoWriter(video_dest_path, fourcc, fps, (w,h))
                    video_writer_initialized = True
            try:
                videoWriter.write(frame)
            except:
                print('error occurred in the loop at frame {}'.format(i+start_frame))
                pass
        else:
            print('not recognized frame {}'.format(i+start_frame))
            break
    cap.release()
    videoWriter.release()
    
def save_video_from_folder_of_frames(dir_complete_path, video_dest_path, fps, 
                                     write_on_frame = False,
                                     origin = (20, 20),
                                     font = cv2.FONT_HERSHEY_SIMPLEX,
                                     fontScale = 1, 
                                     color = (255, 255, 255),
                                     thickness = 1):
    '''
    Save video in a given path creating a sequence of the frames in a given folder

    Parameters
    ----------
    dir_complete_path : string
        path to the directory containing the frames
    video_dest_path : string (path to the video)
        where to save the video
    fps : int
        fps the video should be saved
    write_on_frame : bool, optional
        if writing on each frame the name of the corresponding image, by default False
    origin : tuple of 2 int, optional
        position of the origin (x, y) of the text, by default (20, 20)
    font : _type_, optional
        _description_, by default cv2.FONT_HERSHEY_SIMPLEX
    fontScale : int, optional
        _description_, by default 1
    color : tuple, optional
        _description_, by default (255, 255, 255)
    thickness : int, optional
        _description_, by default 1
    '''
    files_list = __utils__.list_files_in_this_dir(dir_complete_path)

    video_writer_initialized = False

    for f in files_list:
        file_name = os.path.split(f)[1]
            
        frame = cv2.imread(f)
            
        if not video_writer_initialized:
            h, w = frame.shape[:2]
            fourcc = general.get_correct_fourcc(os.path.splitext(video_dest_path)[1])
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

def save_frames_from_start_frame_to_end_frame(video_source_path_or_cap, 
                                              folder_dest_path, start_frame = 0, 
                                              end_frame = -1, every_n_frames = 1, string_fmt = None,
                                              file_extension = '.png'):
    '''
    Save all the frames contained in a video in single images

    Parameters
    ----------
    dir_complete_path : string
        path to the directory containing the frames
    video_dest_path : string (path to the folder)
        where to save the single frames
    start_frame : int, optional
        if negative, takes the last (-)n frames
        by default 0
    end_frame : int, optional
        by default -1, corresponds to the last frame
    every_n_frames : int, optional
        by default 1, corresponds to the number of frames skipped at every iteration
    string_fmt : string, optional
        how to format the string to create the name of each file.
        Should have a '{}' to insert the  frame number
        by default None, creates the frame num with filename_f{frame_num}
    file_extension : string, optional
        extension of the saved frames, by default '.png'
    '''
    cap = general.get_cap(video_source_path_or_cap)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if start_frame < 0:
        start_frame = total_frames+start_frame
    if end_frame < 0:
        end_frame = total_frames+end_frame

    if end_frame == -1:
        end_frame = total_frames
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    if not string_fmt:
        # take into account leading zeros
        string_fmt = 'f{'+':0{}'.format(len(str(end_frame)))+'d}'

    if every_n_frames < 84:
        for i in range(end_frame-start_frame):
            ret, frame = cap.read()
            if i%every_n_frames != 0:
                continue
            if ret == True:
                try: 
                    cv2.imwrite(os.path.join(folder_dest_path,string_fmt.format(i+start_frame)+file_extension), frame)
                except:
                    print('error occurred in the loop at frame {}'.format(i+start_frame))
                    pass
            else:
                print('not recognized frame {}'.format(i+start_frame))
                break
    else:
        for i in range(end_frame-start_frame):
            if i%every_n_frames != 0:
                continue
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if ret == True:
                    try: 
                        cv2.imwrite(os.path.join(folder_dest_path,string_fmt.format(i+start_frame)+file_extension), frame)
                    except:
                        print('error occurred in the loop at frame {}'.format(i+start_frame))
                        pass
                else:
                    print('not recognized frame {}'.format(i+start_frame))
                    break

    cap.release() 


def get_frame_at_index(video_source_path_or_cap, frame_num):
    '''
    Returns the image at a given index of the video

    Parameters
    ----------
    dir_complete_path : string
        path to the directory containing the frames
    frame_num : int
        index of the frame

    Returns
    -------
    frame or None
        frame of the video at the given index
        matrix width*height*3 or matrix width*height*1
    
    '''
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


def record_video(saving_folder, source = 0, video_freq = 30, 
                 ext = '.mov', max_frames = 1800, 
                max_duration = 60, save_csv = True, display_video = True, 
                print_execution = True, write_on_frame = True,
                string_fmt = 'frame: {:05d} time: {:03.3f}',
                origin = (20, 20), font = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale = 1, color = (255, 255, 255), thickness = 1):
    '''
    Records a video from the specified source, saving it in the path specified 
    in saving_folder with the name video.ext

    Parameters
    ----------
    saving_folder : string
        path to the folder where the video is saved
    source : int, optional
        where to get the video from, by default 0
    video_freq : int, optional
        theorical video frequency of frame saving, by default 30
    ext : string, optional
        extension of the saved video, by default '.mov'.
    max_frames : int, optional
        max number of frames in the video, by default 1800
    max_duration : int, optional
        max duratoin of the video in seconds, by default 60
    save_csv : bool, optional
        if saving a csv file containg the times of recording of each frame, by default True
    display_video : bool, optional
        if displaying the video while recording, by default True
    print_execution : bool, optional
        if printing coiunter and elasped time, by default True
    write_on_frame : bool, optional
        if writing on the frame, by default True
    string_fmt : str, optional
        format of the string that is written on the frames, by default 'frame: {:05d} time: {:03.3f}'
    origin : tuple of 2 int, optional
        position of the origin (x, y) of the text, by default (20, 20)
    font : _type_, optional
        _description_, by default cv2.FONT_HERSHEY_SIMPLEX
    fontScale : int, optional
        _description_, by default 1
    color : tuple, optional
        _description_, by default (255, 255, 255)
    thickness : int, optional
        _description_, by default 1
    '''
    # initialize capture
    capture = cv2.VideoCapture(source)
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    fourcc = general.get_correct_fourcc(ext)

    saving_path_folder = os.path.join(saving_folder,  __utils__.this_moment())
    os.makedirs(saving_path_folder, exist_ok = True)

    # initialize video writer
    video_saving_path = os.path.join(saving_path_folder, 'video'+ext)
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
                stringForImage =  string_fmt.format(counter, elapsed)
                frame = cv2.putText(orig_frame, stringForImage, origin, font, fontScale, color, thickness, cv2.LINE_AA)
            else:
                frame = orig_frame

            video_writer.write(frame)
            if display_video:    
                cv2.imshow('press esc to terminate', frame)
            if save_csv:
                __utils__.write_row_csv(csv_raw, [counter, elapsed])
            if print_execution:
                print(string_fmt.format(counter, elapsed))
        # press esc to exit
        if cv2.waitKey(1) == 27:
            break

    elapsed = t.stop()
    print('{c:.0f} frames in {e:.2f} seconds'.format(c=counter, e=elapsed))
    print('{f:.2f} Hz'.format(f=(counter/elapsed)))

    capture.release()
    video_writer.release()
    cv2.destroyAllWindows()

    
    

    


