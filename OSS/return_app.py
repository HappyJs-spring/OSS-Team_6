# return_app.py
import ctypes
import os

DLL_PATH = './return_c_lib.dll' # DLL 파일 경로
VALUE_TO_PASS = int(input('게임 시작:1, 게임 종료:0')) #전달하ㄹ 값
if VALUE_TO_PASS == 0:
    print('종료합니다')
else:
    if not os.path.exists(DLL_PATH):
        print(f"오류: '{DLL_PATH}'")
        exit()

    try:
        c_lib = ctypes.CDLL(DLL_PATH) #DLL 로드

        # return_number 함수 설정
        c_lib.play_game.argtypes = [ctypes.c_int]  # 인자 타입 정의: 정수 하나를 받음
        c_lib.play_game.restype = ctypes.c_int # !!!!!!!!!!!!반환 타입 정의: 정수(c_int)를 반환하도록 설정!!!!!!!!!!!!!!!

        
        print(f"Python에서 C 함수로 값 {VALUE_TO_PASS} 전달")
        result_from_c = c_lib.play_game(VALUE_TO_PASS)  # C 함수 호출 후, 반환된 정수 값을 Python 변수 result_from_c에 저장
        print(f"Python이 C 함수로부터 받은 최종 반환 값: {result_from_c}")

        # C 로직 검사
        if result_from_c == VALUE_TO_PASS * 2:
            print("성공", result_from_c)
        else:
            print("오류: C로부터 받은 값:", result_from_c)

    #에러 처리
    except OSError as e:
        print(f"\nDLL 로드 중 오류 발생: {e}")
        print("Python과 DLL의 비트 수(32비트/64비트)가 일치하는지 확인하세요.")
    except Exception as e:
        print(f"\n예기치 않은 오류 발생: {e}")