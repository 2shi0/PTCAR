#カメラを決めるくん
import cv2

print(u"webカメラを走査します。")

cam="使用可能カメラ："

for i1 in range(0, 20): 
    cap1 = cv2.VideoCapture( i1, cv2.CAP_DSHOW )
    if cap1.isOpened(): 
        cam+=(str(i1)+", ")
        print("VideoCapture(", i1, ") : Found")
    else:
        print("VideoCapture(", i1, ") : None")
    cap1.release() 

print("\n"+cam[:-2])

while(True):
    cid=input(u"何番のカメラを確認しますか？: ")
    if cid.isdecimal():
        capture = cv2.VideoCapture(int(cid))
        while(True):
            ret, frame = capture.read()
            cv2.imshow('Press q to close',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        capture.release()
        cv2.destroyAllWindows()


        ans=input(u"映りましたか？(y/n)")
        if ans == "y":
            f = open('config.txt', 'w')
            f.write(cid)
            f.close
            print(ans+u"番のカメラを登録しました。")
            break;
        elif ans=="n":
            print(u"次のカメラを映します")
        else:
            input(u"じゃあnoってことで…")
    else:
        print(u"整数を入力してください。")