# Utveckla för NodeMCU
För att kunna programmera NodeMCU (det mikroprocessorkort som vi kommer att använda under labben) så måste man ha en utvecklingsmiljö installerad. Det finns ett par alternagiv, dels [Arduino IDE](https://www.arduino.cc/en/software) som är en enkel utvecklingsmiljö samt [PlatformIO](https://platformio.org/) som har lite mer att bjuda på. Vilken som helst av dem går bra att använda för labbarna.

## Arduino IDE
I Arduino IDE måste man göra lite konfiguration för att få tillgång till NodeMCU. Efter att man installerat går man till "Preferences" och matar in följande URL i "Additional boards manager URLs:"

`http://arduino.esp8266.com/stable/package_esp8266com_index.json`
Gå sedan till "Boards Manager" och sök efter "nodemcu". Installera.

Nu ska det gå att välja "NodeMCU 1.0 (ESP-12E Module)" när man väljer kort.

# USB Driver för Mac M1
För att prata serieport från IDE:n så måste man ha en drivrutin installerad. Ladda hem och installera.
[Driver för Mac M1](https://www.silabs.com/Support%20Documents/Software/Mac_OSX_VCP_Driver.zip)
