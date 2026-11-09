# Ordering the PCB from JLCPCB

How to order the module PCB from JLCPCB, assembled except for the D1 Mini. You need one board per character. For a 10-character display, order 10, or 15 if you want spares.

The board is 2 layers, 40 × 80 mm. The smallest trace is 0.25 mm (10 mil), the vias are 0.3 mm, and all components are through-hole on the top side. Standard JLCPCB options cover everything.

## 1. Generate the production files in EasyEDA

The repo contains EasyEDA Standard source files, not Gerbers, so you generate the Gerbers first.

1. Open <https://easyeda.com/editor> (Standard edition) and log in. A JLCPCB account works.
2. **File → Open → EasyEDA Source…** and choose `PCB_PCB_SplitFlap_2023-06-04.json`. When asked, pick **Import File**. "Extract Libs" only copies the footprints into your library.
3. Press **Shift+B** to rebuild the copper fills.
4. **Design → Check DRC**. The **Design Manager → DRC Errors** list on the left should be empty.
5. Export three files:
   - **Fabrication → PCB Fabrication File (Gerber)** → *Generate Gerber*. This gives a `.zip`.
   - **Fabrication → BOM** → *Export BOM*. This gives a `.csv`.
   - **Fabrication → Pick and Place File** → *Export*. This gives a `.csv`, which JLCPCB calls the "CPL".

## 2. PCB options

Upload the Gerber `.zip` at jlcpcb.com → *Order now*. The dimensions and layer count are filled in from the file.

| Option | Choose | Why |
|---|---|---|
| Base Material | FR-4 | Standard |
| Layers | 2 | |
| Dimensions | 40 × 80 mm | Detected from the Gerbers |
| PCB Qty | 10 (or 15) | One per character |
| Product Type | Industrial/Consumer electronics | |
| Different Design | 1 | |
| Delivery Format | Single PCB | |
| PCB Thickness | 1.6 mm | |
| PCB Color | Green | Cheapest and fastest; other colours are fine |
| Silkscreen | White | Set automatically by the PCB colour |
| Material Type | FR4 TG135 | The branded laminates (KB6164, KB6165F TG155, Nan Ya) give no benefit here |
| Surface Finish | LeadFree HASL | Easy to solder and stores well. Avoid OSP (short shelf life) and ENIG (unnecessary cost) |

### High-spec options

| Option | Choose | Why |
|---|---|---|
| Outer Copper Weight | 1 oz | Enough for the currents |
| Via Covering | Tented | |
| Via Plating Method | Not Specified | |
| Min via hole size/diameter | 0.3 mm / (0.4/0.45 mm) | Matches the board's 0.3 mm vias. Smaller options only add cost |
| Board Outline Tolerance | ±0.2 mm (Regular) | |
| Confirm Production file | **Yes** | You approve JLCPCB's production files before manufacturing. Worth it for an imported design; adds about a day |
| Mark on PCB | Remove Mark | No order number printed on the board (formerly "Remove order number") |
| Electrical Test | Flying Probe Fully Test | Free |
| Gold Fingers, Castellated Holes, Edge Plating, Blind Slots, UL Marking, Humidity Indicator Card | No | Not needed |

## 3. PCB Assembly options

Turn on **PCB Assembly**.

| Option | Choose | Why |
|---|---|---|
| PCBA Type | **Standard** | Economic assembly handles surface-mount parts only; every part here is through-hole |
| Assembly Side | **Top Side** | All footprints are on the top |
| PCBA Qty | Same as PCB qty | |
| Tooling holes | Added by JLCPCB | |
| Confirm Parts Placement | **Yes** | You check part orientation in the preview (step 5) |
| Stencil Storage | No | |
| Fixture Storage | No | |
| Parts Selection | **By Customer (Self-Service)** | The BOM already contains the LCSC part numbers |

### Advanced options

| Option | Choose | Why |
|---|---|---|
| Bake Components | No | |
| Board Cleaning | No | |
| Packaging | Antistatic bubble film | Default |
| Depanel boards & edge rail before delivery | No | Boards are delivered as single PCBs |
| Flying Probe Test | No | The bare boards are already tested |
| Function test | No | |
| Photo Confirmation | No | Optional: photos of the finished boards for a small fee |
| Conformal Coating | No | |
| Special stencil | No | |
| Solder Paste | High temp. (default) | Irrelevant, because there are no paste-soldered parts |
| Nitrogen reflow soldering | No | |
| Assembly remark | No | |

Accept the assembly terms and click **Next**.

## 4. Upload the BOM and CPL, then match the parts

Upload the BOM and CPL `.csv` files. The parts should match automatically:

| Ref | Part | LCSC # |
|---|---|---|
| U4 | ULN2003APG (DIP-16) | C5251 |
| D1 | 1N4148 (DO-35) | C2992430 |
| 12VIN, 12VOUT | JST B2B-XH-AM (2-pin) | C161869 |
| HALL | JST B3B-XH-AM (3-pin) | C161870 |
| I2C-A, I2C-B | JST B4B-XH-AM (4-pin) | C161871 |
| CN2 (motor) | JST B5B-XH-AM (5-pin) | C161872 |
| U2 | 9-pin female header, 2.54 mm | C5224028 |
| **U1** | **Wemos D1 Mini** | **Not available, so untick it ("do not place")** |

If a part is out of stock, choose an equivalent through-hole part with the same footprint. These substitutes worked in November 2026, when the original parts were out of stock:

| Ref | Substitute | LCSC # | Note |
|---|---|---|---|
| 12VIN, 12VOUT | JST B2B-XH-A(LF)(SN) | C158012 | Same connector, without the locating peg |
| I2C-A, I2C-B | JST B4B-XH-A(LF)(SN) | C144395 | Same connector, without the locating peg |
| U4 | ULN2003A (DIP-16) | C93000 | Same chip from another manufacturer |

## 5. Check the placement preview

Before you confirm, check that:

- **U4 (ULN2003):** the notch and pin 1 match the outline printed on the board.
- **D1 (1N4148):** the stripe on the diode is on the same side as the stripe printed on the board (toward the HALL connector).
- **The JST connectors:** they are vertical, so what matters is that pin 1 of each part sits on pin 1 of its footprint. On HALL and I2C-A/B, pin 1 is GND. On 12VIN/12VOUT, check that the latch slot faces the same way as the outline printed on the board.

Rotate any part that's wrong, then confirm.

## 6. After ordering

1. **"Reviewed and approved" email.** JLCPCB checked your files and found no problems. They now prepare the production files. Nothing to do yet.
2. **Production file approval.** You chose "Confirm Production file: Yes", so you get a second email when the files are ready. Open the order in *Order History*, check the outline, holes and silkscreen, and click **Confirm**. The order waits until you do.
3. **Parts placement approval.** Check the placement image again (U4 pin 1, the D1 stripe, connector pin 1) and confirm it.
4. **Production and shipping.** Nothing else is needed from you. You get a tracking number when the order ships.

If JLCPCB finds a problem at any step, they email you and hold the order until you reply.

## 7. When the boards arrive

- **Solder the D1 Mini (U1)** onto each board yourself. Use the ESP8266EX version without the metal shield (see the README).
- **Master board only:** add the modifications from the README's *Building Notes*:
  - 2 × 4.7 kΩ pullups on SDA/SCL (D2/D1)
  - the hall sensor rerouted to D0, with a 10 kΩ pullup
  - the reset button

## Parts JLCPCB doesn't assemble

Order these separately (they're also listed in the README):

- Wemos D1 Mini
- 28BYJ-48 **12 V** motor
- KY-003 hall sensor
- 2 × 1 mm magnet
- 12 V power supply, 12 V → 5 V step-down converter, DC socket and switch
- JST-XH cable housings and crimp contacts

LCSC sells the cable housings: XHP-2, XHP-3, XHP-4, and SXH-001T-P0.6 contacts.
