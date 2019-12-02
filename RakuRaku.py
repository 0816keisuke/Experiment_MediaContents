# Copyright (C) 2019 Keisuke Fukada  Contact: keisukefukada.0816☆gmail.com(☆を@に変更) 又はその他各種SNSまで.
# 2019年 情報通信実験"メディアコンテンツ"においてクソ楽が出来る「RakuRaku」プログラム
# 出来ること：ファイル名の一括編集，画像一覧表(.txtファイル)の生成，学習データの反転画像生成
# 動作保証環境：Jupyter Notebook 5.7.8
# Last Revised at 2019/12/02
# (注意)正しい入力がされないとエラーが起きる場合があります．その時は実行し直してください．

import glob
import os
from PIL import Image, ImageOps

# 画像ファイル名の編集(ファイル名を「0012.jpg」のようにする)(9999枚まで対応)
def Get_Path(num1):
    print('\n名前を編集したいファイルが置かれている相対/絶対パスを入力してください．')
    path = input()            # Ex) ./Positive
    print('\nファイルの拡張子を入力してください Ex) .jpg')
    ext = input()             # Ex) .jpg
    addr = path + '/*' + ext  # Ex) ./Positive/*.jpg
    flist = glob.glob(addr)   # 指定したpath，拡張子の全ファイルを取得
    i = 1
    if num1 == '1':
        Rename_File(flist, path, i)
    elif num1 == '3':
        Generate_Reverse(flist)
    else:
        print('エラーが起きました．やり直してください．')

# ファイル名を一括で変更する
def Rename_File(flist, path, i):
    for file in flist:
        if i<10:               # 1～9枚の時
            os.rename(file, path +'/000' + str(i) + '.jpg') # ./Positive/0001.jpg
        elif 10 <= i < 100:    # 10～99の時
            os.rename(file, path + '/00' + str(i) + '.jpg')
        elif 100 <= i < 1000:  # 100～999の時
            os.rename(file, path + '/0' + str(i) + '.jpg')
        else:                  # 1000～9999の時
            os.rename(file, path + '/' + str(i) + '.jpg')
        i+=1
    list = glob.glob(path)
    print('\n処理が完了しました．正しく処理されたかファイルを確認してください．')

# 画像の一覧表ファイルフォーマット(.txt)ファイルの生成
def Generate_File(num2):
    print('\n画像ファイルが置かれている相対/絶対パスを入力してください．')
    path = input()            # Ex) ./Positive
    path.replace('\\', '/')   # 入力されたpathの'\'を'/'に書き換え(エスケープ文字なので)
    flist = os.listdir(path)  #pathにおける全ファイル名を取得する

    print('\n新たに生成する一覧表ファイル名及び拡張子を入力してください．Ex) test.txt')
    name = input()
    f = open(name, 'w')       # ファイルを書き込み専用で開く(該当ファイルがなければ新規作成)
    
    if num2 == '1':          # 正例画像一覧表の作成
        # ここでは，一覧表ファイルにおいて, 「Count=1, x1=0, y1=0」とする. つまり「画像の縦横のサイズ」のみ扱う
        for file in flist:
            file = path + '/' + file    # Ex) ./Positive/0001.jpg
            img = Image.open(file)      # 各画像をimgで取得
            w, h = img.size             # imgのサイズ(横w, 縦h)を取得(int型)
            ww = str(w)                 # サイズをstr型に変換
            hh = str(h)
            line = file + ' 1 0 0 ' + ww + ' ' + hh +'\n' # Ex) ./Positive/0001.jpg 1 0 0 240 480
            f.write(line)                # Ex) ./Positive/0001.jpg 1 0 0 240 480 これをファイルに書き込み
        f.close()                        # openした.txtファイルを閉じる
        print('\n処理が完了しました．ファイルが正しく生成されたか確認してください．')

    elif num2 == '2':        # 負例画像一覧表の作成
        for file in flist:
            file = path + '/' + file + '\n'
            f.write(file)
        f.close()            # openした.txtファイルを閉じる
        print('\n処理が完了しました．ファイルが正しく生成されたか確認してください．')

# 学習データの反転画像の生成
def Generate_Reverse(flist):
    print('反転画像を生成中です．時間がかかることがあります．しばらくお待ちください(100枚あると15秒くらいかかるよ)．')
    for file in flist:
        new_path = os.path.dirname(file) + '/Reverse_' + os.path.basename(file) # Ex) ./Positive + /Reverse_ + 0012.jpg
        img = Image.open(file)             # 各画像をimgで取得
        img_reverse = ImageOps.mirror(img) # imgを反転
        img_reverse.save(new_path)         # 反転画像を'元画像名_reverse'で保存

    print('\n反転画像を"Reverse_ファイル名"として作成しました．ファイル名を編集するために，次の作業を行ってください．')
    Get_Path('1')                          # 画像ファイル名の編集

if __name__ == '__main__':
    print('ファイル名の編集をしますか？画像一覧表ファイルを生成しますか？')
    print('該当する番号を選んでください．\n1: ファイル名の編集,  2: 画像一覧表ファイルの生成，3: 反転画像の生成')
    num1 = input()

    if num1 == '1' or num1 == '3':
        Get_Path(num1)  # ファイル名の編集，反転画像の生成
    elif num1 == '2':  # 画像一覧表ファイルの生成
        print('\n正例画像の矩形表現付き一覧表ファイルを生成しますか？負例画像の一覧表ファイルを生成しますか？')
        print('該当する番号を選んでください．\n1: 正例画像一覧表， 2: 負例画像一覧表')
        num2 = input()
        if num2 == '1' or num2 == '2':
            Generate_File(num2)
        else:
            print('\n不適切な入力です．実行し直してください．')
    else:
        print('\n不適切な入力です．実行し直してください．')