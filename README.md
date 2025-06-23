# 📋 Todo List Manager

A beautiful and feature-rich Todo List Manager built with Python's tkinter library. This application provides an intuitive GUI for managing your daily tasks with advanced features like priority levels, due dates, filtering, and persistent storage.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

- **Intuitive GUI**: Clean and modern interface built with tkinter
- **Priority Levels**: Organize tasks with High, Medium, and Low priorities
- **Due Dates**: Set and track due dates for your tasks
- **Smart Filtering**: Filter tasks by status, priority, or completion
- **Visual Indicators**: Color-coded priorities and status indicators
- **Persistent Storage**: Tasks are automatically saved to JSON file
- **Task Statistics**: Real-time statistics showing total, completed, and pending tasks
- **Bulk Operations**: Clear all completed tasks at once
- **Overdue Alerts**: Visual highlighting for overdue and due today tasks

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/teaminfinitydev/To-Do-List-Manager.git
   cd To-Do-List-Manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### System Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- Operating System: Windows, macOS, or Linux

## 🎯 How to Use

### Adding Tasks
1. Enter your task in the text field
2. Select priority level (High, Medium, Low)
3. Click "Add Task" or press Enter
4. Your task will appear in the list with priority indicators

### Managing Tasks
- **Complete Task**: Select a task and click "✓ Complete"
- **Edit Task**: Select a task and click "✏️ Edit"
- **Delete Task**: Select a task and click "🗑️ Delete"
- **Set Due Date**: Select a task and click "📅 Set Due Date"

### Filtering Tasks
Use the filter dropdown to view:
- All tasks
- Pending tasks only
- Completed tasks only
- Tasks by priority level

### Visual Indicators
- **○** = Pending task
- **✓** = Completed task
- **🔴** = High priority
- **🟡** = Medium priority
- **🟢** = Low priority
- **📅** = Due date set
- **Red text** = Overdue tasks
- **Orange text** = Due today
- **Gray text** = Completed tasks

## 📁 Project Structure

```
To-Do-List-Manager/
├── main.py              # Main application file
├── requirements.txt     # Project dependencies
├── README.md           # Project documentation
└── tasks.json          # Task data storage (auto-generated)
```

## 🛠️ Technical Details

### Architecture
- **Language**: Python 3.7+
- **GUI Framework**: tkinter
- **Data Storage**: JSON file format
- **Design Pattern**: Object-oriented programming with separation of concerns

### Key Classes
- **Task**: Represents individual tasks with properties like text, priority, due date, and completion status
- **TodoApp**: Main application class handling GUI and task management logic

### Data Persistence
Tasks are automatically saved to `tasks.json` file in the same directory as the application. The file is created automatically when you first add a task.

## 🎨 Customization

### Modifying Colors
You can customize the color scheme by modifying the style configurations in the `setup_styles()` method:

```python
style.configure('Priority.High.TLabel', foreground='#dc3545')  # Red for high priority
style.configure('Priority.Medium.TLabel', foreground='#fd7e14')  # Orange for medium priority
style.configure('Priority.Low.TLabel', foreground='#28a745')  # Green for low priority
```

### Adding New Features
The modular design makes it easy to extend functionality:
- Add new task properties in the `Task` class
- Extend filtering options in the `filter_tasks()` method
- Customize the GUI layout in the `create_widgets()` method

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add type hints for better code documentation
- Test your changes thoroughly
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Bug Reports

If you encounter any issues, please create an issue on GitHub with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and operating system

## 🌟 Acknowledgments

- Built with Python's tkinter library
- Inspired by modern todo list applications
- Thanks to the Python community for excellent documentation

## 📈 Future Enhancements

- [ ] Task categories and tags
- [ ] Export/import functionality
- [ ] Keyboard shortcuts
- [ ] Task reminders and notifications
- [ ] Dark mode theme
- [ ] Multi-user support
- [ ] Cloud synchronization
- [ ] Mobile companion app

---

**Made with ❤️ by [teaminfinitydev]**

*If you find this project useful, please consider giving it a ⭐ on GitHub!*