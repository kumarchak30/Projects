import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv

class ExpenseInvoiceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Invoice Tracker")
        self.root.geometry("1000x600")

        # Create and configure the treeview style
        style = ttk.Style()
        style.configure("Treeview", bordercolor="black", relief="solid", borderwidth=1)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        # Create top panel for the buttons
        top_panel = tk.Frame(self.root)
        top_panel.pack(side=tk.TOP, fill=tk.X)

        buttons = ["Enter Query", "Exec Query", "Save", "Clear All", "Reports",
                   "Inv Entry", "Client Info", "Consultant Info", "Consultant Entry", "Payments Entry"]
        for button in buttons:
            tk.Button(top_panel, text=button, command=lambda b=button: self.button_clicked(b)).pack(side=tk.LEFT)

        # Add "Add Entry" button
        tk.Button(top_panel, text="Add Entry", command=self.add_entry).pack(side=tk.LEFT)

        # Create the main panel with a grid layout (2 rows)
        main_panel = tk.Frame(self.root)
        main_panel.pack(fill=tk.BOTH, expand=True)

        # Create the top table panel
        top_table_panel = tk.Frame(main_panel)
        top_table_panel.pack(fill=tk.BOTH, expand=True)

        self.top_columns = ["Pay Name", "Pay Date", "Pay Amount ($)", "Pay Type", "Pay Description", "Bank File Name"]
        self.top_treeview = self.create_table(top_table_panel, self.top_columns)

        # Create the bottom table panel
        bottom_table_panel = tk.Frame(main_panel)
        bottom_table_panel.pack(fill=tk.BOTH, expand=True)

        self.bottom_columns = ["Consultant Id", "Client Id", "Invoice No", "Inv From Date", "Inv To Date", "Inv Qty",
                               "Inv City", "Inv Date", "Inv Rate", "Inv Amount", "Inv Paid"]
        self.bottom_treeview = self.create_table(bottom_table_panel, self.bottom_columns)

        # Add labels and text fields for Billed Amount, Paid Amount, and +/- amount
        summary_panel = tk.Frame(bottom_table_panel)
        summary_panel.pack(side=tk.TOP, fill=tk.X)

        tk.Label(summary_panel, text="Billed Amount").pack(side=tk.LEFT)
        self.billed_amount_var = tk.StringVar()
        tk.Entry(summary_panel, textvariable=self.billed_amount_var, width=10).pack(side=tk.LEFT)

        tk.Label(summary_panel, text="Paid Amount").pack(side=tk.LEFT)
        self.paid_amount_var = tk.StringVar()
        tk.Entry(summary_panel, textvariable=self.paid_amount_var, width=10).pack(side=tk.LEFT)

        tk.Label(summary_panel, text="(+/-)").pack(side=tk.LEFT)
        self.diff_amount_var = tk.StringVar()
        tk.Entry(summary_panel, textvariable=self.diff_amount_var, width=10).pack(side=tk.LEFT)

    def create_table(self, parent, columns):
        treeview = ttk.Treeview(parent, columns=columns, show='headings')
        treeview.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=100, anchor=tk.CENTER)

        return treeview

    def button_clicked(self, button):
        if button == "Clear All":
            self.clear_all()
        elif button == "Reports":
            self.generate_report()

    def clear_all(self):
        for treeview in [self.top_treeview, self.bottom_treeview]:
            for item in treeview.get_children():
                treeview.delete(item)
        self.billed_amount_var.set("")
        self.paid_amount_var.set("")
        self.diff_amount_var.set("")

    def generate_report(self):
        self.save_table_data_to_csv("table_data.csv")
        self.save_table_data_to_pdf("table_data.pdf")
        messagebox.showinfo("Report", "Report generated successfully")

    def save_table_data_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.top_treeview["columns"])
            for row_id in self.top_treeview.get_children():
                row = self.top_treeview.item(row_id)['values']
                writer.writerow(row)

            writer.writerow([])  # Blank line to separate tables

            writer.writerow(self.bottom_treeview["columns"])
            for row_id in self.bottom_treeview.get_children():
                row = self.bottom_treeview.item(row_id)['values']
                writer.writerow(row)

    def save_table_data_to_pdf(self, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica", 12)
        c.drawString(30, height - 30, "Top Table Data")

        data = [self.top_treeview["columns"]]
        for row_id in self.top_treeview.get_children():
            row = self.top_treeview.item(row_id)['values']
            data.append(row)

        table_height = height - 50
        for row in data:
            x = 30
            for value in row:
                c.drawString(x, table_height, str(value))
                x += 100
            table_height -= 20

        c.drawString(30, table_height - 30, "Bottom Table Data")
        table_height -= 50

        data = [self.bottom_treeview["columns"]]
        for row_id in self.bottom_treeview.get_children():
            row = self.bottom_treeview.item(row_id)['values']
            data.append(row)

        for row in data:
            x = 30
            for value in row:
                c.drawString(x, table_height, str(value))
                x += 100
            table_height -= 20

        c.save()

    def add_entry(self):
        table_choice = simpledialog.askstring("Table Selection", "Enter 'top' to add to the top table or 'bottom' to add to the bottom table:")
        if table_choice not in ['top', 'bottom']:
            messagebox.showerror("Error", "Invalid table selection")
            return

        if table_choice == 'top':
            columns = self.top_columns
            treeview = self.top_treeview
        else:
            columns = self.bottom_columns
            treeview = self.bottom_treeview

        entry_data = []
        for col in columns:
            value = simpledialog.askstring("Input", f"Enter value for {col}:")
            entry_data.append(value)

        treeview.insert("", "end", values=entry_data)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseInvoiceTracker(root)
    root.mainloop()
