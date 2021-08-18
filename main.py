import sys
import utime
import urandom
import machine
from machine import Pin, Signal, ADC, I2C, PWM
import driver_i2clcd1602

# VARIABLE
mode=0
userpassword=[0,0,0,0]
status="opened"
checkpass=0
wrongpass=0
saveinput=[0,0,0,0]

# GPIO DEFINE
pin_servo=PWM(Pin(4, Pin.OUT), freq=50, duty=75)
pin_button01=Signal(Pin(27, Pin.IN, Pin.PULL_UP), invert=True)
pin_button02=Signal(Pin(18, Pin.IN, Pin.PULL_UP), invert=True)
pin_button03=Signal(Pin(19, Pin.IN, Pin.PULL_UP), invert=True)
i2c = I2C(1, sda=Pin(21), scl=Pin(22))

# GPIO INIT
addreesslist=i2c.scan() # list
I2C_ADDR = int(addreesslist[0]) #0x27
lcd = driver_i2clcd1602.I2CLCD1602(i2c, addr=I2C_ADDR)
lcd.on()

pin_servo.duty(75)
utime.sleep(1)

while True :
    lcd.clear()
    lcd.puts("ROTATE GAME",0,0)
    lcd.puts("SELECT YOUR MODE",0,1)

    while True :
        if pin_button01.value() == 1 :
            mode=1
            utime.sleep(0.3)
            break
        elif pin_button02.value() == 1 :
            mode=2
            utime.sleep(0.3)
            break
        utime.sleep(0.1)
    
    if mode == 1 :
        lcd.clear()
        lcd.puts("MODE:TIME RANDOM",0,0)
        lcd.puts("PUSH BUTTON 3",0,1)
        while True :
            if pin_button03.value() == 1 :
                break
            utime.sleep(0.1)
        temp=0
        while temp < 8 :
            pin_servo.duty(urandom.randrange(30,120))
            utime.sleep(0.5)
            temp+=1
        pin_servo.duty(urandom.randrange(30,120))
        utime.sleep(3)
    elif mode == 2 :
        lcd.clear()
        lcd.puts("MODE:PUSH RANDOM",0,0)
        lcd.puts("PUSH BUTTON 3",0,1)
        while True :
            pin_servo.duty(urandom.randrange(30,120))
            utime.sleep(0.01)
            if pin_button03.value() == 1 :
                break
            utime.sleep(0.1)
        pin_servo.duty(urandom.randrange(30,120))
        utime.sleep(3)
    mode=0