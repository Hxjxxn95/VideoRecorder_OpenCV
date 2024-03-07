import cv2 as cv
import numpy as np

# 카메라 영상 얻기
cap = cv.VideoCapture(0)

# 동영상 파일 저장을 위한 설정
width = cap.get(cv.CAP_PROP_FRAME_WIDTH) 
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT) 
fps = cap.get(cv.CAP_PROP_FPS)
fourcc = cv.VideoWriter_fourcc(*'mp4v') # 코덱 정의
out = cv.VideoWriter('video.mp4', fourcc, fps, (int(width), int(height))) 

# 미리보기와 녹화 모드 설정
record = False

# 마우스 클릭 상태와 위치 저장
mouse_is_pressed = False
mouse_x, mouse_y = -1, -1

# 마우스 클릭 이벤트 처리 함수
def mouse_callback(event, x, y, flags, param):
    global mouse_is_pressed, mouse_x, mouse_y
    if event == cv.EVENT_LBUTTONDOWN:
        mouse_is_pressed = True
        mouse_x, mouse_y = x, y
    elif event == cv.EVENT_LBUTTONUP:
        mouse_is_pressed = False

# 마우스 클릭 이벤트 설정
cv.namedWindow('frame')
cv.setMouseCallback('frame', mouse_callback)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # 녹화 모드일 때 화면에 빨간색 원 표시
        if record:
            cv.circle(frame, (50, 50), 10, (0, 0, 255), -1)
            out.write(frame)

        # 마우스 클릭 상태일 때, 클릭된 위치 주변 확대
        if mouse_is_pressed:
            roi = frame[mouse_y-50:mouse_y+50, mouse_x-50:mouse_x+50]
            roi = cv.resize(roi, (200, 200))
            frame[0:200, 0:200] = roi

        # 화면에 영상 표시
        cv.imshow('frame', frame)

        # 키 입력 받기
        key = cv.waitKey(1)

        # Space 키로 녹화 모드 전환
        if key == ord(' '):
            record = not record

        # ESC 키로 프로그램 종료
        elif key == 27:
            break
        

    else:
        break




# 작업 완료 후 해제
cap.release()
out.release()
cv.destroyAllWindows()