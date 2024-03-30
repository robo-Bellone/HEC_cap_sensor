import serial

# 시리얼 포트 설정 (COM 포트 번호와 보드레이트는 실제 환경에 맞게 변경하세요)
serial_port = 'COM5'  # 예: Windows에서의 COM 포트 번호
baud_rate = 115200     # 예: 통신 속도

# 시리얼 포트 열기
try:
    ser = serial.Serial(serial_port, baud_rate)
    print("시리얼 포트가 성공적으로 열렸습니다.")
    print("포트 설정:", ser)

except serial.SerialException:
    print(f"{serial_port} 포트를 열 수 없습니다. 포트 번호를 확인해 주세요.")

finally:
    ser.close()
    print("시리얼 포트가 닫혔습니다.")