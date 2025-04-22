import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from functools import reduce
import os

class ExcelMergeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Timepair Merger")

        self.df = None
        self.columns = []
        self.timepair_sets = []

        self.setup_ui()

    def setup_ui(self):
        # File picker
        file_frame = tk.Frame(self.root)
        file_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(file_frame, text="Open Excel File", command=self.load_file).pack(side="left")

        # Main content frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Columns list
        columns_frame = tk.LabelFrame(main_frame, text="Columns")
        columns_frame.pack(side="left", fill="y", padx=(0, 5))

        self.columns_listbox = tk.Listbox(columns_frame, selectmode=tk.MULTIPLE)
        self.columns_listbox.pack(fill="both", expand=True)

        # Timepair sets
        self.sets_frame = tk.LabelFrame(main_frame, text="Timepair Sets")
        self.sets_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        tk.Button(self.sets_frame, text="+ Add Timepair Set", command=self.add_timepair_set).pack(anchor="w", padx=5, pady=5)

        # Scrollable timepair sets
        canvas = tk.Canvas(self.sets_frame)
        scrollbar = tk.Scrollbar(self.sets_frame, orient="vertical", command=canvas.yview)
        self.timepair_container = tk.Frame(canvas)

        self.timepair_container.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.timepair_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Export button
        export_frame = tk.Frame(self.root)
        export_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(export_frame, text="Merge and Save", command=self.merge_and_save).pack(side="right")

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not filepath:
            return

        try:
            self.df = pd.read_excel(filepath)
            self.columns = list(self.df.columns)
            self.columns_listbox.delete(0, tk.END)
            for col in self.columns:
                self.columns_listbox.insert(tk.END, col)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def add_timepair_set(self):
        frame = tk.LabelFrame(self.timepair_container, text=f"Set {len(self.timepair_sets) + 1}", padx=5, pady=5)
        frame.pack(fill="x", padx=5, pady=5)

        tk.Label(frame, text="Datetime Column:").grid(row=0, column=0, sticky="w")
        datetime_cb = ttk.Combobox(frame, values=self.columns, state="readonly")
        datetime_cb.grid(row=0, column=1, sticky="ew")

        tk.Label(frame, text="Value Columns:").grid(row=1, column=0, sticky="nw")
        value_lb = tk.Listbox(frame, selectmode=tk.MULTIPLE, exportselection=False, height=5)
        for col in self.columns:
            value_lb.insert(tk.END, col)
        value_lb.grid(row=1, column=1, sticky="ew")

        frame.columnconfigure(1, weight=1)
        self.timepair_sets.append((datetime_cb, value_lb))

    def merge_and_save(self):
        if self.df is None:
            messagebox.showwarning("No File", "Please load an Excel file first.")
            return

        timepairs = {}
        for datetime_cb, value_lb in self.timepair_sets:
            datetime_col = datetime_cb.get()
            if not datetime_col:
                continue
            value_indices = value_lb.curselection()
            value_cols = [value_lb.get(i) for i in value_indices]
            if not value_cols:
                continue
            timepairs[datetime_col] = value_cols
        print(timepairs)
        if not timepairs:
            messagebox.showwarning("No Timepairs", "Please configure at least one timepair set.")
            return

        try:
            merged = self.merge_function(self.df, timepairs)
            savepath = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
            if savepath:
                merged.to_excel(savepath, index=False)
                messagebox.showinfo("Success", "Merged file saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge: {e}")

    def merge_function(self, df, timepairs):
        dataframes = []
        for time_col, value_cols in timepairs.items():

            for value_col in value_cols:
                temp_df = df[[time_col, value_col]].dropna()
                # Use .loc to modify the datetime column
                temp_df.loc[:, 'datetime'] = pd.to_datetime(temp_df[time_col])
                dataframes.append(temp_df[["datetime",value_col]])
        merged_df = reduce(lambda left, right: pd.merge(left, right, on='datetime', how='outer'), dataframes)
        merged_df.sort_values('datetime').reset_index(drop=True)
        return merged_df

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    root.iconbitmap(os.path.join("images","excel_data_merger.ico"))
    app = ExcelMergeApp(root)
    root.mainloop()
