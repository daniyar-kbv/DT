import cv2
import numpy as np


def draw_boinding_box(frame, row, c=0.002):
    height = frame.shape[0]
    width = frame.shape[1]
    thickness = int(width * c)
    width_offset = int(width * 0.025)
    height_offset = int(height * 0.013)

    xmin = int(row['xmin'])
    xmax = int(row['xmax'])
    ymin = int(row['ymin'])
    ymax = int(row['ymax'])
    classname = row['name'].replace('rotation', '')
    confidence = str(round(row['confidence'] * 100, 2))

    frame = np.array(frame)

    frame = cv2.rectangle(img=frame,
                          pt1=(xmin, ymin),
                          pt2=(xmax, ymax),
                          color=(0, 0, 255),
                          thickness=thickness)

    frame = cv2.putText(img=frame,
                        text=f'{classname}: {confidence}%',
                        org=(xmin, ymin - height_offset),
                        fontFace=cv2.FONT_HERSHEY_PLAIN,
                        fontScale=thickness,
                        color=(0, 0, 255),
                        thickness=thickness)

    if type(frame) == np.ndarray:
        return frame
    else:
        return cv2.UMat.get(frame)


def detect(frame, model):
    results = model(frame)
    results = results.pandas().xyxy[0]
    for row in range(results.shape[0]):
        frame = draw_boinding_box(frame, results.iloc[row])
    return frame, results[results['name'] == 'eye_closedrotation'].shape[0] > 0, \
           results[results['name'] == 'yawnrotation'].shape[0] > 0


def process(filename, model):
    cap = cv2.VideoCapture(filename)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    filename_parts = filename.split('.')
    filename_out = f'{filename_parts[0]}_out.{filename_parts[1]}'

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video_writer = cv2.VideoWriter(filename_out, fourcc, 30, (width, height))

    warning = False
    closed_count = 0

    while True:
        ret, frame = cap.read()
        if ret:
            frame = frame[:, :, ::-1]
            frame, is_closed, is_yawn = detect(frame, model)

            if is_closed:
                closed_count += 1
            else:
                closed_count = 0

            if is_yawn:
                warning = True

            if warning and closed_count <= 30:
                frame = cv2.putText(img=frame,
                                    text=f'WARNING',
                                    org=(20, 200),
                                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=10,
                                    color=(255, 255, 0),
                                    thickness=10)

            if closed_count > 30:
                frame = cv2.putText(img=frame,
                                    text=f'ALARM',
                                    org=(20, 200),
                                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=10,
                                    color=(255, 0, 0),
                                    thickness=10)

            frame = frame[:, :, ::-1]

            video_writer.write(frame)
        else:
            break

    cap.release()

    return filename_out
