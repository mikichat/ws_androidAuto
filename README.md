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
