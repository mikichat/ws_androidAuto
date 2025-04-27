import cv2
import numpy as np
import os
import time
import keyboard
from capture import ScreenCapture

class ImageFinder:
    def __init__(self, screen_capture):
        self.screen_capture = screen_capture

    def find_image_on_screen(self, template_path, threshold=0.8):
        """
        화면에서 특정 이미지를 찾는 함수
        """
        screenshot = self.screen_capture.capture()
        if screenshot is None:
            print("스크린샷을 가져오는데 실패했습니다.")
            return None
            
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)  # 컬러로 템플릿 이미지 로드
        if template is None:
            print(f"템플릿 이미지를 로드하는데 실패했습니다: {template_path}")
            return None
            
        print(f"스크린샷 크기: {screenshot.shape[:2]}")
        print(f"템플릿 이미지 크기: {template.shape[:2]}")
        
        try:
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)  # 컬러 이미지를 사용
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

    def click_if_image_found(self, button_name, buttons):
        """
        지정된 버튼 이미지를 화면에서 찾아 클릭하는 함수
        """
        if button_name not in buttons:
            print(f"알 수 없는 버튼 이름입니다: {button_name}")
            return False
            
        template_path = buttons[button_name]
        position = self.find_image_on_screen(template_path)
        
        if position:
            x, y = position
            os.system(f'adb shell input tap {x} {y}')
            return True
        return False

class Deungdaegeom:
    """
    등대와 검 관련 자동화를 처리하는 클래스
    """
    def __init__(self):
        self.buttons = {
            'deungdae': 'images/deungdae_geom/deungdae.png',
            'geom': 'images/deungdae_geom/geom.png',
            'bogi': 'images/deungdae_geom/bogi.png',
            'tamheom': 'images/deungdae_geom/tamheom.png',
            'jeontu': 'images/deungdae_geom/jeontu.png',
            'nagagi': 'images/deungdae_geom/nagagi.png'
        }
        self.screen_capture = ScreenCapture()
        self.image_finder = ImageFinder(self.screen_capture)  # ImageFinder 인스턴스 생성
            
    def find_image_on_screen(self, template_path, threshold=0.8):
        """
        화면에서 특정 이미지를 찾는 함수
        """
        screenshot = self.screen_capture.capture()
        if screenshot is None:
            print("스크린샷을 가져오는데 실패했습니다.")
            return None
            
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)  # 컬러로 템플릿 이미지 로드
        if template is None:
            print(f"템플릿 이미지를 로드하는데 실패했습니다: {template_path}")
            return None
            
        print(f"스크린샷 크기: {screenshot.shape[:2]}")
        print(f"템플릿 이미지 크기: {template.shape[:2]}")
        
        try:
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)  # 컬러 이미지를 사용
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
        return self.image_finder.click_if_image_found(button_name, self.buttons)
        
    def click_all_buttons(self):
        """
        모든 버튼을 순서대로 클릭하는 함수
        """
        # (64, 143) 좌표 클릭
        print("좌표 클릭 (64,143)")
        os.system('adb shell input tap 64 143')
        time.sleep(1)
        print("4.검 등대 버튼 클릭 시도...")
        if self.click_if_image_found('deungdae'):
            print("등대 버튼을 클릭했습니다. 검 을 찾는 중...")
            time.sleep(1)  # 화면 전환을 위한 대기
            
            if self.click_if_image_found('geom'):
                print("검 을 클릭했습니다. 보기 버튼을 찾는 중...")
                # bogi 버튼이 나타날 때까지 최대 5초 대기
                for _ in range(5):
                    if self.click_if_image_found('bogi'):
                        print("보기 버튼을 클릭했습니다. tamheom 버튼을 찾는 중...")
                        # tamheom 버튼이 나타날 때까지 최대 5초 대기
                        for _ in range(5):
                            if self.click_if_image_found('tamheom'):
                                print("탐험 버튼을 클릭했습니다. 전투 버튼을 찾는 중...")
                                # 전투 버튼이 나타날 때까지 최대 5초 대기
                                for _ in range(5):
                                    if self.click_if_image_found('jeontu'):
                                        print("전투 버튼을 클릭했습니다. 나가기 버튼을 찾는 중...")
                                        # 나가기 버튼이 나타날 때까지 최대 7초 대기
                                        for _ in range(7):
                                            if self.click_if_image_found('nagagi'):
                                                print("나가기 버튼을 찾아서 클릭했습니다!")
                                                return True
                                            time.sleep(1)
                                        print("나가기 버튼을 찾을 수 없습니다.")
                                        return False
                                    time.sleep(1)
                                print("전투 버튼을 찾을 수 없습니다.")
                                return False
                            time.sleep(1)
                        print("탐험 버튼을 찾을 수 없습니다.")
                        return False
                    time.sleep(1)
                print("보기 버튼을 찾을 수 없습니다.")
                # 나가기 버튼을 찾아서 클릭
                if self.click_if_image_found('nagagi'):
                    print("나가기 버튼을 찾아서 클릭했습니다!")
                    return True
                else:
                    print("나가기 버튼을 찾을 수 없습니다.")
                    return False
            else:
                print("검 을 찾을 수 없습니다.")
                return False
        else:
            print("등대 버튼을 찾을 수 없습니다.")
            return False
            
    def run(self):
        """
        프로그램 실행 함수
        """
        print("프로그램을 종료하려면 'q'를 누르세요.")
        print("등대, 검, 보기, 탐험, 전투, 나가기 버튼을 순서대로 클릭하려면 't'를 누르세요.")
        print("화면 캡처는 별도의 capture.py 프로그램을 실행하세요.")
        
        while True:
            try:
                if keyboard.is_pressed('q'):  # q를 누르면 프로그램 종료
                    print("프로그램을 종료합니다.")
                    break
                    
                if keyboard.is_pressed('t'):  # t를 누르면 모든 버튼 순서대로 클릭
                    print("\n모든 버튼 클릭을 순서대로 시도합니다...")
                    self.click_all_buttons()
                    time.sleep(1)  # 연속 실행 방지를 위한 대기
                    
            except Exception as e:
                print(f"오류 발생: {str(e)}")
                break
                
            time.sleep(0.1)  # CPU 사용량 감소를 위한 짧은 대기

if __name__ == "__main__":
    app = Deungdaegeom()
    app.run() 