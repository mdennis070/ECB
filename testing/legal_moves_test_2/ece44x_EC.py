import spidev
import RPi.GPIO as GPIO

class Electronics_Control:
    chess_EC = spidev.SpiDev()

    latch_pin = 13
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(latch_pin, GPIO.OUT)
    GPIO.output(latch_pin, 1)

    LED_START_FRAME = [0x00, 0x00, 0x00, 0x00]
    LED_END_FRAME = [0xff, 0xff, 0xff, 0xff]

    PIECE_WHITE = 0b10
    PIECE_BLACK = 0b00

    white_pos = [[False for itr1 in range(0, 8)] for itr2 in range(0, 8)]
    black_pos = [[False for itr1 in range(0, 8)] for itr2 in range(0, 8)]
    
    num_PCBs = 4

    def __init__(self, PCBs=4):
        self.chess_EC.open(1, 0)
        self.chess_EC.max_speed_hz = 500000 # 500kHz 
        self.num_PCBs = PCBs
        pass
    #

    def __del__(self):
        self.chess_EC.close()
        GPIO.cleanup()
        pass
    #

    def parse_sensor_data(self, sensor_data):

        # 4 bytes represent 1 PCB
        bytes_per_PCB = 4
        
        #for item in sensor_data[0:bytes_per_PCB*self.num_PCBs]:
        #    print(bin(item))
        
        for byte in range(0, bytes_per_PCB*self.num_PCBs, bytes_per_PCB):
            row = byte // 2
            
            # shift register 1 and 2
            # tile 1   2   3   4 
            # bit  4:5 6:7 0:1 2:3
            index_mask = [0b00110000, 0b11000000, 0b00000011, 0b00001100]
            index_shift = [4, 6, 0, 2]
            row_1 = sensor_data[byte:byte+2] # two bytes = 8 tiles
            for col in range(0, 4):
                tile_val = row_1[0] & index_mask[col]
                self.white_pos[row][col] = self.PIECE_WHITE == (tile_val >> index_shift[col])
                self.black_pos[row][col] = self.PIECE_BLACK == (tile_val >> index_shift[col])
            #
            
            for col in range(0, 4):
                tile_val = row_1[1] & index_mask[col]
                self.white_pos[row][col+4] = self.PIECE_WHITE == (tile_val >> index_shift[col])
                self.black_pos[row][col+4] = self.PIECE_BLACK == (tile_val >> index_shift[col])
            #

            # shift register 3 and 4
            # tile 1   2   3   4 
            # bit  0:1 2:3 4:5 6:7
            index_mask = [0b00000011, 0b00001100, 0b00110000, 0b11000000]
            index_shift = [0, 2, 4, 6]
            row_2 = sensor_data[byte+2:byte+4] # two bytes = 8 tiles
            for col in range(0, 4):
                tile_val = row_2[0] & index_mask[col]
                self.white_pos[row+1][3-col] = self.PIECE_WHITE == (tile_val >> index_shift[col])
                self.black_pos[row+1][3-col] = self.PIECE_BLACK == (tile_val >> index_shift[col])
            #
            
            for col in range(0, 4):
                tile_val = row_2[1] & index_mask[col]
                self.white_pos[row+1][3-col+4] = self.PIECE_WHITE == (tile_val >> index_shift[col])
                self.black_pos[row+1][3-col+4] = self.PIECE_BLACK == (tile_val >> index_shift[col])
            #
        for row in range(0, 8, 2):
            self.white_pos[row] = self.white_pos[row][::-1]
            self.black_pos[row] = self.black_pos[row][::-1]

        return self.white_pos, self.black_pos
    #

    def format_to_range(self, val, min_val, max_val):
        if(val > max_val):
            return max_val
        elif (val < min_val):
            return min_val
        else:
            return val
    #

    def format_LED_data(self, color_data, brightness):
        brightness = self.format_to_range(brightness, 0, 31)
        
        red = color_data[0]
        red = self.format_to_range(red, 0, 255)
        
        green = color_data[1]
        green = self.format_to_range(green, 0, 255)
        
        blue = color_data[2]
        blue = self.format_to_range(blue, 0, 255)

        formatted_data = [(0b11100000 | brightness), blue, green, red]
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
    def refresh_board(self, LED_data, brightness):
        for row in range(0, 8, 2):
            LED_data[row] = LED_data[row][::-1]

        brightness = brightness * 31 // 10
        xfer_data = self.LED_START_FRAME.copy()

        for row_color in LED_data:
            for tile_color in row_color:
                color = self.format_LED_data(tile_color, brightness)
                #print(color)
                xfer_data.extend(color)
            #
        #
        
        xfer_data.extend(self.LED_END_FRAME)
        #print("xfer data: ", xfer_data)

        GPIO.output(self.latch_pin, 0)
        GPIO.output(self.latch_pin, 1)

        sensor_data = self.chess_EC.xfer2(xfer_data)
        
        return self.parse_sensor_data(sensor_data)
    #
