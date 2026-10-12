"""GTN capture-only prototype. No game automation, no network uploads."""
import datetime as dt
import json
import pathlib
import re
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import mss
from PIL import Image, ImageEnhance, ImageOps
import pytesseract

OUT = pathlib.Path.home() / "Documents" / "GTNMarket"
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT / "ocr_observations.jsonl"

class App:
    def __init__(self, root):
        self.root = root
        root.title("Star Forge GTN — Capture Prototype")
        root.geometry("820x650")
        self.running = False
        self.region = [tk.StringVar(value=v) for v in ("200", "150", "1100", "700")]
        ttk.Label(root, text="SWTOR GTN screen capture (local OCR only)", font=("Segoe UI", 15, "bold")).pack(pady=12)
        ttk.Label(root, text="Set the capture rectangle to your GTN listings. Captures visible screen only; no clicks or uploads.").pack()
        box = ttk.Frame(root); box.pack(pady=10)
        for name, var in zip(("Left","Top","Width","Height"), self.region):
            ttk.Label(box,text=name).pack(side="left",padx=5)
            ttk.Entry(box,textvariable=var,width=7).pack(side="left")
        bar = ttk.Frame(root);bar.pack(pady=8)
        ttk.Button(bar,text="Capture once",command=self.capture).pack(side="left",padx=5)
        ttk.Button(bar,text="Start every 15 seconds",command=self.start).pack(side="left",padx=5)
        ttk.Button(bar,text="Stop",command=self.stop).pack(side="left",padx=5)
        ttk.Button(bar,text="Open observation folder",command=self.open_folder).pack(side="left",padx=5)
        self.status=tk.StringVar(value="Ready. Install Tesseract OCR first; see README.")
        ttk.Label(root,textvariable=self.status,wraplength=770).pack(pady=8)
        self.output=tk.Text(root,wrap="word",font=("Consolas",11))
        self.output.pack(fill="both",expand=True,padx=15,pady=10)
        self.output.insert("end","OCR text will appear here. Review accuracy before using any prices.\n")
        root.protocol("WM_DELETE_WINDOW",self.close)
    def open_folder(self):
        import os
        os.startfile(OUT)
    def start(self):
        if self.running:return
        self.running=True;self.capture()
    def stop(self):
        self.running=False;self.status.set("Stopped")
    def capture(self):
        try:
            left,top,width,height=[int(x.get()) for x in self.region]
            if left<0 or top<0 or width<100 or height<100 or width>8000 or height>8000:raise ValueError("Invalid capture region")
        except ValueError as e:
            messagebox.showerror("Region error",str(e));self.stop();return
        self.status.set("Capturing visible GTN region…")
        def worker():
            try:
                with mss.mss() as sct:
                    shot=sct.grab({"left":left,"top":top,"width":width,"height":height})
                im=Image.frombytes("RGB",shot.size,shot.rgb)
                gray=ImageOps.grayscale(im)
                gray=ImageEnhance.Contrast(gray).enhance(2)
                gray=gray.resize((gray.width*2,gray.height*2))
                text=pytesseract.image_to_string(gray,config="--psm 6")
                # Raw OCR is intentionally not converted into authoritative prices:
                # SWTOR layout needs a screenshot-specific parser and human validation.
                record={"server":"Star Forge","captured_at":dt.datetime.now(dt.timezone.utc).isoformat(),"capture_region":[left,top,width,height],"ocr_text":text,"verified":False}
                with LOG.open("a",encoding="utf-8") as f:f.write(json.dumps(record,ensure_ascii=False)+"\n")
                self.root.after(0,lambda:self.display(record))
            except Exception as e:
                msg=str(e)
                self.root.after(0,lambda:self.status.set("Capture error: "+msg))
                self.root.after(0,self.stop)
            finally:
                self.root.after(15000,self.capture) if self.running else None
        threading.Thread(target=worker,daemon=True).start()
    def display(self,record):
        self.output.delete("1.0","end")
        self.output.insert("end",record["ocr_text"] or "(No text detected. Adjust capture rectangle and SWTOR UI scale.)")
        self.status.set("Captured "+record["captured_at"]+" UTC; saved locally. Unverified OCR, not published.")
    def close(self):
        self.running=False;self.root.destroy()
if __name__=="__main__":
    root=tk.Tk();App(root);root.mainloop()
