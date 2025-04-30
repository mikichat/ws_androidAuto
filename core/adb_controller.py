mport os
import subprocess
import time
import logging

class ADBController:
    """
    ADB 명령을 통해 Android 기기를 제어하는 클래스
    """
    def __init__(self, device_id=None):
        self.device_id = device_id
        self.logger = logging.getLogger('ADBController')
        
    def _build_command(self, command):
        """ADB 명령어 구성"""
        base_cmd = 'adb'
        if self.device_id:
            base_cmd += f' -s {self.device_id}'
        return f'{base_cmd} {command}'
        
    def execute_command(self, command, capture_output=False):
        """
        ADB 명령 실행
        
        Args:
            command (str): 실행할 ADB 명령어
            capture_output (bool): 출력 결과를 반환할지 여부
            
        Returns:
            str or None: capture_output이 True인 경우 명령 출력, 그렇지 않으면 None
        """
        full_command = self._build_command(command)
        self.logger.debug(f"실행 명령어: {full_command}")
        
        try:
            if capture_output:
                result = subprocess.check_output(full_command, shell=True, stderr=subprocess.STDOUT, text=True)
                return result.strip()
            else:
                subprocess.run(full_command, shell=True, check=True)
                return None
        except subprocess.CalledProcessError as e:
            self.logger.error(f"ADB 명령 실행 오류: {str(e)}")
            if capture_output:
                return e.output.strip() if hasattr(e, 'output') else None
            return None
            
    def tap(self, x, y):
        """화면 좌표 탭"""
        self.logger.info(f"탭 동작: ({x}, {y})")
        return self.execute_command(f'shell input tap {x} {y}')
        
    def swipe(self, x1, y1, x2, y2, duration=300):
        """
        화면 스와이프
        
        Args:
            x1, y1: 시작 좌표
            x2, y2: 종료 좌표
            duration: 스와이프 시간(ms)
        """
        self.logger.info(f"스와이프 동작: ({x1}, {y1}) → ({x2}, {y2}), 시간: {duration}ms")
        return self.execute_command(f'shell input swipe {x1} {y1} {x2} {y2} {duration}')
        
    def key_event(self, keycode):
        """키 이벤트 전송"""
        self.logger.info(f"키 이벤트 전송: {keycode}")
        return self.execute_command(f'shell input keyevent {keycode}')
        
    def back(self):
        """뒤로 가기 버튼"""
        self.logger.info("뒤로 가기 버튼 누름")
        return self.key_event(4)
        
    def home(self):
        """홈 버튼"""
        self.logger.info("홈 버튼 누름")
        return self.key_event(3)
        
    def screenshot(self, output_path):
        """
        스크린샷 캡처 및 저장
        
        Args:
            output_path (str): 저장할 경로
            
        Returns:
            bool: 성공 여부
        """
        try:
            self.logger.info(f"스크린샷 캡처: {output_path}")
            # 임시 파일로 스크린샷 저장
            remote_path = '/sdcard/screenshot.png'
            self.execute_command(f'shell screencap -p {remote_path}')
            # 기기에서 로컬로 가져오기
            self.execute_command(f'pull {remote_path} {output_path}')
            # 기기의 임시 파일 삭제
            self.execute_command(f'shell rm {remote_path}')
            return True
        except Exception as e:
            self.logger.error(f"스크린샷 캡처 오류: {str(e)}")
            return False
            
    def check_device(self):
        """
        연결된 디바이스 확인
        
        Returns:
            bool: 디바이스 연결 여부
        """
        try:
            output = self.execute_command('devices', capture_output=True)
            if self.device_id:
                return self.device_id in output
            else:
                # 'device' 문자열이 포함된 라인이 있는지 확인 (연결된 디바이스)
                return '\tdevice' in output
        except Exception as e:
            self.logger.error(f"디바이스 연결 확인 오류: {str(e)}")
            return False