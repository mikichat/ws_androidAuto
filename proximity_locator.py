import cv2
import numpy as np
import os
import time
import keyboard
from capture import ScreenCapture

class Baltop:
    def __init__(self):
        self.buttons = {
            'baltop': 'images/deungdae_geom/geom.png'
        }
        self.screen_capture = ScreenCapture()

    def find_closest_positions(self, template_path, threshold=0.9):
        """
        비교 대상 경로를 받아서 스크린샷에서 이미지를 찾고,
        찾은 픽셀의 거리로 그룹화한 후, 각 그룹에서 가장 작은 x, y 값을 반환하는 함수
        """
        print(f"find_closest_positions 호출: {template_path}")  # 호출 로그 추가
        screenshot = self.screen_capture.capture()
        if screenshot is None:
            print("스크린샷을 가져오는데 실패했습니다.")
            return None
            
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)  # 컬러로 템플릿 이미지 로드
        if template is None:
            print(f"템플릿 이미지를 로드하는데 실패했습니다: {template_path}")
            return None

        print(f"스크린샷 크기: {screenshot.shape[:2]}, 템플릿 이미지 크기: {template.shape[:2]}")  # 디버깅 정보 추가
            
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        
        positions = []
        for pt in zip(*loc[::-1]):  # 모든 위치를 찾기
            positions.append(pt)
        
        if positions:
            print(f"이미지를 찾았습니다. 위치들: {positions}")
            print(f"발톱 이미지 개수: {len(positions)}")  # 개수 출력
            
            # 5픽셀 이하의 가까운 거리 그룹화
            groups = []
            for pos in positions:
                found_group = False
                for group in groups:
                    # 그룹의 첫 번째 점과의 거리 계산
                    if np.linalg.norm(np.array(pos) - np.array(group[0])) <= 5:
                        group.append(pos)
                        found_group = True
                        break
                if not found_group:
                    groups.append([pos])  # 새로운 그룹 생성

            # 각 그룹에서 가장 작은 x, y 값 찾기
            closest_positions = []
            for group in groups:
                closest_position = min(group, key=lambda p: (p[0], p[1]))
                closest_positions.append(closest_position)
                print(f"그룹={group}의 가장 작은 x, y 값: {closest_position}")  # 출력
            
            return closest_positions
        else:
            print("이미지를 찾을 수 없습니다.")
            return None

# 사용 예시
if __name__ == "__main__":
    baltop_instance = Baltop()
    closest_positions = baltop_instance.find_closest_positions(baltop_instance.buttons['baltop'])
    print(f"가장 가까운 위치들: {closest_positions}")
    



