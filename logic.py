import random
import unicodedata
from typing import List, Set
import tkinter as tk
from tkinter import ttk, scrolledtext

class LogicSymbolGenerator:
    def __init__(self):
        # Base symbols to work with
        self.base_symbols = {
            'letters': ['A', 'B', 'C', 'D', 'E', 'F'],
            'quantifiers': ['∀', '∃', '∄'],
            'connectives': ['∧', '∨', '→', '↔', '⊕', '⊗'],
            'modal': ['□', '◇', '◊', '∎'],
            'set_theory': ['∈', '∉', '⊆', '⊂', '∪', '∩', '∅'],
            'misc': ['⊢', '⊨', '≡', '≠', '≈', '∝', '∞', '⊥', '∥']
        }
        
        # Combining symbols and decorators
        self.decorators = ['̅', '̲', '̃', '̄', '̆', '̇', '̈', '̊', '̋', '̌']
        self.positions = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
        
    def get_random_base(self) -> str:
        category = random.choice(list(self.base_symbols.keys()))
        return random.choice(self.base_symbols[category])
    
    def combine_symbols(self, num_symbols: int = 2) -> str:
        symbols = [self.get_random_base() for _ in range(num_symbols)]
        method = random.choice(['stack', 'join', 'overlay'])
        
        if method == 'stack':
            return random.choice(symbols) + random.choice(self.positions)
        elif method == 'join':
            return ''.join(symbols)
        else:  # overlay
            return symbols[0] + random.choice(self.decorators)
    
    def generate_novel_symbol(self) -> str:
        methods = [
            lambda: self.combine_symbols(4),
            lambda: self.combine_symbols(6),
            lambda: self.get_random_base() + random.choice(self.decorators),
            lambda: self.get_random_base() + random.choice(self.positions),
        ]
        return random.choice(methods)()
    
    def generate_batch(self, n: int = 5) -> List[str]:
        symbols: Set[str] = set()
        while len(symbols) < n:
            new_symbol = self.generate_novel_symbol()
            if self.is_valid_symbol(new_symbol):
                symbols.add(new_symbol)
        return list(symbols)
    
    def is_valid_symbol(self, symbol: str) -> bool:
        try:
            symbol.encode('utf-8').decode('utf-8')
            if len(symbol) > 4:
                return False
            for char in symbol:
                if unicodedata.category(char) not in {'So', 'Sm', 'Mn', 'Me', 'Pd', 'Lu'}:  # Added 'Lu' for uppercase letters
                    return False
            return True
        except UnicodeError:
            return False

class SymbolGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Logic Symbol Generator")
        self.generator = LogicSymbolGenerator()
        
        # Configure main window
        self.root.geometry("800x600")
        self.root.configure(padx=20, pady=20)
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Top frame for controls
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill='x', pady=(0, 20))
        
        # Amount entry and generate button
        ttk.Label(control_frame, text="Batch Size:").pack(side='left', padx=(0, 10))
        self.amount_var = tk.StringVar(value="10")
        amount_entry = ttk.Entry(control_frame, textvariable=self.amount_var, width=10)
        amount_entry.pack(side='left', padx=(0, 10))
        
        ttk.Button(control_frame, text="Generate Symbols", command=self.generate_symbols).pack(side='left')
        
        # Create notebook for different views
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        
        # Symbols tab
        symbols_frame = ttk.Frame(self.notebook)
        self.notebook.add(symbols_frame, text="Generated Symbols")
        
        self.symbols_text = scrolledtext.ScrolledText(symbols_frame, wrap=tk.WORD, font=('TkDefaultFont', 14))
        self.symbols_text.pack(expand=True, fill='both')
        
        # Categories tab
        categories_frame = ttk.Frame(self.notebook)
        self.notebook.add(categories_frame, text="Available Symbols")
        
        self.categories_text = scrolledtext.ScrolledText(categories_frame, wrap=tk.WORD, font=('TkDefaultFont', 12))
        self.categories_text.pack(expand=True, fill='both')
        self.update_categories_display()
        
    def generate_symbols(self):
        try:
            amount = int(self.amount_var.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            self.symbols_text.delete(1.0, tk.END)
            self.symbols_text.insert(tk.END, "Please enter a valid positive number")
            return
        
        symbols = self.generator.generate_batch(amount)
        
        self.symbols_text.delete(1.0, tk.END)
        for i, symbol in enumerate(symbols, 1):
            self.symbols_text.insert(tk.END, f"{i}. {symbol}\n")
    
    def update_categories_display(self):
        self.categories_text.delete(1.0, tk.END)
        for category, symbols in self.generator.base_symbols.items():
            self.categories_text.insert(tk.END, f"{category}:\n")
            self.categories_text.insert(tk.END, f"{' '.join(symbols)}\n\n")

def main():
    root = tk.Tk()
    app = SymbolGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()