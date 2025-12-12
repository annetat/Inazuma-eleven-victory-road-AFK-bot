# Inazuma Afk Bot

**Python Version:** 3.9.13

This program is a simple GUI automation bot that uses PyAutoGUI to simulate mouse and keyboard actions, following a predefined sequence to perform in-game tasks.

---

## ⚠ Important Notes

1. **Templates Folder**  
   - If you want to run the program yourself, you need to modify the images in the `templates` folder.  
   - Generally, only `Picture1.png` and `Picture2.png` need to be updated.

2. **Game Resolution**  
   - It is recommended to set the game resolution to **1600x900**, otherwise the bot may fail to detect images and steps might not execute.

3. **Folder Path**  
   - The folder path where you place this program **cannot contain Chinese characters**, otherwise the bot may not work.

4. **How to Run**  
   - After modifying the images, open `Start_bot.bat` (run as Administrator).  
   - The file is safe to run; no viruses are included.

---

## 📝 Bot Steps

| Step | Action | Target |
|------|--------|--------|
| 1    | Click  | Picture1.png |
| 2    | Click  | Picture2.png |
| 3    | Click  | Picture3.png |
| 4    | Click  | Picture4.png |
| 5    | Click  | Picture5.png |
| 6    | Click  | Picture6.png |
| 7    | Click  | Picture7.png |
| 8    | Click  | Picture7.png |
| 9    | Click  | Picture8.png |
| 10   | Press Key | U (Open Commander) |
| 11   | Click  | Picture6.png |
| 12   | Click  | Picture7.png |
| 13   | Click  | Picture7.png (Loop back to Step 1) |

---

## 📦 Setup / How to Run

1. Modify the images in the `templates` folder (at least `Picture1.png` and `Picture2.png`).  
2. Make sure the game resolution is set to **1600x900**; otherwise, you may need to retake all the screenshots.  
3. Ensure the folder path does not contain Chinese characters.  
4. Install all required dependencies:

```powershell
python -m pip install -r requirment.txt

5. Run the bot:

python .\InazumaBot.py