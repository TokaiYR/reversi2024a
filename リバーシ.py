import tkinter as tk

root = tk.Tk()
root.title("リバーシ")

# 先攻"B"(Black)、後攻"W"(White)
player = "B"

# ボードのサイズと背景を定義
canvas = tk.Canvas(root, width=400, height=400, bg="green")
canvas.pack()

# ボードのグリッドとマスの形状を定義
for i in range(8):
    for j in range(8):
        canvas.create_rectangle(i*50, j*50, (i+1)*50, (j+1)*50, outline="black")

# 8×8の空の行列を作成
board = [[" " for i in range(8)] for i in range(8)]

# 初期の中央の石を配置
board[3][3], board[4][4] = "W", "W"
board[3][4], board[4][3] = "B", "B"

# 先攻Aと後攻Bが交互に石を置く
def stone():
    canvas.delete("ishi")
    for i in range(8):
        for j in range(8):
            if board[i][j] == "B":
                canvas.create_oval(i*50+5, j*50+5, (i+1)*50-5, (j+1)*50-5, fill="black", tags="ishi")
            elif board[i][j] == "W":
                canvas.create_oval(i*50+5, j*50+5, (i+1)*50-5, (j+1)*50-5, fill="white", tags="ishi")
# 1マスは50×50px、石がマス内に収まるように石の大きさを±5する

# クリック座標取得
def clicked(event):
    global player
    x, y = event.x//50, event.y//50
    
    # ボードの範囲外をクリックした場合は無効
    if x<0 or x>=8 or y<0 or y>=8:
        return

    # 置けるマスとひっくり返しを定義
    if board[x][y] == " " and any(canput(x, y, dx, dy) for dx, dy in way):
        board[x][y] = player
        for dx, dy in way:
            if canput(x, y, dx, dy):
                flip(x, y, dx, dy)
        stone()

    # 置けない場合のパスと両者置けない場合のゲーム終了
        if not any(np(i, j) for i in range(8) for j in range(8)):
            player = another(player)
            if not any(np(i, j) for i in range(8) for j in range(8)):
                end()
                return
        player = another(player)

    else:
        if not any(np(i, j) for i in range(8) for j in range(8)):
            player = another(player)
            if not any(np(i, j) for i in range(8) for j in range(8)):
                end()
                return

# クリックされたマスに石を置けるか確認
def canput(x, y, dx, dy):
    i, j = x + dx, y + dy
    another_ishi = False

    while 0 <= i < 8 and 0 <= j < 8:
        if board[i][j] == another(player):
            another_ishi = True
        elif board[i][j] == player:
            return another_ishi
        else:
            break
        i += dx
        j += dy
    return False

# 石をひっくり返す
def flip(x, y, dx, dy):
    i, j = x + dx, y + dy

    while board[i][j] == another(player):
        board[i][j] = player
        i += dx
        j += dy

# 指定された座標に石を置けるか確認
def np(x, y):
    if board[x][y] != " ":
        return False
    return any(canput(x, y, dx, dy) for dx, dy in way)

# プレイヤー交代
def another(player):
    return "W" if player == "B" else "B"

# ゲーム終了と判定表示
def end():
    countblack = sum(row.count("B") for row in board)
    countwhite = sum(row.count("W") for row in board)
    winner = "引き分け" if countblack == countwhite else "黒の勝ち！" if countblack > countwhite else "白の勝ち！"
    canvas.create_text(200, 200, text=f"ゲーム終了\n黒: {countblack} 白: {countwhite}\n{winner}", font=("Arial", 40), fill="red", tags="end")

way = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# 左クリックが押されたら関数clickedを呼び出す
canvas.bind("<Button-1>", clicked)
stone()

root.mainloop()
