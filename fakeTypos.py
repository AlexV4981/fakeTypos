import tkinter as tk
from tkinter import ttk
import random

keys_nearby = {
    # Numbers
    '1': "`2qaw", '2': "13qweas", '3': "24wersd", '4': "35ertdf",
    '5': "46rtyfg", '6': "57tyugh", '7': "68yuihj", '8': "79uiojk",
    '9': "80ioikl", '0': "9-oppl", '-': "0=op[]", '=': "-[]",

    # Lowercase letters
    'a': "qwsadz", 'b': "vghn", 'c': "xdfv", 'd': "erwsdfcx", 'e': "234wrds",
    'f': "rtdfgvc", 'g': "tfvghb", 'h': "gbnhj", 'i': "789ujko",
    'j': "hnmkiu", 'k': "jmloi", 'l': "kop;", 'm': "njk,",
    'n': "bhjm", 'o': "890iklp", 'p': "90ol;[-", 'q': "`12was",
    'r': "345etdf", 's': "qweadrzx", 't': "456rfyg", 'u': "678yhji",
    'v': "cfgb", 'w': "123qase", 'x': "zsdc", 'y': "567tghu", 'z': "asx",

    # Uppercase letters (same neighbors)
    'A': "QWSADZ", 'B': "VGHN", 'C': "XDFV", 'D': "ERWSDFCX", 'E': "234WRDS",
    'F': "RTDFGVC", 'G': "TFVGHB", 'H': "GBNHJ", 'I': "789UJK0",
    'J': "HNMKIU", 'K': "JMLOI", 'L': "KOP;", 'M': "NJK,",
    'N': "BHMJ", 'O': "890IKLP", 'P': "90OL;[-", 'Q': "`12WAS",
    'R': "345ETDF", 'S': "QWEADRZX", 'T': "456RFYG", 'U': "678YHJI",
    'V': "CFGB", 'W': "123QASE", 'X': "ZSDC", 'Y': "567TGHU", 'Z': "ASX"
}

class TypoGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Typo Generator")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure style
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Result.TLabel', font=('Courier', 10), background='#f8f8f8')
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Typo Generator", style='Header.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input section
        input_label = ttk.Label(main_frame, text="Enter text:")
        input_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.input_text = tk.Text(main_frame, height=6, width=60, wrap=tk.WORD,
                                font=('Arial', 10), borderwidth=1, relief='solid')
        self.input_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Error rate controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        controls_frame.columnconfigure(1, weight=1)
        controls_frame.columnconfigure(3, weight=1)
        
        # Min error rate
        min_label = ttk.Label(controls_frame, text="Min Error Rate:")
        min_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.min_rate = tk.DoubleVar(value=0.15)
        min_scale = ttk.Scale(controls_frame, from_=0.01, to=0.5, variable=self.min_rate,
                             orient=tk.HORIZONTAL, command=self.on_scale_change)
        min_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        self.min_entry = ttk.Entry(controls_frame, width=6)
        self.min_entry.insert(0, "0.15")
        self.min_entry.grid(row=0, column=2, padx=(0, 10))
        self.min_entry.bind('<Return>', self.on_entry_change)
        
        # Max error rate
        max_label = ttk.Label(controls_frame, text="Max Error Rate:")
        max_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        self.max_rate = tk.DoubleVar(value=0.7)
        max_scale = ttk.Scale(controls_frame, from_=0.1, to=0.9, variable=self.max_rate,
                             orient=tk.HORIZONTAL, command=self.on_scale_change)
        max_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 20), pady=(10, 0))
        
        self.max_entry = ttk.Entry(controls_frame, width=6)
        self.max_entry.insert(0, "0.7")
        self.max_entry.grid(row=1, column=2, padx=(0, 10), pady=(10, 0))
        self.max_entry.bind('<Return>', self.on_entry_change)
        
        # Generate button
        self.generate_btn = ttk.Button(main_frame, text="Generate Typos", command=self.generate_typos)
        self.generate_btn.grid(row=4, column=0, columnspan=2, pady=(10, 20))
        
        # Result section
        result_label = ttk.Label(main_frame, text="Result:")
        result_label.grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        
        self.result_text = tk.Text(main_frame, height=6, width=60, wrap=tk.WORD,
                                 font=('Courier', 10), borderwidth=1, relief='solid',
                                 background='#f8f8f8', state=tk.DISABLED)
        self.result_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Stats label
        self.stats_label = ttk.Label(main_frame, text="", style='TLabel')
        self.stats_label.grid(row=7, column=0, columnspan=2, pady=(10, 0))
        
        # Bind Enter key to generate button
        self.root.bind('<Return>', lambda e: self.generate_typos())
        
    def on_scale_change(self, event=None):
        """Update entry fields when scales change"""
        self.min_entry.delete(0, tk.END)
        self.min_entry.insert(0, f"{self.min_rate.get():.2f}")
        
        self.max_entry.delete(0, tk.END)
        self.max_entry.insert(0, f"{self.max_rate.get():.2f}")
        
    def on_entry_change(self, event=None):
        """Update scales when entry fields change"""
        try:
            min_val = float(self.min_entry.get())
            max_val = float(self.max_entry.get())
            
            if 0 <= min_val <= 0.5 and 0.1 <= max_val <= 0.9 and min_val <= max_val:
                self.min_rate.set(min_val)
                self.max_rate.set(max_val)
            else:
                self.show_error("Please enter valid values: 0 ≤ Min ≤ 0.5, 0.1 ≤ Max ≤ 0.9, Min ≤ Max")
        except ValueError:
            self.show_error("Please enter valid numbers")
    
    def show_error(self, message):
        """Show error message in stats label"""
        self.stats_label.config(text=f"Error: {message}", foreground='red')
    
    def introduce_errors_with_minimum(self, string, min_error_fraction=0.05, max_error_fraction=0.15):
        """Introduce errors while guaranteeing at least some minimum"""
        new_string = list(string)
        n = len(string)
        
        if n == 0:
            return string
            
        # Calculate target number of errors
        min_errors = max(1, int(n * min_error_fraction))
        max_errors = min(n, int(n * max_error_fraction))
        target_errors = random.randint(min_errors, max_errors)
        
        # Choose which positions to change
        positions = random.sample(range(n), target_errors)
        
        for pos in positions:
            letter = string[pos]
            current = keys_nearby.get(letter)
            if current and letter.isalpha():
                new_string[pos] = random.choice(current)
        
        return ''.join(new_string)
    
    def generate_typos(self):
        """Generate typos based on input and settings"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        
        if not input_text:
            self.show_error("Please enter some text")
            return
            
        try:
            min_rate = float(self.min_entry.get())
            max_rate = float(self.max_entry.get())
            
            if not (0 <= min_rate <= 0.5 and 0.1 <= max_rate <= 0.9 and min_rate <= max_rate):
                self.show_error("Invalid error rates: 0 ≤ Min ≤ 0.5, 0.1 ≤ Max ≤ 0.9, Min ≤ Max")
                return
                
        except ValueError:
            self.show_error("Please enter valid numbers for error rates")
            return
        
        # Generate result
        result = self.introduce_errors_with_minimum(input_text, min_rate, max_rate)
        
        # Display result
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", result)
        self.result_text.config(state=tk.DISABLED)
        
        # Calculate and display stats
        original_len = len(input_text)
        errors = sum(1 for a, b in zip(input_text, result) if a != b)
        error_rate = (errors / original_len) * 100 if original_len > 0 else 0
        
        self.stats_label.config(
            text=f"Characters: {original_len} | Errors: {errors} | Error Rate: {error_rate:.1f}%",
            foreground='black'
        )

def main():
    root = tk.Tk()
    app = TypoGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()