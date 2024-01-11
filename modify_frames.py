import cv2
import numpy as np
import os
from . import general


def validate_coordinates(tl_x, tl_y, br_x, br_y):
    """
    Validate and swap coordinates if necessary to ensure tl_x < br_x and tl_y < br_y.

    Parameters:
    - tl_x, tl_y: Top-left coordinates.
    - br_x, br_y: Bottom-right coordinates.

    Returns:
    - Tuple (tl_x, tl_y, br_x, br_y) with validated and possibly swapped coordinates.
    """
    if tl_x > br_x:
        tl_x, br_x = br_x, tl_x
    if tl_y > br_y:
        tl_y, br_y = br_y, tl_y

    return tl_x, tl_y, br_x, br_y


def color_pixels(image, tl, br, colour=['0,0,0'], in_out='out'):
    """
    Color pixels inside or outside a specified rectangle in an image.

    Parameters:
    - image: NumPy array representing the image.
    - tl: Tuple (x, y) representing the top-left coordinates of the rectangle.
    - br: Tuple (x, y) representing the bottom-right coordinates of the rectangle.
    - color: Tuple (B, G, R) representing the color to use for coloring pixels.
    - inside: Boolean flag. If True, color pixels inside the rectangle. If False, color pixels outside.

    Returns:
    - Modified image with pixels colored accordingly.
    """
    h, w, _ = image.shape
    mask = np.zeros((h, w), dtype=np.uint8)

    tl_x, tl_y, br_x, br_y = validate_coordinates(tl[0], tl[1], br[0], br[1])

    # Check for NaN values in tl or br coordinates
    if np.isnan(tl_x) or np.isnan(tl_y) or np.isnan(br_x) or np.isnan(br_y):
        # If NaN values are present, color the entire frame
        image[:, :] = colour
    else:
        if in_out == 'in':
            mask[tl[1]:br[1] + 1, tl[0]:br[0] + 1] = 1
        elif in_out == 'out':
            mask[:tl_y, :] = 1
            mask[br_y + 1:, :] = 1
            mask[:, :tl_x] = 1
            mask[:, br_x + 1:] = 1

        image[mask == 1] = colour

    return image



def save_video_color_pixels_write_on_frames(video_source_path_or_cap, video_dest_path,
                                                        df_vertices, colour = [0,0,0], in_out = 'out', 
                                                        fps = -1, timestamp_list = None, 
                                                        string_fmt = 'frame: {:05d} time: {:03.3f}',
                                                        origin = (20, 20),
                                                        font = cv2.FONT_HERSHEY_SIMPLEX,
                                                        fontScale = 1, 
                                                        color = (0, 0, 255),
                                                        thickness = 1):
    cap = general.get_cap(video_source_path_or_cap) # make sure you import video_lib
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if fps == -1:
        fps = cap.get(cv2.CAP_PROP_FPS)

    tl_x = df_vertices['tl_x'].values
    tl_y = df_vertices['tl_y'].values
    br_x = df_vertices['br_x'].values
    br_y = df_vertices['br_y'].values
        
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
                # write here all the operations on the image
                result = color_pixels(frame, [int(tl_x[i]), int(tl_y[i])], [int(br_x[i]), int(br_y[i])], colour = colour, in_out = in_out)  
                if not timestamp_list is None:
                    timestamp = timestamp_list[i]
                else:
                    timestamp = i / fps 
                stringForImage =  string_fmt.format(i, timestamp)
                imgForVideo = cv2.putText(result, stringForImage, origin, font, fontScale, color, thickness, cv2.LINE_AA)
                videoWriter.write(imgForVideo)
            except:
                print('error occurred in the loop at iteration {}'.format(i))
                # # write another time the image
                # videoWriter.write(imgForVideo)
                pass
        else:
            print('not recognized frame at iteration {}'.format(i))
            # # write another time the image
            # videoWriter.write(imgForVideo)
            pass
    cap.release()
    videoWriter.release()