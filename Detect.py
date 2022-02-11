import cv2
import numpy as np
#라즈베리 파이의 경우 아래 주석 해제
#import picamera
from os import listdir
from os.path import isdir, isfile, join
from datetime import datetime
from openpyxl import load_workbook


# 얼굴 인식용 haarcascade 로딩
face_classifier = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')    

# 사용자 얼굴 학습
def train(name):
    data_path = 'faces/' + name + '/'
    #파일만 리스트로 만듬
    face_pics = [f for f in listdir(data_path) if isfile(join(data_path,f))]
    
    Training_Data, Labels = [], []
    
    # 사용자의 사진을 불러옴
    for i, files in enumerate(face_pics):
        image_path = data_path + face_pics[i]
        n = np.fromfile(image_path, dtype=np.uint8)
        img = cv2.imdecode(n, cv2.IMREAD_GRAYSCALE)

        Training_Data.append(np.asarray(img, dtype=np.uint8))
        Labels.append(i)
    # 학습할 데이터(이미지)가 없으면 함수 종료
    if len(Labels) == 0:
        print("학습할 이미지가 없습니다.")
        return None
    # Lables 를 32비트 정수로 변환함
    Labels = np.asarray(Labels, dtype=np.int32)
    # 모델 생성
    model = cv2.face.LBPHFaceRecognizer_create()
    # 학습
    model.train(np.asarray(Training_Data), np.asarray(Labels))
    print(name + " : 모델 학습 완료")

    #학습 모델 리턴
    return model

# 여러 사용자 학습
def trains():
    #faces 폴더의 하위 폴더를 학습
    data_path = 'faces/'
    # 폴더만 색출
    model_dirs = [f for f in listdir(data_path) if isdir(join(data_path,f))]
    
    #학습 모델 저장할 딕셔너리
    models = {}
    # 각 폴더에 있는 얼굴들 학습
    for model in model_dirs:
        print('model :' + model)
        # 학습 시작
        result = train(model)
        # 학습이 안되었다면 패스!
        if result is None:
            continue
        # 학습되었으면 저장
        models[model] = result

    # 학습된 모델 딕셔너리 리턴
    return models   

#얼굴 검출
def face_detector(img, size = 0.5):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray,1.3,5)
        if faces == ():
            return img,[]
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
            roi = img[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200,200))
        return img,roi   #검출된 좌표에 사각 박스 그리고(img), 검출된 부위를 잘라(roi) 전달

# 인식 시작
def run(models):    
    print("출석체크 프로그램 시작")
    #카메라 열기 
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    try:
        while True:
            #카메라로 부터 사진 한장 읽기 
            ret, frame = cap.read()
            # 얼굴 검출 시도 
            image, face = face_detector(frame)
            try:            
                min_score = 999       #예측된 사람일 확률
                min_score_name = ""   #예측된 사람의 이름
            
                #검출된 사진을 흑백으로 변환 
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                #위에서 학습한 모델로 예측시도
                for key, model in models.items():
                    result = model.predict(face)                
                    #result[1] 에 들어가는 값은 신뢰도 임
                    if min_score > result[1]:
                        min_score = result[1]
                        min_score_name = key
                        uid = min_score_name.split("_")[0]
                        uname = min_score_name.split("_")[1]
                # 0에 가까울 수록 정확하다.         
                if min_score < 500:
                    # 정확도 
                    confidence = int(100*(1-(min_score)/300))
                    # 유사도 화면에 표시 
                    display_string = str(confidence)+'% Confidence it is ' + uid
                cv2.putText(image,display_string,(100,120), cv2.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)
                
                #80 보다 크면 동일 인물로 간주해 UnLocked! 
                if confidence > 80:
                    cv2.putText(image,  uid, (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    # 저장할 파일의 경로와 이름지정
                    now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    load_wb = load_workbook("attend.xlsx")
                    load_ws = load_wb['Sheet1']
                    '''
                    for cell in load_ws['C']:  
                        if cell.value == now:
                            pass
                        else:
                    '''
                    write_ws= load_wb.active
                    write_ws.append([uid,uname,now])
                    load_wb.save("attend.xlsx")
                    break      
                    
            #얼굴 검출 안됨 
            except:
                cv2.imshow('Face Cropper', image)
                pass
            #Enter 입력으로 프로그램 종료
            if cv2.waitKey(1)==13:
                break
        #카메라 끄기
        cap.release()
        #열려있는 창 닫기
        cv2.destroyAllWindows()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    # 학습 시작
    models = trains()
    # 시작
    run(models)