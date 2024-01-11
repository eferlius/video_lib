import cv2
import os
from . import general

"""
date: 2023-11-23 12:37:07
note: just collection of useful function to be reused
"""
"""
date: 2024-01-10 18:21:51
note: check for the break 
"""

def function_copy_paste_save_video_with_operations_on_frames(video_source_path_or_cap, 
                                                             video_dest_path, fps = -1, 
                                                             OTHER_PARAMETERS_FOR_YOUR_FUNCTION = None):
    '''
    The video is played and saved while operations are executed 

    Parameters
    ----------
    video_source_path_or_cap : _type_
        _description_
    video_dest_path : _type_
        _description_
    fps : int, optional
        _description_, by default -1
    OTHER_PARAMETERS_FOR_YOUR_FUNCTION : _type_, optional
        _description_, by default None
    '''
    cap = general.get_cap(video_source_path_or_cap)
    # use the one below if copy paste out of video_lib library
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
                    fourcc = general.get_correct_fourcc(ext)
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

def function_copy_paste_save_video_with_operations_on_frames_write_on_frames(video_source_path_or_cap, video_dest_path, 
                                    fps = -1, timestamp_list = None, 
                                    OTHER_PARAMETERS_FOR_YOUR_FUNCTION = None,
                                    string_fmt = 'frame: {:05d} time: {:03.3f}',
                                    origin = (20, 20),
                                    font = cv2.FONT_HERSHEY_SIMPLEX,
                                    fontScale = 1, 
                                    color = (0, 0, 255),
                                    thickness = 1):
    cap = video_lib.general.get_cap(video_source_path_or_cap) # make sure you import video_lib
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if fps == -1:
        fps = cap.get(cv2.CAP_PROP_FPS)
    video_writer_initialized = False
    for i in range(total_frames):
        ret, frame = cap.read()
        if ret == True:
            if not video_writer_initialized:
                    h, w = frame.shape[:2]
                    fourcc = general.get_correct_fourcc(ext)
                    videoWriter = cv2.VideoWriter(video_dest_path, fourcc, fps, (w,h))
                    video_writer_initialized = True
            try:
                # write here all the operations on the image
                # result = foo(frame)      
                if not timestamp_list is None:
                    timestamp = timestamp_list[i]
                else:
                    timestamp = i / fps 
                stringForImage =  string_fmt.format(i, timestamp)
                imgForVideo = cv2.putText(result, stringForImage, origin, font, fontScale, color, thickness, cv2.LINE_AA)
                videoWriter.write(imgForVideo)
            except:
                print('error occurred in the loop at iteration {}'.format(i))
                pass
        else:
            print('not recognized frame at iteration {}'.format(i))
            break
    cap.release()
    videoWriter.release()

def function_copy_paste_play_video_with_operations_on_frames(video_source_path_or_cap, 
                                                             video_dest_path, fps = -1, 
                                                             OTHER_PARAMETERS_FOR_YOUR_FUNCTION = None):
    '''
    The video is played but not saved while operations are executed 

    Parameters
    ----------
    video_source_path_or_cap : _type_
        _description_
    video_dest_path : _type_
        _description_
    fps : int, optional
        _description_, by default -1
    OTHER_PARAMETERS_FOR_YOUR_FUNCTION : _type_, optional
        _description_, by default None
    '''
    cap = general.get_cap(video_source_path_or_cap)
    # use the one below if copy paste out of video_lib library
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