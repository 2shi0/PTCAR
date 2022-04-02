import cv2
import numpy as np

# カメラCh.(ここでは0)を指定
camera = cv2.VideoCapture(0)

# arucoライブラリ
aruco = cv2.aruco

# ARパターンの読み込み
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

parameters = aruco.DetectorParameters_create()

# カード画像（テスト用）
im_src = cv2.imread('img0.jpg')

# 撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
while True:
    # フレームを取得
    ret, frame = camera.read()

    # マーカを検出
    # corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)

    # ARマーカを検出
    # type(ids)= <class 'numpy.ndarray'> ※ARマーカ―検出
    # type(ids)= <class 'NoneType'>      ※ARマーカ―未検出
    ## corners: 検出した各ARマーカーの4隅の座標
    corners, ids, _ = aruco.detectMarkers(
        frame, dictionary, parameters=parameters)

    # 検出したマーカに描画する（古いコード）
    # aruco.drawDetectedMarkers(frame, corners, ids, (0, 255, 0))

    if np.all(ids != None):
        # 検出したARマーカーの数ループする
        for c in corners:
            # cornersをカード型に変形
            x1 = (c[0][0][0], c[0][0][1])
            x2 = (c[0][1][0], c[0][1][1])
            x3 = (
                round((c[0][2][0]-c[0][1][0])*0.4)+c[0][2][0],
                round((c[0][2][1]-c[0][1][1])*0.4)+c[0][2][1]
            )
            x4 = (
                round((c[0][3][0]-c[0][0][0])*0.4)+c[0][3][0],
                round((c[0][3][1]-c[0][0][1])*0.4)+c[0][3][1]
            )

            size = im_src.shape
            pts_dst = np.array([x1, x2, x3, x4])
            pts_src = np.array(
                [
                    [0, 0],
                    [size[1] - 1, 0],
                    [size[1] - 1, size[0] - 1],
                    [0, size[0] - 1]
                ], dtype=float
            )
            h, status = cv2.findHomography(pts_src, pts_dst)
            temp = cv2.warpPerspective(
                im_src.copy(), h, (frame.shape[1], frame.shape[0]))
            cv2.fillConvexPoly(frame, pts_dst.astype(int), 0, 16)

            # カード画像を描画
            frame = cv2.add(frame, temp)

            # マーカー描画（デバッグ用）
            # aruco.drawDetectedMarkers(frame, corners, ids, (255,0,0))

    # フレームを画面に表示
    cv2.imshow('camera', frame)

    # キー操作があればwhileループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 撮影用オブジェクトとウィンドウの解放
camera.release()
cv2.destroyAllWindows()
