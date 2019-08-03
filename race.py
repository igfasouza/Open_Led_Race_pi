import keyboard
import curses
import pygame
import _rpi_ws281x as ws

from rpi_ws281x import PixelStrip, Color

LED_COUNT      = 302     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 5)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest

color1 = Color(255,0,0)
color2 = Color(0,255,0)

tbeep = 4
speed1 = 0
speed2 = 0
total1 = 0
current1 = 1
total2 = 0
current2 = 1
loop1 = 0
loop2 = 0

leader = 0
loop_max = 5
acel = 0.2
friction = 0.01
kf = 1.5

flag1_sw1 = 0
flag_sw2 = 0

laps1 = 0
laps2 = 0
total_laps = 2


def clean(strip):
   for i in range(strip.numPixels()):
      strip.setPixelColor(i,Color(0,0,0))     
      strip.show()
     
def show_winner(strip,color):
   for i in range(strip.numPixels()):
      strip.setPixelColor(i,color)     
      strip.show()

def winner(player1, player2, color1, color2, strip):
    if(player1 > player2):
        show_winner(strip, color1)
    else:
        show_winner(strip, color2)
     
def draw_car(strip, dist, color):
   strip.setPixelColor(dist-1,Color(0,0,0))
   strip.setPixelColor(dist-2,Color(0,0,0))
   strip.setPixelColor(dist-3,Color(0,0,0))
   for i in range(5):
      strip.setPixelColor(i+dist,color)
      strip.show()
      
def clean_last(strip, dist, laps):
   if dist > 295:
      laps = laps + 1
      dist = 5
      strip.setPixelColor(295,Color(0,0,0))
      strip.setPixelColor(296,Color(0,0,0))
      strip.setPixelColor(297,Color(0,0,0))            
      strip.setPixelColor(298,Color(0,0,0))
      strip.setPixelColor(299,Color(0,0,0))

def car_speed(dist):
    return dist + 3

def clean_last_position():
    strip.setPixelColor(295,Color(0,0,0))
    strip.setPixelColor(296,Color(0,0,0))
    strip.setPixelColor(297,Color(0,0,0))            
    strip.setPixelColor(298,Color(0,0,0))
    strip.setPixelColor(299,Color(0,0,0))
    
def finish_lap():
    global current1
    global laps1
    global total1
    global current2
    global laps2
    global total2
    if current1 > 295:
        laps1 = laps1 + 1
        total1 += current1
        current1 = 1
        clean_last_position()
    if current2 > 295:
        laps2 = laps2 + 1
        total2 += current2
        current2 = 1
        clean_last_position()
        
def reset_variables():
    global laps1
    laps1 = 0
    global laps2
    laps2 = 0
    global current1
    current1 = 1
    global current2
    current2 = 1
    global total1
    total1 = 0
    global total2
    total2 = 0
        
def start_game():
    global laps1
    global laps2
    global total_laps
    global strip
    global current1
    global current2
    global color1
    global color2
    global total1
    global total2
    
    clean(strip)
    
    pygame.init()
    screen = pygame.display.set_mode((1,1)) 
    
    #cli = curses.initscr()
    #cli.nodelay(1)
    
    key = pygame.key.get_pressed()
        
    while True:
        if laps1 == total_laps or laps2 == total_laps:
            #curses.endwin()
            pygame.quit()
            break        
            
        draw_car(strip, current1, color1)
        draw_car(strip, current2, color2)
        
        #key = cli.getch()
     
        #if keyboard.is_pressed('a'):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    current1 = car_speed(current1)
                if event.key == pygame.K_w:
                    current2 = car_speed(current2)
                
        #if key == 97: # key a
         #   current1 = car_speed(current1)
        #if key == 119: # key w
            #current2 = car_speed(current2)
            
        if current1 > 295 or current2 > 295:
            finish_lap()         
         
        strip.show()
         
    print("game finished")
    total1 += current1
    total2 += current2
    winner(total1, total2, color1, color2, strip)
    reset_variables()
    
        
# Main program logic follows:
if __name__ == '__main__':
   strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 0 )
   strip.begin()
   clean(strip)
      
   try:
  
      while True:
   
          start_game()
          
          varinput = input("New game? ")
          if varinput == 'n':
             break
          
      
   except KeyboardInterrupt:
      clean(strip)

