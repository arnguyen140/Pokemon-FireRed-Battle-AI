# PokemonFireRedBattleAI

An AI that takes control of battles (single battles for now) in the game Pokemon FireRed.

Requirements:
- Play Pokemon FireRed on a Windows computer
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
- Set in-game text speed to medium or slow otherwise AI won't work
- Run "FireRedBattleAI.py" (ideally while you're scrolling through the trainer dialogue in the overworld) before "Trainer XYZ would like to battle!" appears
- Continue to press through the dialogue until the screen turns black and you enter the battle environment
- Then don't press any buttons and let the AI play
- The AI will stop once the overworld appears again, allowing you to take control again

Progress:
<br />
11/24/23: AI can currently do single battles (apart from tutorial battle), but there is no double battle support for the AI (yet).

6/28/24: AI can play the tutorial battle.
