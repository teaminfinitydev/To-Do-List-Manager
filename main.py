import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, date
from typing import List, Dict, Any

class Task:
    def __init__(self, text: str, priority: str = "Medium", due_date: str = None):
        self.text = text
        self.completed = False
        self.priority = priority
        self.due_date = due_date
        self.created_date = datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'text': self.text,
            'completed': self.completed,
            'priority': self.priority,
            'due_date': self.due_date,
            'created_date': self.created_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        task = cls(data['text'], data.get('priority', 'Medium'), data.get('due_date'))
        task.completed = data.get('completed', False)
        task.created_date = data.get('created_date', datetime.now().strftime("%Y-%m-%d"))
        return task

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.tasks: List[Task] = []
        self.filtered_tasks: List[Task] = []
        self.data_file = "tasks.json"
        
        self.setup_styles()
        self.create_widgets()
        self.load_tasks()
        self.refresh_task_list()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('Custom.TButton', font=('Arial', 10))
        style.configure('Priority.High.TLabel', foreground='#dc3545', font=('Arial', 9, 'bold'))
        style.configure('Priority.Medium.TLabel', foreground='#fd7e14', font=('Arial', 9, 'bold'))
        style.configure('Priority.Low.TLabel', foreground='#28a745', font=('Arial', 9, 'bold'))
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        title_label = ttk.Label(main_frame, text="📋 Todo List Manager", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        input_frame = ttk.LabelFrame(main_frame, text="Add New Task", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        self.task_entry = ttk.Entry(input_frame, font=('Arial', 11))
        self.task_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, 
                                    values=["High", "Medium", "Low"], width=10, state="readonly")
        priority_combo.grid(row=0, column=1, padx=(0, 10))
        
        add_button = ttk.Button(input_frame, text="Add Task", command=self.add_task, style='Custom.TButton')
        add_button.grid(row=0, column=2)
        
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filter:").grid(row=0, column=0, padx=(0, 10))
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                  values=["All", "Pending", "Completed", "High Priority", "Medium Priority", "Low Priority"],
                                  width=15, state="readonly")
        filter_combo.grid(row=0, column=1, padx=(0, 20))
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_tasks())
        
        stats_frame = ttk.Frame(filter_frame)
        stats_frame.grid(row=0, column=2, sticky=tk.E)
        
        self.stats_label = ttk.Label(stats_frame, text="", font=('Arial', 10))
        self.stats_label.grid(row=0, column=0)
        
        list_frame = ttk.LabelFrame(main_frame, text="Tasks", padding="10")
        list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.task_listbox = tk.Listbox(list_frame, font=('Arial', 11), height=15,
                                     selectmode=tk.SINGLE, activestyle='none')
        self.task_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.task_listbox.configure(yscrollcommand=scrollbar.set)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="✓ Complete", command=self.toggle_task, 
                  style='Custom.TButton').grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="✏️ Edit", command=self.edit_task, 
                  style='Custom.TButton').grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="🗑️ Delete", command=self.delete_task, 
                  style='Custom.TButton').grid(row=0, column=2, padx=(0, 10))
        ttk.Button(button_frame, text="📅 Set Due Date", command=self.set_due_date, 
                  style='Custom.TButton').grid(row=0, column=3, padx=(0, 10))
        ttk.Button(button_frame, text="🔄 Refresh", command=self.refresh_data, 
                  style='Custom.TButton').grid(row=0, column=4, padx=(0, 10))
        ttk.Button(button_frame, text="🗂️ Clear Completed", command=self.clear_completed, 
                  style='Custom.TButton').grid(row=0, column=5)
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            priority = self.priority_var.get()
            task = Task(task_text, priority)
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
            self.refresh_task_list()
            messagebox.showinfo("Success", f"Task '{task_text}' added successfully!")
        else:
            messagebox.showwarning("Warning", "Please enter a task!")
    
    def toggle_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.filtered_tasks):
                task = self.filtered_tasks[index]
                task.completed = not task.completed
                self.save_tasks()
                self.refresh_task_list()
                status = "completed" if task.completed else "pending"
                messagebox.showinfo("Success", f"Task marked as {status}!")
        else:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def edit_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.filtered_tasks):
                task = self.filtered_tasks[index]
                new_text = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=task.text)
                if new_text and new_text.strip():
                    task.text = new_text.strip()
                    self.save_tasks()
                    self.refresh_task_list()
                    messagebox.showinfo("Success", "Task updated successfully!")
        else:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def delete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.filtered_tasks):
                task = self.filtered_tasks[index]
                if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{task.text}'?"):
                    self.tasks.remove(task)
                    self.save_tasks()
                    self.refresh_task_list()
                    messagebox.showinfo("Success", "Task deleted successfully!")
        else:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def set_due_date(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.filtered_tasks):
                task = self.filtered_tasks[index]
                date_str = simpledialog.askstring("Set Due Date", 
                                                "Enter due date (YYYY-MM-DD):", 
                                                initialvalue=task.due_date or "")
                if date_str:
                    try:
                        datetime.strptime(date_str, "%Y-%m-%d")
                        task.due_date = date_str
                        self.save_tasks()
                        self.refresh_task_list()
                        messagebox.showinfo("Success", "Due date set successfully!")
                    except ValueError:
                        messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                elif date_str == "":
                    task.due_date = None
                    self.save_tasks()
                    self.refresh_task_list()
                    messagebox.showinfo("Success", "Due date cleared!")
        else:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def clear_completed(self):
        completed_tasks = [task for task in self.tasks if task.completed]
        if completed_tasks:
            if messagebox.askyesno("Confirm Clear", f"Delete {len(completed_tasks)} completed tasks?"):
                self.tasks = [task for task in self.tasks if not task.completed]
                self.save_tasks()
                self.refresh_task_list()
                messagebox.showinfo("Success", f"{len(completed_tasks)} completed tasks deleted!")
        else:
            messagebox.showinfo("Info", "No completed tasks to clear!")
    
    def refresh_data(self):
        self.load_tasks()
        self.filter_tasks()
        messagebox.showinfo("Success", "Data refreshed from file!")
    
    def filter_tasks(self):
        filter_type = self.filter_var.get()
        
        if filter_type == "All":
            self.filtered_tasks = self.tasks.copy()
        elif filter_type == "Pending":
            self.filtered_tasks = [task for task in self.tasks if not task.completed]
        elif filter_type == "Completed":
            self.filtered_tasks = [task for task in self.tasks if task.completed]
        elif filter_type == "High Priority":
            self.filtered_tasks = [task for task in self.tasks if task.priority == "High"]
        elif filter_type == "Medium Priority":
            self.filtered_tasks = [task for task in self.tasks if task.priority == "Medium"]
        elif filter_type == "Low Priority":
            self.filtered_tasks = [task for task in self.tasks if task.priority == "Low"]
        
        self.refresh_task_list()
    
    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        
        if not hasattr(self, 'filtered_tasks'):
            self.filtered_tasks = self.tasks.copy()
        
        for task in self.filtered_tasks:
            status = "✓" if task.completed else "○"
            priority_symbol = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[task.priority]
            due_info = f" 📅 {task.due_date}" if task.due_date else ""
            
            task_display = f"{status} {priority_symbol} {task.text}{due_info}"
            self.task_listbox.insert(tk.END, task_display)
            
            if task.completed:
                self.task_listbox.itemconfig(tk.END, {'fg': 'gray'})
            elif task.due_date:
                try:
                    due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
                    if due_date < date.today():
                        self.task_listbox.itemconfig(tk.END, {'fg': 'red'})
                    elif due_date == date.today():
                        self.task_listbox.itemconfig(tk.END, {'fg': 'orange'})
                except ValueError:
                    pass
        
        self.update_stats()
    
    def update_stats(self):
        total = len(self.tasks)
        completed = len([task for task in self.tasks if task.completed])
        pending = total - completed
        
        self.stats_label.config(text=f"Total: {total} | Completed: {completed} | Pending: {pending}")
    
    def save_tasks(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")
    
    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    tasks_data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
                self.tasks = []
        else:
            self.tasks = []
    
    def on_closing(self):
        self.save_tasks()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()