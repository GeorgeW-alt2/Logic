import random
import unicodedata
from typing import List, Set, Dict, Optional
import tkinter as tk
from tkinter import ttk, scrolledtext
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class SymbolCategory:
    name: str
    symbols: List[str]
    description: str

class LogicSymbolGenerator:
    def __init__(self):
        # Enhanced symbol categories with descriptions
        self.categories: Dict[str, SymbolCategory] = {
            'letters': SymbolCategory(
                'Letters',
                ['A', 'B', 'C', 'D', 'E', 'F'],
                'Basic logical variables'
            ),
            'quantifiers': SymbolCategory(
                'Quantifiers',
                ['∀', '∃', '∄'],
                'Universal and existential quantifiers'
            ),
            'connectives': SymbolCategory(
                'Connectives',
                ['∧', '∨', '→', '↔', '⊕', '⊗'],
                'Logical connectives and operators'
            ),
            'modal': SymbolCategory(
                'Modal Operators',
                ['□', '◇', '◊', '∎'],
                'Modal logic operators'
            ),
            'set_theory': SymbolCategory(
                'Set Theory',
                ['∈', '∉', '⊆', '⊂', '∪', '∩', '∅'],
                'Set theory operators and relations'
            ),
            'misc': SymbolCategory(
                'Miscellaneous',
                ['⊢', '⊨', '≡', '≠', '≈', '∝', '∞', '⊥', '∥'],
                'Additional logical and mathematical symbols'
            )
        }
        
        # Enhanced decorators with descriptions
        self.decorators = {
            'overline': '̅',
            'underline': '̲',
            'tilde': '̃',
            'macron': '̄',
            'breve': '̆',
            'dot': '̇',
            'diaeresis': '̈',
            'ring': '̊',
            'double_acute': '̋',
            'caron': '̌'
        }
        
        self.positions = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
        self.symbol_cache: Dict[str, Set[str]] = defaultdict(set)
        
    def get_random_base(self, category: Optional[str] = None) -> str:
        """Get a random base symbol, optionally from a specific category."""
        if category and category in self.categories:
            return random.choice(self.categories[category].symbols)
        category = random.choice(list(self.categories.keys()))
        return random.choice(self.categories[category].symbols)
    
    def combine_symbols(self, length: int, method: Optional[str] = None) -> str:
        """
        Combine multiple base symbols into a new compound symbol.
        
        Args:
            length: The desired length of the combined symbol
            method: Optional specific combination method ('stack', 'join', 'overlay')
        
        Returns:
            A combined symbol string
        """
        if length <= 0:
            return ""
            
        if length == 1:
            return self.get_random_base()
            
        if not method:
            method = random.choice(['stack', 'join', 'overlay'])
            
        if method == 'stack':
            return self.get_random_base() + random.choice(self.positions)
        elif method == 'join':
            symbols = [self.get_random_base() for _ in range(length)]
            return ''.join(symbols)
        else:  # overlay
            return self.get_random_base() + random.choice(list(self.decorators.values()))
    
    def generate_novel_symbol(self, min_length: int, max_length: int, cache_key: str = '') -> str:
        """
        Generate a novel logic-like symbol with specified constraints.
        
        Args:
            min_length: Minimum symbol length
            max_length: Maximum symbol length
            cache_key: Optional key for caching generated symbols
            
        Returns:
            A novel symbol string
        """
        length = random.randint(min_length, max_length)
        new_symbol = self.combine_symbols(length)
        
        # Avoid duplicates using cache
        if cache_key:
            while new_symbol in self.symbol_cache[cache_key]:
                new_symbol = self.combine_symbols(length)
            self.symbol_cache[cache_key].add(new_symbol)
            
        return new_symbol
    
    def generate_batch(self, n: int = 5, min_length: int = 1, max_length: int = 4) -> List[str]:
        """
        Generate a batch of novel symbols.
        
        Args:
            n: Number of symbols to generate
            min_length: Minimum symbol length
            max_length: Maximum symbol length
            
        Returns:
            List of generated symbols
        """
        cache_key = f"{n}-{min_length}-{max_length}"
        symbols: Set[str] = set()
        attempts = 0
        max_attempts = n * 10
        
        while len(symbols) < n and attempts < max_attempts:
            new_symbol = self.generate_novel_symbol(min_length, max_length, cache_key)
            if self.is_valid_symbol(new_symbol):
                symbols.add(new_symbol)
            attempts += 1
            
        return list(symbols)
    
    def is_valid_symbol(self, symbol: str) -> bool:
        """
        Validate a generated symbol.
        
        Args:
            symbol: Symbol to validate
            
        Returns:
            Boolean indicating if the symbol is valid
        """
        try:
            symbol.encode('utf-8').decode('utf-8')
            if len(symbol) > 15:
                return False
            valid_categories = {'So', 'Sm', 'Mn', 'Me', 'Pd', 'Lu'}
            return all(unicodedata.category(char) in valid_categories for char in symbol)
        except UnicodeError:
            return False

class SymbolGeneratorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Enhanced Logic Symbol Generator")
        self.generator = LogicSymbolGenerator()
        
        # Configure main window with better defaults
        self.root.geometry("900x700")
        self.root.configure(padx=20, pady=20)
        
        # Apply a modern theme if available
        try:
            self.root.tk.call('source', 'azure.tcl')
            self.root.tk.call('set_theme', 'light')
        except tk.TclError:
            pass
        
        self.create_widgets()
        
    def create_widgets(self):
        # Use grid geometry manager for more precise control
        self.create_control_panel()
        self.create_notebook()
        self.create_status_bar()
        
    def create_control_panel(self):
        control_frame = ttk.LabelFrame(self.root, text="Generation Controls")
        control_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        # Batch size controls
        ttk.Label(control_frame, text="Batch Size:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_var = tk.StringVar(value="10")
        ttk.Entry(control_frame, textvariable=self.amount_var, width=10).grid(row=0, column=1, padx=5)
        
        # Length controls
        ttk.Label(control_frame, text="Symbol Length:").grid(row=0, column=2, padx=5)
        self.min_length_var = tk.StringVar(value="1")
        self.max_length_var = tk.StringVar(value="4")
        
        ttk.Label(control_frame, text="Min:").grid(row=0, column=3)
        min_length_combo = ttk.Combobox(control_frame, textvariable=self.min_length_var, 
                                       values=[str(i) for i in range(1, 16)], width=3)
        min_length_combo.grid(row=0, column=4, padx=5)
        
        ttk.Label(control_frame, text="Max:").grid(row=0, column=5)
        max_length_combo = ttk.Combobox(control_frame, textvariable=self.max_length_var,
                                       values=[str(i) for i in range(1, 16)], width=3)
        max_length_combo.grid(row=0, column=6, padx=5)
        
        # Generate button
        ttk.Button(control_frame, text="Generate Symbols", 
                  command=self.generate_symbols).grid(row=0, column=7, padx=10)
        
        # Configure grid weights
        control_frame.grid_columnconfigure(7, weight=1)
        
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Symbols tab
        symbols_frame = ttk.Frame(self.notebook)
        self.notebook.add(symbols_frame, text="Generated Symbols")
        
        self.symbols_text = scrolledtext.ScrolledText(
            symbols_frame, wrap=tk.WORD, font=('TkDefaultFont', 14)
        )
        self.symbols_text.pack(expand=True, fill='both')
        
        # Categories tab with enhanced display
        categories_frame = ttk.Frame(self.notebook)
        self.notebook.add(categories_frame, text="Symbol Categories")
        
        self.categories_text = scrolledtext.ScrolledText(
            categories_frame, wrap=tk.WORD, font=('TkDefaultFont', 14)
        )
        self.categories_text.pack(expand=True, fill='both')
        self.update_categories_display()
        
    def create_status_bar(self):
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(
            self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.grid(row=2, column=0, sticky='ew', padx=5, pady=(5,0))
        self.status_var.set("Ready")
        
    def validate_lengths(self, event=None):
        """Validate and correct length inputs."""
        try:
            min_len = int(self.min_length_var.get())
            max_len = int(self.max_length_var.get())
            
            if min_len > max_len:
                self.min_length_var.set(str(max_len))
                self.max_length_var.set(str(min_len))
                self.status_var.set("Length values swapped to maintain valid range")
        except ValueError:
            self.min_length_var.set("1")
            self.max_length_var.set("4")
            self.status_var.set("Invalid length values reset to defaults")
    
    def generate_symbols(self):
        """Generate and display new symbols."""
        try:
            amount = int(self.amount_var.get())
            min_length = int(self.min_length_var.get())
            max_length = int(self.max_length_var.get())
            
            if amount <= 0 or min_length <= 0 or max_length <= 0:
                raise ValueError
                
        except ValueError:
            self.status_var.set("Error: Please enter valid positive numbers")
            self.symbols_text.delete(1.0, tk.END)
            self.symbols_text.insert(tk.END, "Please enter valid positive numbers")
            return
        
        self.validate_lengths()
        
        # Update status and generate symbols
        self.status_var.set("Generating symbols...")
        self.root.update_idletasks()
        
        symbols = self.generator.generate_batch(
            amount, 
            min_length=int(self.min_length_var.get()),
            max_length=int(self.max_length_var.get())
        )
        
        # Display results
        self.symbols_text.delete(1.0, tk.END)
        for i, symbol in enumerate(symbols, 1):
            self.symbols_text.insert(tk.END, f"{i}. {symbol}\n")
            
        self.status_var.set(f"Generated {len(symbols)} symbols successfully")
    
    def update_categories_display(self):
        """Update the categories display with enhanced formatting."""
        self.categories_text.delete(1.0, tk.END)
        for category in self.generator.categories.values():
            self.categories_text.insert(tk.END, f"{category.name}:\n")
            self.categories_text.insert(tk.END, f"Description: {category.description}\n")
            self.categories_text.insert(tk.END, f"Symbols: {' '.join(category.symbols)}\n\n")

def main():
    root = tk.Tk()
    app = SymbolGeneratorGUI(root)
    
    # Configure grid weights for resizing
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    root.mainloop()

if __name__ == "__main__":
    main()