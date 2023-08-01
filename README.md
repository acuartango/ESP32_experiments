# ESP32_experiments

I do this only for fun, i'm not an expert!

I'll try to put here some experiments made with a cheap (~4€) ESP32:

ESP-32S ESP-WROOM-32

https://es.aliexpress.com/item/32864722159.html?storeId=1022067&spm=a219c.search0604.3.3.6bfd39c3a2uUEC&ws_ab_test=searchweb0_0%2Csearchweb201602_2_10065_10068_10547_319_317_10548_10696_10084_453_10083_454_10618_10307_10820_10821_10301_10303_537_536_10059_10884_10887_321_322_10103%2Csearchweb201603_52%2CppcSwitch_0&algo_expid=39d76576-ead1-4353-898d-c7744f8c93ec-0&algo_pvid=39d76576-ead1-4353-898d-c7744f8c93ec&transAbTest=ae803_5

Color Screen 240x320 2,8"   SPI TFT LCD Touch Panel  ILI9341  (~6€)
https://es.aliexpress.com/item/32815224002.html?spm=a2g0s.9042311.0.0.274263c05yMBw1


To use the LCD Screen i've tried this library:
https://github.com/20after4/micropython-esp32-wrover-lcd


The first is to put micropython in our ESP32 chip (I've done in Linux terminal):
- Install the firmware tool "esptool"
```
pip install esptool
```

- Erase Flash
```
esptool.py --port /dev/ttyUSB0 erase_flash
```
- Install Micropython FOR ESP32! (https://micropython.org/download#esp32)
```
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20190701-v1.11-81-g9ca478913.bin
```
- How to connect to the ESP32's python shell:
```
sudo screen /dev/ttyUSB0 115200
```

- To copy files to the ESP32 we'll need the tool "ampy":
```
pip install adafruit-ampy
```
- List files
```
sudo ampy --port /dev/ttyUSB0 ls
boot.py
```

- Download the code of this library in our linux:
git clone https://github.com/20after4/micropython-esp32-wrover-lcd.git


- copy all needed files from linux to ESP32:
```
sudo ampy --port /dev/ttyUSB0 put ili9341.py
```

- If we need to delete ESP32's  files from linux:
```
sudo ampy --port /dev/ttyUSB0 rm test.py
```

- Connect that ESP32's Pins to LCD Screen (all names are written in the chips!):
```
SDO(MISO)		-	G12
LED			    -	3.3V  (backlight if we want to switch on&off we can connect to other Pin and switch on or off...)
SCK			    -	G14
SDI(MOSI)		-	G13
DC			    -	G5
RESET 		  -	G16
CS			    -	G15
GND			    -	GND
VCC 			  -	5v
```

- Write this at ESP32's micropython shell
```
import ili9341

from machine import Pin, SPI

--spi = SPI(mosi=Pin(13), sck=Pin(14))

spi = SPI(mosi=Pin(13), miso=Pin(12),sck=Pin(14))

display = ili9341.ILI9341(spi, cs=Pin(15), dc=Pin(5), rst=Pin(16))

# Fill the screen in black

display.fill(0)

# Write a pixel

display.pixel(120, 160, 0)
```


## Ejemplo de ESP32-CAM para montar una web en el esp32 que saque y muestre una foto

Pasos 
- Carga en el ESP32-CAM el firmare de @lemariva
  - https://github.com/lemariva/micropython-camera-driver/tree/master/firmware
    - micropython_camera_feeeb5ea3_esp32_idf4_4.bin
    - 
- Copia este programa en el raíz del ESP32-CAM como "main.py" para que se ejecute
  - sudo bin/ampy --port /dev/ttyUSB0 put servidorWebMostrarFoto2.py main.py
- Conecta al ESP32 para ver algunos logs
  - sudo screen /dev/ttyUSB0 115200
 



enjoy!
