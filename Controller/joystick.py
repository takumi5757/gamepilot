import time

from evdev import UInput, list_devices,InputDevice, AbsInfo, ecodes as e

def contoller(vjoystick, steer_value, accel_value, brake_value, dt):
    """バーチャルなジョイスティックを操作する
    
    Args:
        vjoystick(evdev.uinput.UInput): バーチャルジョイスティックインスタンス
        steer_value(int): ステアリング操作量、0~256の整数、中心が128
        accel_value(int): アクセル操作量、0~256の整数、フルスロットルが256
        brake_value(int): ブレーキ操作量、0~256の整数、フルブレーキが256
        dt(float): 入力する時間
        
    """
    vjoy.write(e.EV_ABS, e.ABS_X, steer_value)#steer
    vjoy.write(e.EV_ABS, e.ABS_RZ, accel_value)#accel
    vjoy.write(e.EV_ABS, e.ABS_Z, brake_value)#brake
    vjoy.write(e.EV_ABS, e.ABS_Z, 0)#brake
    vjoy.syn()
    time.sleep(dt)

if __name__ == "__main__":
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        print(f"{device.path}, {device.name}")
    print("どのデバイスの仮想デバイスを作成しますか？")
    print("パスを入力してください  /dev/input/以下を入力")
    device_path = input(">> ")
    device_path = "/dev/input/" + device_path
    vjoy = UInput.from_device(InputDevice(device_path),name='vjoy')

    print(vjoy)
    vjoy.close()

    
    