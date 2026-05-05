import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')


def knapsack(items, capacity):
    """Solve the 0/1 knapsack problem and return best profit, total weight, and selected items."""
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = items[i - 1]['weight']
        value = items[i - 1]['value']
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]

    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(items[i - 1])
            w -= items[i - 1]['weight']

    selected_items.reverse()
    total_weight = sum(item['weight'] for item in selected_items)
    max_profit = dp[n][capacity]
    return max_profit, total_weight, selected_items


class CargoLoadingApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Cargo Loading System')
        self.items = []
        self.item_rows = []

        self.create_ui()
        self.update_optimize_button()

    def create_ui(self):
        self.root.geometry('1020x680')
        self.root.minsize(940, 620)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure((0, 1), weight=1)
        self.root.configure(fg_color='#14141f')

        wrapper = ctk.CTkFrame(self.root, corner_radius=22, fg_color='#17182a')
        wrapper.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=18, pady=18)
        wrapper.grid_rowconfigure(0, weight=1)
        wrapper.grid_columnconfigure((0, 1), weight=1)

        left_panel = ctk.CTkFrame(wrapper, corner_radius=20, fg_color='#1f213a')
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(18, 9), pady=18)
        left_panel.grid_columnconfigure(0, weight=1)

        right_panel = ctk.CTkFrame(wrapper, corner_radius=20, fg_color='#1f213a')
        right_panel.grid(row=0, column=1, sticky='nsew', padx=(9, 18), pady=18)
        right_panel.grid_rowconfigure((0, 1), weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            left_panel,
            text='Cargo Loading System',
            font=ctk.CTkFont(size=24, weight='bold'),
            anchor='w'
        )
        title.grid(row=0, column=0, sticky='w', padx=20, pady=(20, 4))

        subtitle = ctk.CTkLabel(
            left_panel,
            text='Build the best cargo manifest with optimized profit.',
            font=ctk.CTkFont(size=14),
            text_color='#b3b6dc',
            anchor='w'
        )
        subtitle.grid(row=1, column=0, sticky='w', padx=20, pady=(0, 18))

        form_card = ctk.CTkFrame(left_panel, corner_radius=20, fg_color='#141723')
        form_card.grid(row=2, column=0, sticky='nsew', padx=20, pady=8)
        form_card.grid_columnconfigure(0, weight=1)

        input_label = ctk.CTkLabel(form_card, text='Cargo Item Details', font=ctk.CTkFont(size=16, weight='bold'))
        input_label.grid(row=0, column=0, sticky='w', padx=18, pady=(18, 12))

        self.name_entry = ctk.CTkEntry(form_card, placeholder_text='Item Name', corner_radius=14)
        self.name_entry.grid(row=1, column=0, sticky='ew', padx=18, pady=(0, 12))

        self.weight_entry = ctk.CTkEntry(form_card, placeholder_text='Weight', corner_radius=14)
        self.weight_entry.grid(row=2, column=0, sticky='ew', padx=18, pady=(0, 12))

        self.value_entry = ctk.CTkEntry(form_card, placeholder_text='Value', corner_radius=14)
        self.value_entry.grid(row=3, column=0, sticky='ew', padx=18, pady=(0, 18))

        self.add_item_button = ctk.CTkButton(
            form_card,
            text='➕ Add Item',
            corner_radius=18,
            fg_color='#4567ff',
            hover_color='#567dff',
            command=self.add_item
        )
        self.add_item_button.grid(row=4, column=0, sticky='ew', padx=18, pady=(0, 20))

        capacity_card = ctk.CTkFrame(left_panel, corner_radius=20, fg_color='#141723')
        capacity_card.grid(row=3, column=0, sticky='nsew', padx=20, pady=(10, 18))
        capacity_card.grid_columnconfigure(0, weight=1)

        capacity_label = ctk.CTkLabel(capacity_card, text='Truck Capacity', font=ctk.CTkFont(size=16, weight='bold'))
        capacity_label.grid(row=0, column=0, sticky='w', padx=18, pady=(18, 12))

        self.capacity_entry = ctk.CTkEntry(capacity_card, placeholder_text='Enter capacity', corner_radius=14)
        self.capacity_entry.grid(row=1, column=0, sticky='ew', padx=18, pady=(0, 18))
        self.capacity_entry.bind('<KeyRelease>', lambda event: self.update_optimize_button())

        action_frame = ctk.CTkFrame(left_panel, corner_radius=20, fg_color='#141723')
        action_frame.grid(row=4, column=0, sticky='ew', padx=20, pady=(0, 18))
        action_frame.grid_columnconfigure((0, 1), weight=1)

        self.optimize_button = ctk.CTkButton(
            action_frame,
            text='🚀 Optimize',
            corner_radius=18,
            fg_color='#6f42c1',
            hover_color='#7d56d6',
            command=self.calculate_knapsack,
            state='disabled'
        )
        self.optimize_button.grid(row=0, column=0, sticky='ew', padx=(4, 8), pady=8)

        self.reset_button = ctk.CTkButton(
            action_frame,
            text='♻️ Reset',
            corner_radius=18,
            fg_color='#2f2f5f',
            hover_color='#42476d',
            command=self.reset_form
        )
        self.reset_button.grid(row=0, column=1, sticky='ew', padx=(8, 4), pady=8)

        self.status_label = ctk.CTkLabel(
            left_panel,
            text='Add cargo items and set capacity to enable optimization.',
            font=ctk.CTkFont(size=13),
            text_color='#98a1d9',
            anchor='w'
        )
        self.status_label.grid(row=5, column=0, sticky='w', padx=24, pady=(0, 8))

        items_card = ctk.CTkFrame(right_panel, corner_radius=20, fg_color='#141723')
        items_card.grid(row=0, column=0, sticky='nsew', padx=20, pady=(20, 10))
        items_card.grid_rowconfigure(1, weight=1)
        items_card.grid_columnconfigure(0, weight=1)

        items_title = ctk.CTkLabel(items_card, text='📦 Cargo Manifest', font=ctk.CTkFont(size=18, weight='bold'))
        items_title.grid(row=0, column=0, sticky='w', padx=18, pady=(18, 8))

        self.items_area = ctk.CTkScrollableFrame(items_card, corner_radius=16, border_width=1, border_color='#2d2f46', fg_color='#141723')
        self.items_area.grid(row=1, column=0, sticky='nsew', padx=18, pady=(0, 18))
        self.items_area.grid_columnconfigure(0, weight=1)

        self.no_items_label = ctk.CTkLabel(
            self.items_area,
            text='No cargo items yet.\nClick Add Item to begin.',
            font=ctk.CTkFont(size=14),
            text_color='#7b83c8',
            justify='center'
        )
        self.no_items_label.grid(row=0, column=0, pady=18, padx=18)

        result_card = ctk.CTkFrame(right_panel, corner_radius=20, fg_color='#141723')
        result_card.grid(row=1, column=0, sticky='nsew', padx=20, pady=(0, 20))
        result_card.grid_rowconfigure(2, weight=1)
        result_card.grid_columnconfigure(0, weight=1)

        result_title = ctk.CTkLabel(result_card, text='📊 Optimization Result', font=ctk.CTkFont(size=18, weight='bold'))
        result_title.grid(row=0, column=0, sticky='w', padx=18, pady=(18, 12))

        grid_frame = ctk.CTkFrame(result_card, corner_radius=16, fg_color='#1f2340')
        grid_frame.grid(row=1, column=0, sticky='ew', padx=18, pady=(0, 14))
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        self.profit_value = ctk.CTkLabel(
            grid_frame,
            text='0',
            font=ctk.CTkFont(size=22, weight='bold'),
            text_color='#9bd6ff'
        )
        self.profit_value.grid(row=0, column=0, sticky='w', padx=16, pady=(16, 6))

        self.weight_value = ctk.CTkLabel(
            grid_frame,
            text='0 / 0',
            font=ctk.CTkFont(size=22, weight='bold'),
            text_color='#c8a0ff'
        )
        self.weight_value.grid(row=0, column=1, sticky='e', padx=16, pady=(16, 6))

        profit_label = ctk.CTkLabel(grid_frame, text='Maximum Profit', font=ctk.CTkFont(size=12), text_color='#b3b6dc')
        profit_label.grid(row=1, column=0, sticky='w', padx=16, pady=(0, 14))

        weight_label = ctk.CTkLabel(grid_frame, text='Total Weight Used', font=ctk.CTkFont(size=12), text_color='#b3b6dc')
        weight_label.grid(row=1, column=1, sticky='e', padx=16, pady=(0, 14))

        self.result_box = ctk.CTkTextbox(result_card, width=420, height=180, corner_radius=16, fg_color='#16182f', text_color='#e3e8ff')
        self.result_box.grid(row=2, column=0, sticky='nsew', padx=18, pady=(0, 18))
        self.result_box.configure(state='disabled')

    def add_item(self):
        name = self.name_entry.get().strip()
        weight_text = self.weight_entry.get().strip()
        value_text = self.value_entry.get().strip()

        if not name or not weight_text or not value_text:
            messagebox.showerror('Missing Input', 'Please enter name, weight, and value for each cargo item.')
            return

        try:
            weight = int(weight_text)
            value = int(value_text)
            if weight <= 0 or value < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror('Invalid Input', 'Weight must be a positive integer and value must be a non-negative integer.')
            return

        item = {
            'id': len(self.items),
            'name': name,
            'weight': weight,
            'value': value
        }

        self.items.append(item)
        self.insert_item_row(item)
        self.clear_inputs()
        self.update_status(f'{len(self.items)} cargo item(s) added. Ready to optimize.')
        self.animate_add_notice('Item added successfully! ✨')
        self.update_optimize_button()

    def insert_item_row(self, item):
        if self.no_items_label.winfo_exists():
            self.no_items_label.grid_forget()

        row_frame = ctk.CTkFrame(self.items_area, corner_radius=16, fg_color='#141723')
        row_frame.grid(row=len(self.item_rows), column=0, sticky='ew', pady=(0, 10), padx=8)
        row_frame.grid_columnconfigure(0, weight=3)
        row_frame.grid_columnconfigure(1, weight=1)
        row_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(row_frame, text=item['name'], anchor='w', font=ctk.CTkFont(size=14, weight='bold')).grid(row=0, column=0, sticky='w', padx=16, pady=12)
        ctk.CTkLabel(row_frame, text=str(item['weight']), anchor='center', font=ctk.CTkFont(size=13)).grid(row=0, column=1, padx=12)
        ctk.CTkLabel(row_frame, text=str(item['value']), anchor='center', font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=12)

        self.item_rows.append((item, row_frame))
        self.flash_row(row_frame)

    def flash_row(self, row_frame):
        original_color = '#141723'
        highlight_color = '#2d3b7b'
        row_frame.configure(fg_color=highlight_color)

        def reset_color():
            row_frame.configure(fg_color=original_color)

        self.root.after(220, reset_color)

    def animate_add_notice(self, message):
        notice = ctk.CTkLabel(
            self.root,
            text=message,
            fg_color='#3657ff',
            text_color='white',
            corner_radius=16,
            font=ctk.CTkFont(size=12, weight='bold')
        )
        self.root.update_idletasks()
        start_x = self.root.winfo_width() + 20
        target_x = self.root.winfo_width() - 300
        notice.place(x=start_x, y=26)

        def slide(step=0):
            nonlocal start_x
            if start_x > target_x:
                start_x -= 20
                notice.place(x=start_x, y=26)
                self.root.after(10, slide)
            else:
                self.root.after(1200, notice.destroy)

        slide()

    def update_optimize_button(self):
        capacity_text = self.capacity_entry.get().strip()
        has_items = len(self.items) > 0
        is_capacity_valid = False

        if capacity_text:
            try:
                capacity = int(capacity_text)
                is_capacity_valid = capacity > 0
            except ValueError:
                is_capacity_valid = False

        if has_items and is_capacity_valid:
            self.optimize_button.configure(state='normal')
        else:
            self.optimize_button.configure(state='disabled')

    def calculate_knapsack(self):
        if not self.items:
            messagebox.showwarning('No Items', 'Please add cargo items before optimizing.')
            return

        capacity_text = self.capacity_entry.get().strip()
        try:
            capacity = int(capacity_text)
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror('Invalid Capacity', 'Truck capacity must be a positive integer.')
            return

        max_profit, used_weight, selected_items = knapsack(self.items, capacity)
        self.highlight_selected_items(selected_items)
        self.display_result(max_profit, used_weight, selected_items, capacity)

    def highlight_selected_items(self, selected_items):
        selected_ids = {item['id'] for item in selected_items}
        for item, row_frame in self.item_rows:
            if item['id'] in selected_ids:
                row_frame.configure(fg_color='#3042a8')
            else:
                row_frame.configure(fg_color='#141723')

    def display_result(self, profit, weight, selected_items, capacity):
        self.profit_value.configure(text=f'{profit}')
        self.weight_value.configure(text=f'{weight} / {capacity}')

        self.result_box.configure(state='normal')
        self.result_box.delete('1.0', tk.END)
        self.result_box.insert(tk.END, 'Selected Items:\n')

        if not selected_items:
            self.result_box.insert(tk.END, '  • None (capacity too low or no item selected)\n')
        else:
            for item in selected_items:
                self.result_box.insert(tk.END, f'  • {item["name"]} — weight {item["weight"]}, value {item["value"]}\n')

        self.result_box.configure(state='disabled')

    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)

    def reset_form(self):
        self.items.clear()
        self.clear_inputs()
        self.capacity_entry.delete(0, tk.END)
        self.update_optimize_button()
        self.update_status('Add cargo items and set capacity to enable optimization.')
        self.profit_value.configure(text='0')
        self.weight_value.configure(text='0 / 0')
        self.result_box.configure(state='normal')
        self.result_box.delete('1.0', tk.END)
        self.result_box.configure(state='disabled')

        for _, row_frame in self.item_rows:
            row_frame.destroy()
        self.item_rows.clear()

        self.no_items_label = ctk.CTkLabel(
            self.items_area,
            text='No cargo items yet.\nClick Add Item to begin.',
            font=ctk.CTkFont(size=14),
            text_color='#7b83c8',
            justify='center'
        )
        self.no_items_label.grid(row=0, column=0, pady=18, padx=18)

    def update_status(self, text):
        self.status_label.configure(text=text)


def main():
    root = ctk.CTk()
    app = CargoLoadingApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
