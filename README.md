# gamepilot  

自動運転OSSのOpenpilotを使ってトラック運転ゲーム(Eurotruck2)でACCとLKAを動作させることが目的  
ゲーム画面をキャプチャし、Openpilotに入力する。Openpilotの出力を元に制御量をバーチャルコントローラに送る  

車両の位置はキャプチャ画像から推定  
車両のスピードはキャプチャ画像をXGboostで画像分類を行っている  
その経緯は↓  
[wiki](https://github.com/takumi5757/gamepilot/wiki)  

画面から速度を読み取りコンソールに出力  
![demo](https://github.com/takumi5757/gamepilot/blob/master/GetSpeedValue/sample/get_speed_value2.gif)  

バーチャルジョイスティック動作  
![demo](https://github.com/takumi5757/gamepilot/blob/master/Controller/sample/virtual_joystick2.gif)
