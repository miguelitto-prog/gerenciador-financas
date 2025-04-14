import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

class FinanceManager:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gerenciador de Finanças")
        self.window.geometry("600x500")
        
        
        self.data_file = "transactions.json"
        self.transactions = self.load_data()
        
        self.create_widgets()
        
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []
        
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.transactions, f)
            
    def create_widgets(self):
        
        input_frame = ttk.LabelFrame(self.window, text="Nova Transação", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        
        ttk.Label(input_frame, text="Tipo:").grid(row=0, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar(value="Receita")
        type_menu = ttk.OptionMenu(input_frame, self.type_var, "Receita", "Receita", "Despesa")
        type_menu.grid(row=0, column=1, padx=5, pady=5)
        
        
        ttk.Label(input_frame, text="Descrição:").grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(input_frame)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        
        ttk.Label(input_frame, text="Valor:").grid(row=2, column=0, padx=5, pady=5)
        self.valor_entry = ttk.Entry(input_frame)
        self.valor_entry.grid(row=2, column=1, padx=5, pady=5)
        
        
        ttk.Button(input_frame, text="Adicionar", command=self.add_transaction).grid(row=3, column=0, columnspan=2, pady=10)
        
        
        display_frame = ttk.LabelFrame(self.window, text="Transações", padding=10)
        display_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        
        self.balance_label = ttk.Label(display_frame, text=f"Saldo: R$ {self.calculate_balance():.2f}")
        self.balance_label.pack(pady=5)
        
        
        self.create_transaction_table(display_frame)
        
    def add_transaction(self):
        try:
            valor = float(self.valor_entry.get())
            if self.type_var.get() == "Despesa":
                valor = -valor
                
            transaction = {
                'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'tipo': self.type_var.get(),
                'descricao': self.desc_entry.get(),
                'valor': valor
            }
            
            self.transactions.append(transaction)
            self.save_data()
            
            
            self.balance_label.config(text=f"Saldo: R$ {self.calculate_balance():.2f}")
            self.update_transaction_table()
            
            
            self.desc_entry.delete(0, "end")
            self.valor_entry.delete(0, "end")
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor válido!")
            
    def calculate_balance(self):
        return sum(t['valor'] for t in self.transactions)
    
    def create_transaction_table(self, parent):
        
        columns = ('data', 'tipo', 'descricao', 'valor')
        self.tree = ttk.Treeview(parent, columns=columns, show='headings')
        
    
        self.tree.heading('data', text='Data')
        self.tree.heading('tipo', text='Tipo')
        self.tree.heading('descricao', text='Descrição')
        self.tree.heading('valor', text='Valor')
        
        
        self.tree.column('data', width=150)
        self.tree.column('tipo', width=100)
        self.tree.column('descricao', width=200)
        self.tree.column('valor', width=100)
        
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        

        self.update_transaction_table()
        
    def update_transaction_table(self):
    
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        
        for t in self.transactions:
            self.tree.insert('', 'end', values=(
                t['data'],
                t['tipo'],
                t['descricao'],
                f"R$ {t['valor']:.2f}"
            ))
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = FinanceManager()
    app.run() 