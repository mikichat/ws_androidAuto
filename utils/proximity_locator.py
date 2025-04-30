import numpy as np
import logging

class ProximityLocator:
    """
    이미지 간의 근접성을 분석하고 가장 가까운 좌표를 찾는 클래스
    """
    def __init__(self):
        self.logger = logging.getLogger('ProximityLocator')
        
    def find_closest_point(self, reference_point, points_list):
        """
        주어진 참조 지점에서 가장 가까운 지점을 찾는 함수
        
        Args:
            reference_point (tuple): 참조 지점 (x, y) 좌표
            points_list (list): 대상 지점들의 (x, y) 또는 (x, y, score) 좌표 리스트
            
        Returns:
            tuple or None: 가장 가까운 지점의 (x, y) 또는 (x, y, score) 좌표, 리스트가 비어있으면 None
        """
        if not points_list:
            return None
            
        ref_x, ref_y = reference_point
        
        min_distance = float('inf')
        closest_point = None
        
        for point in points_list:
            x, y = point[0], point[1]
            distance = np.sqrt((x - ref_x)**2 + (y - ref_y)**2)
            
            if distance < min_distance:
                min_distance = distance
                closest_point = point
                
        self.logger.info(f"참조 지점 ({ref_x}, {ref_y})에서 가장 가까운 좌표: {closest_point}, 거리: {min_distance:.2f}")
        return closest_point
        
    def find_closest_points_to_each_reference(self, reference_points, target_points, max_distance=None):
        """
        각 참조 지점에 대해 가장 가까운 대상 지점을 찾는 함수
        
        Args:
            reference_points (list): 참조 지점들의 (x, y) 좌표 리스트
            target_points (list): 대상 지점들의 (x, y) 또는 (x, y, score) 좌표 리스트
            max_distance (float, optional): 최대 허용 거리, None이면 제한 없음
            
        Returns:
            dict: {참조 지점 인덱스: 가장 가까운 대상 지점}의 딕셔너리
        """
        result = {}
        
        # 남은 대상 지점들
        remaining_targets = list(target_points)
        
        for i, ref_point in enumerate(reference_points):
            if not remaining_targets:
                break
                
            closest = self.find_closest_point(ref_point, remaining_targets)
            
            if closest:
                # 거리 계산
                distance = np.sqrt((closest[0] - ref_point[0])**2 + (closest[1] - ref_point[1])**2)
                
                # 최대 거리 제한이 없거나, 거리가 최대 허용 거리 이내인 경우
                if max_distance is None or distance <= max_distance:
                    result[i] = closest
                    # 이미 할당된 대상 지점 제거
                    remaining_targets.remove(closest)
                    
        return result