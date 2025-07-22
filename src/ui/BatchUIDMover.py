import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from typing import Dict, List, Set, Tuple


class BatchUIDMover:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(parent.window)

        # Window setup
        self.root.title("Batch UID Mover")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Data storage
        self.uid_mappings: List[Dict[str, int]] = []
        self.existing_uids: Set[int] = set()

        # Get existing UIDs from datatable
        self._load_existing_uids()

        # Create GUI
        self._create_widgets()

        # Make window modal
        self.root.transient(parent.window)
        self.root.focus()
        # self.root.grab_set()

        # Center window
        self._center_window()

    def _load_existing_uids(self):
        """Load existing unique IDs from the datatable"""
        try:
            if hasattr(self.parent, 'datatable') and hasattr(self.parent.datatable, 'get_all_unique_ids'):
                self.existing_uids = self.parent.datatable.get_all_unique_ids()
            else:
                messagebox.showwarning("Warning", "Could not load existing UIDs from datatable", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load existing UIDs: {str(e)}", parent=self.root)

    def _center_window(self):
        """Center the window on the parent"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)  # Manual input
        main_frame.rowconfigure(1, weight=0)  # Buttons

        # === Manual Input Section ===
        text_frame = ttk.LabelFrame(main_frame, text="Manual Input (old,new format)", padding="5")
        text_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        # Text widget with scrollbar
        text_container = ttk.Frame(text_frame)
        text_container.grid(row=0, column=0, sticky="nsew")
        text_container.columnconfigure(0, weight=1)
        text_container.rowconfigure(0, weight=1)

        self.text_input = tk.Text(text_container, height=8, wrap="none")
        text_scrollbar = ttk.Scrollbar(text_container, orient="vertical", command=self.text_input.yview)
        self.text_input.configure(yscrollcommand=text_scrollbar.set)

        self.text_input.grid(row=0, column=0, sticky="nsew")
        text_scrollbar.grid(row=0, column=1, sticky="ns")

        self.text_input.insert("1.0", "Enter mappings in format:\n1244,1\n1120,59\n...")
        self.text_input.bind("<FocusIn>", self._clear_placeholder)

        # === Buttons Section ===
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        button_frame.columnconfigure(0, weight=1)

        process_btn = ttk.Button(button_frame, text="Process Mappings", command=self._process_mappings)
        process_btn.pack(side=tk.LEFT, padx=(0, 5))

        load_json_btn = ttk.Button(button_frame, text="Load JSON", command=self._browse_and_load_json)
        load_json_btn.pack(side=tk.LEFT, padx=(0, 5))

        clear_btn = ttk.Button(button_frame, text="Clear All", command=self._clear_all)
        clear_btn.pack(side=tk.LEFT, padx=(0, 5))

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.root.destroy)
        cancel_btn.pack(side=tk.RIGHT)

    def _browse_and_load_json(self):
        """Browse and load JSON file"""
        filename = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            parent=self.root
        )

        if not filename:
            return

        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            if 'Items' not in data:
                messagebox.showerror("Error", "JSON file must contain 'Items' array", parent=self.root)
                return

            mappings = []
            for item in data['Items']:
                if 'oldUniqueId' in item and 'newUniqueId' in item:
                    try:
                        old_id = int(item['oldUniqueId'])
                        new_id = int(item['newUniqueId'])
                        mappings.append({'old': old_id, 'new': new_id})
                    except (ValueError, TypeError):
                        continue

            if not mappings:
                messagebox.showwarning("Warning", "No valid UID mappings found in JSON file", parent=self.root)
                return

            text_content = "\n".join([f"{m['old']},{m['new']}" for m in mappings])
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", text_content)

            messagebox.showinfo("Success", f"Loaded {len(mappings)} mappings from JSON", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file: {str(e)}", parent=self.root)

    def _clear_placeholder(self, event):
        current_text = self.text_input.get("1.0", tk.END).strip()
        if current_text.startswith("Enter mappings in format:"):
            self.text_input.delete("1.0", tk.END)

    def _clear_all(self):
        """Clear all input fields"""
        result = messagebox.askyesno("Confirm Clear",
                                     f"Are you sure you want to clear mappings?",
                                     parent=self.root)
        if result:
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", "Enter mappings in format:\n1244,1\n1120,59\n...")

    def _process_mappings(self):
        """Process the UID mappings and show preview window"""
        # Parse text input
        text_content = self.text_input.get("1.0", tk.END).strip()
        if not text_content or text_content.startswith("Enter mappings in format:"):
            messagebox.showwarning("Warning", "Please enter some UID mappings", parent=self.root)
            return

        mappings = []
        lines = text_content.split('\n')

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            try:
                parts = line.split(',')
                if len(parts) != 2:
                    raise ValueError(f"Line {line_num}: Expected format 'old,new'")

                old_id = int(parts[0].strip())
                new_id = int(parts[1].strip())
                mappings.append({'old': old_id, 'new': new_id})

            except ValueError as e:
                messagebox.showerror("Error", f"Invalid format on line {line_num}: {line}\n{str(e)}", parent=self.root)
                return

        if not mappings:
            messagebox.showwarning("Warning", "No valid mappings found", parent=self.root)
            return

        # Open preview window
        self._open_preview_window(mappings)

    def _open_preview_window(self, mappings: List[Dict[str, int]]):
        """Open preview window with collision detection"""

        # Freeze this window
        # self._set_widgets_state('disabled')
        self.root.attributes('-disabled', True)

        preview_window = UIDPreviewWindow(self, mappings, self.existing_uids)

        # Use wait_window to pause until preview closes
        preview_window.root.wait_window()

        # Re-enable this window
        # self._set_widgets_state('normal')
        self.root.attributes('-disabled', False)

        if preview_window.cancelled:
            self.root.focus()
            return

        if hasattr(preview_window, 'approved_mappings') and preview_window.approved_mappings:
            self._execute_uid_updates(preview_window.approved_mappings)

            # Re-populate text input with skipped mappings
        if hasattr(preview_window, 'skipped_mappings') and preview_window.skipped_mappings:
            lines = [f"{m['old']},{m['new']}" for m in preview_window.skipped_mappings]
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", "\n".join(lines))
        else:
            self.root.destroy()

    def _execute_uid_updates(self, mappings: List[Dict[str, int]]):
        """Execute the UID updates using datatable.update_uid with a two-phase renaming to avoid collisions."""
        success_count = 0
        error_count = 0
        errors = []

        # 1) Compute an offset larger than any existing or target UID
        all_ids = set(self.existing_uids)
        for m in mappings:
            all_ids.add(m['old'])
            all_ids.add(m['new'])
        offset = max(all_ids) + 1

        # 2) Phase 1: rename old_id → (new_id + offset)
        for m in mappings:
            old_id = m['old']
            temp_id = m['new'] + offset
            try:
                if hasattr(self.parent, 'datatable') and hasattr(self.parent.datatable, 'update_uid'):
                    self.parent.datatable.update_uid(old_id, temp_id)
                    success_count += 1
                else:
                    raise AttributeError("datatable.update_uid method not found")
            except Exception as e:
                error_count += 1
                errors.append(f"Phase 1: {old_id} → {temp_id}: {e}")

        # 3) Phase 2: rename (new_id + offset) → new_id
        for m in mappings:
            temp_id = m['new'] + offset
            new_id = m['new']
            try:
                if hasattr(self.parent, 'datatable') and hasattr(self.parent.datatable, 'update_uid'):
                    self.parent.datatable.update_uid(temp_id, new_id)
                    success_count += 1
                else:
                    raise AttributeError("datatable.update_uid method not found")
            except Exception as e:
                error_count += 1
                errors.append(f"Phase 2: {temp_id} → {new_id}: {e}")

        # 4) Report results
        if success_count:
            messagebox.showinfo(
                "Update Complete",
                f"Successfully executed {success_count} UID operations",
                parent=self.root
            )

        if error_count:
            msg = f"Failed {error_count} operations:\n\n" + "\n".join(errors[:10])
            if len(errors) > 10:
                msg += f"\n...and {len(errors) - 10} more errors"
            messagebox.showerror("Update Errors", msg, parent=self.root)

    # def _set_widgets_state(self, state: str):
    #     """Enable or disable all child widgets"""
    #     for child in self.root.winfo_children():
    #         try:
    #             child.configure(state=state)
    #         except tk.TclError:
    #             pass  # Some widgets like frames or labels may not support 'state'


class UIDPreviewWindow:
    def __init__(self, parent, mappings: List[Dict[str, int]], existing_uids: Set[int]):
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.mappings = mappings
        self.existing_uids = existing_uids
        self.approved_mappings = None
        self.cancelled = True

        # Window setup
        self.root.title("Preview UID Mappings")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        # Make modal
        self.root.transient(parent.root)
        self.root.focus()

        # Analyze collisions
        self.collision_info = self._analyze_collisions()

        self.unique_ids_not_found = set()

        # Create GUI
        self._create_widgets()

        # Center window
        self._center_window()

    def _center_window(self):
        """Center the window on the parent"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")

    def _analyze_collisions(self) -> Dict[str, List[int]]:
        """Analyze collision types in the mappings"""
        new_ids = [m['new'] for m in self.mappings]
        new_id_counts = {}

        # Count occurrences of each new ID
        for new_id in new_ids:
            new_id_counts[new_id] = new_id_counts.get(new_id, 0) + 1

        # Find duplicates within mappings (red)
        internal_collisions = [new_id for new_id, count in new_id_counts.items() if count > 1]

        # Find collisions with existing UIDs (yellow), excluding those that will be replaced
        old_ids = {m['old'] for m in self.mappings}
        external_collisions = [
            new_id for new_id in new_ids
            if new_id in self.existing_uids and new_id not in old_ids
        ]

        return {
            'internal': internal_collisions,
            'external': external_collisions
        }

    def _create_widgets(self):
        """Create preview window widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Info label
        info_text = f"Preview {len(self.mappings)} UID mappings"
        if self.collision_info['internal'] or self.collision_info['external']:
            info_text += " (Collisions detected!)"

        info_label = ttk.Label(main_frame, text=info_text)
        info_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Treeview with scrollbars
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Create treeview
        self.tree = ttk.Treeview(tree_frame, columns=('old', 'song_id', 'new', 'collides_with', 'status'),
                                 show='headings')
        self.tree.heading('old', text='Old UID')
        self.tree.heading('song_id', text='Song ID')
        self.tree.heading('new', text='New UID')
        self.tree.heading('collides_with', text='Collides With')
        self.tree.heading('status', text='Status')

        # Configure column widths
        self.tree.column('old', width=50)
        self.tree.column('song_id', width=50)
        self.tree.column('new', width=50)
        self.tree.column('collides_with', width=50)
        self.tree.column('status', width=200)

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Populate tree
        self._populate_tree()

        # Enable editing
        self.tree.bind('<Double-1>', self._handle_double_click)

        # Legend
        legend_frame = ttk.LabelFrame(main_frame, text="Legend", padding="5")
        legend_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(legend_frame, text="• Red: Duplicate new UIDs in this batch").pack(anchor=tk.W)
        ttk.Label(legend_frame, text="• Yellow: New UID already exists in datatable").pack(anchor=tk.W)
        ttk.Label(legend_frame, text="• White: No conflicts").pack(anchor=tk.W)
        ttk.Label(legend_frame, text="• Double-click New UID to edit").pack(anchor=tk.W)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=(10, 0))

        ok_btn = ttk.Button(button_frame, text="Apply Changes", command=self._apply_changes)
        ok_btn.pack(side=tk.LEFT, padx=(0, 5))

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.root.destroy)
        cancel_btn.pack(side=tk.RIGHT)

    def _populate_tree(self):
        """Populate the treeview with mappings and collision info"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add mappings
        for mapping in self.mappings:
            old_id = mapping['old']
            new_id = mapping['new']

            # Get song ID from old UID
            try:
                song_id = self.parent.parent.datatable.get_songid_from_unique_id(old_id)
            except Exception:
                song_id = ''

            # Determine status and color
            if song_id == '':
                status = f"WARNING: No song with unique id {old_id}"
                self.unique_ids_not_found.add(old_id)
                tags = ('red',)
            elif new_id in self.collision_info['internal']:
                status = "COLLISION: Duplicate in batch"
                tags = ('red',)
            elif new_id in self.collision_info['external']:
                status = "WARNING: Already exists in DB"
                tags = ('yellow',)
            else:
                status = "OK"
                tags = ('white',)

            # Get song ID from new UID if it collides
            collides_with = ''
            if new_id in self.collision_info['external']:
                try:
                    collides_with = str(self.parent.parent.datatable.get_songid_from_unique_id(new_id))
                except Exception:
                    collides_with = 'Error'

            self.tree.insert(
                '', 'end',
                values=(old_id, song_id, new_id, collides_with, status),
                tags=tags
            )

        # Configure tags
        self.tree.tag_configure('red', background='#ffcccc')
        self.tree.tag_configure('yellow', background='#ffffcc')
        self.tree.tag_configure('white', background='white')

    def _handle_double_click(self, event):
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)

        # Only allow editing the 'new' column
        if column == '#3':  # New UID column
            self._edit_new_uid(item)

        # Double-click on 'Song ID' column to copy
        elif column in ('#1', '#2'):  # Song ID column
            song_id = self.tree.item(item, 'values')[1]
            if song_id:
                old_songid = self.parent.parent.current_songid
                self.parent.parent.load_song(old_songid, song_id)
                self.parent.parent.songid_entry.delete(0, tk.END)
                self.parent.parent.songid_entry.insert(0, song_id)
        elif column == '#4':
            song_id = self.tree.item(item, 'values')[3]
            if song_id:
                old_songid = self.parent.parent.current_songid
                self.parent.parent.load_song(old_songid, song_id)
                self.parent.parent.songid_entry.delete(0, tk.END)
                self.parent.parent.songid_entry.insert(0, song_id)


    def _edit_new_uid(self, item):
        """Edit the new UID value"""
        current_values = self.tree.item(item, 'values')
        current_new_id = current_values[2]

        # Create entry dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit New UID")
        dialog.geometry("300x120")
        dialog.transient(self.root)
        # dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        # Widgets
        ttk.Label(dialog, text="New UID:").pack(pady=5)

        entry_var = tk.StringVar(value=current_new_id)
        entry = ttk.Entry(dialog, textvariable=entry_var, width=20)
        entry.pack(pady=5)
        entry.select_range(0, tk.END)
        entry.focus()

        def save_edit():
            try:
                new_value = int(entry_var.get())
                # Update mapping
                old_id = int(current_values[0])
                for mapping in self.mappings:
                    if mapping['old'] == old_id:
                        mapping['new'] = new_value
                        break

                # Re-analyze collisions and refresh tree
                self.collision_info = self._analyze_collisions()
                self._populate_tree()
                dialog.destroy()

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer", parent=dialog)

        def cancel_edit():
            dialog.destroy()

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Save", command=save_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel_edit).pack(side=tk.LEFT, padx=5)

        # Bind Enter key to save
        entry.bind('<Return>', lambda e: save_edit())

    def _apply_changes(self):
        """Apply only the safe UID changes"""
        self.approved_mappings = []
        self.skipped_mappings = []

        for mapping in self.mappings:
            new_id = mapping['new']
            if new_id in self.collision_info['internal'] or new_id in self.collision_info['external'] or mapping['old'] in self.unique_ids_not_found:
                self.skipped_mappings.append(mapping)
            else:
                self.approved_mappings.append(mapping)

        if not self.approved_mappings:
            messagebox.showwarning("No Valid Mappings", "No valid UID mappings to apply.", parent=self.root)
            return

        # Close the preview window; let the parent process approved ones
        self.cancelled = False
        self.root.destroy()

