# androidAuto

## 📖 프로젝트 소개
`androidAuto`는 Android Auto 환경에서 동작하는 앱/플러그인(또는 라이브러리)입니다.  
(여기에 프로젝트의 목적과 주요 기능을 한두 문장으로 작성하세요.)

UIAutomator2 를 이용해서 제어 가능

## 🚀 주요 기능
- 기능 1: deungdae_check.py 등대 의 체크 클릭 오토
- 기능 2: deungdae_tent.py 등대 의 텐트 클릭 오토
- 기능 3: deungdae_skull.py 등대 의 해골 클릭 오토
- 기능 4: deungdae_geom.py 등대 의 검 클릭 오토
- 기능 5: deungdae_baltop.py 등대 의 발톱 클릭 오토

- 함수 : proximity_locator.py 이미지 비교 및 가까운 좌표 1개씩 추출

## 기능 우선 순위
순위 . 기능명칭
1 . deungdae_check
2 . deungdae_tent
3 . deungdae_skull
4 . deungdae_geom
5 . deungdae_baltop


본 기능은 등대를 클릭후 체크 이미지가 있다면 체크 기능을 모두 수행하고
2순위,3순위,4순위 를 각각 수행한다.

# 기능 설명 : 기능=동작순서
등대---
	|-체크(check)=체크(check)[터치]-나가기(nagagi)[터치]
	|-검(geom)=보기(bogi)[터치]-탐험(tamheom)[터치]-전투(jeontu)[터치]-2초지연
	|-체크(check)=체크(check)[터치]-나가기(nagagi)[터치]
	|-해골(skull)=보기(bogi)[터치]-공격(gongyeok)[터치]-균등배치(gyunbaechi)[터치]-출정(chuljeong)[터치]
	|-체크(check)=체크(check)[터치]-나가기(nagagi)[터치]
	|-발톱(baltop)=보기(bogi)[터치]-공격(gongyeok)[터치]-균등배치(gyunbaechi)[터치]-출정(chuljeong)[터치]
	|-체크(check)=체크(check)[터치]-나가기(nagagi)[터치]
	|-텐트(tent)=보기(bogi)[터치]-구조(gujo)[터치]
	|-체크(check)=체크(check)[터치]-나가기(nagagi)[터치]



## ⚙️ 설치 및 실행 방법
1. 저장소 클론  

2. 의존성 설치  

3. 앱 빌드 및 실행  


## 🎯 사용 예시
```bash
# 예시 명령어나 스크린샷, 코드 스니펫 등을 여기에 추가
```

## 🤝 기여


## 📝 라이선스
이 프로젝트는 [MIT 라이선스](LICENSE) 아래 배포됩니다.

## 📧 연락처




androidAuto
📖 프로젝트 소개
androidAuto는 안드로이드 게임 자동화를 위한 이미지 인식 기반 자동화 도구입니다.
ADB를 통해 안드로이드 기기를 제어하고, OpenCV를 이용한 이미지 인식으로 게임의 다양한 작업을 자동화합니다.
🚀 주요 기능

기능 1: 등대 체크 - 등대 메뉴의 체크 기능 자동 수행
기능 2: 등대 텐트 - 등대 메뉴의 텐트 기능 자동 수행
기능 3: 등대 해골 - 등대 메뉴의 해골 기능 자동 수행
기능 4: 등대 검 - 등대 메뉴의 검 기능 자동 수행
기능 5: 등대 발톱 - 등대 메뉴의 발톱 기능 자동 수행

기능 우선 순위

deungdae_check
deungdae_tent
deungdae_skull
deungdae_geom
deungdae_baltop

본 프로그램은 등대를 클릭 후 체크 이미지가 있다면 체크 기능을 모두 수행하고,
2순위, 3순위, 4순위, 5순위 기능을 각각 순서대로 수행합니다.
📂 프로젝트 구조
androidAuto/
├── core/                   # 핵심 기능 모듈
│   ├── adb_controller.py   # ADB 제어
│   ├── screen_capture.py   # 화면 캡처
│   └── image_finder.py     # 이미지 인식
├── operations/             # 작업 처리 모듈
│   ├── deungdae_base.py    # 기본 등대 작업 클래스
│   ├── deungdae_check.py   # 체크 작업
│   ├── deungdae_tent.py    # 텐트 작업
│   ├── deungdae_skull.py   # 해골 작업
│   ├── deungdae_geom.py    # 검 작업
│   └── deungdae_baltop.py  # 발톱 작업
├── utils/                  # 유틸리티 기능
│   └── proximity_locator.py # 근접 좌표 탐색
├── images/                 # 이미지 리소스
│   ├── common/             # 공통 사용 이미지
│   ├── deungdae_check/     # 체크 작업 이미지
│   ├── deungdae_tent/      # 텐트 작업 이미지
│   ├── deungdae_skull/     # 해골 작업 이미지
│   ├── deungdae_geom/      # 검 작업 이미지
│   └── deungdae_baltop/    # 발톱 작업 이미지
├── logs/                   # 로그 저장 디렉토리
├── config.json             # 설정 파일
├── main.py                 # 메인 실행 파일
└── README.md               # 설명서
⚙️ 설치 및 설정

저장소 클론

bashgit clone https://github.com/mikichat/ws_androidAuto.git
cd androidAuto

필요한 패키지 설치

bashpip install -r requirements.txt

ADB 설정


Android SDK 플랫폼 도구를 다운로드하여 설치
ADB가 시스템 경로에 추가되었는지 확인
개발자 옵션 및 USB 디버깅 활성화


설정 파일 수정 (선택 사항)


config.json 파일을 필요에 맞게 수정

🎯 사용 방법

안드로이드 기기를 USB로 연결하거나 무선 ADB 연결 설정
기기가 정상적으로 인식되는지 확인

bashadb devices

프로그램 실행

bash# 기본 설정으로 모든 기능 실행
python main.py

# 특정 기능만 실행
python main.py --operation check  # 체크 기능만 실행

# 상세 로그 출력
python main.py --log-level debug

# 여러 사이클 실행
python main.py --cycles 3 --interval 60  # 3회 실행, 각 사이클 사이 60초 대기

# 특정 디바이스 지정
python main.py --device YOUR_DEVICE_ID
📋 명령줄 옵션

--device: ADB 디바이스 ID (여러 기기가 연결된 경우)
--operation: 실행할 작업 (check, geom, skull, baltop, tent, all)
--log-level: 로그 수준 (debug, info, warning, error)
--cycles: 실행 사이클 수
--interval: 사이클 간 대기 시간(초)

🛠️ 기능 추가 및 커스터마이징
새로운 기능을 추가하려면:

operations/ 디렉토리에 새 작업 클래스 추가
DeungdaeOperation 클래스 상속
execute() 메서드 구현
main.py의 operations 딕셔너리에 추가
