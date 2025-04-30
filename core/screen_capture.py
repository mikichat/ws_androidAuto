import cv2
import numpy as np
import os
import tempfile
import logging
from datetime import datetime

class ScreenCapture:
    """
    화면 캡처를 처리하는 클래스
    """
    def __init__(self, adb_controller):
        self.adb_controller = adb_controller
        self.logger = logging.getLogger('ScreenCapture')
        self.temp_dir = os.path.join(tempfile.gettempdir(), 'androidAuto')
        os.makedirs(self.temp_dir, exist_ok=True)
        
    def capture(self):
        """
        현재 화면을 캡처하여 OpenCV 이미지로 반환
        
        Returns:
            numpy.ndarray or None: 캡처된 이미지 (BGR 형식) 또는 실패 시 None
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        temp_file = os.path.join(self.temp_dir, f'screenshot_{timestamp}.png')
        
        try:
            success = self.adb_controller.screenshot(temp_file)
            if not success:
                self.logger.error("화면 캡처 실패")
                return None
                
            # 이미지 로드
            image = cv2.imread(temp_file)
            
            # 임시 파일 삭제
            try:
                os.remove(temp_file)
            except:
                pass
                
            return image
        except Exception as e:
            self.logger.error(f"화면 캡처 중 오류 발생: {str(e)}")
            return None
            
    def save_screenshot(self, output_dir, prefix="screenshot"):
        """
        스크린샷을 파일로 저장
        
        Args:
            output_dir (str): 저장할 디렉토리 경로
            prefix (str): 파일명 접두사
            
        Returns:
            str or None: 저장된 파일 경로 또는 실패 시 None
        """
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"{prefix}_{timestamp}.png")
        
        try:
            success = self.adb_controller.screenshot(output_path)
            if success:
                self.logger.info(f"스크린샷 저장 완료: {output_path}")
                return output_path
            else:
                self.logger.error("스크린샷 저장 실패")
                return None
        except Exception as e:
            self.logger.error(f"스크린샷 저장 중 오류 발생: {str(e)}")
            return None
