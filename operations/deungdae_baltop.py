from operations.deungdae_base import DeungdaeOperation

class DeungdaeBaltop(DeungdaeOperation):
    """
    등대의 발톱 작업을 처리하는 클래스
    """
    def __init__(self, adb_controller, image_finder):
        button_images = {
            'deungdae': 'images/common/deungdae.png',
            'baltop': 'images/deungdae_baltop/baltop.png',
            'bogi': 'images/common/bogi.png',
            'gongyeok': 'images/common/gongyeok.png',
            'gyunbaechi': 'images/common/gyunbaechi.png',
            'chuljeong': 'images/common/chuljeong.png',
            'nagagi': 'images/common/nagagi.png'
        }
        super().__init__(adb_controller, image_finder, button_images)
        
    def execute(self):
        """
        등대에서 발톱 작업 실행
        
        Returns:
            bool: 작업 성공 여부
        """
        self.logger.info("등대 발톱 작업 시작")
        
        # 왼쪽 상단 고정 메뉴 클릭 (등대로 가기 위해)
        self.click_coordinate(64, 143)
        
        # 등대 버튼 클릭
        if not self.click_if_image_found('deungdae'):
            self.logger.error("등대 버튼을 찾을 수 없습니다.")
            return False
            
        # 발톱 버튼 클릭
        if not self.click_if_image_found('baltop'):
            self.logger.warning("발톱 버튼을 찾을 수 없습니다.")
            # 나가기 버튼을 클릭하고 종료
            self.click_if_image_found('nagagi')
            return False
            
        # 보기 버튼 클릭
        if not self.click_if_image_found('bogi'):
            self.logger.warning("보기 버튼을 찾을 수 없습니다.")
            # 나가기 버튼을 클릭하고 종료
            self.click_if_image_found('nagagi')
            return False
            
        # 공격 버튼 클릭