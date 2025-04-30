import time
from operations.deungdae_base import DeungdaeOperation

class DeungdaeTent(DeungdaeOperation):
    """
    등대의 텐트 작업을 처리하는 클래스
    """
    def __init__(self, adb_controller, image_finder):
        button_images = {
            'deungdae': 'images/common/deungdae.png',
            'tent': 'images/deungdae_tent/tent.png',
            'bogi': 'images/common/bogi.png',
            'gujo': 'images/deungdae_tent/gujo.png',
            'nagagi': 'images/common/nagagi.png'
        }
        super().__init__(adb_controller, image_finder, button_images)
        
    def execute(self):
        """
        등대에서 텐트 작업 실행
        
        Returns:
            bool: 작업 성공 여부
        """
        self.logger.info("등대 텐트 작업 시작")
        
        # 왼쪽 상단 고정 메뉴 클릭 (등대로 가기 위해)
        self.click_coordinate(64, 143)
        
        # 등대 버튼 클릭
        if not self.click_if_image_found('deungdae'):
            self.logger.error("등대 버튼을 찾을 수 없습니다.")
            return False
            
        # 텐트 버튼 클릭
        if not self.click_if_image_found('tent'):
            self.logger.warning("텐트 버튼을 찾을 수 없습니다.")
            # 나가기 버튼을 클릭하고 종료
            self.click_if_image_found('nagagi')
            return False
            
        # 보기 버튼 클릭
        if not self.click_if_image_found('bogi'):
            self.logger.warning("보기 버튼을 찾을 수 없습니다.")
            # 나가기 버튼을 클릭하고 종료
            self.click_if_image_found('nagagi')
            return False
            
        # 구조 버튼 클릭
        if not self.click_if_image_found('gujo'):
            self.logger.warning("구조 버튼을 찾을 수 없습니다.")
            # 나가기 버튼을 클릭하고 종료
            self.click_if_image_found('nagagi')
            return False
            
        # 나가기 버튼 클릭
        if not self.click_if_image_found('nagagi'):
            self.logger.warning("나가기 버튼을 찾을 수 없습니다.")
            # 백 버튼으로 대체
            self.adb_controller.back()
            return False
            
        self.logger.info("등대 텐트 작업 완료")
        return True