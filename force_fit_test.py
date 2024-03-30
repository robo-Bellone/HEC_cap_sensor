import numpy as np
import matplotlib.pyplot as plt
import time
import threading
from force_test import  read_serial_data, left_f_data, left_b_data, right_f_data, right_b_data

# 데이터 입력
data = np.array( [[100, 10], [200, 20], [300, 30], [400, 40], [500, 50],[1000,99]])

################# 센서 값 ####################

left_f_data_fit = float(left_f_data[0])
left_b_data_fit = float(left_f_data[0])
right_f_data_fit = float(left_f_data[0])
right_b_data_fit = float(left_f_data[0])
#x_input = 250

#############################################

# 원본 데이터 그리기
plt.scatter(data[:, 0], data[:, 1], label='Original Data')

# 각 데이터 포인트 사이에 직선 그리기
for i in range(len(data) - 1):
    x_values = [data[i][0], data[i+1][0]]
    y_values = [data[i][1], data[i+1][1]]
    plt.plot(x_values, y_values, 'r-')

def predict_y(data, x_input):
    # 데이터가 정렬되어 있다고 가정
    for i in range(len(data) - 1):
        x_start, y_start = data[i]
        x_end, y_end = data[i + 1]
        
        # 입력된 x가 현재 구간에 있는지 확인
        if x_start <= x_input <= x_end:
            # 구간 내에서의 선형 보간 수행
            slope = (y_end - y_start) / (x_end - x_start)  # 기울기
            y_predicted = y_start + slope * (x_input - x_start)  # y값 계산
            return y_predicted
    
    # x_input이 데이터 범위 밖인 경우 
    return None  # 혹은 적절한 예외 처리

def process_data():
    while True:
        if left_f_data:  # 데이터가 비어있지 않은 경우에만 실행
            try:
                # 센서 데이터 처리 로직
                left_f_data_fit = float(left_f_data[-1])
                left_b_data_fit = float(left_b_data[-1])
                right_f_data_fit = float(right_f_data[-1])
                right_b_data_fit = float(right_b_data[-1])

                # 각 센서 값에 대한 y값 예측 및 출력
                left_f_data_map = predict_y(data, left_f_data_fit)
                left_b_data_map = predict_y(data, left_b_data_fit)
                right_f_data_map = predict_y(data, right_f_data_fit)
                right_b_data_map = predict_y(data, right_b_data_fit)

                print(f"Left F Data Map: {left_f_data_map}, Left B Data Map: {left_b_data_map}, Right F Data Map: {right_f_data_map}, Right B Data Map: {right_b_data_map}")
            except IndexError:
                pass  # 센서 데이터가 준비되지 않았을 경우 무시
        time.sleep(0.01)  # 0.01초마다 반복

# 데이터 처리를 위한 별도의 스레드 시작
data_thread = threading.Thread(target=process_data, daemon=True)
data_thread.start()



plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Predicted Force Mapping')
plt.show()
