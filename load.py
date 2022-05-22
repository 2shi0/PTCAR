#デッキリストを生成するくん
import cv2
import glob
import os

# cardsディレクトリ存在確認
SAMPLE_DIR = "cards"

# ディレクトリが存在しない場合、ディレクトリを作成する
if not os.path.exists(SAMPLE_DIR):
    
    os.makedirs(SAMPLE_DIR)

# デッキテキストの初期化
f = open("cards/list.txt", "w")

# カード画像を読み込み
dir = glob.glob("cards/*.jpg", recursive=True)
card = []

# 行番号
g = 0

for i, d in enumerate(dir):
    img = cv2.imread(d)
    height = img.shape[0]
    width = img.shape[1]
    img = cv2.resize(img , (int(width*0.5), int(height*0.5)))
    idx = d.find("\\")
    r = d[idx+len("\\"):]

    """
    cv2.imshow("Press any key", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """

    while(1):
        n = input(r+u"を何枚採用しますか？：")
        if n.isdecimal():
            n = int(n)
            print(str(n)+u"投します")
            break
        else:
            print(u"整数を入力してください")

    for i in range(n):
        f.write(f'{g:02}'+":"+r+"\n")
        g+=1

# 対応表を閉じる
f.close()

print(str(g)+u"枚のプロキシを作成しました")