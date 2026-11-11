# Binary Learning on Raspberry Pi Pico

![University of Gibraltar logo](logo.png)

A set of interactive, visual examples for learning binary numbers and 8-bit
arithmetic on a Raspberry Pi Pico. The examples use the **Pico Display 2** and
its built-in A button.

## What you'll need

- Raspberry Pi Pico
- Pimoroni Pico Display 2
- MicroPython firmware for the Pico that includes the Pimoroni `picographics`
  library and Pico Display 2 support
- Thonny or another tool for copying and running MicroPython files on the Pico

## Getting started

1. Install the compatible Pimoroni MicroPython firmware on your Pico.
2. Connect the Pico Display 2 to the Pico.
3. Open one of the Python files in Thonny and run it on the Pico.
4. To explore other values, edit the settings near the top of the file and run
   it again.

These are MicroPython programs for the Pico, not regular desktop Python
scripts. They import `machine` and Pimoroni's `picographics` library.

## Examples

### `simple-binary.py`

Displays an 8-bit unsigned number as eight bits, with each bit's place value,
and shows its decimal value. Change `value` near the top of the file to try a
different number from 0 to 255.

### `represent-binary.py`

Displays a signed decimal number in four 8-bit representations:

- Unsigned
- Signed magnitude
- One's complement
- Two's complement

Change `number` near the top of the file. Press the Pico Display 2 **A button**
to cycle through the representations. Each representation has its own range,
shown on the display.

### `binary-arithmetic.py`

Shows 8-bit addition or two's-complement subtraction. Edit `number_a`,
`number_b`, and `operation` near the top of the file. Set `operation` to
`"add"` or `"subtract"`.

For addition, press the **A button** to cycle between unsigned, signed
magnitude, one's complement, and two's complement modes. Subtraction is always
shown as the two's-complement operation `A - B = A + (-B)`. Results outside
the selected representation's range are reported as overflow.
