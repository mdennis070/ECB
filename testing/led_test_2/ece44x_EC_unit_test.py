import time

from ece44x_EC import Electronics_Control as EC

board_EC = EC(4)

brightness = 4 # 1 to 10
color_off = (0, 0, 0)
color_on_w = (0, 255, 0)
color_on_b = (255, 0, 0)
board_colors = [[color_off for i in range(0, 8)] for j in range(0, 8)]

[piece_pos_w, piece_pos_b] = board_EC.refresh_board(board_colors, brightness)

count = 0
while True:
    for row in range(0, 8):
        for tile in range(0, 8):
            if piece_pos_w[row][tile]:
                board_colors[row][tile] = color_on_w
            elif piece_pos_b[row][tile]:
                board_colors[row][tile] = color_on_b
            else:
                board_colors[row][tile] = color_off
    #for row in board_colors:
    #    print(row)
    [piece_pos_w, piece_pos_b] = board_EC.refresh_board(board_colors, brightness)
    
    for row in range(0, 8):
        print("w row {}: ".format(row), piece_pos_w[row])
    print("\n")
    for row in range(0, 8):
        print("b row {}: ".format(row), piece_pos_b[row])
    print("count: {}".format(count))
    print("\n")
    count = count + 1
    time.sleep(0.1)

'''
LED_colors = [[(0, 0, 0) for i in range(0, 8)] for j in range(0, 8)]
for x in LED_colors:
        print(x)
print("\n\n")

[output_1, output_2] = board_EC.refresh_board(LED_colors, 10)

for x in output_1:
        print(x)

print("\n\n")
for x in output_2:
        print(x)
'''
