# AGENTS.md

Instructions for AI coding agents working in this repository.

## Git workflow

- After every completed change, commit it and push to `origin` without asking first.
- `origin` is our fork (`github.com/ganymedes/SplitFlap`). Never push to the upstream repository.
- Use small, focused commits with a descriptive message.

## Keep the docs in sync

The docs are `README.md`, the other `.md` files (such as `pcb/ORDERING.md` and `models/print/README.md`) and the PDF guides in `guides/`.

- Every change must leave the docs accurate. When a change affects anything they describe (features, web UI or REST API, serial commands, reset-button behaviour, pins and wiring, PCB fixes, parts, build, flashing or assembly steps, dependencies), update every affected doc in the same commit.
- The same applies to decisions and new findings, even when no code changes. Examples: a PCB fix found in an upstream issue, a measured value, a part choice. Write them into every doc they affect.
- A PDF guide is updated through its HTML source in `guides/src/<name>/`, and then the PDF is rebuilt from it. Commit the source and the PDF together.
- If you notice a doc already disagrees with the code or with what we know, fix the doc (or flag it if the code looks wrong).

## Project

ESP8266 (Wemos D1 Mini) firmware for split-flap display modules, built with PlatformIO (`platformio.ini`, env `d1_mini`). Every module runs the same firmware. The master runs the web server and drives the other modules over I2C.

- `src/`, `include/`: firmware sources (C++ / Arduino framework)
- `data/`: web frontend, uploaded to the LittleFS filesystem
- `models/`, `pcb/`: 3D models and PCB files
- `guides/`: step-by-step build guides as PDFs (`guides/<name>.pdf`), each built from an HTML source in `guides/src/<name>/`. List every guide in the README's *Guides* section.

## Build

- Build: `pio run`
- Upload firmware: `pio run -t upload`
- Upload filesystem (`data/`): `pio run -t uploadfs`
- Serial monitor: `pio device monitor` (57600 baud)

## Gotchas

- `include/moduleVersion.h` is generated before every build by `randomInt.py`. It holds a random build ID that modules compare to check they run the same firmware. It is gitignored: never commit it and never edit it by hand.
- `platformio.ini` uses a patched ESP8266 core (`dmlambo/ESP8266-Arduino-I2C`) for I2C stability. Don't replace it with the stock core.
- Changing the `Config` struct breaks configs already saved in EEPROM on deployed modules (see README FAQ).
