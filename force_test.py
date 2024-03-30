'''
### 시리얼값 들어오는지 체크용 

import serial
import time

serial_port = 'COM7'  # 예: Windows에서의 COM 포트 번호
baud_rate = 9600     # 아두이노와 일치하는 통신 속도

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)  # timeout을 추가했습니다.
    print("시리얼 포트가 성공적으로 열렸습니다.")
    print("포트 설정:", ser)
    
    # 데이터 읽기 시도
    while True:
        if ser.in_waiting > 0:  # 입력 대기중인 데이터가 있는지 확인
            line = ser.readline().decode('utf-8').rstrip()  # 한 줄을 읽고 디코딩, 공백 제거
            print(line)  # 읽은 데이터 출력

except serial.SerialException:
    print(f"{serial_port} 포트를 열 수 없습니다. 포트 번호를 확인해 주세요.")
except KeyboardInterrupt:
    print("프로그램을 종료합니다.")

finally:
    ser.close()
    print("시리얼 포트가 닫혔습니다.")
'''

import serial
import threading
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# 시리얼 포트 설정 및 연결
serial_port = 'COM7'  # 보고 세팅
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# 전역 변수 선언 및 초기화
left_f_data = [0]
left_b_data = [0]
right_f_data = [0]
right_b_data = [0]

is_reading = True

def read_serial_data(ser):
    global left_f_data, left_b_data, right_f_data, right_b_data, is_reading

    while is_reading:

        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()

            try:
                left_f, left_b, right_f, right_b = map(float, line.split(','))
                left_f_data.append(left_f)
                left_b_data.append(left_b)
                right_f_data.append(right_f)
                right_b_data.append(right_b)

                print(f"Left F: {left_f}, Left B: {left_b}, Right F: {right_f}, Right B: {right_b}")
                
                # 각 데이터 리스트의 크기를 50으로 유지
                for data_list in [left_f_data, left_b_data, right_f_data, right_b_data]:
                    if len(data_list) > 50:
                        data_list.pop(0)
            except ValueError:
                pass  # 변환 실패 시 무시

def update_graph(frame):
    
    # 데이터가 존재하는 경우에만 업데이트
    if len(left_f_data) > 0:
        # x 데이터의 길이를 현재 y 데이터의 길이와 동일하게 조정
        x_len = len(left_f_data)  # 모든 데이터 리스트는 동일한 길이를 가짐을 가정
        x_data = np.arange(x_len)

        # x_data 설정을 업데이트 해야 함
        lines[0].set_data(x_data, left_f_data)
        lines[1].set_data(x_data, left_b_data)
        lines[2].set_data(x_data, right_f_data)
        lines[3].set_data(x_data, right_b_data)

        # x 축의 범위를 적절히 조정
        ax.set_xlim(0, max(50, x_len - 1))

    return lines

if __name__ == "__main__":
    # 그래프 초기 설정
    fig, ax = plt.subplots()
    x_data = np.arange(50)
    lines = [ax.plot(x_data, np.zeros(50), label=label)[0] for label in ['Left F', 'Left B', 'Right F', 'Right B']]
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 1023)
    ax.legend()

    # 시리얼 데이터 읽기를 위한 스레드 시작
    thread = threading.Thread(target=read_serial_data, args=(ser,))
    thread.start()

    # 애니메이션 시작
    ani = FuncAnimation(fig, update_graph, blit=False, interval=1)

    # 그래프 표시
    plt.show()

    # 종료 시 처리
    is_reading = False
    thread.join()
    ser.close()
# # 그래프 초기 설정
# fig, ax = plt.subplots()
# x_data = np.arange(50)
# lines = [ax.plot(x_data, np.zeros(50), label=label)[0] for label in ['Left F', 'Left B', 'Right F', 'Right B']]
# ax.set_xlim(0, 50)
# ax.set_ylim(0, 1023)
# ax.legend()
 
# # 시리얼 데이터 읽기를 위한 스레드 시작
# thread = threading.Thread(target=read_serial_data, args=(ser,))
# thread.start()

# # 애니메이션 시작
# ani = FuncAnimation(fig, update_graph, blit=False, interval=1)

# # 그래프 표시
# plt.show()

# # 종료 시 처리
# is_reading = False
# thread.join()
# ser.close()



