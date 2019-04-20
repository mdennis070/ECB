#import spidev

class Electronics_Control:
	#chess_EC = SpiDev()

	LED_start_frame = (0x00, 0x00, 0x00, 0x00)
	LED_end_frame = (0xff, 0xff, 0xff, 0xff)

	piece_white = 0b01
	piece_black = 0b11

	white_pos = [[False for itr1 in range(0, 8)] for itr2 in range(0, 8)]
	black_pos = [[False for itr1 in range(0, 8)] for itr2 in range(0, 8)]

	def __init__(self):
		#chess_EC.open(1, 0)
		pass
	#

	def __del__(self):
		#chess_EC.close()
		pass
	#

	def parse_sensor_data(self, sensor_data):
		for itr in range(0, 16, 2):
			row = itr // 2
			tile_cluster_1 = sensor_data[itr] # 4 tiles
			for col in range(0, 4):
				tile_val = (tile_cluster_1 & (0b11 << (col*2)))
				white_pos[row][col] = piece_white == tile_val
				black_pos[row][col] = piece_black == tile_val
			#

			tile_cluster_2 = sensor_data[itr + 1] # 4 tiles
			for col in range(0, 4):
				tile_val = (tile_cluster_2 & (0b11 << (col*2)))
				white_pos[row][col + 4] = piece_white == tile_val
				black_pos[row][col + 4] = piece_black == tile_val
			#
		#
		return white_pos, black_pos
	#

	def format_to_range(self, val, min, max):
		if(val > max):
			return max
		elif (val < min):
			return min
		else:
			return val
	#

	def format_LED_data(self, color_data, brightness):
		brightness = format_to_range(brightness, 0, 31)
		red = color_data[0]
		format_to_range(red, 0, 255)
		green = color_data[1]
		format_to_range(green, 0, 255)
		blue = color_data[2]
		blue = format_to_range(blue, 0, 255)

		formatted_data = (0b111 | brightness, blue, green, red)
		return formatted_data
	#

	'''
	input:
		LED_data: 8x8 array with each element a tuple.
			Each element will describe the color of one LED
			Tuple will be (red, gree, blue)
			0 <= red, green, blue <= 255
		brightness:
			0 <= brightness <= 10
	return:
		white_pos: 8x8 array. True if white has a piece at
			that location False otherwise
		black_pos: 8x8 array. True if blakc has a piece at
			that location False otherwise
	'''
	#Temporarily make this a dummy test function
	#make a true/false array with correct pawn positions
	def refresh_board(self, LED_data, brightness):
		print("TEST VALUES. FAKE REFRESH BOARD")
		white_pos = [[False for i in range(0,8)] for j in range(0,8)]
		black_pos = [[False for i in range(0,8)] for j in range(0,8)]

	    #State that pawns are in the correct locations
		for x in range(0,8):
			white_pos[1][x] = True
			black_pos[6][x] = True

		#Correct Knight position
		white_pos[0][1] = True
		white_pos[0][6] = True
		black_pos[7][1] = True
		black_pos[7][6] = True

		# #Correct Bishop position
		white_pos[0][2] = True
		white_pos[0][5] = True
		black_pos[7][2] = True
		black_pos[7][5] = True

		# #Correct Rook location
		white_pos[0][0] = True
		white_pos[0][7] = True
		black_pos[7][0] = True
		black_pos[7][7] = True

		# #Correct Queen position
		white_pos[0][3] = True
		black_pos[7][3] = True

		# #Correct King position
		white_pos[0][4] = True
		black_pos[7][4] = True

		#Fail Test condition because this means that a white piece at b2 (1,1) is not present
		#white_pos[1][1] = False #Put a false value to fail the Test
		#white_pos[0][2] = False
		#black_pos[5][5] = False
		return (white_pos, black_pos)
	#
