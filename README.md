# PokemonFireRedBattleAI

An AI that takes control of battles (single battles for now) in the game Pokemon FireRed.

Requirements:
- Emulator and ROM for Pokemon FireRed
  - Set in-game text speed to medium or slow otherwise AI won't work
- Tesseract OCR
  - After installing Tesseract, paste the traineddata file into tessdata folder
- Node.js and npm
- Install Pokemon Showdown Damage Calculator --> https://github.com/smogon/damage-calc

Packages (pip install):
- re
- cv2
- mss
- time
- math
- random
- ctypes
- subprocess
- numpy
- pandas
- difflib
- pypokedex
- pytesseract
- pydirectinput
- PIL
- win32gui

How to use:
- Run the AI file as you're entering the battle (ideally while you're scrolling through the trainer dialogue in the overworld) before "Trainer XYZ would like to battle!" appears
- Once the screen turns black and enters the battle environment don't press any buttons
- Stop the AI once the overworld appears again

Progress:
<br />
AI can currently do single battles, but there is no double battle support for the AI (yet).
