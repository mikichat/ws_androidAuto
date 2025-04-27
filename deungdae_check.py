# Android 기기의 화면을 캡처하고 이미지 인식을 통해 자동화하는 스크립트

import cv2  # OpenCV 라이브러리 - 이미지 처리를 위해 사용
import numpy as np  # 수치 계산을 위한 넘파이 라이브러리
import os  # 시스템 명령어 실행을 위한 라이브러리
import time  # 시간 지연이 필요할 때 사용
import keyboard  # 키보드 이벤트 감지를 위한 라이브러리
from capture import ScreenCapture  # 화면 캡처 클래스 임포트
from deungdae_tent import DeungdaeTent  # DeungdaeTent 클래스 임포트
from deungdae_skull import DeungdaeSkull  # DeungdaeSkull 클래스 임포트
from deungdae_geom import Deungdaegeom  # Deungdaegeom 클래스 임포트
from deungdae_baltop import Deungdaebaltop  # Deungdaebaltop 클래스 임포트

class Deungdaecheck:
    """
    등대와 텐트 관련 자동화를 처리하는 클래스
    """
    def __init__(self):
        self.buttons = {
            'deungdae': 'images/deungdae_check/deungdae.png',
            'check': 'images/deungdae_check/check.png',
            'nagagi': 'images/deungdae_check/nagagi.png'
        }
        self.screen_capture = ScreenCapture()
            
    def find_image_on_screen(self, template_path, threshold=0.8):
        """
        화면에서 특정 이미지를 찾는 함수
        """
        screenshot = self.screen_capture.capture()
        if screenshot is None:
            print("스크린샷을 가져오는데 실패했습니다.")
            return None
            
        # 흑백으로 변환
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)  # 흑백으로 템플릿 이미지 로드
        if template is None:
            print(f"템플릿 이미지를 로드하는데 실패했습니다: {template_path}")
            return None
            
        print(f"스크린샷 크기: {screenshot_gray.shape[:2]}")
        print(f"템플릿 이미지 크기: {template.shape[:2]}")
        
        try:
            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            
            if len(loc[0]) > 0:
                y, x = loc[0][0], loc[1][0]
                h, w = template.shape[:2]
                center_x = x + w // 2
                center_y = y + h // 2
                print(f"이미지를 찾았습니다. 위치: ({center_x}, {center_y})")
                return (center_x, center_y)
            else:
                print("이미지를 찾을 수 없습니다.")
                return None
        except Exception as e:
            print(f"이미지 매칭 중 오류 발생: {str(e)}")
            return None
            
    def click_if_image_found(self, button_name):
        """
        지정된 버튼 이미지를 화면에서 찾아 클릭하는 함수
        """
        if button_name not in self.buttons:
            print(f"알 수 없는 버튼 이름입니다: {button_name}")
            return False
            
        template_path = self.buttons[button_name]
        # 나가기 버튼은 임계값을 0.5로 낮추고, 나머지는 0.8 유지
        threshold = 0.8 if button_name == 'nagagi' else 0.8
        position = self.find_image_on_screen(template_path, threshold)
        
        if position:
            x, y = position
            os.system(f'adb shell input tap {x} {y}')
            return True
        return False
        
    def click_all_buttons(self):
        """
        모든 버튼을 순서대로 클릭하는 함수
        """
        print("1.체크 등대 버튼 클릭 시도...")
        if self.click_if_image_found('deungdae'):
            print("등대 버튼을 클릭했습니다. 체크를 찾는 중...")
            time.sleep(1)  # 화면 전환을 위한 대기
            
            if self.click_if_image_found('check'):
                print("체크를 클릭했습니다. 나가기 버튼을 찾는 중...")
                # 나가기 버튼이 나타날 때까지 최대 5초 대기
                for _ in range(5):
                    if self.click_if_image_found('nagagi'):
                        print("나가기 버튼을 찾아서 클릭했습니다!")
                        return True
                    time.sleep(1)
                print("나가기 버튼을 찾을 수 없습니다.")
                return False
            else:
                print("체크를 찾을 수 없습니다.")
                return False
        else:
            print("등대 버튼을 찾을 수 없습니다.")
            return False
            
    def run_all_features(self):
        """
        모든 기능을 순서대로 실행하는 함수
        """
        while True:  # 무한 루프를 통해 반복 실행
            print("모든 기능을 수행합니다...")
            
            # 첫 번째 기능 수행
            if self.click_all_buttons():
                print("첫 번째 기능이 성공적으로 완료되었습니다.")
            else:
                print("첫 번째 기능이 실패했습니다. 다음 기능으로 진행합니다.")
            
            # 두 번째 기능 수행
            tent_app = DeungdaeTent()
            if tent_app.click_all_buttons():
                print("두 번째 기능이 성공적으로 완료되었습니다.")
            else:
                print("두 번째 기능이 실패했습니다. 다음 기능으로 진행합니다.")
            
            # 세 번째 기능 수행
            skull_app = DeungdaeSkull()
            if skull_app.click_all_buttons():
                print("세 번째 기능이 성공적으로 완료되었습니다.")
            else:
                print("세 번째 기능이 실패했습니다. 다음 기능으로 진행합니다.")
            
            # 네 번째 기능 수행
            geom_app = Deungdaegeom()
            if geom_app.click_all_buttons():
                print("네 번째 기능이 성공적으로 완료되었습니다.")
            else:
                print("네 번째 기능이 실패했습니다. 다음 기능으로 진행합니다.")

             # 다섯 번째 기능 수행
            baltop_app = Deungdaebaltop()
            if baltop_app.click_all_buttons():
                print("네 번째 기능이 성공적으로 완료되었습니다.")
            else:
                print("네 번째 기능이 실패했습니다. 다음 기능으로 진행합니다.")
            
            # 모든 기능을 수행한 후 잠시 대기
            time.sleep(1)  # 연속 실행 방지를 위한 대기

    def run(self):
        """
        프로그램 실행 함수
        """
        print("프로그램을 종료하려면 'q'를 누르세요.")
        print("모든 기능을 수행하려면 't'를 누르세요.")
        
        while True:
            try:
                if keyboard.is_pressed('q'):  # q를 누르면 프로그램 종료
                    print("프로그램을 종료합니다.")
                    break
                    
                if keyboard.is_pressed('t'):  # t를 누르면 모든 기능 수행
                    print("\n모든 기능을 수행합니다...")
                    self.run_all_features()
                    time.sleep(1)  # 연속 실행 방지를 위한 대기
                    
            except Exception as e:
                print(f"오류 발생: {str(e)}")
                break
                
            time.sleep(0.1)  # CPU 사용량 감소를 위한 짧은 대기

if __name__ == "__main__":
    app = Deungdaecheck()
    app.run()