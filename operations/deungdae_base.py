import time
import logging
import abc

class DeungdaeOperation(abc.ABC):
    """
    등대 작업의 기본 클래스 (추상 클래스)
    모든 등대 관련 작업 클래스의 기본이 되는 추상 클래스입니다.
    """
    def __init__(self, adb_controller, image_finder, button_images, wait_time=1.0):
        self.adb_controller = adb_controller
        self.image_finder = image_finder
        self.button_images = button_images
        self.wait_time = wait_time  # 버튼 클릭 후 기본 대기 시간
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def click_if_image_found(self, button_name, timeout=5, wait_after=None):
        """
        지정된 버튼 이미지를 화면에서 찾아 클릭하는 함수
        
        Args:
            button_name (str): 버튼 이름
            timeout (int): 이미지를 찾을 때까지 대기할 최대 시간(초)
            wait_after (float, optional): 클릭 후 대기 시간, None이면 기본값 사용
            
        Returns:
            bool: 이미지를 찾아 클릭했으면 True, 그렇지 않으면 False
        """
        if button_name not in self.button_images:
            self.logger.error(f"알 수 없는 버튼 이름입니다: {button_name}")
            return False
            
        template_path = self.button_images[button_name]
        
        end_time = time.time() + timeout
        while time.time() < end_time:
            result = self.image_finder.find_image_on_screen(template_path)
            if result:
                x, y, _ = result
                self.logger.info(f"'{button_name}' 버튼을 찾아 ({x}, {y}) 좌표 클릭")
                self.adb_controller.tap(x, y)
                
                # 클릭 후 대기
                wait_time = wait_after if wait_after is not None else self.wait_time
                if wait_time > 0:
                    time.sleep(wait_time)
                return True
                
            time.sleep(0.5)  # 짧은 대기 후 재시도
            
        self.logger.warning(f"'{button_name}' 버튼을 찾을 수 없습니다.")
        return False
        
    def click_coordinate(self, x, y, wait_after=None):
        """
        특정 좌표를 클릭하는 함수
        
        Args:
            x (int): X 좌표
            y (int): Y 좌표
            wait_after (float, optional): 클릭 후 대기 시간, None이면 기본값 사용
        """
        self.logger.info(f"좌표 ({x}, {y}) 클릭")
        self.adb_controller.tap(x, y)
        
        # 클릭 후 대기
        wait_time = wait_after if wait_after is not None else self.wait_time
        if wait_time > 0:
            time.sleep(wait_time)
            
    @abc.abstractmethod
    def execute(self):
        """
        작업을 실행하는 메인 함수 (각 하위 클래스에서 구현해야 함)
        
        Returns:
            bool: 작업 성공 여부
        """
        pass