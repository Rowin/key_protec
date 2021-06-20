from wiegand import Wiegand
from machine import Pin

wiegand_one = Pin(27, Pin.IN, Pin.PULL_DOWN)

while True:
    print(wiegand_one.value())

# wiegand_one.irq(handler=lambda _: print("IRQ"), trigger=Pin.IRQ_FALLING)