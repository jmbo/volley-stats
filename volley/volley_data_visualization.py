
from PIL import Image, ImageDraw, ImageFont
import pdb
import math
from typing import List, Set, Dict, Tuple, Union

class VolleyCourt(object):

    # bunch o ratios based on image size
    court_size_ratio       = .75
    circle_size_ratio      = .125
    font_size_ratio        = .025
    label_font_size_ratio  = .075
    net_length_ratio       = .875
    pole_size_ratio        = .03125

    court_start_xy_ratios  = (.125,  .1875)
    left_pole_xy_ratios    = (.0625, .1875)
    right_pole_xy_ratios   = (.9375, .1875)

    front_left_xy_ratios   = (.275, .3125)
    front_center_xy_ratios = (.5,   .3125)
    front_right_xy_ratios  = (.725, .3125)
    back_left_xy_ratios    = (.275, .725)
    back_center_xy_ratios  = (.5,   .725)
    back_right_xy_ratios   = (.725, .725)

    negative_text_offset_ratios  = ( 0.00625, -0.0125)
    positive_text_offset_ratios  = (-0.05625, -0.0125)
    bottom_text_offset_ratios = (-0.0125,   0.0875)

    data_green_rgb = (0, 255, 0, 100)
    data_red_rgb   = (255, 0, 0, 100)

    def __init__(self, size: int) -> None:

        # size is a determining factor for almost all drawable elements
        self.imgsize = size
        # base Image object is a blank fully transparent image
        self.court_diagram = Image.new('RGBA',size = (self.imgsize, self.imgsize), color = (255,255,255,0))
        self.draw = ImageDraw.Draw(self.court_diagram)
        self.courtsize = self.imgsize * self.court_size_ratio
        self.pole_size = self.imgsize * self.pole_size_ratio
        self.circle_size = int(self.circle_size_ratio * self.imgsize)
        self.font_size = int(self.font_size_ratio * self.imgsize) 
        self.font = ImageFont.truetype("arial.ttf", size = self.font_size)
        self.label_font_size = int(self.label_font_size_ratio * self.imgsize) 
        self.label_font = ImageFont.truetype("arial.ttf", size = self.label_font_size)

        # lots of x,y cooridinates canb be calculated from ratios now
        self.court_start_xy  = tuple([int(self.imgsize * x) for x in self.court_start_xy_ratios])
        self.left_pole_xy    = tuple([int(self.imgsize * x) for x in self.left_pole_xy_ratios])
        self.right_pole_xy   = tuple([int(self.imgsize * x) for x in self.right_pole_xy_ratios])

        self.front_left_xy   = tuple([int(self.imgsize * x) for x in self.front_left_xy_ratios])
        self.front_center_xy = tuple([int(self.imgsize * x) for x in self.front_center_xy_ratios])
        self.front_right_xy  = tuple([int(self.imgsize * x) for x in self.front_right_xy_ratios])

        self.back_left_xy    = tuple([int(self.imgsize * x) for x in self.back_left_xy_ratios])
        self.back_center_xy  = tuple([int(self.imgsize * x) for x in self.back_center_xy_ratios])
        self.back_right_xy   = tuple([int(self.imgsize * x) for x in self.back_right_xy_ratios])

        # court positions in rotation order, starting first with serving position
        self.court_positions_xy_list = [self.back_right_xy, self.back_center_xy, self.back_left_xy, 
                                        self.front_left_xy, self.front_center_xy,self.front_right_xy]

        # draw the basic elements of the court
        self.draw_court()

    def draw_court(self) -> None:
        #break out self variables into nicer names
        court_start_x, court_start_y = self.court_start_xy
        left_pole_x, left_pole_y = self.left_pole_xy
        right_pole_x, right_pole_y = self.right_pole_xy
        # draw the main court square
        self.draw_rectangle(self.court_start_xy, self.courtsize, width = 8)

        # draw the 10ft line
        self.draw.line((court_start_x, court_start_y + self.courtsize // 3,
                        court_start_x + self.courtsize, court_start_y + self.courtsize // 3 ),
                        fill = "black",
                        width = 5)
        
        # draw the net line 
        # need to adjust the x and y to cover the pixel width of the main rectangle lines
        self.draw.line((left_pole_x, left_pole_y + 4,
                        right_pole_x, left_pole_y + 4),
                        fill = "black",
                        width = 12)

        # draw the net circles
        self.draw_circle((left_pole_x, left_pole_y + 4),  self.pole_size, fill="black")
        self.draw_circle((right_pole_x, right_pole_y + 4),  self.pole_size, fill="black")

        # label the net
        label = "Net"
        w, h = self.draw.textsize(label, font = self.label_font)
        self.draw.text(((self.imgsize - w) / 2, court_start_y - (h*1.25) ), "Net", font=self.label_font, fill = 'black')
        

    def export(self, filename: str) -> None:
        # save the image to a file
        # this is down by "pasting the court onto a white background and maintaining its opacity settings"
        background = Image.new('RGBA',size = (self.imgsize, self.imgsize), color = (255,255,255,255))
        background.paste(self.court_diagram, (0,0), self.court_diagram)
        background.save(filename)

    def show(self) -> None:
        background = Image.new('RGBA',size = (self.imgsize, self.imgsize), color = (255,255,255,255))
        background.paste(self.court_diagram, (0,0), self.court_diagram)
        background.show()

    def draw_rectangle(self, coords: Tuple[int,int], size: int, width: int) -> None:
        x, y = coords
        self.draw.rectangle( (x, y, x + size, y + size), outline = "black", fill = None, width = width)
    
    def draw_circle(self, coords: Tuple[int,int], size: int, fill: Union[Tuple[int,int,int,int],str]) -> None:
        x, y = coords
        radius = size // 2
        self.draw.ellipse( (x - radius, y - radius, x + radius, y + radius), fill)
    

    def draw_semicircle_left(self, coords: Tuple[int,int], size: int, fill: Tuple[int,int,int,int]) -> None:
        x, y = coords
        radius = size // 2
        self.draw.chord((x - radius, y - radius, x + radius, y + radius), 90, 90 + 180, fill)       

    def draw_semicircle_right(self, coords: Tuple[int,int], size: int, fill: Tuple[int,int,int,int]) -> None:
        x, y = coords
        radius = size // 2
        self.draw.chord((x - radius, y - radius, x + radius, y + radius), 270, 90, fill)    

    def draw_data_circle(self, coords: Tuple[int,int], size: int, plus_value: int, minus_value: int) -> None:
        self.draw_semicircle_left(  coords, size = size, fill = self.data_green_rgb)
        self.draw_semicircle_right( coords, size = size, fill = self.data_red_rgb)
        self.draw.text(self.get_text_coords(coords, self.positive_text_offset_ratios) , f"{plus_value:>2}%",  font=self.font, fill = 'black')
        self.draw.text(self.get_text_coords(coords, self.negative_text_offset_ratios) , f"{minus_value:>2}%", font=self.font, fill = 'black')


    def get_text_coords(self, circle_coords: Tuple[int,int], text_offset_ratios: Tuple[int,int]) -> Tuple[int,int]:
        circle_x, circle_y = circle_coords
        text_offset_ratio_x, text_offset_ratio_y = text_offset_ratios
        return (circle_x + (text_offset_ratio_x * self.imgsize),
                circle_y + (text_offset_ratio_y * self.imgsize))

    def populate_image(self, data) -> None:
        # draw the label for the player name and number 
        self.draw.text((0,0) , f"{data['player']}, {data['number']}", font=self.label_font, fill = 'black')

        # break out the stats into nice variables 
        total_plus,total_minus = data['pm_stats']
        pos_stats_percentages = [(int(round(plus / total_plus,2) * 100),
                                  int(round(minus / total_minus,2) * 100)) 
                                  for (plus, minus) in data['pos_stats'] 
                                ]


        for ((plus,minus), court_pos_xy) in zip(pos_stats_percentages, self.court_positions_xy_list):
            self.draw_data_circle( court_pos_xy, self.circle_size, plus, minus)

        # self.draw_data_circle( self.front_left_xy ,   self.circle_size, example, example)
        # self.draw_data_circle( self.front_center_xy , self.circle_size, example, example)
        # self.draw_data_circle( self.front_right_xy ,  self.circle_size, example, example)
        
        # self.draw_data_circle( self.back_left_xy ,   self.circle_size, example, example)
        # self.draw_data_circle( self.back_center_xy , self.circle_size, example, example)
        # self.draw_data_circle( self.back_right_xy ,  self.circle_size, example, example)


        #TODO: make draw Helper class
# x1 y1 x2 y2

size = 1600
data = {'player': 'player', 'number': '??', 'total_match_points': 1, 'total_match_serves': 2, 'games': 1, 'pm_stats': [14, -25], 'pos_stats': [[1, -4], [3, -4], [4, -6], [1, -5], [3, -3], [2, -3]], 'ppg': 1.0, 'pps': 0.5}

court = VolleyCourt(size)
court.populate_image(data)
court.show()
court.export("test_court.png")
