mport cv2
import numpy as np
import logging

class ImageFinder:
    """
    이미지 인식 및 매칭을 처리하는 클래스
    """
    def __init__(self, screen_capture, threshold=0.8):
        self.screen_capture = screen_capture
        self.default_threshold = threshold
        self.logger = logging.getLogger('ImageFinder')

    def find_image_on_screen(self, template_path, threshold=None):
        """
        화면에서 특정 이미지를 찾는 함수
        
        Args:
            template_path (str): 찾을 이미지 템플릿의 경로
            threshold (float, optional): 매칭 임계값 (기본값: None, 클래스 기본값 사용)
            
        Returns:
            tuple or None: 이미지가 발견된 경우 (center_x, center_y), 발견되지 않은 경우 None
        """
        if threshold is None:
            threshold = self.default_threshold
            
        screenshot = self.screen_capture.capture()
        if screenshot is None:
            self.logger.error("스크린샷을 가져오는데 실패했습니다.")
            return None
            
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            self.logger.error(f"템플릿 이미지를 로드하는데 실패했습니다: {template_path}")
            return None
            
        self.logger.debug(f"스크린샷 크기: {screenshot.shape[:2]}")
        self.logger.debug(f"템플릿 이미지 크기: {template.shape[:2]}")
        
        try:
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            
            if len(loc[0]) > 0:
                # 최고 매칭 포인트 가져오기
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                self.logger.info(f"이미지를 찾았습니다. 위치: ({center_x}, {center_y}), 매칭 점수: {max_val:.4f}")
                return (center_x, center_y, max_val)
            else:
                self.logger.debug(f"이미지를 찾을 수 없습니다: {template_path}")
                return None
        except Exception as e:
            self.logger.error(f"이미지 매칭 중 오류 발생: {str(e)}")
            return None

    def find_all_matches(self, template_path, threshold=None, max_results=10):
        """
        화면에서 특정 이미지의 모든 매칭 포인트를 찾는 함수
        
        Args:
            template_path (str): 찾을 이미지 템플릿의 경로
            threshold (float, optional): 매칭 임계값
            max_results (int, optional): 반환할 최대 결과 수
            
        Returns:
            list: (x, y, score) 튜플의 리스트, 매칭 점수에 따라 내림차순 정렬됨
        """
        if threshold is None:
            threshold = self.default_threshold
            
        screenshot = self.screen_capture.capture()
        if screenshot is None:
            self.logger.error("스크린샷을 가져오는데 실패했습니다.")
            return []
            
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            self.logger.error(f"템플릿 이미지를 로드하는데 실패했습니다: {template_path}")
            return []
            
        try:
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            h, w = template.shape[:2]
            
            # 임계값 이상의 모든 매칭 포인트 찾기
            locations = []
            result_flat = result.flatten()
            indices = np.argsort(result_flat)[::-1]  # 매칭 점수에 따라 내림차순 정렬된 인덱스
            
            height, width = result.shape
            count = 0
            
            for idx in indices:
                if count >= max_results:
                    break
                    
                if result_flat[idx] < threshold:
                    break
                    
                y = idx // width
                x = idx % width
                
                # 중복 방지를 위해 이미 발견된 위치와 충분히 떨어져 있는지 확인
                is_duplicate = False
                for loc_x, loc_y, _ in locations:
                    distance = np.sqrt((loc_x - (x + w//2))**2 + (loc_y - (y + h//2))**2)
                    if distance < max(w, h) // 2:
                        is_duplicate = True
                        break
                        
                if not is_duplicate:
                    center_x = x + w // 2
                    center_y = y + h // 2
                    locations.append((center_x, center_y, result_flat[idx]))
                    count += 1
                    
            self.logger.info(f"이미지 {template_path}에 대해 {len(locations)}개의 매칭 포인트를 찾았습니다.")
            return locations
            
        except Exception as e:
            self.logger.error(f"이미지 매칭 중 오류 발생: {str(e)}")
            return []