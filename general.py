import cv2

def is_cap_or_path(input):
    if isinstance(input, cv2.VideoCapture):
        return 'cap'
    if isinstance(input, str):
        return 'path'
    
def get_cap(video_source_path_or_cap):
    '''
    if input is a path to a video, returns a cv2.VideoCapture object
    if input is a cv2.VideoCapture, returns the input

    Parameters
    ----------
    video_source_path_or_cap : string (path to the video) or capture object
        where to find the video

    Returns
    -------
    capture object

    Raises
    ------
    Exception
        if it's not possible to return a cv2.VideoCapture
    '''
    if is_cap_or_path(video_source_path_or_cap) == 'cap':
        return video_source_path_or_cap
    elif is_cap_or_path(video_source_path_or_cap) == 'path':
        # Create a VideoCapture object and read from input file
        cap = cv2.VideoCapture(video_source_path_or_cap)
        # Check if camera opened successfully
        if (cap.isOpened() == False):
            print("Error opening video file")
        return cap
    else:
        raise Exception("Input should be a cv2.VideoCsapture object or a path to a video")