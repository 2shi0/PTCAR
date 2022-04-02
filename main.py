import cv2
import numpy as np

# カメラCh.(ここでは0)を指定
camera = cv2.VideoCapture(0)

# arucoライブラリ
aruco = cv2.aruco

# ARパターンの読み込み
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# 撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
while True:
    # フレームを取得
    ret, frame = camera.read()

    # マーカを検出
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)

    # 検出したマーカに描画する
    aruco.drawDetectedMarkers(frame, corners, ids, (0, 255, 0))

    # フレームを画面に表示
    cv2.imshow('camera', frame)

    # キー操作があればwhileループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 撮影用オブジェクトとウィンドウの解放
camera.release()
cv2.destroyAllWindows()
