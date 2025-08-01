"""
Graphical User Interface module for the Morse Code Converter application.

This module provides a GUI for the Morse Code Converter application using tkinter.
"""

import json
import threading
import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from typing import Optional

from .errors import InputError
from .factory import MorseCodeConverterFactory
from .logging_config import get_logger
from .morse_code_player import MorseCodePlayer

# Create a logger for this module
logger = get_logger(__name__)


class MorseCodeConverterGUI:
    """
    A class that provides a graphical user interface for the Morse Code Converter application.
    
    This class uses tkinter to create a GUI that allows users to convert text to Morse code,
    convert Morse code to text, and play Morse code as audio.
    """

    def __init__(self, root: Optional[tk.Tk] = None):
        """
        Initialize the GUI.
        
        Args:
            root (tk.Tk, optional): The root tkinter window. If not provided, a new one will be created.
        """
        # Initialize components
        self.converter = MorseCodeConverterFactory.create_converter()
        self.player = MorseCodePlayer()

        # Create the root window if not provided
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root

        self.root.title("Morse Code Converter")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Dictionary to store keyboard shortcuts
        self.shortcuts = {
            "<Control-1>": self._switch_to_tab_1,
            "<Control-2>": self._switch_to_tab_2,
            "<Control-3>": self._switch_to_tab_3,
            "<Control-q>": self.root.destroy,
            "<F1>": self._show_help,
            "<Control-h>": self._show_history,
            "<Control-s>": self._save_conversion,
            "<Control-o>": self._load_conversion
        }

        # Initialize conversion history
        self.text_to_morse_history = []
        self.morse_to_text_history = []
        self.max_history_size = 10  # Maximum number of items to keep in history

        # Set up the main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create the notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create tabs
        self.text_to_morse_tab = ttk.Frame(self.notebook)
        self.morse_to_text_tab = ttk.Frame(self.notebook)
        self.play_morse_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.text_to_morse_tab, text="Text to Morse")
        self.notebook.add(self.morse_to_text_tab, text="Morse to Text")
        self.notebook.add(self.play_morse_tab, text="Play Morse")

        # Set up each tab
        self._setup_text_to_morse_tab()
        self._setup_morse_to_text_tab()
        self._setup_play_morse_tab()

        # Set up the status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Set up the progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Initialize the progress bar as hidden
        self.progress_bar.pack_forget()

        logger.info("GUI initialized")

    def _setup_text_to_morse_tab(self):
        """Set up the Text to Morse tab."""
        # Create frames for input, output, and buttons
        input_frame = ttk.LabelFrame(self.text_to_morse_tab, text="Input Text", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        output_frame = ttk.LabelFrame(self.text_to_morse_tab, text="Morse Code Output", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        button_frame = ttk.Frame(self.text_to_morse_tab, padding="10")
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        # Create input text area
        self.text_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=5)
        self.text_input.pack(fill=tk.BOTH, expand=True)

        # Create output text area
        self.morse_output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=5)
        self.morse_output.pack(fill=tk.BOTH, expand=True)

        # Create buttons
        convert_button = ttk.Button(button_frame, text="Convert to Morse",
                                    command=self._convert_text_to_morse)
        convert_button.pack(side=tk.LEFT, padx=5)

        play_button = ttk.Button(button_frame, text="Play Morse Code",
                                 command=self._play_morse_from_text)
        play_button.pack(side=tk.LEFT, padx=5)

        save_button = ttk.Button(button_frame, text="Save",
                                 command=self._save_conversion)
        save_button.pack(side=tk.LEFT, padx=5)

        load_button = ttk.Button(button_frame, text="Load",
                                 command=self._load_conversion)
        load_button.pack(side=tk.LEFT, padx=5)

        clear_button = ttk.Button(button_frame, text="Clear",
                                  command=lambda: self._clear_text(self.text_input, self.morse_output))
        clear_button.pack(side=tk.LEFT, padx=5)

    def _setup_morse_to_text_tab(self):
        """Set up the Morse to Text tab."""
        # Create frames for input, output, and buttons
        input_frame = ttk.LabelFrame(self.morse_to_text_tab, text="Input Morse Code", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        output_frame = ttk.LabelFrame(self.morse_to_text_tab, text="Text Output", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        button_frame = ttk.Frame(self.morse_to_text_tab, padding="10")
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        # Create input text area
        self.morse_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=5)
        self.morse_input.pack(fill=tk.BOTH, expand=True)

        # Create output text area
        self.text_output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=5)
        self.text_output.pack(fill=tk.BOTH, expand=True)

        # Create buttons
        convert_button = ttk.Button(button_frame, text="Convert to Text",
                                    command=self._convert_morse_to_text)
        convert_button.pack(side=tk.LEFT, padx=5)

        play_button = ttk.Button(button_frame, text="Play Morse Code",
                                 command=self._play_morse_from_morse)
        play_button.pack(side=tk.LEFT, padx=5)

        clear_button = ttk.Button(button_frame, text="Clear",
                                  command=lambda: self._clear_text(self.morse_input, self.text_output))
        clear_button.pack(side=tk.LEFT, padx=5)

    def _setup_play_morse_tab(self):
        """Set up the Play Morse tab."""
        # Create frames for input and buttons
        input_frame = ttk.LabelFrame(self.play_morse_tab, text="Input Morse Code", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        button_frame = ttk.Frame(self.play_morse_tab, padding="10")
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        # Create input text area
        self.play_morse_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10)
        self.play_morse_input.pack(fill=tk.BOTH, expand=True)

        # Create buttons
        play_button = ttk.Button(button_frame, text="Play Morse Code",
                                 command=self._play_morse_from_play_tab)
        play_button.pack(side=tk.LEFT, padx=5)

        clear_button = ttk.Button(button_frame, text="Clear",
                                  command=lambda: self._clear_text(self.play_morse_input))
        clear_button.pack(side=tk.LEFT, padx=5)

    def _convert_text_to_morse(self):
        """Convert text to Morse code."""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            self._show_error("Input Error", "Text cannot be empty")
            return

        try:
            morse_code = self.converter.to_morse_code(text)
            self.morse_output.delete("1.0", tk.END)
            self.morse_output.insert("1.0", morse_code)
            self.status_var.set("Text converted to Morse code successfully")
            logger.info("Text converted to Morse code successfully")

            # Add to history
            self._add_to_text_to_morse_history(text, morse_code)
        except Exception as e:
            self._show_error("Conversion Error", str(e))

    def _convert_morse_to_text(self):
        """Convert Morse code to text."""
        morse_code = self.morse_input.get("1.0", tk.END).strip()
        if not morse_code:
            self._show_error("Input Error", "Morse code cannot be empty")
            return

        try:
            # Validate Morse code characters
            self._validate_morse_code(morse_code)

            text = self.converter.from_morse_code(morse_code)
            self.text_output.delete("1.0", tk.END)
            self.text_output.insert("1.0", text)
            self.status_var.set("Morse code converted to text successfully")
            logger.info("Morse code converted to text successfully")

            # Add to history
            self._add_to_morse_to_text_history(morse_code, text)
        except Exception as e:
            self._show_error("Conversion Error", str(e))

    def _play_morse_from_text(self):
        """Play Morse code from the text input."""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            self._show_error("Input Error", "Text cannot be empty")
            return

        try:
            morse_code = self.converter.to_morse_code(text)
            self._play_morse_code(morse_code)
        except Exception as e:
            self._show_error("Playback Error", str(e))

    def _play_morse_from_morse(self):
        """Play Morse code from the Morse code input."""
        morse_code = self.morse_input.get("1.0", tk.END).strip()
        if not morse_code:
            self._show_error("Input Error", "Morse code cannot be empty")
            return

        try:
            # Validate Morse code characters
            self._validate_morse_code(morse_code)

            self._play_morse_code(morse_code)
        except Exception as e:
            self._show_error("Playback Error", str(e))

    def _play_morse_from_play_tab(self):
        """Play Morse code from the Play Morse tab."""
        morse_code = self.play_morse_input.get("1.0", tk.END).strip()
        if not morse_code:
            self._show_error("Input Error", "Morse code cannot be empty")
            return

        try:
            # Validate Morse code characters
            self._validate_morse_code(morse_code)

            self._play_morse_code(morse_code)
        except Exception as e:
            self._show_error("Playback Error", str(e))

    def _play_morse_code(self, morse_code: str):
        """
        Play Morse code with a progress bar.
        
        Args:
            morse_code (str): The Morse code to play.
        """
        # Show the progress bar
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        self.progress_var.set(0)
        self.status_var.set("Playing Morse code...")

        # Create a thread to play the Morse code
        def play_thread():
            try:
                # Calculate the total length for progress updates
                total_chars = len(morse_code)

                # Process each character in the Morse code string
                for i, char in enumerate(morse_code):
                    # Update progress
                    progress = (i + 1) / total_chars * 100
                    self.progress_var.set(progress)
                    self.root.update_idletasks()

                    # Play the character
                    if char == '.':
                        sound = self.player.create_sine_wave(self.player.dot_length / 1000.0)
                        sound.play()
                    elif char == '-':
                        sound = self.player.create_sine_wave(self.player.dash_length / 1000.0)
                        sound.play()
                    elif char == ' ':
                        time.sleep(self.player.char_pause)
                    else:
                        time.sleep(self.player.pause)

                    # Pause between elements
                    time.sleep(self.player.pause)

                # Final pause
                time.sleep(self.player.word_pause)

                # Update status and hide progress bar
                self.status_var.set("Morse code playback completed")
                self.progress_var.set(100)
                self.root.update_idletasks()
                time.sleep(0.5)  # Show 100% for a moment
                self.progress_bar.pack_forget()

                logger.info("Morse code playback completed")
            except Exception as e:
                # Handle errors
                self.root.after(0, lambda: self._show_error("Playback Error", str(e)))
                self.progress_bar.pack_forget()

        # Start the thread
        threading.Thread(target=play_thread, daemon=True).start()

    def _validate_morse_code(self, morse_code: str):
        """
        Validate Morse code characters.
        
        Args:
            morse_code (str): The Morse code to validate.
            
        Raises:
            InputError: If the Morse code contains invalid characters.
        """
        valid_chars = {'.', '-', ' '}
        invalid_chars = [char for char in morse_code if char not in valid_chars]
        if invalid_chars:
            unique_invalid = set(invalid_chars)
            raise InputError(
                f"Invalid characters in Morse code: {', '.join(unique_invalid)}. "
                f"Only dots (.), dashes (-), and spaces are allowed."
            )

    def _clear_text(self, *text_widgets):
        """
        Clear the text in the specified text widgets.
        
        Args:
            *text_widgets: The text widgets to clear.
        """
        for widget in text_widgets:
            widget.delete("1.0", tk.END)
        self.status_var.set("Ready")

    def _show_error(self, title: str, message: str):
        """
        Show an error message.
        
        Args:
            title (str): The title of the error message.
            message (str): The error message.
        """
        messagebox.showerror(title, message)
        self.status_var.set(f"Error: {message}")
        logger.error(f"{title}: {message}")

    def _switch_to_tab_1(self, event=None):
        """Switch to the first tab (Text to Morse)."""
        self.notebook.select(0)
        self.status_var.set("Switched to Text to Morse tab")
        return "break"  # Prevent the event from propagating

    def _switch_to_tab_2(self, event=None):
        """Switch to the second tab (Morse to Text)."""
        self.notebook.select(1)
        self.status_var.set("Switched to Morse to Text tab")
        return "break"  # Prevent the event from propagating

    def _switch_to_tab_3(self, event=None):
        """Switch to the third tab (Play Morse)."""
        self.notebook.select(2)
        self.status_var.set("Switched to Play Morse tab")
        return "break"  # Prevent the event from propagating

    def _show_help(self, event=None):
        """Show help information."""
        help_text = """
Morse Code Converter - Keyboard Shortcuts

Tab Navigation:
  Ctrl+1: Switch to Text to Morse tab
  Ctrl+2: Switch to Morse to Text tab
  Ctrl+3: Switch to Play Morse tab

General:
  Ctrl+Q: Quit the application
  F1: Show this help
  Ctrl+H: Show conversion history

Text to Morse Tab:
  Alt+C: Convert text to Morse code
  Alt+P: Play Morse code
  Alt+L: Clear fields

Morse to Text Tab:
  Alt+C: Convert Morse code to text
  Alt+P: Play Morse code
  Alt+L: Clear fields

Play Morse Tab:
  Alt+P: Play Morse code
  Alt+L: Clear field
"""
        messagebox.showinfo("Keyboard Shortcuts", help_text)
        return "break"  # Prevent the event from propagating

    def _add_to_text_to_morse_history(self, text: str, morse_code: str):
        """
        Add a text-to-morse conversion to the history.
        
        Args:
            text (str): The original text.
            morse_code (str): The converted Morse code.
        """
        # Add to the beginning of the list (most recent first)
        self.text_to_morse_history.insert(0, {"text": text, "morse_code": morse_code})

        # Limit the history size
        if len(self.text_to_morse_history) > self.max_history_size:
            self.text_to_morse_history.pop()

        logger.debug(f"Added to text-to-morse history: {text} -> {morse_code}")

    def _add_to_morse_to_text_history(self, morse_code: str, text: str):
        """
        Add a morse-to-text conversion to the history.
        
        Args:
            morse_code (str): The original Morse code.
            text (str): The converted text.
        """
        # Add to the beginning of the list (most recent first)
        self.morse_to_text_history.insert(0, {"morse_code": morse_code, "text": text})

        # Limit the history size
        if len(self.morse_to_text_history) > self.max_history_size:
            self.morse_to_text_history.pop()

        logger.debug(f"Added to morse-to-text history: {morse_code} -> {text}")

    def _show_history(self, event=None):
        """Show the conversion history."""
        # Create a new top-level window
        history_window = tk.Toplevel(self.root)
        history_window.title("Conversion History")
        history_window.geometry("600x400")
        history_window.minsize(400, 300)

        # Create a notebook with tabs for different history types
        notebook = ttk.Notebook(history_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        text_to_morse_tab = ttk.Frame(notebook)
        morse_to_text_tab = ttk.Frame(notebook)

        notebook.add(text_to_morse_tab, text="Text to Morse History")
        notebook.add(morse_to_text_tab, text="Morse to Text History")

        # Populate Text to Morse history tab
        self._populate_history_tab(
            text_to_morse_tab,
            self.text_to_morse_history,
            ["Text", "Morse Code"],
            self._use_text_to_morse_history_item
        )

        # Populate Morse to Text history tab
        self._populate_history_tab(
            morse_to_text_tab,
            self.morse_to_text_history,
            ["Morse Code", "Text"],
            self._use_morse_to_text_history_item
        )

        # Add a close button
        close_button = ttk.Button(history_window, text="Close", command=history_window.destroy)
        close_button.pack(pady=10)

        # Make the window modal
        history_window.transient(self.root)
        history_window.grab_set()
        self.root.wait_window(history_window)

        return "break"  # Prevent the event from propagating

    def _save_conversion(self, event=None):
        """Save the current conversion to a file."""
        # Determine which tab is currently active
        current_tab = self.notebook.index(self.notebook.select())

        # Get the appropriate data based on the active tab
        if current_tab == 0:  # Text to Morse tab
            text = self.text_input.get("1.0", tk.END).strip()
            morse_code = self.morse_output.get("1.0", tk.END).strip()
            data = {"type": "text_to_morse", "text": text, "morse_code": morse_code}
        elif current_tab == 1:  # Morse to Text tab
            morse_code = self.morse_input.get("1.0", tk.END).strip()
            text = self.text_output.get("1.0", tk.END).strip()
            data = {"type": "morse_to_text", "morse_code": morse_code, "text": text}
        elif current_tab == 2:  # Play Morse tab
            morse_code = self.play_morse_input.get("1.0", tk.END).strip()
            data = {"type": "play_morse", "morse_code": morse_code}
        else:
            self._show_error("Save Error", "Unknown tab selected")
            return "break"

        # Show a file dialog to let the user choose where to save the file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Conversion"
        )

        if not file_path:
            # User cancelled the dialog
            return "break"

        try:
            # Save the data to the file
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)

            self.status_var.set(f"Conversion saved to {file_path}")
            logger.info(f"Conversion saved to {file_path}")
        except Exception as e:
            self._show_error("Save Error", str(e))

        return "break"  # Prevent the event from propagating

    def _load_conversion(self, event=None):
        """Load a conversion from a file."""
        # Show a file dialog to let the user choose which file to load
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load Conversion"
        )

        if not file_path:
            # User cancelled the dialog
            return "break"

        try:
            # Load the data from the file
            with open(file_path, "r") as f:
                data = json.load(f)

            # Check the type of conversion and switch to the appropriate tab
            if data.get("type") == "text_to_morse":
                # Switch to the Text to Morse tab
                self.notebook.select(0)

                # Set the text and morse code
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert("1.0", data.get("text", ""))

                self.morse_output.delete("1.0", tk.END)
                self.morse_output.insert("1.0", data.get("morse_code", ""))

            elif data.get("type") == "morse_to_text":
                # Switch to the Morse to Text tab
                self.notebook.select(1)

                # Set the morse code and text
                self.morse_input.delete("1.0", tk.END)
                self.morse_input.insert("1.0", data.get("morse_code", ""))

                self.text_output.delete("1.0", tk.END)
                self.text_output.insert("1.0", data.get("text", ""))

            elif data.get("type") == "play_morse":
                # Switch to the Play Morse tab
                self.notebook.select(2)

                # Set the morse code
                self.play_morse_input.delete("1.0", tk.END)
                self.play_morse_input.insert("1.0", data.get("morse_code", ""))

            else:
                self._show_error("Load Error", "Unknown conversion type")
                return "break"

            self.status_var.set(f"Conversion loaded from {file_path}")
            logger.info(f"Conversion loaded from {file_path}")
        except Exception as e:
            self._show_error("Load Error", str(e))

        return "break"  # Prevent the event from propagating

    def _populate_history_tab(self, tab, history, columns, use_callback):
        """
        Populate a history tab with a treeview of history items.
        
        Args:
            tab: The tab to populate.
            history: The history list.
            columns: The column names.
            use_callback: The callback to call when a history item is used.
        """
        if not history:
            # Show a message if there's no history
            label = ttk.Label(tab, text="No conversion history yet.")
            label.pack(pady=20)
            return

        # Create a frame for the treeview
        frame = ttk.Frame(tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the treeview
        treeview = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )

        # Configure the scrollbar
        scrollbar.config(command=treeview.yview)

        # Set up the columns
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=100, anchor=tk.W)

        # Add the history items
        for i, item in enumerate(history):
            values = [item[col.lower().replace(" ", "_")] for col in columns]
            treeview.insert("", tk.END, iid=str(i), values=values)

        treeview.pack(fill=tk.BOTH, expand=True)

        # Create a button frame
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        # Add a button to use the selected history item
        use_button = ttk.Button(
            button_frame,
            text="Use Selected",
            command=lambda: self._use_history_item(treeview, history, use_callback)
        )
        use_button.pack(side=tk.LEFT, padx=5)

        # Add a button to clear the history
        clear_button = ttk.Button(
            button_frame,
            text="Clear History",
            command=lambda: self._clear_history(history, treeview)
        )
        clear_button.pack(side=tk.LEFT, padx=5)

    def _use_history_item(self, treeview, history, callback):
        """
        Use a selected history item.
        
        Args:
            treeview: The treeview containing the history items.
            history: The history list.
            callback: The callback to call with the selected history item.
        """
        # Get the selected item
        selected = treeview.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a history item to use.")
            return

        # Get the index of the selected item
        index = int(selected[0])

        # Call the callback with the selected item
        callback(history[index])

    def _use_text_to_morse_history_item(self, item):
        """
        Use a text-to-morse history item.
        
        Args:
            item: The history item to use.
        """
        # Switch to the Text to Morse tab
        self.notebook.select(0)

        # Set the text and morse code
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", item["text"])

        self.morse_output.delete("1.0", tk.END)
        self.morse_output.insert("1.0", item["morse_code"])

        self.status_var.set("Loaded from history")
        logger.info("Loaded text-to-morse conversion from history")

    def _use_morse_to_text_history_item(self, item):
        """
        Use a morse-to-text history item.
        
        Args:
            item: The history item to use.
        """
        # Switch to the Morse to Text tab
        self.notebook.select(1)

        # Set the morse code and text
        self.morse_input.delete("1.0", tk.END)
        self.morse_input.insert("1.0", item["morse_code"])

        self.text_output.delete("1.0", tk.END)
        self.text_output.insert("1.0", item["text"])

        self.status_var.set("Loaded from history")
        logger.info("Loaded morse-to-text conversion from history")

    def _clear_history(self, history, treeview):
        """
        Clear the history.
        
        Args:
            history: The history list to clear.
            treeview: The treeview to update.
        """
        # Confirm with the user
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the history?"):
            # Clear the history
            history.clear()

            # Clear the treeview
            for item in treeview.get_children():
                treeview.delete(item)

            # Add a message
            treeview.insert("", tk.END, values=["No history items"])

            self.status_var.set("History cleared")
            logger.info("Conversion history cleared")

    def _bind_shortcuts(self):
        """Bind keyboard shortcuts to the root window."""
        for shortcut, callback in self.shortcuts.items():
            self.root.bind(shortcut, callback)

        # Tab-specific shortcuts
        # Text to Morse tab
        self.text_input.bind("<Alt-c>", lambda e: self._convert_text_to_morse())
        self.text_input.bind("<Alt-p>", lambda e: self._play_morse_from_text())
        self.text_input.bind("<Alt-l>", lambda e: self._clear_text(self.text_input, self.morse_output))

        # Morse to Text tab
        self.morse_input.bind("<Alt-c>", lambda e: self._convert_morse_to_text())
        self.morse_input.bind("<Alt-p>", lambda e: self._play_morse_from_morse())
        self.morse_input.bind("<Alt-l>", lambda e: self._clear_text(self.morse_input, self.text_output))

        # Play Morse tab
        self.play_morse_input.bind("<Alt-p>", lambda e: self._play_morse_from_play_tab())
        self.play_morse_input.bind("<Alt-l>", lambda e: self._clear_text(self.play_morse_input))

    def run(self):
        """Run the GUI application."""
        # Bind keyboard shortcuts before running the application
        self._bind_shortcuts()

        # Show initial help message
        self.status_var.set("Press F1 for keyboard shortcuts")

        self.root.mainloop()


def run_gui():
    """Run the Morse Code Converter GUI application."""
    try:
        root = tk.Tk()
        app = MorseCodeConverterGUI(root)
        app.run()
    except Exception as e:
        logger.exception(f"Error running GUI: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    run_gui()
