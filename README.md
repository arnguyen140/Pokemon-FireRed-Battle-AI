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

Progress:
<br />
AI can currently do single battles, but there is no double battle support for the AI (yet).
