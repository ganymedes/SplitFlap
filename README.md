# SplitFlap

ESP8266 based controller for split flap display modules. The code is all-in-one, meaning each module runs the same code, but in different modes set in EEPROM. The master runs the web server and controls the first unit, and each other unit acts as an I2C slave to control its own unipolar stepper motor.

## Video!

[![Splitflap Display in Action!](https://img.youtube.com/vi/YFdsrr4tarE/maxresdefault.jpg)](https://www.youtube.com/watch?v=YFdsrr4tarE)

## Attribution
This design is mostly [David Königsmann's fantastic design](https://github.com/Dave19171/split-flap) with changes to improve printability, improve durability, or reduce filament use. Specifically the unit has been reduced to 8 characters so it could be printed on an Ender 3 V2. That said, most of the changes are just personal preference, and hats off to David for his great design.

## Printing
Ready-to-print files for a **10-character** display are in [models/print](models/print/README.md). They use David's original 10-character case, the reinforced frame and rotors from this repo, and David's flaps (the umlaut-free set, matching the firmware). That folder has the quantities and print notes. The case pieces are up to about 241 mm long, so they need a bed larger than an Ender 3 V2's.

The 8-character version described above is still available as a single assembly in [models/AssemblyWithChanges.step](models/AssemblyWithChanges.step).

## Electronics
The name of the game is low-cost, and ease of construction. Not that David's design isn't already low cost, but I am a cheapskate. Each module's BOM is very low, making use of the ULN2003 that you usually get with your 28BYJ-48 steppers (as with David's) but instead of having an Arduino Nano for each, along with an ESP01, each module only uses a single ultra-cheap Wemos Lolin D1 Mini V4 (any version with the ESP8266EX, without the metal sheild, will work). The rest is just support components, and everything is through-hole mounted. 

## Software
The main difference between the two projects is in the software. Since David's module was split into two MCUs, on two different architectures, he had to maintain two different codebases. Therefore I chose to unify mine, not just for ease of programming (and debugging) but also easy of maintenance. Since everything is software controlled, including the I2C address, one only has to connect to Serial over USB on the master, or on the unit itself, to change any running parameters they want. 
Similarly, the web interface does a few things for you. There is a frontend to change what's displayed, and to change, for example, the timezone and date formating. However, there is also a RESTful API available if someone wanted to make their own front end.
Finally, indeed the software uses the Arduino platform code, but rather than being an Arduino project, it is a PlatformIO project. This was important for organization, since the way Arudino mangles up your code means compartmentalizing is often impossible.

## Wire implementation
The ESP8266 core has a bad I2C implementation. I've patched it up manually to keep it from doing weird things, and destabilizing the system, such as doing clock stretching in odd places, or setting SDA low/high immediately before or after toggling SCL. I've also enabled GCALL by means of always responding ACK to address 0. It seems to work, but it is certainly being misused. 

## Ordering the PCB
See [pcb/ORDERING.md](pcb/ORDERING.md) for a step-by-step guide to ordering the module PCB from JLCPCB, assembled except for the D1 Mini. It covers generating the Gerber, BOM and placement files in EasyEDA, every order option, and part matching.

## Guides
Step-by-step guides with photos are in [guides/](guides/). Their sources (HTML, images) are in [guides/src](guides/src/).

| Guide | Covers |
|---|---|
| [Soldering](guides/soldering.pdf) | Fitting the D1 Mini to the module PCB on plug-in headers, the fixes from *Building Notes* below, the USB power rule, multimeter checks, and wiring the 5 V converter |

## Building Notes
The PCB is missing four fixes. They have not been added to the schematic or the PCB, so you add them by hand. The [soldering guide](guides/soldering.pdf) shows where.

| Fix | Boards | Parts |
|---|---|---|
| Reroute the hall sensor from D3 to D0 | Every module | Remove the D3 pin from the D1 Mini's male header before soldering it, add a wire from D3 to D0 |
| Pullup on D0 | Every module | 1 × 10 kΩ from D0 to 3V3 |
| I2C pullups | Master only (one per display) | 2 × 4.7 kΩ, from SDA (D2) and from SCL (D1) to 3V3 |
| Capacitor on the motor driver | Every module | 1 × 10 nF ceramic, 50 V, under the board between pins 8 (GND) and 9 (COM) of the ULN2003 (U4). They are the two chip pins next to the 12V sockets, opposite each other. |

Why each fix is needed:

- **Hall sensor on D0, not D3.** D3 is GPIO0, which the ESP8266 reads at power-on to decide how to boot. If it is low, the chip waits for new firmware instead of starting. The hall sensor pulls its line low whenever the magnet is in front of it, so a module whose drum stopped there would not start. D0 plays no part in booting, and the firmware reads the sensor on D0 (`HALL` in [include/Config.h](include/Config.h)).
- **10 kΩ pullup on D0.** The diode on the PCB keeps the sensor's 5 V away from the 3.3 V input, so the sensor can only pull the line low. Without a magnet nothing pulls the line high, and the input floats and gives random readings. Most ESP8266 pins have a built-in pullup, but D0 does not.
- **4.7 kΩ pullups on SDA and SCL.** All modules share one I2C bus. Each module can only pull the lines low, and the pullups pull them back high. One pair is enough for the whole display. The other modules switch their built-in pullups off in slave mode ([src/main.cpp](src/main.cpp)), so the pullups sit on the master. The built-in ones are too weak for a bus that runs through ten modules and their cables.
- **10 nF on the ULN2003.** dmlambo, who designed this board, lists this fix in [issue #1](https://github.com/dmlambo/SplitFlap/issues/1) of the original repo: "add small cap between com and ground on driver chip (7-10nF)". The issue gives no reason. Our explanation: each time the driver switches a motor coil off, the coil sends a short voltage spike back into the 12 V line through COM (pin 9), and the board has no capacitor on the 12 V line to absorb it. A display without it probably still works. The capacitor is cheap insurance against noise on the lines all modules share.

## Wiring
Each module PCB has six JST-XH sockets. The motor, hall sensor, power supply, converter and connector parts are listed in [pcb/ORDERING.md](pcb/ORDERING.md#parts-jlcpcb-doesnt-assemble).

| Socket | Pins | Connects to |
|---|---|---|
| 12VIN, 12VOUT | 1 = +12 V, 2 = GND | The 12 V supply, and on to the next module, pin 1 to pin 1. The two sockets are wired together. |
| I2C-A, I2C-B | 1 = GND, 2 = +5 V, 3 = SDA, 4 = SCL | The previous and the next module, pin 1 to pin 1. The two sockets are wired together. |
| 5-pin motor socket | 1–4 = coils, 5 = +12 V | The 28BYJ-48 motor. Its plug fits directly. |
| HALL | 1 = GND, 2 = +5 V, 3 = signal | The KY-003 hall sensor. |

Chain the modules: the 12 V supply goes into 12VIN of module 1, each module's 12VOUT goes to the next module's 12VIN, and each I2C-B goes to the next module's I2C-A. The master can be any module. Figure 8 in the [soldering guide](guides/soldering.pdf) shows the whole chain.

### Power
The PCB has no voltage regulator. The 12 V only reaches the motor and the ULN2003. The D1 Mini and the hall sensor run on a separate 5 V line, and every module gets it through the I2C cables.

- **One 12 V → 5 V step-down converter per display.** Use one with a fixed 5 V output, rated 2.5 A or more. Our estimate, not measured: about 80 mA per D1 Mini, with short WiFi peaks above that, so about 1 A for 10 modules. Our pick is the DFRobot DFR0831 (7–24 V in, 5 V 4 A out). It sits next to module 1: its input is wired straight to the DC socket, together with the lead to module 1's 12VIN, and its output goes into module 1's free I2C-A (+ to 5V, − to GND). Step 7 of the [soldering guide](guides/soldering.pdf) shows how to make the leads, wire the DC socket and test everything.
- **Never put 12 V on the 5 V line.** The D1 Mini's 5V pin can't take it.
- **Plug in the 12 V supply before you plug USB into any D1 Mini, or unplug the converter first.** dmlambo writes in [issue #1](https://github.com/dmlambo/SplitFlap/issues/1) that the converter "lets current pass through to the in side of the board when powering from USB, which tries to power the motors", and suggests a diode on the master's 5 V input. We follow this rule instead, because a diode would lower the 5 V line by about 0.4 V. That the rule avoids the problem is our reading: with the 12 V on, the converter's input already sits at 12 V. Firmware updates don't need USB (see the FAQ).
- **Testing a single module without the converter:** plug USB into its D1 Mini, which also powers the 5 V line, and connect 12 V to 12VIN for the motor.

## FAQ
### How do I disconnect my display from the network?
There's a reset button on the left side. Press it three times. This should clear your credentials.

### How do I update my firmware/filesystem?
Go to http://splitflap.local/update.html and put your firmware.bin/littlefs.bin file into the form and press submit. Wait about 30 seconds, or until the form times out. Do not reset your device until you regain contact with it through the web portal, or you might interrupt the update sequence.

### I flashed a new firmware that had a change to the Config structure, and now my display isn't responding
There's a reset button on the left side. Press it six times. This makes the module the master again (it does not toggle). Since six presses also counts as three or more, it clears your WiFi credentials too, so you will have to reconnect it to your network.
