import os
import sys
import time
import logging
import argparse
from core.adb_controller import ADBController
from core.screen_capture import ScreenCapture
from core.image_finder import ImageFinder
from operations.deungdae_check import DeungdaeCheck
from operations.deungdae_geom import DeungdaeGeom
from operations.deungdae_skull import DeungdaeSkull
from operations.deungdae_baltop import DeungdaeBaltop
from operations.deungdae_tent import DeungdaeTent

def setup_logging(log_level):
    """로깅 설정"""
    log_levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR
    }
    level = log_levels.get(log_level.lower(), logging.INFO)
    
    # 로그 포맷 설정
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 로그 디렉토리 생성
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # 현재 시간을 로그 파일명에 포함
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'android_auto_{timestamp}.log')
    
    # 로깅 핸들러 설정
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.info(f"로깅 시작. 로그 레벨: {log_level}, 파일: {log_file}")
    return logging.getLogger('main')

def parse_arguments():
    """명령줄 인수 파싱"""
    parser = argparse.ArgumentParser(description='Android Auto 자동화 도구')
    parser.add_argument('--device', help='ADB 디바이스 ID (여러 기기가 연결된 경우)')
    parser.add_argument('--operation', choices=['check', 'geom', 'skull', 'baltop', 'tent', 'all'], 
                        default='all', help='실행할 작업 (기본값: all)')
    parser.add_argument('--log-level', choices=['debug', 'info', 'warning', 'error'], 
                        default='info', help='로그 레벨 (기본값: info)')
    parser.add_argument('--cycles', type=int, default=1, 
                        help='실행 사이클 수 (기본값: 1)')
    parser.add_argument('--interval', type=int, default=0, 
                        help='사이클 간 대기 시간(초) (기본값: 0)')
    
    return parser.parse_args()

def main():
    """메인 함수"""
    args = parse_arguments()
    logger = setup_logging(args.log_level)
    logger.info("Android Auto 프로그램 시작")
    
    try:
        # ADB 컨트롤러 초기화
        adb_controller = ADBController(args.device)
        
        # 디바이스 연결 확인
        if not adb_controller.check_device():
            logger.error("연결된 디바이스가 없거나 지정한 디바이스를 찾을 수 없습니다.")
            return
            
        # 화면 캡처 및 이미지 찾기 초기화
        screen_capture = ScreenCapture(adb_controller)
        image_finder = ImageFinder(screen_capture)
        
        # 작업 클래스 초기화
        operations = {
            'check': DeungdaeCheck(adb_controller, image_finder),
            'geom': DeungdaeGeom(adb_controller, image_finder),
            'skull': DeungdaeSkull(adb_controller, image_finder),
            'baltop': DeungdaeBaltop(adb_controller, image_finder),
            'tent': DeungdaeTent(adb_controller, image_finder)
        }
        
        # 작업 순서 설정 (우선순위에 따라)
        operation_order = ['check', 'tent', 'skull', 'geom', 'baltop']
        
        # 실행할 작업 목록
        if args.operation == 'all':
            selected_operations = operation_order
        else:
            selected_operations = [args.operation]
            
        # 지정된 사이클 수만큼 작업 실행
        for cycle in range(1, args.cycles + 1):
            logger.info(f"사이클 {cycle}/{args.cycles} 시작")
            
            # 우선순위에 따라 작업 실행
            for op_name in selected_operations:
                operation = operations[op_name]
                logger.info(f"{op_name} 작업 실행 시작")
                
                success = operation.execute()
                
                if success:
                    logger.info(f"{op_name} 작업 성공적으로 완료")
                else:
                    logger.warning(f"{op_name} 작업 실패")
                    
                # 작업 간 짧은 대기
                time.sleep(1)
                
            # 사이클 간 대기
            if cycle < args.cycles and args.interval > 0:
                logger.info(f"다음 사이클까지 {args.interval}초 대기")
                time.sleep(args.interval)
                
        logger.info("모든 작업 완료")
            
    except KeyboardInterrupt:
        logger.info("사용자에 의해 프로그램 종료")
    except Exception as e:
        logger.exception(f"예상치 못한 오류 발생: {str(e)}")
    
if __name__ == "__main__":
    main()