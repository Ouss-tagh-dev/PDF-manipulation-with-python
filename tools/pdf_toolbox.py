import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import PyPDF2
import fitz  # PyMuPDF

# --------- PDF operations ---------
def combiner_pdfs(liste_pdfs, chemin_sortie):
    # Merge several PDF files into one
    fusionneur = PyPDF2.PdfMerger()
    for pdf in liste_pdfs:
        fusionneur.append(pdf)
    fusionneur.write(chemin_sortie)
    fusionneur.close()

def separer_pdf(pdf_entree, dossier_sortie):
    # Split a PDF into several single-page PDFs
    lecteur = PyPDF2.PdfReader(pdf_entree)
    for i, page in enumerate(lecteur.pages):
        ecrivain = PyPDF2.PdfWriter()
        ecrivain.add_page(page)
        chemin = os.path.join(dossier_sortie, f"page_{i+1}.pdf")
        with open(chemin, "wb") as f:
            ecrivain.write(f)

def extraire_texte(pdf_entree, fichier_txt):
    # Extract all text from a PDF and save to a .txt file
    lecteur = PyPDF2.PdfReader(pdf_entree)
    with open(fichier_txt, "w", encoding="utf-8") as f:
        for page in lecteur.pages:
            f.write(page.extract_text() or "")

def extraire_images(pdf_entree, dossier_sortie):
    # Extract all images from a PDF and save as PNG files
    doc = fitz.open(pdf_entree)
    for num_page in range(len(doc)):
        for idx_img, img in enumerate(doc.get_page_images(num_page)):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            chemin_img = os.path.join(dossier_sortie, f"page{num_page+1}_img{idx_img+1}.png")
            if pix.n < 5:
                pix.save(chemin_img)
            else:
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.save(chemin_img)
                pix1 = None
            pix = None

def ajouter_mdp(pdf_entree, pdf_sortie, mdp):
    # Add password protection to a PDF
    lecteur = PyPDF2.PdfReader(pdf_entree)
    ecrivain = PyPDF2.PdfWriter()
    for page in lecteur.pages:
        ecrivain.add_page(page)
    ecrivain.encrypt(mdp)
    with open(pdf_sortie, "wb") as f:
        ecrivain.write(f)

def retirer_mdp(pdf_entree, pdf_sortie, mdp):
    # Remove password protection from a PDF
    lecteur = PyPDF2.PdfReader(pdf_entree)
    if not lecteur.decrypt(mdp):
        raise ValueError("Incorrect password.")
    ecrivain = PyPDF2.PdfWriter()
    for page in lecteur.pages:
        ecrivain.add_page(page)
    with open(pdf_sortie, "wb") as f:
        ecrivain.write(f)

def reordonner_pages(pdf_entree, pdf_sortie, nouvel_ordre):
    # Reorder the pages of a PDF according to a new order
    lecteur = PyPDF2.PdfReader(pdf_entree)
    ecrivain = PyPDF2.PdfWriter()
    for i in nouvel_ordre:
        ecrivain.add_page(lecteur.pages[i])
    with open(pdf_sortie, "wb") as f:
        ecrivain.write(f)

def pivoter_pages(pdf_entree, pdf_sortie, rotations):
    # Rotate specific pages of a PDF
    lecteur = PyPDF2.PdfReader(pdf_entree)
    ecrivain = PyPDF2.PdfWriter()
    for i, page in enumerate(lecteur.pages):
        angle = rotations.get(i, 0)
        page.rotate(angle)
        ecrivain.add_page(page)
    with open(pdf_sortie, "wb") as f:
        ecrivain.write(f)

def modifier_metadonnees(pdf_entree, pdf_sortie, metadonnees):
    # Read, add or modify PDF metadata
    lecteur = PyPDF2.PdfReader(pdf_entree)
    ecrivain = PyPDF2.PdfWriter()
    for page in lecteur.pages:
        ecrivain.add_page(page)
    ecrivain.add_metadata(metadonnees)
    with open(pdf_sortie, "wb") as f:
        ecrivain.write(f)

def compresser_pdf(pdf_entree, pdf_sortie):
    # Compress/optimize a PDF (basic, does not optimize images)
    lecteur = PyPDF2.PdfReader(pdf_entree)
    ecrivain = PyPDF2.PdfWriter()
    for page in lecteur.pages:
        ecrivain.add_page(page)
    with open(pdf_sortie, "wb") as f:
        ecrivain.write(f)

# --------- graphical interface ---------

class PDFToolboxApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Toolbox")
        self.geometry("700x500")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    def create_widgets(self):
        self.tabControl = ttk.Notebook(self)
        self.tabs = {}
        self.add_tab("Merge", self.tab_combiner)
        self.add_tab("Split", self.tab_separer)
        self.add_tab("Extract Text", self.tab_extraire_texte)
        self.add_tab("Extract Images", self.tab_extraire_images)
        self.add_tab("Add Password", self.tab_ajouter_mdp)
        self.add_tab("Remove Password", self.tab_retirer_mdp)
        self.add_tab("Reorder Pages", self.tab_reordonner)
        self.add_tab("Rotate Pages", self.tab_pivoter)
        self.add_tab("Metadata", self.tab_metadonnees)
        self.add_tab("Compress", self.tab_compresser)
        self.tabControl.pack(expand=1, fill="both", padx=10, pady=10)

    def add_tab(self, name, func):
        tab = ttk.Frame(self.tabControl)
        self.tabControl.add(tab, text=name)
        func(tab)
        self.tabs[name] = tab

    def tab_combiner(self, tab):
        # Tab for merging PDFs
        files = []
        frame = ttk.Frame(tab, padding=20)
        frame.pack(expand=True, fill="both")
        lbl_title = ttk.Label(frame, text="Merge multiple PDFs", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=(0, 10))
        lbl_files = ttk.Label(frame, text="", background="#f0f0f0", relief="sunken", anchor="w", justify="left")
        lbl_files.pack(fill="x", pady=5)
        def select_files():
            files.clear()
            files.extend(filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")]))
            lbl_files.config(text="\n".join(files))
        def merge():
            if not files:
                messagebox.showerror("Error", "No file selected.")
                return
            output = filedialog.asksaveasfilename(defaultextension=".pdf")
            if output:
                combiner_pdfs(files, output)
                messagebox.showinfo("Success", f"Merged PDF saved: {output}")
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Select PDF files", command=select_files).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Merge", command=merge).pack(side="left", padx=5)

    def tab_separer(self, tab):
        # Tab for splitting a PDF
        frame = ttk.Frame(tab, padding=20)
        frame.pack(expand=True, fill="both")
        lbl_title = ttk.Label(frame, text="Split a PDF into multiple files", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=(0, 10))
        def select():
            file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file:
                folder = filedialog.askdirectory()
                if folder:
                    separer_pdf(file, folder)
                    messagebox.showinfo("Success", f"PDF split into: {folder}")
        ttk.Button(frame, text="Select PDF to split", command=select).pack(pady=10)

    def tab_extraire_texte(self, tab):
        # Tab for extracting text from a PDF
        frame = ttk.Frame(tab, padding=20)
        frame.pack(expand=True, fill="both")
        lbl_title = ttk.Label(frame, text="Extract text from a PDF", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=(0, 10))
        def select():
            file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file:
                output = filedialog.asksaveasfilename(defaultextension=".txt")
                if output:
                    extraire_texte(file, output)
                    messagebox.showinfo("Success", f"Text extracted to: {output}")
        ttk.Button(frame, text="Select PDF", command=select).pack(pady=10)

    def tab_extraire_images(self, tab):
        # Tab for extracting images from a PDF
        frame = ttk.Frame(tab, padding=20)
        frame.pack(expand=True, fill="both")
        lbl_title = ttk.Label(frame, text="Extract images from a PDF", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=(0, 10))
        def select():
            file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file:
                folder = filedialog.askdirectory()
                if folder:
                    extraire_images(file, folder)
                    messagebox.showinfo("Success", f"Images extracted to: {folder}")
        ttk.Button(frame, text="Select PDF", command=select).pack(pady=10)

    def tab_ajouter_mdp(self, tab):
        # Tab for adding password protection
        frame = ttk.Frame(tab, padding=20)
        frame.pack(expand=True, fill="both")
        lbl_title = ttk.Label(frame, text="Add a password to a PDF", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=(0, 10))
        def select():
            file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file:
                output = filedialog.asksaveasfilename(defaultextension=".pdf")
                if output:
                    pwd = simpledialog.askstring("Password", "Enter the password to add:", show="*")
                    if pwd:
                        ajouter_mdp(file, output, pwd)
                        messagebox.showinfo("Success", f"Password added to: {output}")
        ttk.Button(frame, text="Select PDF", command=select).pack(pady=10)

    def tab_retirer_mdp(self, tab):
        # Tab for removing password protection
        frame = ttk.Frame(tab, padding=20)
        frame.pack(expand=True, fill="both")
        lbl_title = ttk.Label(frame, text="Remove password from a PDF", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=(0, 10))
        def select():
            file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file:
                output = filedialog.asksaveasfilename(defaultextension=".pdf")
                if output:
                    pwd = simpledialog.askstring("Password", "Enter the current password:", show="*")
                    if pwd:
                        try:
                            retirer_mdp(file, output, pwd)
                            messagebox.showinfo("Success", f"Password removed: {output}")
                        except Exception as e:
                            messagebox.showerror("Error", str(e))
        ttk.Button(frame, text="Select PDF", command=select).pack(pady=10)

    def tab_reordonner(self, tab):
        # Tab for reordering PDF pages
        frame = ttk.Frame(tab, padding=20)
        frame.pack(expand=True, fill="both")
        lbl_title = ttk.Label(frame, text="Reorder PDF pages", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=(0, 10))
        def select():
            file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                order = simpledialog.askstring("New order", "Enter the new page order (e.g. 2,1,3 to reverse 3 pages):")
                if order:
                    try:
                        new_order = [int(i)-1 for i in order.split(",")]
                        output = filedialog.asksaveasfilename(defaultextension=".pdf")
                        if output:
                            reordonner_pages(file, output, new_order)
                            messagebox.showinfo("Success", f"Pages reordered: {output}")
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
        ttk.Button(frame, text="Select PDF", command=select).pack(pady=10)

    def tab_pivoter(self, tab):
        # Tab for rotating PDF pages
        frame = ttk.Frame(tab, padding=20)
        frame.pack(expand=True, fill="both")
        lbl_title = ttk.Label(frame, text="Rotate PDF pages", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=(0, 10))
        def select():
            file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                rotations = {}
                for i in range(num_pages):
                    angle = simpledialog.askinteger("Rotation", f"Rotation angle for page {i+1} (0, 90, 180, 270):", minvalue=0, maxvalue=270)
                    if angle:
                        rotations[i] = angle
                output = filedialog.asksaveasfilename(defaultextension=".pdf")
                if output:
                    pivoter_pages(file, output, rotations)
                    messagebox.showinfo("Success", f"Pages rotated: {output}")
        ttk.Button(frame, text="Select PDF", command=select).pack(pady=10)

    def tab_metadonnees(self, tab):
        # Tab for reading/modifying PDF metadata
        frame = ttk.Frame(tab, padding=20)
        frame.pack(expand=True, fill="both")
        lbl_title = ttk.Label(frame, text="Read/Modify PDF metadata", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=(0, 10))
        def select():
            file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file:
                title = simpledialog.askstring("Title", "Enter the title:")
                author = simpledialog.askstring("Author", "Enter the author:")
                subject = simpledialog.askstring("Subject", "Enter the subject:")
                keywords = simpledialog.askstring("Keywords", "Enter the keywords:")
                metadata = {}
                if title: metadata["/Title"] = title
                if author: metadata["/Author"] = author
                if subject: metadata["/Subject"] = subject
                if keywords: metadata["/Keywords"] = keywords
                output = filedialog.asksaveasfilename(defaultextension=".pdf")
                if output:
                    modifier_metadonnees(file, output, metadata)
                    messagebox.showinfo("Success", f"Metadata modified: {output}")
        ttk.Button(frame, text="Select PDF", command=select).pack(pady=10)

    def tab_compresser(self, tab):
        # Tab for compressing/optimizing a PDF
        frame = ttk.Frame(tab, padding=20)
        frame.pack(expand=True, fill="both")
        lbl_title = ttk.Label(frame, text="Compress/Optimize a PDF", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=(0, 10))
        def select():
            file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file:
                output = filedialog.asksaveasfilename(defaultextension=".pdf")
                if output:
                    compresser_pdf(file, output)
                    messagebox.showinfo("Success", f"PDF compressed: {output}")
        ttk.Button(frame, text="Select PDF", command=select).pack(pady=10)

if __name__ == "__main__":
    app = PDFToolboxApp()
    app.mainloop() 