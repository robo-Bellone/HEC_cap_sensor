import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# 전역 변수 선언
roll, pitch, yaw, gyro_x, gyro_y, gyro_z = (0,)*6
roll_data, pitch_data, yaw_data = [], [], []

def read_serial_data():
    global roll, pitch, yaw, gyro_x, gyro_y, gyro_z
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        if line.startswith("*"):
            _, values = line.split("*")
            data_parts = values.split(",")

            # 각 값을 전역 변수에 저장
            roll = float(data_parts[0])
            pitch = float(data_parts[1])
            yaw = float(data_parts[2])
            gyro_x = float(data_parts[3])
            gyro_y = float(data_parts[4])
            gyro_z = float(data_parts[5])

def update_graph(frame):
    # 전역 변수에서 데이터 읽기
    global roll, pitch, yaw
    read_serial_data()

    # 데이터 추가
    roll_data.append(roll)
    pitch_data.append(pitch)
    yaw_data.append(yaw)

    # 데이터 리스트 유지
    if len(roll_data) > 50:
        roll_data.pop(0)
        pitch_data.pop(0)
        yaw_data.pop(0)

    # 그래프 데이터 업데이트
    line_roll.set_data(np.arange(len(roll_data)), roll_data)
    line_pitch.set_data(np.arange(len(pitch_data)), pitch_data)
    line_yaw.set_data(np.arange(len(yaw_data)), yaw_data)

    # 변수 값 출력
    print(f"Roll: {roll:.2f}, Pitch: {pitch:.2f}, Yaw: {yaw:.2f}, Gyro_x: {gyro_x:.2f}, Gyro_y: {gyro_y:.2f}, Gyro_z: {gyro_z:.2f}")

    return line_roll, line_pitch, line_yaw

# 시리얼 포트 설정 및 연결
serial_port = 'COM5'
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# 그래프 초기 설정
fig, ax = plt.subplots()
ax.set_xlim(0, 50)
ax.set_ylim(-180, 180)
line_roll, = ax.plot([], [], label='Roll')
line_pitch, = ax.plot([], [], label='Pitch')
line_yaw, = ax.plot([], [], label='Yaw')
ax.legend()

# 애니메이션 시작
ani = FuncAnimation(fig, update_graph, blit=True, interval=1)

# 그래프 표시
plt.show()

# 시리얼 연결 종료
ser.close()




