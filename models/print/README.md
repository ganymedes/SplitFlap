# Print files

Everything needed to print a **10-character** split-flap display.

| Folder | Parts | Source |
|---|---|---|
| `case/` | FrontCover, MiddleFrame, BackCover: Left, Center and Right of each | [David Königsmann's original](https://www.printables.com/model/69464-split-flap-display) (10 characters, 513 mm wide) |
| `unit/` | Frame, BigRotor, MiniRotor | This fork's `models/AssemblyWithChanges.step`, exported to STL (the rotor and frame are slightly reinforced compared with David's) |
| `flaps/` | Flaps 1–45 | David Königsmann's original, using the umlaut-free set for 28–31 |

## Quantities

| Part | Per character | 10 characters |
|---|---|---|
| `case/*` (9 pieces) | — | 1 set |
| `unit/Frame.stl` | 1 | 10 |
| `unit/BigRotor.stl` | 1 | 10 |
| `unit/MiniRotor.stl` | 1 | 10 |
| Flaps 1–45 | 45 (one of each) | 450 |

## Printing

- The largest case piece is about 241 mm long, so it needs a bed at least that wide. It does not fit a 220 mm bed (Ender 3 V2 and similar).
- Flaps are two-colour. Each `.3mf` file holds a whole plate of nine flaps with the letters as separate parts. Alternatively, use the STLs: `FlapN.stl` is the flap body and `FlapN_1.stl`, `FlapN_2.stl`, … are the letter parts.
- `flaps/28-36/` uses David's umlaut-free flaps for 28–31 (showing `$ & #` instead of `Ä Ö Ü`), which matches this firmware. Flaps 32–36 are the standard ones.
- STLs exported from the STEP file keep the assembly's position and orientation, so lay them flat in the slicer.

## License

David Königsmann's design is released under GPL v3. See `../LICENSE` and `../ATTRIBUTION`.
