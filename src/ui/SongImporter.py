import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.datatable import Datatable
from src import constants
from src.config import config
import os


class SongImporter:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(parent.window)
        self.source_datatable = None
        self.import_queue = []  # List of songs to import
        self.unique_id_remappings = {}  # Dict of {old_uid: new_uid}

        # Window setup
        self.root.title("Import Songs")
        self.root.geometry("1400x1000")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')

        # Make window modal
        self.root.transient(parent.window)
        self.root.grab_set()

        # Configure styles
        style = ttk.Style()
        style.configure('SongImporter.TFrame', background='white', relief='raised', borderwidth=1)

        self.setup_ui()

    def setup_ui(self):
        """Setup the UI components"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Header frame
        header_frame = ttk.Frame(main_frame, style='SongImporter.TFrame')
        header_frame.pack(fill='x', pady=(0, 10))

        # Load datatable button
        load_btn = ttk.Button(header_frame, text='📁 Load Source Datatable',
                              command=self.load_source_datatable)
        load_btn.pack(side='left', padx=10, pady=10)

        # Status label
        self.status_label = tk.Label(header_frame, text='No source datatable loaded',
                                     bg='white', fg='red', font=('Arial', 9))
        self.status_label.pack(side='left', padx=10, pady=10)

        # Language selection
        lang_frame = tk.Frame(header_frame, bg='white')
        lang_frame.pack(side='right', padx=10, pady=10)

        tk.Label(lang_frame, text='Language:', bg='white', font=('Arial', 9)).pack(side='left')

        languages = constants.LANGUAGES
        self.lang_combo = ttk.Combobox(lang_frame, values=languages, state='readonly', width=12)
        self.lang_combo.set(languages[0])
        self.lang_combo.pack(side='left', padx=(5, 0))
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)

        # Content frame
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True)

        # Left panel - Source songs
        left_panel = ttk.Frame(content_frame, style='SongImporter.TFrame')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Left panel header
        left_header = tk.Frame(left_panel, bg='white')
        left_header.pack(fill='x', padx=10, pady=10)

        tk.Label(left_header, text='Available Songs', font=('Arial', 11, 'bold'),
                 bg='white').pack(side='left')

        # Search controls
        search_controls = tk.Frame(left_panel, bg='white')
        search_controls.pack(fill='x', padx=10, pady=(0, 10))

        tk.Label(search_controls, text='Search:', bg='white').pack(side='left')

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_controls, textvariable=self.search_var, width=25)
        self.search_entry.pack(side='left', padx=(5, 0))

        # Source songs tree
        source_tree_frame = tk.Frame(left_panel, bg='white')
        source_tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        self.source_tree = ttk.Treeview(source_tree_frame,
                                        columns=("Title", "Sub", "SongId", "UniqueId"),
                                        show="headings", selectmode="extended")

        # Source tree scrollbar
        source_vsb = ttk.Scrollbar(source_tree_frame, orient="vertical",
                                   command=self.source_tree.yview)
        source_vsb.pack(side='right', fill='y')

        self.source_tree.configure(yscrollcommand=source_vsb.set)
        self.source_tree.pack(side='left', fill='both', expand=True)

        # Configure source tree headings
        self.source_tree.heading("Title", text="Title")
        self.source_tree.heading("Sub", text="Sub")
        self.source_tree.heading("SongId", text="Song ID")
        self.source_tree.heading("UniqueId", text="Unique ID")

        # Configure column widths
        self.source_tree.column("Title", width=200, minwidth=150)
        self.source_tree.column("Sub", width=150, minwidth=100)
        self.source_tree.column("SongId", width=100, minwidth=80)
        self.source_tree.column("UniqueId", width=100, minwidth=80)

        # Middle panel - Control buttons
        middle_panel = tk.Frame(content_frame, bg='#f0f0f0')
        middle_panel.pack(side='left', fill='y', padx=10)

        # Add some vertical space
        tk.Label(middle_panel, text='', bg='#f0f0f0').pack(pady=50)

        # Add to import queue button
        self.add_btn = ttk.Button(middle_panel, text='➡️ Add to Import',
                                  command=self.add_to_import_queue, state='disabled')
        self.add_btn.pack(pady=5)

        # Remove from import queue button
        self.remove_btn = ttk.Button(middle_panel, text='⬅️ Remove from Import',
                                     command=self.remove_from_import_queue, state='disabled')
        self.remove_btn.pack(pady=5)

        # Right panel - Import queue
        right_panel = ttk.Frame(content_frame, style='SongImporter.TFrame')
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))

        # Right panel header
        right_header = tk.Frame(right_panel, bg='white')
        right_header.pack(fill='x', padx=10, pady=10)

        tk.Label(right_header, text='Import Queue', font=('Arial', 11, 'bold'),
                 bg='white').pack(side='left')

        # Import queue tree
        import_tree_frame = tk.Frame(right_panel, bg='white')
        import_tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        self.import_tree = ttk.Treeview(import_tree_frame,
                                        columns=("Title", "Sub", "SongId", "UniqueId", "Status"),
                                        show="headings", selectmode="extended")

        # Import tree scrollbar
        import_vsb = ttk.Scrollbar(import_tree_frame, orient="vertical",
                                   command=self.import_tree.yview)
        import_vsb.pack(side='right', fill='y')

        self.import_tree.configure(yscrollcommand=import_vsb.set)
        self.import_tree.pack(side='left', fill='both', expand=True)

        # Configure import tree headings
        self.import_tree.heading("Title", text="Title")
        self.import_tree.heading("Sub", text="Sub")
        self.import_tree.heading("SongId", text="Song ID")
        self.import_tree.heading("UniqueId", text="Unique ID (Editable)")
        self.import_tree.heading("Status", text="Status")

        # Configure column widths
        self.import_tree.column("Title", width=200, minwidth=150)
        self.import_tree.column("Sub", width=150, minwidth=100)
        self.import_tree.column("SongId", width=100, minwidth=80)
        self.import_tree.column("UniqueId", width=120, minwidth=100)
        self.import_tree.column("Status", width=140, minwidth=100)

        # Bottom frame
        bottom_frame = tk.Frame(main_frame, bg='#f0f0f0')
        bottom_frame.pack(fill='x', pady=(10, 0))

        # Instructions
        instructions_label = tk.Label(bottom_frame,
                                      text="💡 Double-click Unique ID in import queue to edit",
                                      font=('Arial', 8), fg='#666', bg='#f0f0f0')
        instructions_label.pack(side='left')

        # Import button
        self.import_btn = ttk.Button(bottom_frame, text='📥 Import Songs',
                                     command=self.import_songs, state='disabled')
        self.import_btn.pack(side='right', padx=(5, 0))

        # Cancel button
        cancel_btn = ttk.Button(bottom_frame, text='❌ Cancel',
                                command=self.root.destroy)
        cancel_btn.pack(side='right')

        # Bind events
        self.search_var.trace_add("write", lambda *args: self.perform_search())
        self.source_tree.bind('<Double-1>', lambda e: self.add_to_import_queue())
        self.import_tree.bind('<Double-1>', self.on_import_tree_double_click)

    def load_source_datatable(self):
        """Load source datatable from folder"""
        folder_path = filedialog.askdirectory(initialdir=config.import_datatable_dir,
                                              title="Select Source Datatable Folder",
                                              parent=self.root)
        if not folder_path:
            return

        try:
            # Import the Datatable class (assuming it's available)
            self.source_datatable = Datatable(folder_path)

            # Update UI
            self.status_label.config(text=f'Loaded: {os.path.basename(folder_path)}',
                                     fg='green')
            self.add_btn.config(state='normal')
            self.remove_btn.config(state='normal')
            self.import_btn.config(state='normal')

            # Load songs
            self.perform_search()

            if folder_path != config.import_datatable_dir:
                config.update_import_datatable_dir(folder_path)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load datatable: {str(e)}",
                                 parent=self.root)

    def perform_search(self):
        """Perform search in source songs"""
        if not self.source_datatable:
            return

        self.source_tree.delete(*self.source_tree.get_children())
        query = self.search_var.get().lower()

        try:
            song_list = self.source_datatable.get_song_list(main_genre_only=True)
            lang_idx = self.lang_combo.current()

            # Configure genre colors
            try:
                genre_colors = constants.GENRE_COLOURS
                for genre, color in genre_colors.items():
                    self.source_tree.tag_configure(str(genre), background=color)
            except (ImportError, AttributeError):
                pass

            for genre, songs in enumerate(song_list):
                for song in songs:
                    # Get title and sub for display
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
                        values = (title, sub, song.id, song.uniqueId)
                        self.source_tree.insert("", tk.END, values=values,
                                                tags=(str(genre),))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load songs: {str(e)}",
                                 parent=self.root)

    def add_to_import_queue(self):
        """Add selected songs to import queue with validation"""
        if not self.source_datatable:
            return

        selection = self.source_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select songs to add.",
                                   parent=self.root)
            return

        lang_idx = self.lang_combo.current()
        added_unique_ids = []
        unique_id_to_values = {}

        for item in selection:
            values = self.source_tree.item(item)['values']
            song_id = values[2]
            unique_id = values[3]
            if not any(song['song_id'] == song_id for song in self.import_queue):
                added_unique_ids.append(unique_id)
                unique_id_to_values[unique_id] = song_id

        if not added_unique_ids:
            messagebox.showinfo("No Changes", "Selected songs are already in the import queue.",
                                parent=self.root)
            return

        try:
            songs = self.source_datatable.select_song_list(added_unique_ids)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch song data: {str(e)}",
                                 parent=self.root)
            return

        for song in songs:
            is_uid_taken = self.parent.datatable.is_uid_taken(song.uniqueId)
            is_song_id_taken = self.parent.datatable.is_song_id_taken(song.id)

            song_data = {
                'title_all': song.title,
                'sub_all': song.sub,
                'title': song.title[lang_idx] if lang_idx < len(song.title) else song.title[0],
                'sub': song.sub[lang_idx] if lang_idx < len(song.sub) else song.sub[0],
                'song_id': song.id,
                'original_unique_id': song.uniqueId,
                'new_unique_id': song.uniqueId,
                'is_uid_taken': is_uid_taken,
                'is_song_id_taken': is_song_id_taken,
            }

            self.import_queue.append(song_data)

        self.update_import_queue_display()

    def remove_from_import_queue(self):
        """Remove selected songs from import queue"""
        selection = self.import_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select songs to remove.",
                                   parent=self.root)
            return

        # Get song IDs to remove
        song_ids_to_remove = []
        for item in selection:
            values = self.import_tree.item(item)['values']
            song_id = values[2]  # SongId
            song_ids_to_remove.append(song_id)

        # Remove from queue
        self.import_queue = [song for song in self.import_queue
                             if song['song_id'] not in song_ids_to_remove]

        # Update display
        self.update_import_queue_display()

    def update_import_queue_display(self):
        self.import_tree.delete(*self.import_tree.get_children())
        self.import_tree.tag_configure('uid_conflict', background='#ffcccc')
        self.import_tree.tag_configure('song_id_conflict', background='#ffe0b3')
        self.import_tree.tag_configure('both_conflict', background='#ffb3b3')

        lang_idx = self.lang_combo.current()

        for song in self.import_queue:
            title = song['title_all'][lang_idx] if lang_idx < len(song['title_all']) else song['title_all'][0]
            sub = song['sub_all'][lang_idx] if lang_idx < len(song['sub_all']) else song['sub_all'][0]
            song_id = song['song_id']
            uid = song['new_unique_id']

            # Determine status
            uid_taken = song['is_uid_taken']
            song_id_taken = song['is_song_id_taken']

            if song_id_taken:
                status = "❌ Song ID taken"
                tags = ('song_id_conflict',)
            elif uid_taken:
                status = "❌ Unique ID taken"
                tags = ('uid_conflict',)
            else:
                status = ""
                tags = ()

            values = (title, sub, song_id, uid, status)
            self.import_tree.insert("", tk.END, values=values, tags=tags)

    def on_import_tree_double_click(self, event):
        """Handle double-click on import tree to edit unique ID"""
        item = self.import_tree.identify_row(event.y)
        column = self.import_tree.identify_column(event.x)

        # Only allow editing the UniqueId column (column #4)
        if item and column == '#4':
            self.edit_unique_id(item)

    def edit_unique_id(self, item):
        """Edit unique ID in place"""
        values = self.import_tree.item(item)['values']
        song_id = values[2]
        current_uid = values[3]

        # Find the song in our queue
        song_data = next((song for song in self.import_queue
                          if song['song_id'] == song_id), None)
        if not song_data:
            return

        # Create entry widget for editing
        bbox = self.import_tree.bbox(item, column='#4')
        if not bbox:
            return

        x, y, width, height = bbox

        # Create entry widget
        entry = tk.Entry(self.import_tree, width=width // 8)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, current_uid)
        entry.select_range(0, tk.END)
        entry.focus()

        def save_edit():
            new_uid = entry.get()
            entry.destroy()

            if new_uid != current_uid:
                # Validate new unique ID
                is_taken = self.parent.datatable.is_uid_taken(new_uid)

                # Update song data
                song_data['new_unique_id'] = new_uid
                song_data['is_uid_taken'] = is_taken

                # Update remappings
                if song_data['original_unique_id'] != new_uid:
                    self.unique_id_remappings[song_data['original_unique_id']] = new_uid
                elif song_data['original_unique_id'] in self.unique_id_remappings:
                    del self.unique_id_remappings[song_data['original_unique_id']]

                # Update display
                self.update_import_queue_display()

        def cancel_edit():
            entry.destroy()

        entry.bind('<Return>', lambda e: save_edit())
        entry.bind('<Escape>', lambda e: cancel_edit())
        entry.bind('<FocusOut>', lambda e: save_edit())

    def on_language_change(self, event):
        """Handle language change"""
        self.perform_search()
        self.update_import_queue_display()

    def import_songs(self):
        """Import the songs in the queue"""
        if not self.import_queue:
            messagebox.showwarning("No Songs", "No songs in import queue.",
                                   parent=self.root)
            return

        # Check for UID conflicts
        conflicts = [song for song in self.import_queue if song['is_uid_taken'] or song['is_song_id_taken']]
        if conflicts:
            conflict_count = len(conflicts)
            messagebox.showerror("Song Import Error: UID Conflicts",
                                 f"There are {conflict_count} songs with conflicts.",
                                 parent=self.root)
            return

        try:
            # Prepare data for import
            song_ids_to_import = [song['song_id'] for song in self.import_queue]

            # Call the import function
            self.parent.datatable.import_songs(self.source_datatable,
                                               song_ids_to_import,
                                               self.unique_id_remappings)

            messagebox.showinfo("Success",
                                f"Successfully imported {len(song_ids_to_import)} songs.",
                                parent=self.root)
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import songs: {str(e)}",
                                 parent=self.root)
