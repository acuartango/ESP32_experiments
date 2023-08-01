import network
import uos
import time
import socket
import machine
# Soporte para cámaras OV2640 y OV7670.
import camera
import ujson
from machine import Pin, UART
import binascii

bytes_types = (bytes, bytearray)  # Types acceptable as binary data

# Base64 encoding/decoding uses binascii

def b64encode(s, altchars=None):
    """Encode a byte string using Base64.

    s is the byte string to encode.  Optional altchars must be a byte
    string of length 2 which specifies an alternative alphabet for the
    '+' and '/' characters.  This allows an application to
    e.g. generate url or filesystem safe Base64 strings.

    The encoded byte string is returned.
    """
    if not isinstance(s, bytes_types):
        raise TypeError("expected bytes, not %s" % s.__class__.__name__)
    # Strip off the trailing newline
    encoded = binascii.b2a_base64(s)[:-1]
    if altchars is not None:
        if not isinstance(altchars, bytes_types):
            raise TypeError("expected bytes, not %s"
                            % altchars.__class__.__name__)
        assert len(altchars) == 2, repr(altchars)
        return encoded.translate(bytes.maketrans(b'+/', altchars))
    return encoded

# Configura la conexión WiFi
WIFI_SSID = 'miWifi'
WIFI_PASSWORD = 'miClave'

# Configura los pines para la cámara
CAMERA_LED_PIN = 4
CAMERA_LED = Pin(CAMERA_LED_PIN, Pin.OUT)

# Inicializar la cámara
#camera.init(0, format=camera.JPEG)
camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)

# flip up side down
camera.flip(1)
# left / right
camera.mirror(1)

# framesize: The options are the following:
# FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
# FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
# FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA FRAME_FHD
# FRAME_P_HD FRAME_P_3MP FRAME_QXGA FRAME_QHD FRAME_WQXGA
# FRAME_P_FHD FRAME_QSXGA
# Check this link for more information: https://bit.ly/2YOzizz
camera.framesize (camera.FRAME_240X240)
# 10-63 lower number means higher quality
camera.quality(10)
# -2,2 (default 0). 2 brightness
camera.brightness(0)
# sturation -2,2 (default 0). -2 grayscale 
camera.saturation(0)
# The options are the following:
# WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME
camera.whitebalance(camera.WB_NONE)
# EFFECT_NONE (default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO
camera.speffect(camera.EFFECT_NONE)


'''
FRAME_240X240   FRAME_96X96     FRAME_CIF       FRAME_FHD
FRAME_HD        FRAME_HQVGA     FRAME_HVGA      FRAME_P_3MP
FRAME_P_FHD     FRAME_P_HD      FRAME_QCIF      FRAME_QHD
FRAME_QQVGA     FRAME_QSXGA     FRAME_QVGA      FRAME_QXGA
FRAME_SVGA      FRAME_SXGA      FRAME_UXGA      FRAME_VGA
FRAME_WQXGA     FRAME_XGA
'''

# Función para capturar una foto
def capture_photo_base64():
    print("Capturando foto...")
    CAMERA_LED.on()
    time.sleep(1/2)  # Espera 1/2 segundos para asegurarse de que el LED de la cámara esté encendido
    img = camera.capture()
    time.sleep(1)  # Espera 1 segundo para asegurarse de que la captura de la imagen se haya completado
    CAMERA_LED.off()
    print("Imagen:")
    #print(img)
    return str(b64encode(img))[2:-1]

# Configura la conexión WiFi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
while not sta_if.isconnected():
    pass

# Imprime la dirección IP para acceder al servidor
print("Conexión establecida. Dirección IP:", sta_if.ifconfig()[0])

# Configura el servidor web
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
s.listen(1)

print("Servidor web listo.")

def handle_request(conn):
    html=''

    request = conn.recv(1024)
    print("Solicitud recibida:")
    print(request)

    if "takePhoto" in str(request):
        foto = capture_photo_base64()
        print("Tamaño foto: " + str(len(foto)))
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>ESP32-CAM</title>
        </head>
        <body>
            <h1>ESP32-CAM</h1>
            <img src="data:image/jpeg;base64,{}" width="640" height="480" />
            <a href="/takePhoto">Sacar Foto</a>
        </body>
        </html>""".format(foto)
    else:
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>ESP32-CAM</title>
            <style>
                .boton-enlace {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: #fff;
                    text-decoration: none;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                }
                .boton-enlace:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <h1>ESP32-CAM</h1>
            <a href="/takePhoto" class="boton-enlace">Sacar Foto</a>
        </body>
        </html>"""
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html\r\n"
    response += "Content-Length: {}\r\n".format(len(html))
    response += "\r\n"
    response += html
    conn.sendall(response)
    conn.close()

while True:
    print("Dirección IP del ESP32-CAM:", sta_if.ifconfig()[0])
    conn, addr = s.accept()
    print("Conexión entrante desde:", addr)
    handle_request(conn)



'''
# Acceso a la SD card

uos.mount(machine.SDCard(), "/sd") 
now_file = '-'.join([ str(x) for x in time.localtime()[:6] ]) + '.jpg'
imgFile = open("/sd/" + now_file, "wb")
imgFile.write(img)
imgFile.close()
uos.umount("/sd")

'''
