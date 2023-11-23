import cv2
from . import general

"""
date: 2023-11-23 12:37:07
note: just 
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