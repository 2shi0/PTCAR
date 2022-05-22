#映像を出力するくん
from tkinter import messagebox
import cv2
import numpy as np

# カメラCh.を指定
try:
    f = open('config.txt', 'r')
    data = f.read()
    f.close()
except:
    messagebox.showwarning("エラー","config.txtを読み込めませんでした")
    exit()

camera = cv2.VideoCapture(int(data), cv2.CAP_DSHOW)

# arucoライブラリ
aruco = cv2.aruco

# ARパターンの読み込み
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

parameters = aruco.DetectorParameters_create()

# カード画像の格納庫
card = []

# 対応表を読み込み
try:
    f = open('cards/list.txt', 'r')
except:
    messagebox.showwarning("list.txt不在","load.pyでlistを生成してください")
    exit()

# 行ごとにスライス
list = f.readlines()

# 画像の読み込み
for i in list:
    i=i[:-1]
    i=i[3:]
    
    card.append(cv2.imread("cards/"+i))

# 対応表を閉じる
f.close()

# 撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
while True:
    try:
        # フレームを取得
        ret, frame = camera.read()

        # ARマーカを検出
        # type(ids)= <class 'numpy.ndarray'> ※ARマーカ―検出
        # type(ids)= <class 'NoneType'>      ※ARマーカ―未検出
        ## corners: 検出した各ARマーカーの4隅の座標
        corners, ids, _ = aruco.detectMarkers(
            frame, dictionary, parameters=parameters)

        if np.all(ids != None):
            # 検出したARマーカーの数ループする
            for i, c in enumerate(corners):

                # 範囲外のマーカーだったら次のマーカーへ
                if int(ids[i])>len(card)-1:
                    continue

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

                
                size = card[int(ids[i])].shape
                pts_dst = np.array([x1, x2, x3, x4])
                pts_src = np.array(
                    [
                        [0, 0],
                        [size[1] - 1, 0],
                        [size[1] - 1, size[0] - 1],
                        [0, size[0] - 1]
                    ], dtype=float
                )

                im_src = card[int(ids[i])]

                h, status = cv2.findHomography(pts_src, pts_dst)
                temp = cv2.warpPerspective(
                    im_src.copy(), h, (frame.shape[1], frame.shape[0]))
                cv2.fillConvexPoly(frame, pts_dst.astype(int), 0, 16)

                # カード画像を描画
                frame = cv2.add(frame, temp)

        # フレームを画面に表示
        cv2.imshow('Press q to close', frame)

        # キー操作があればwhileループを抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        messagebox.showwarning("?????","何かよくわからないエラー")
        exit()

# 撮影用オブジェクトとウィンドウの解放
camera.release()
cv2.destroyAllWindows()