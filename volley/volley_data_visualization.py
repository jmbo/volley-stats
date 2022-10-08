
from PIL import Image, ImageDraw, ImageFont
import pdb
import math
from typing import List, Set, Dict, Tuple, Union

class VolleyCourt(object):

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
        # self.court_diagram = Image.open(image_path)
        # self.imgsize = self.court_diagram.height
        self.imgsize = size
        self.court_diagram = Image.new('RGBA',size = (self.imgsize, self.imgsize), color = (255,255,255,0))
        self.draw = ImageDraw.Draw(self.court_diagram)
        self.courtsize = self.imgsize * self.court_size_ratio
        self.pole_size = self.imgsize * self.pole_size_ratio
        self.circle_size = int(self.circle_size_ratio * self.imgsize)
        # self.draw = ImageDraw.Draw(self.court_diagram)
        self.font_size = int(self.font_size_ratio * self.imgsize) 
        self.font = ImageFont.truetype("arial.ttf", size = self.font_size)
        self.label_font_size = int(self.label_font_size_ratio * self.imgsize) 
        self.label_font = ImageFont.truetype("arial.ttf", size = self.label_font_size)
        # self.background = Image.new('RGBA',size = (self.imgsize, self.imgsize), color = (255,255,255,255))

        self.court_start_xy  = tuple([int(self.imgsize * x) for x in self.court_start_xy_ratios])
        self.left_pole_xy    = tuple([int(self.imgsize * x) for x in self.left_pole_xy_ratios])
        self.right_pole_xy   = tuple([int(self.imgsize * x) for x in self.right_pole_xy_ratios])

        self.front_left_xy   = tuple([int(self.imgsize * x) for x in self.front_left_xy_ratios])
        self.front_center_xy = tuple([int(self.imgsize * x) for x in self.front_center_xy_ratios])
        self.front_right_xy  = tuple([int(self.imgsize * x) for x in self.front_right_xy_ratios])

        self.back_left_xy    = tuple([int(self.imgsize * x) for x in self.back_left_xy_ratios])
        self.back_center_xy  = tuple([int(self.imgsize * x) for x in self.back_center_xy_ratios])
        self.back_right_xy   = tuple([int(self.imgsize * x) for x in self.back_right_xy_ratios])

        
        self.draw_court()

    def draw_court(self):
        # draw the main court square
        self.draw_rectangle(self.court_start_xy, self.courtsize, width = 8)

        # draw the 10ft line
        self.draw.line((self.court_start_xy[0] , self.court_start_xy[1] + self.courtsize // 3,
                        self.court_start_xy[0] + self.courtsize, self.court_start_xy[1] + self.courtsize // 3 ),
                        fill = "black",
                        width = 5)
        
        # draw the net line 
        # need to adjust the x and y to cover the lines of
        self.draw.line((self.left_pole_xy[0] , self.left_pole_xy[1] + 4,
                        self.right_pole_xy[0] , self.right_pole_xy[1] + 4),
                        fill = "black",
                        width = 12)

        # draw the net circles
        self.draw_circle((self.left_pole_xy[0],self.left_pole_xy[1] + 4),  self.pole_size, fill="black")
        self.draw_circle((self.right_pole_xy[0],self.right_pole_xy[1] + 4),  self.pole_size, fill="black")

        # label the net
        label = "Net"
        w, h = self.draw.textsize(label, font = self.label_font)
        self.draw.text(((self.imgsize - w) / 2, self.court_start_xy[1] - (h*1.25) ), "Net", font=self.label_font, fill = 'black')
        

    def export(self, filename: str) -> None:
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

    def draw_line(self, coords: Tuple[int,int], length: int, width: int):
        self.draw.line((125,size-1200-100 + 4, size-100,size-1200-100+4 ), fill = "black", width = 12)
    
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
        self.draw_semicircle_left(  coords, size = size, fill = (0, 255, 0, 100))
        self.draw_semicircle_right( coords, size = size, fill = (255, 0, 0, 100))
        self.draw.text(self.get_text_coords(coords, self.positive_text_offset_ratios) , f"{plus_value:>2}%",  font=self.font, fill = 'black')
        self.draw.text(self.get_text_coords(coords, self.negative_text_offset_ratios) , f"{minus_value:>2}%", font=self.font, fill = 'black')


    def get_text_coords(self, circle_coords: Tuple[int,int], text_offset_ratios: Tuple[int,int]):
        return (circle_coords[0] + (text_offset_ratios[0] * self.imgsize),
                circle_coords[1] + (text_offset_ratios[1] * self.imgsize))

    def populate_image(self, data):
        # self.draw_circle( self.front_left_xy,   self.circle_size, fill = (0, 255, 0, 100))
        # self.draw_circle( self.front_center_xy, self.circle_size, fill = (0, 255, 0, 100))
        # self.draw_circle( self.front_right_xy,  self.circle_size, fill = (0, 255, 0, 100))

        # self.draw_circle(self.draw, back_left_xy,    self.circle_size, fill = (0, 255, 0, 100))
        # self.draw_circle(self.draw, back_middle_xy,  self.circle_size, fill = (0, 255, 0, 100))

        example =  15

        self.draw_data_circle( self.front_left_xy ,   self.circle_size, example, example)
        self.draw_data_circle( self.front_center_xy , self.circle_size, example, example)
        self.draw_data_circle( self.front_right_xy ,  self.circle_size, example, example)
        
        self.draw_data_circle( self.back_left_xy ,   self.circle_size, example, example)
        self.draw_data_circle( self.back_center_xy , self.circle_size, example, example)
        self.draw_data_circle( self.back_right_xy ,  self.circle_size, example, example)


        
        self.draw_semicircle_right( self.back_right_xy, size = self.circle_size,fill = (255, 0, 0, 100))
        self.draw_semicircle_left( self.back_right_xy, size = self.circle_size,fill = (0, 255, 0, 100))

        # get_left_text_coords
        # draw.text((back_right_xy[0] + 5, back_right_xy[1] - 10) , f"{thirty:>2}%", font=font, fill = 'black')
        # draw.text((back_right_xy[0] -45, back_right_xy[1] - 10) , f"{one:>2}%", font=font, fill = 'black')
        self.draw.text(self.get_text_coords(self.back_right_xy, self.positive_text_offset_ratios) , f"{example:>2}%", font=self.font, fill = 'black')
        self.draw.text(self.get_text_coords(self.back_right_xy, self.negative_text_offset_ratios) , f"{example:>2}%", font=self.font, fill = 'black')


# x1 y1 x2 y2

size = 1600
data = {'player': 'player', 'num': '??', 'total_match_points': 1, 'total_match_serves': 2, 'games': 1, 'pm_stats': [14, -25], 'pos_stats': [[1, -4], [3, -4], [4, -6], [1, -5], [3, -3], [2, -3]], 'ppg': 1.0, 'pps': 0.5}

court = VolleyCourt(size)
court.populate_image(data)
court.show()
court.export("test_court.png")
