"""
Modern Folder JSON Editor with improved UI and song reordering
I LOVE VIBE CODING
"""
import os
import tkinter as tk
import traceback
from tkinter import filedialog, messagebox, simpledialog, ttk
import json

from src import constants
from src.config import config


class EventFolderEditor:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(parent.window)
        self.root.title("Event Folder Editor")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        # Configure styles
        self.setup_styles()

        self.folder_data = []
        self.current_file_path = None

        # Create main layout
        self.create_widgets()

    def setup_styles(self):
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure button style
        style.configure('Modern.TButton',
                        padding=(10, 5),
                        font=('Arial', 9))

        # Configure frame style
        style.configure('Card.TFrame',
                        relief='raised',
                        borderwidth=1,
                        background='white')

        # Configure label style
        style.configure('Heading.TLabel',
                        font=('Arial', 12, 'bold'),
                        background='white')

        style.configure('Field.TLabel',
                        font=('Arial', 9),
                        background='white')

    def create_widgets(self):
        """Create and layout all widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Header
        self.create_header(main_frame)

        # Content area with two columns
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, pady=(10, 0))

        # Left column - Folder List
        self.create_folder_list_panel(content_frame)

        # Right column - Folder Details
        self.create_details_panel(content_frame)

    def create_header(self, parent):
        """Create header with file operations"""
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 10))

        # Title
        title_label = ttk.Label(header_frame, text="Event Folder Editor",
                                style='Heading.TLabel')
        title_label.pack(side='left', padx=10, pady=10)

        # File operations
        file_frame = tk.Frame(header_frame, bg='white')
        file_frame.pack(side='right', padx=10, pady=10)

        ttk.Button(file_frame, text="📁 Open JSON",
                   command=self.open_file,
                   style='Modern.TButton').pack(side='left', padx=(0, 5))

        ttk.Button(file_frame, text="💾 Save JSON",
                   command=self.save_file,
                   style='Modern.TButton').pack(side='left', padx=5)

        ttk.Button(file_frame, text="💾 Save As...",
                   command=self.save_file_as,
                   style='Modern.TButton').pack(side='left', padx=5)

    def create_folder_list_panel(self, parent):
        """Create left panel with folder list"""
        left_frame = ttk.Frame(parent, style='Card.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Folder list header
        list_header = tk.Frame(left_frame, bg='white')
        list_header.pack(fill='x', padx=10, pady=10)

        ttk.Label(list_header, text="Folders", style='Heading.TLabel').pack(side='left')

        # Folder list buttons
        list_buttons = tk.Frame(list_header, bg='white')
        list_buttons.pack(side='right')

        ttk.Button(list_buttons, text="➕ Add",
                   command=self.add_folder,
                   style='Modern.TButton').pack(side='left', padx=2)

        ttk.Button(list_buttons, text="🗑️ Delete",
                   command=self.delete_folder,
                   style='Modern.TButton').pack(side='left', padx=2)

        # Folder listbox with scrollbar
        listbox_frame = tk.Frame(left_frame, bg='white')
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Scrollbar
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')

        # Listbox
        self.folder_listbox = tk.Listbox(listbox_frame,
                                         yscrollcommand=scrollbar.set,
                                         font=('Arial', 9),
                                         selectmode='single',
                                         relief='flat',
                                         borderwidth=0,
                                         highlightthickness=1,
                                         highlightcolor='#4CAF50',
                                         # selectbackground='#E8F5E8'
                                         )
        self.folder_listbox.pack(fill='both', expand=True)
        self.folder_listbox.bind('<<ListboxSelect>>', self.on_folder_select)

        scrollbar.config(command=self.folder_listbox.yview)

    def create_details_panel(self, parent):
        """Create right panel with folder details"""
        right_frame = ttk.Frame(parent, style='Card.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        # Details header
        details_header = tk.Frame(right_frame, bg='white')
        details_header.pack(fill='x', padx=10, pady=10)

        ttk.Label(details_header, text="Folder Details", style='Heading.TLabel').pack(side='left')

        # Form frame
        form_container = tk.Frame(right_frame, bg='white')
        form_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Create form fields
        self.entries = {}
        self.create_form_fields(form_container)

        # Songs section
        songs_frame = tk.Frame(form_container, bg='white')
        songs_frame.pack(fill='x', pady=(20, 0))

        ttk.Label(songs_frame, text="Songs", style='Heading.TLabel').pack(anchor='w')

        songs_button_frame = tk.Frame(songs_frame, bg='white')
        songs_button_frame.pack(fill='x', pady=(5, 0))

        ttk.Button(songs_button_frame, text="🎵 Edit Songs",
                   command=self.edit_songs,
                   style='Modern.TButton').pack(side='left')

        # Auto-save note
        note_frame = tk.Frame(form_container, bg='white')
        note_frame.pack(fill='x', pady=(20, 0))

        note_label = tk.Label(note_frame,
                              text="💡 Changes are automatically saved when you switch between folders",
                              font=('Arial', 8),
                              fg='#666',
                              bg='white')
        note_label.pack(anchor='w')

    def create_form_fields(self, parent):
        """Create form fields for folder properties"""
        fields = [
            ("commentName", "Folder Name"),
            ("commentId", "Comment ID"),
            ("verupNo", "Version Number"),
            ("priority", "Priority")
        ]

        for i, (key, label) in enumerate(fields):
            field_frame = tk.Frame(parent, bg='white')
            field_frame.pack(fill='x', pady=5)

            # Label
            ttk.Label(field_frame, text=label, style='Field.TLabel').pack(anchor='w')

            # Entry
            entry = tk.Entry(field_frame,
                             font=('Arial', 9),
                             relief='solid',
                             borderwidth=1,
                             highlightthickness=2,
                             highlightcolor='#4CAF50')
            entry.pack(fill='x', pady=(2, 0))

            self.entries[key] = entry

            # Bind focus events for better UX
            entry.bind('<FocusIn>', lambda e: e.widget.config(highlightcolor='#4CAF50'))
            entry.bind('<FocusOut>', lambda e: e.widget.config(highlightcolor='#ddd'))

    def open_file(self):
        """Open and load JSON file"""
        file_path = filedialog.askopenfilename(
            initialdir=config.event_folder_dir,
            title="Open Event Folder File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            parent=self.root
        )
        if not file_path:
            return
        if os.path.basename(file_path) != "event_folder_data.json":
            messagebox.showerror("Error", f"File not event_folder_data.json", parent=self.root)
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.folder_data = json.load(f)
            self.current_file_path = file_path
            self.refresh_folder_list()
            self.update_window_title()
            if os.path.dirname(file_path) != config.event_folder_dir:
                config.update_event_folder_dir(os.path.dirname(file_path))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}", parent=self.root)

    def update_window_title(self):
        """Update window title with current file"""
        if self.current_file_path:
            self.root.title(f"Event Folder Editor - {self.current_file_path}")
        else:
            self.root.title("Event Folder Editor")

    def refresh_folder_list(self):
        """Refresh the folder list display"""
        self.folder_listbox.delete(0, tk.END)
        for i, folder in enumerate(self.folder_data):
            display = f"{folder.get('commentName', 'Unnamed')} ({folder.get('commentId', 'No ID')})"
            self.folder_listbox.insert(tk.END, display)

    def on_folder_select(self, event):
        """Handle folder selection"""
        index = self.get_selected_index()
        if index is None:
            return

        folder = self.folder_data[index]
        for key in self.entries:
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, str(folder.get(key, "")))

    def get_selected_index(self):
        """Get the currently selected folder index"""
        selection = self.folder_listbox.curselection()
        return selection[0] if selection else None

    def update_selected_folder(self):
        """Update the selected folder with form data"""
        index = self.get_selected_index()
        if index is None:
            return True

        folder = self.folder_data[index]

        try:
            for key, entry in self.entries.items():
                value = entry.get().strip()
                if key in ["verupNo", "priority"]:
                    folder[key] = int(value) if value else 0
                else:
                    folder[key] = value
            return True
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter valid numbers for Version Number and Priority",
                                 parent=self.root)
            return False

    def add_folder(self):
        """Add a new folder"""
        new_folder = {
            "commentName": "New Folder",
            "commentId": f"folder_event{len(self.folder_data) + 1}",
            "folderId": len(self.folder_data) + 1,
            "verupNo": 1,
            "priority": 1000,
            "songNo": []
        }
        self.folder_data.append(new_folder)
        self.refresh_folder_list()

        # Select the new folder
        self.folder_listbox.select_set(tk.END)
        self.folder_listbox.see(tk.END)
        self.on_folder_select(None)

    def delete_folder(self):
        """Delete the selected folder"""
        index = self.get_selected_index()
        if index is None:
            messagebox.showwarning("No Selection", "Please select a folder to delete.", parent=self.root)
            return

        folder = self.folder_data[index]
        result = messagebox.askyesno("Confirm Delete",
                                     f"Are you sure you want to delete folder '{folder.get('commentName', 'Unnamed')}'?",
                                     parent=self.root)
        if result:
            del self.folder_data[index]
            self.refresh_folder_list()
            # Clear form
            for entry in self.entries.values():
                entry.delete(0, tk.END)

    def edit_songs(self):
        """Edit songs for the selected folder"""
        index = self.get_selected_index()
        if index is None:
            messagebox.showwarning("No Selection", "Please select a folder to edit songs.", parent=self.root)
            return

        if not self.update_selected_folder():
            return

        folder = self.folder_data[index]
        self.open_song_editor(folder)

    def open_song_editor(self, folder):
        """Open song editor window"""
        if not hasattr(self.parent, 'datatable'):
            messagebox.showerror('Song Editor Error', 'Please open datatable first', parent=self.root)
            return

        song_window = tk.Toplevel(self.root)
        song_window.title(f'Edit Songs - {folder["commentName"]}')
        song_window.geometry('1500x700')
        song_window.configure(bg='#f0f0f0')
        song_window.focus_set()

        # Make window modal
        song_window.transient(self.root)
        song_window.grab_set()

        # Configure styles for this window
        style = ttk.Style()
        style.configure('SongEditor.TFrame', background='white', relief='raised', borderwidth=1)

        # Current songs in folder
        current_songs = folder.get('songNo', []).copy()

        # Language selection
        langvar = tk.IntVar(value=0)  # Default to Japanese

        # Create main layout
        main_frame = tk.Frame(song_window, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Header
        header_frame = ttk.Frame(main_frame, style='SongEditor.TFrame')
        header_frame.pack(fill='x', pady=(0, 10))

        title_label = ttk.Label(header_frame, text=f"Songs in '{folder['commentName']}'",
                                font=('Arial', 12, 'bold'), background='white')
        title_label.pack(side='left', padx=10, pady=10)

        # Language selection
        lang_frame = tk.Frame(header_frame, bg='white')
        lang_frame.pack(side='right', padx=10, pady=10)

        tk.Label(lang_frame, text='Language:', bg='white', font=('Arial', 9)).pack(side='left')

        languages = ['Japanese', 'English', 'Chinese (T)', 'Korean', 'Chinese (S)']
        lang_combo = ttk.Combobox(lang_frame, values=languages, state='readonly', width=12)
        lang_combo.set(languages[0])
        lang_combo.pack(side='left', padx=(5, 0))

        # Content area with two panels
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True)

        # Left panel - Current songs
        left_panel = ttk.Frame(content_frame, style='SongEditor.TFrame')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Current songs header
        current_header = tk.Frame(left_panel, bg='white')
        current_header.pack(fill='x', padx=10, pady=10)

        tk.Label(current_header, text='Current Songs', font=('Arial', 11, 'bold'),
                 bg='white').pack(side='left')

        # Current songs buttons
        current_buttons = tk.Frame(current_header, bg='white')
        current_buttons.pack(side='right')

        remove_btn = ttk.Button(current_buttons, text='🗑️ Remove Selected',
                                style='Modern.TButton')
        remove_btn.pack(side='left', padx=2)

        clear_btn = ttk.Button(current_buttons, text='🧹 Clear All',
                               style='Modern.TButton')
        clear_btn.pack(side='left', padx=2)

        # Reorder buttons
        reorder_frame = tk.Frame(current_header, bg='white')
        reorder_frame.pack(side='right', padx=(10, 0))

        move_up_btn = ttk.Button(reorder_frame, text='⬆️ Move Up',
                                 style='Modern.TButton')
        move_up_btn.pack(side='left', padx=2)

        move_down_btn = ttk.Button(reorder_frame, text='⬇️ Move Down',
                                   style='Modern.TButton')
        move_down_btn.pack(side='left', padx=2)

        # Current songs tree
        current_tree_frame = tk.Frame(left_panel, bg='white')
        current_tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        current_tree = ttk.Treeview(current_tree_frame,
                                    columns=("Order", "Title", "Sub", "SongId", "UniqueId"),
                                    show="headings", selectmode="extended")

        # Current songs scrollbar
        current_vsb = ttk.Scrollbar(current_tree_frame, orient="vertical",
                                    command=current_tree.yview)
        current_vsb.pack(side='right', fill='y')

        current_tree.configure(yscrollcommand=current_vsb.set)
        current_tree.pack(side='left', fill='both', expand=True)

        # Configure current songs tree headings
        current_tree.heading("Order", text="#")
        current_tree.heading("Title", text="Title")
        current_tree.heading("Sub", text="Sub")
        current_tree.heading("SongId", text="Song ID")
        current_tree.heading("UniqueId", text="Unique ID")

        # Configure column widths
        current_tree.column("Order", width=40, minwidth=40)
        current_tree.column("Title", width=200, minwidth=150)
        current_tree.column("Sub", width=150, minwidth=100)
        current_tree.column("SongId", width=100, minwidth=80)
        current_tree.column("UniqueId", width=100, minwidth=80)

        # Right panel - Song search/browser
        right_panel = ttk.Frame(content_frame, style='SongEditor.TFrame')
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))

        # Search header
        search_header = tk.Frame(right_panel, bg='white')
        search_header.pack(fill='x', padx=10, pady=10)

        tk.Label(search_header, text='Add Songs', font=('Arial', 11, 'bold'),
                 bg='white').pack(side='left')

        # Search controls
        search_controls = tk.Frame(right_panel, bg='white')
        search_controls.pack(fill='x', padx=10, pady=(0, 10))

        tk.Label(search_controls, text='Search:', bg='white').pack(side='left')

        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_controls, textvariable=search_var, width=25)
        search_entry.pack(side='left', padx=(5, 10))

        add_btn = ttk.Button(search_controls, text='➕ Add Selected',
                             style='Modern.TButton')
        add_btn.pack(side='right')

        # Search results tree
        search_tree_frame = tk.Frame(right_panel, bg='white')
        search_tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        search_tree = ttk.Treeview(search_tree_frame,
                                   columns=("Title", "Sub", "SongId", "UniqueId"),
                                   show="headings", selectmode="extended")

        # Search results scrollbar
        search_vsb = ttk.Scrollbar(search_tree_frame, orient="vertical",
                                   command=search_tree.yview)
        search_vsb.pack(side='right', fill='y')

        search_tree.configure(yscrollcommand=search_vsb.set)
        search_tree.pack(side='left', fill='both', expand=True)

        # Configure search tree headings
        search_tree.heading("Title", text="Title")
        search_tree.heading("Sub", text="Sub")
        search_tree.heading("SongId", text="Song ID")
        search_tree.heading("UniqueId", text="Unique ID")

        # Genre colors - configure for both trees
        try:
            genre_colors = constants.GENRE_COLOURS
            for genre, color in genre_colors.items():
                search_tree.tag_configure(str(genre), background=color)
                current_tree.tag_configure(str(genre), background=color)
        except AttributeError:
            # Fallback if constants not available
            pass

        # Bottom buttons
        bottom_frame = tk.Frame(main_frame, bg='#f0f0f0')
        bottom_frame.pack(fill='x', pady=(10, 0))

        # Reorder instructions
        instructions_label = tk.Label(bottom_frame,
                                    text="💡 Use Move Up/Down buttons or drag & drop to reorder songs",
                                    font=('Arial', 8), fg='#666', bg='#f0f0f0')
        instructions_label.pack(side='left')

        ttk.Button(bottom_frame, text='💾 Save Changes',
                   style='Modern.TButton').pack(side='right', padx=(5, 0))

        ttk.Button(bottom_frame, text='❌ Cancel',
                   style='Modern.TButton').pack(side='right')

        # Drag and drop variables
        drag_data = {'item': None, 'start_index': None}

        # Helper functions
        def update_current_songs():
            """Update the current songs display"""
            current_tree.delete(*current_tree.get_children())
            if not current_songs:
                return

            try:
                song_data = self.parent.datatable.select_song_list(current_songs)
                lang_idx = lang_combo.current()

                for i, song in enumerate(song_data):
                    values = (
                        str(i + 1),  # Order number
                        song.title[lang_idx] if lang_idx < len(song.title) else song.title[0],
                        song.sub[lang_idx] if lang_idx < len(song.sub) else song.sub[0],
                        song.id,
                        song.uniqueId
                    )
                    current_tree.insert("", tk.END, values=values,
                                        tags=(str(song.mainGenre),))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load current songs: {str(e)}", parent=song_window)

        def perform_search():
            """Perform search in all songs"""
            search_tree.delete(*search_tree.get_children())
            query = search_var.get().lower()

            if not hasattr(self.parent, 'datatable'):
                return

            try:
                song_list = self.parent.datatable.get_song_list(main_genre_only=True)
                lang_idx = lang_combo.current()

                for genre, songs in enumerate(song_list):
                    for song in songs:
                        # Always get title and sub for display
                        title = song.title[lang_idx] if lang_idx < len(song.title) else song.title[0]
                        sub = song.sub[lang_idx] if lang_idx < len(song.sub) else song.sub[0]

                        if not query:  # Show all if no search query
                            should_show = True
                        else:
                            should_show = (query in title.lower() or
                                           query in sub.lower() or
                                           query in song.id.lower() or
                                           query in str(song.uniqueId))

                        if should_show:
                            values = (
                                title,
                                sub,
                                song.id,
                                song.uniqueId
                            )
                            search_tree.insert("", tk.END, values=values,
                                               tags=(str(genre),))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to perform search: {str(e)}", parent=song_window)

        def add_selected_songs():
            """Add selected songs to current folder"""
            selection = search_tree.selection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select songs to add.", parent=song_window)
                return

            added_count = 0
            for item in selection:
                values = search_tree.item(item)['values']
                unique_id = values[3]  # UniqueId is at index 3

                if unique_id not in current_songs:
                    current_songs.append(unique_id)
                    added_count += 1

            if added_count > 0:
                update_current_songs()
            else:
                messagebox.showinfo("No Changes", "Selected songs are already in the folder.", parent=song_window)

        def remove_selected_songs():
            """Remove selected songs from current folder"""
            selection = current_tree.selection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select songs to remove.", parent=song_window)
                return

            # Get indices of selected items
            indices_to_remove = []
            for item in selection:
                values = current_tree.item(item)['values']
                order = int(values[0]) - 1  # Convert to 0-based index
                indices_to_remove.append(order)

            # Sort indices in reverse order to avoid index shifting issues
            indices_to_remove.sort(reverse=True)

            removed_count = 0
            for index in indices_to_remove:
                if 0 <= index < len(current_songs):
                    current_songs.pop(index)
                    removed_count += 1

            if removed_count > 0:
                update_current_songs()

        def clear_all_songs():
            """Clear all songs from folder"""
            if current_songs:
                result = messagebox.askyesno("Confirm Clear",
                                             "Are you sure you want to remove all songs from this folder?",
                                             parent=song_window)
                if result:
                    current_songs.clear()
                    update_current_songs()
                    messagebox.showinfo("Success", "All songs removed from folder.", parent=song_window)

        def move_song_up():
            """Move selected song up in the list"""
            selection = current_tree.selection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a song to move up.", parent=song_window)
                return

            if len(selection) > 1:
                messagebox.showwarning("Multiple Selection", "Please select only one song to move.", parent=song_window)
                return

            item = selection[0]
            values = current_tree.item(item)['values']
            order = int(values[0]) - 1  # Convert to 0-based index

            if order > 0:
                # Swap with previous song
                current_songs[order], current_songs[order - 1] = current_songs[order - 1], current_songs[order]
                update_current_songs()

                # Reselect the moved item
                new_item = current_tree.get_children()[order - 1]
                current_tree.selection_set(new_item)
                current_tree.focus(new_item)
                current_tree.see(new_item)

        def move_song_down():
            """Move selected song down in the list"""
            selection = current_tree.selection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a song to move down.", parent=song_window)
                return

            if len(selection) > 1:
                messagebox.showwarning("Multiple Selection", "Please select only one song to move.", parent=song_window)
                return

            item = selection[0]
            values = current_tree.item(item)['values']
            order = int(values[0]) - 1  # Convert to 0-based index

            if order < len(current_songs) - 1:
                # Swap with next song
                current_songs[order], current_songs[order + 1] = current_songs[order + 1], current_songs[order]
                update_current_songs()

                # Reselect the moved item
                new_item = current_tree.get_children()[order + 1]
                current_tree.selection_set(new_item)
                current_tree.focus(new_item)
                current_tree.see(new_item)

        def on_drag_start(event):
            """Handle drag start for reordering"""
            item = current_tree.identify_row(event.y)
            if item:
                values = current_tree.item(item)['values']
                drag_data['item'] = item
                drag_data['start_index'] = int(values[0]) - 1  # Convert to 0-based index
                current_tree.configure(cursor='hand2')

        def on_drag_motion(event):
            """Handle drag motion"""
            if drag_data['item']:
                # Visual feedback could be added here
                pass

        def on_drag_end(event):
            """Handle drag end for reordering"""
            if drag_data['item']:
                target_item = current_tree.identify_row(event.y)
                if target_item and target_item != drag_data['item']:
                    target_values = current_tree.item(target_item)['values']
                    target_index = int(target_values[0]) - 1  # Convert to 0-based index

                    start_index = drag_data['start_index']

                    if start_index != target_index:
                        # Remove the item from its original position
                        song_to_move = current_songs.pop(start_index)
                        # Insert it at the new position
                        current_songs.insert(target_index, song_to_move)
                        update_current_songs()

                        # Reselect the moved item
                        new_item = current_tree.get_children()[target_index]
                        current_tree.selection_set(new_item)
                        current_tree.focus(new_item)
                        current_tree.see(new_item)

                current_tree.configure(cursor='')
                drag_data['item'] = None
                drag_data['start_index'] = None

        def save_changes():
            """Save changes and close window"""
            folder['songNo'] = current_songs.copy()
            messagebox.showinfo("Success", f"Saved {len(current_songs)} songs to folder.", parent=song_window)
            song_window.destroy()

        def cancel_changes():
            """Cancel changes and close window"""
            song_window.destroy()

        def on_language_change(event):
            """Handle language change"""
            update_current_songs()
            perform_search()

        def on_key_press(event):
            """Handle key press events"""
            if event.keysym == 'Delete':
                if event.widget == current_tree:
                    remove_selected_songs()
            elif event.keysym == 'Return':
                if event.widget == search_tree:
                    add_selected_songs()
                elif event.widget == search_entry:
                    perform_search()
            elif event.keysym == 'Up' and event.state & 0x4:  # Ctrl+Up
                if event.widget == current_tree:
                    move_song_up()
                    return 'break'
            elif event.keysym == 'Down' and event.state & 0x4:  # Ctrl+Down
                if event.widget == current_tree:
                    move_song_down()
                    return 'break'

        # Bind events
        search_var.trace_add("write", lambda *args: perform_search())
        lang_combo.bind('<<ComboboxSelected>>', on_language_change)

        # Button commands
        add_btn.config(command=add_selected_songs)
        remove_btn.config(command=remove_selected_songs)
        clear_btn.config(command=clear_all_songs)
        move_up_btn.config(command=move_song_up)
        move_down_btn.config(command=move_song_down)

        # Bottom button commands
        for widget in bottom_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                text = widget.cget('text')
                if 'Save' in text:
                    widget.config(command=save_changes)
                elif 'Cancel' in text:
                    widget.config(command=cancel_changes)

        # Drag and drop bindings for current songs tree
        current_tree.bind('<Button-1>', on_drag_start)
        current_tree.bind('<B1-Motion>', on_drag_motion)
        current_tree.bind('<ButtonRelease-1>', on_drag_end)

        # Key bindings
        song_window.bind('<Key>', on_key_press)
        current_tree.bind('<Delete>', on_key_press)
        current_tree.bind('<KeyPress>', on_key_press)
        search_tree.bind('<Return>', on_key_press)
        search_tree.bind('<KeyPress>', on_key_press)
        search_entry.bind('<Return>', on_key_press)

        # Double-click to add songs
        search_tree.bind('<Double-1>', lambda e: add_selected_songs())

        # Focus on search entry
        search_entry.focus()

        # Initialize displays
        update_current_songs()
        perform_search()

        # Handle window closing
        def on_closing():
            song_window.destroy()

        song_window.protocol("WM_DELETE_WINDOW", on_closing)

    def save_file(self):
        """Save to current file"""
        if not self.current_file_path:
            self.save_file_as()
            return

        if not self.update_selected_folder():
            return

        try:
            with open(self.current_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.folder_data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Success", "File saved successfully!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}", parent=self.root)

    def save_file_as(self):
        """Save as new file"""
        if not self.update_selected_folder():
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Folder JSON File",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            parent=self.root
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.folder_data, f, indent=4, ensure_ascii=False)
            self.current_file_path = file_path
            self.update_window_title()
            messagebox.showinfo("Success", "File saved successfully!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}", parent=self.root)