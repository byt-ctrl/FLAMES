import re
import uuid
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class FlamesGame :

    """a tkinter-based FLAMES game with customizable categories and history tracking."""

    def __init__(self,root) :

        """initialize the game with root window and default settings."""
        self.root = root
        self.root.title("FLAMES Game")
        self.root.state('zoomed')  # for proper view
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(True,True)

        # game state
        self.history=[]
        self.stats={"Friends":0, "Lovers":0, "Affectionate":0,
                      "Marriage":0,"Enemy":0, "Sibling":0}
        self.custom_flames=self.stats.copy()
        self.theme="light"

        # color schemes for light and dark themes
        self.colors={
            "light": {"bg":"#f0f4f8","frame_bg":"#ffffff","text": "#2c3e50",
                      "button_bg":"#3498db","button_fg":"white",
                      "button_active":"#2980b9","error":"#e74c3c"},
            "dark": {"bg":"#2c3e50","frame_bg":"#34495e","text":"#ecf0f1",
                     "button_bg":"#e74c3c","button_fg":"white",
                     "button_active":"#c0392b","error":"#ff7675"}
        }

        self.setup_gui()
        self.setup_keyboard_shortcuts()

    def setup_gui(self) :

        """configure the main GUI layout and widgets."""
        # main frame
        self.main_frame=tk.Frame(self.root,bg=self.colors[self.theme]["bg"])
        self.main_frame.pack(expand=True,fill="both",padx=20,pady=20)

        # title
        self.title_label=tk.Label(self.main_frame,text="FLAMES Game",font=("Helvetica",24,"bold"), # GUI
                                    bg=self.colors[self.theme]["bg"],fg=self.colors[self.theme]["text"])
        self.title_label.pack(pady=10)

        # settings frame
        self.settings_frame=tk.Frame(self.main_frame,bg=self.colors[self.theme]["bg"]) # GUI
        self.settings_frame.pack(anchor="ne")
        tk.Button(self.settings_frame,text="Toggle Theme",font=("Arial",10),
                  bg=self.colors[self.theme]["button_bg"],fg=self.colors[self.theme]["button_fg"],
                  command=self.toggle_theme,relief="flat").pack(side="left",padx=5)
        tk.Button(self.settings_frame,text="Customize FLAMES",font=("Arial",10),
                  bg=self.colors[self.theme]["button_bg"], fg=self.colors[self.theme]["button_fg"],
                  command=self.open_flames_customizer,relief="flat").pack(side="left",padx=5)

        # input frame
        self.input_frame=tk.Frame(self.main_frame, bg=self.colors[self.theme]["frame_bg"],
                                    bd=2, relief="groove")
        self.input_frame.pack(pady=10, padx=10, fill="x")

        # name inputs
        tk.Label(self.input_frame,text="Your Name :",font=("Arial",12),
                 bg=self.colors[self.theme]["frame_bg"],fg=self.colors[self.theme]["text"]).grid(
                     row=0,column=0,padx=10,pady=5,sticky="e")
        self.name1_entry=tk.Entry(self.input_frame,font=("Arial",12),width=20)
        self.name1_entry.grid(row=0,column=1,padx=10,pady=5)
        self.name1_error=tk.Label(self.input_frame,text="",font=("Arial",10),
                                    bg=self.colors[self.theme]["frame_bg"],
                                    fg=self.colors[self.theme]["error"])
        self.name1_error.grid(row=0,column=2,padx=5)

        tk.Label(self.input_frame,text="Partner's Name : ",font=("Arial",12),
                 bg=self.colors[self.theme]["frame_bg"],fg=self.colors[self.theme]["text"]).grid(
                     row=1,column=0,padx=10,pady=5,sticky="e")
        self.name2_entry=tk.Entry(self.input_frame,font=("Arial",12),width=20)
        self.name2_entry.grid(row=1,column=1,padx=10,pady=5)
        self.name2_error=tk.Label(self.input_frame,text="",font=("Arial",10),
                                    bg=self.colors[self.theme]["frame_bg"],
                                    fg=self.colors[self.theme]["error"])
        self.name2_error.grid(row=1,column=2,padx=5)

        # real-time validation
        self.name1_entry.bind("<KeyRelease>",self.validate_inputs_real_time)
        self.name2_entry.bind("<KeyRelease>",self.validate_inputs_real_time)

        # button frame
        self.button_frame=tk.Frame(self.main_frame,bg=self.colors[self.theme]["bg"])
        self.button_frame.pack(pady=10)
        tk.Button(self.button_frame,text="Calculate (Enter)",font=("Arial",12,"bold"),
                  bg=self.colors[self.theme]["button_bg"], fg=self.colors[self.theme]["button_fg"],
                  command=self.calculate_flames,relief="flat",
                  activebackground=self.colors[self.theme]["button_active"]).pack(side="left",padx=5)
        tk.Button(self.button_frame, text="Clear (Ctrl+C)", font=("Arial", 12,"bold"),
                  bg=self.colors[self.theme]["button_bg"],fg=self.colors[self.theme]["button_fg"],
                  command=self.clear_inputs,relief="flat",
                  activebackground=self.colors[self.theme]["button_active"]).pack(side="left",padx=5)
        tk.Button(self.button_frame, text="Export History", font=("Arial", 12, "bold"),
                  bg=self.colors[self.theme]["button_bg"], fg=self.colors[self.theme]["button_fg"],
                  command=self.export_history, relief="flat",
                  activebackground=self.colors[self.theme]["button_active"]).pack(side="left",padx=5)
        tk.Button(self.button_frame,text="Load History",font=("Arial",12,"bold"),
                  bg=self.colors[self.theme]["button_bg"],fg=self.colors[self.theme]["button_fg"],
                  command=self.load_history,relief="flat",
                  activebackground=self.colors[self.theme]["button_active"]).pack(side="left",padx=5)

        # result frame
        self.result_frame=tk.Frame(self.main_frame,bg=self.colors[self.theme]["frame_bg"],
                                     bd=2,relief="groove")
        self.result_frame.pack(pady=10,padx=10,fill="x")
        self.result_label = tk.Label(self.result_frame,text="Result will appear here",
                                     font=("Arial",14),bg=self.colors[self.theme]["frame_bg"],
                                     fg=self.colors[self.theme]["text"])
        self.result_label.pack(pady=10)

        # statistics frame
        self.stats_frame=tk.Frame(self.main_frame, bg=self.colors[self.theme]["frame_bg"],
                                    bd=2,relief="groove")
        self.stats_frame.pack(pady=10,padx=10,fill="x")
        self.stats_label=tk.Label(self.stats_frame,text="Games Played: 0\nMost Common : None",
                                    font=("Arial",10),bg=self.colors[self.theme]["frame_bg"],
                                    fg=self.colors[self.theme]["text"])
        self.stats_label.pack(pady=5)

        # history frame
        self.history_frame=tk.Frame(self.main_frame,bg=self.colors[self.theme]["frame_bg"],
                                      bd=2,relief="groove")
        self.history_frame.pack(pady=10,padx=10,fill="both",expand=True)
        tk.Label(self.history_frame,text="History",font=("Arial",12,"bold"),
                 bg=self.colors[self.theme]["frame_bg"],fg=self.colors[self.theme]["text"]).pack(
                     anchor="w",padx=10,pady=5)

        # scrollable history
        self.history_canvas=tk.Canvas(self.history_frame,bg=self.colors[self.theme]["frame_bg"],
                                        highlightthickness=0)
        self.history_scrollbar=tk.Scrollbar(self.history_frame,orient="vertical",
                                              command=self.history_canvas.yview)
        self.history_inner_frame=tk.Frame(self.history_canvas,
                                            bg=self.colors[self.theme]["frame_bg"])

        self.history_inner_frame.bind(
            "<Configure>",
            lambda e : self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all"))
        )

        self.history_canvas.create_window((0,0),window=self.history_inner_frame,anchor="nw")
        self.history_canvas.configure(yscrollcommand=self.history_scrollbar.set)
        self.history_canvas.pack(side="left",fill="both",expand=True)
        self.history_scrollbar.pack(side="right",fill="y")

        # window resize handling
        self.root.bind("<Configure>",self.on_resize)

    def setup_keyboard_shortcuts(self) :

        """bind keyboard shortcuts for common actions."""
        self.root.bind('<Return>',lambda event: self.calculate_flames())
        self.root.bind('<Control-c>',lambda event: self.clear_inputs())
        self.root.bind('<Control-t>',lambda event: self.toggle_theme())

    def on_resize(self,event) :
        """update scroll region on window resize."""
        self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all"))

    def toggle_theme(self) :
        """switch between light and dark themes and update all widgets."""
        self.theme="dark" if self.theme=="light" else "light"
        self.update_theme()

    def update_theme(self) :
        """apply current theme colors to all widgets recursively."""
        # update root and main containers
        self.root.configure(bg=self.colors[self.theme]["bg"])
        for frame in [self.main_frame,self.settings_frame,self.input_frame,self.button_frame,
                      self.result_frame,self.stats_frame,self.history_frame,self.history_inner_frame] :
            frame.configure(bg=self.colors[self.theme]["bg" if frame==self.main_frame else "frame_bg"])
        self.history_canvas.configure(bg=self.colors[self.theme]["frame_bg"])

        # recursively update all widgets
        def update_widget_colors(widget) :
            if isinstance(widget, tk.Label) :
                widget.configure(
                    bg=self.colors[self.theme]["frame_bg" if widget.master in [self.input_frame,self.result_frame,
                                                                               self.stats_frame,self.history_frame,
                                                                               self.history_inner_frame] else "bg"],
                    fg=self.colors[self.theme]["text" if widget!=self.name1_error and widget!=self.name2_error else "error"]
                )
            elif isinstance(widget,tk.Button) :
                widget.configure(
                    bg=self.colors[self.theme]["button_bg"],
                    fg=self.colors[self.theme]["button_fg"],
                    activebackground=self.colors[self.theme]["button_active"]
                )
            elif isinstance(widget,tk.Frame) :
                widget.configure(
                    bg=self.colors[self.theme]["frame_bg" if widget in [self.input_frame,self.result_frame,
                                                                        self.stats_frame,self.history_frame,
                                                                        self.history_inner_frame] else "bg"]
                )
            elif isinstance(widget,tk.Canvas) :
                widget.configure(bg=self.colors[self.theme]["frame_bg"])
            # recurse through children
            for child in widget.winfo_children() :
                update_widget_colors(child)

        update_widget_colors(self.main_frame)

    def open_flames_customizer(self) :
        """open a window to customize FLAMES categories."""
        window=tk.Toplevel(self.root)
        window.title("Customize FLAMES")
        window.geometry("400x400")
        window.configure(bg=self.colors[self.theme]["bg"])

        tk.Label(window,text="Customize FLAMES Categories",font=("Arial",14,"bold"),
                 bg=self.colors[self.theme]["bg"],fg=self.colors[self.theme]["text"]).pack(pady=10)

        entries={}
        for a,category in enumerate(self.custom_flames) :
            frame=tk.Frame(window, bg=self.colors[self.theme]["bg"])
            frame.pack(fill="x",padx=10,pady=5)
            tk.Label(frame,text=f"Category {a+1} :",font=("Arial",10),
                     bg=self.colors[self.theme]["bg"],fg=self.colors[self.theme]["text"]).pack(side="left")
            entry=tk.Entry(frame,font=("Arial",10))
            entry.insert(0,category)
            entry.pack(side="left",padx=5)
            entries[category]=entry

        def save_categories() : 
            new_categories={}
            for old_category , entry in entries.items() :
                new_category=entry.get().strip()
                if not new_category :
                    messagebox.showerror("Error","Categories cannot be empty.",parent=window)
                    return
                if not re.match(r"^[a-zA-Z\s]+$",new_category) :
                    messagebox.showerror("Error","Categories must contain only alphabets and spaces.",parent=window)
                    return
                new_categories[new_category]=self.stats[old_category]

            if len(set(new_categories.keys())) != len(new_categories) :
                messagebox.showerror("Error","Categories must be unique.",parent=window)
                return

            self.stats=new_categories
            self.custom_flames=self.stats.copy()
            messagebox.showinfo("Success","Categories updated successfully.",parent=window)
            window.destroy()

        tk.Button(window,text="Save",font=("Arial",10,"bold"),
                  bg=self.colors[self.theme]["button_bg"],fg=self.colors[self.theme]["button_fg"],
                  command=save_categories,relief="flat").pack(pady=10)

    def validate_inputs_real_time(self,event=None) :
        """provide real-time feedback for input validation."""
        name1=self.name1_entry.get().strip()
        name2=self.name2_entry.get().strip()

        self.name1_error.configure(text="")
        self.name2_error.configure(text="")

        if name1 and not re.match(r"^[a-zA-Z\s]+$",name1):
            self.name1_error.configure(text="Alphabets only")
        if name2 and not re.match(r"^[a-zA-Z\s]+$",name2):
            self.name2_error.configure(text="Alphabets only")
        if name1 and name2 and name1.lower()==name2.lower() :
            self.name1_error.configure(text="Names cannot be same")
            self.name2_error.configure(text="Names cannot be same")

    def validate_input(self,name1,name2) :
        """validate inputs before calculation."""
        if not name1 or not name2 :
            messagebox.showerror("Error","Both names are required.")
            return False
        if name1.lower()==name2.lower() :
            messagebox.showerror("Error","Names cannot be the same.")
            return False
        if not re.match(r"^[a-zA-Z\s]+$",name1) or not re.match(r"^[a-zA-Z\s]+$",name2) :
            messagebox.showerror("Error","Names must contain only alphabets and spaces.")
            return False
        return True


    def remove_common_chars(self,list1,list2) : 
        """remove common characters from two lists."""
        list1,list2=list1.copy(),list2.copy()
        for char in set(list1) & set(list2) :
            while char in list1 and char in list2 :
                list1.remove(char)
                list2.remove(char)
        return list1,list2

    def calculate_flames(self) :
        """calculate and display the FLAMES result."""
        name1=self.name1_entry.get().strip().lower()
        name2=self.name2_entry.get().strip().lower()

        if not self.validate_input(name1,name2) :
            return

        # prepare name lists
        name1_list=list(name1.replace(" ", ""))
        name2_list=list(name2.replace(" ", ""))

        # remove common characters
        name1_list,name2_list=self.remove_common_chars(name1_list,name2_list)
        count=len(name1_list)+len(name2_list)

        # FLAMES calculation
        flames=list(self.custom_flames.keys())
        while len(flames)>1 :
            split_index=(count % len(flames))-1
            flames=flames[split_index + 1:]+flames[:split_index] if split_index >= 0 else flames[:-1]

        result=flames[0]

        # update history
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry=f"[{timestamp}] {name1.capitalize()} & {name2.capitalize()} : {result}"
        self.history.append(history_entry)
        tk.Label(self.history_inner_frame, text=history_entry, font=("Arial", 10),
                 bg=self.colors[self.theme]["frame_bg"], fg=self.colors[self.theme]["text"]).pack(
                     anchor="w", padx=10, pady=2)

        # update stats
        self.stats[result]+=1
        total_games=sum(self.stats.values())
        most_common=max(self.stats, key=self.stats.get) if total_games > 0 else "None"
        self.stats_label.configure(text=f"Games Played: {total_games}\nMost Common: {most_common}")

        # sisplay result
        self.animate_result(result)

    def animate_result(self,result) :

        """animate the result display with fade and scale effects."""
        colors=["#3498db","#e74c3c","#2ecc71","#f1c40f","#9b59b6"]

        def animate(alpha=0.0 , color_index=0 , scale=1.0 , growing=True) :
            alpha=min(alpha + 0.05, 1.0)
            scale=scale + 0.1 if growing else scale - 0.1
            growing=False if scale >= 1.5 else True if scale <= 1.0 else growing
            self.result_label.configure(
                text=f"Relationship : {result}",
                fg=colors[color_index % len(colors)],
                font=("Arial",int(14 * scale))
            )
            if alpha<1.0 :
                self.root.after(50,animate,alpha,color_index+1,scale,growing)

        animate()

    def clear_inputs(self) :

        """reset's input fields and result display."""
        self.name1_entry.delete(0,tk.END)
        self.name2_entry.delete(0,tk.END)
        self.name1_error.configure(text="")
        self.name2_error.configure(text="")
        self.result_label.configure(text="Result will appear here", fg=self.colors[self.theme]["text"],
                                    font=("Arial",14))
        self.name1_entry.focus_set()

    def export_history(self) :
        """save history to a text file."""
        if not self.history :
            messagebox.showinfo("Info","No history to export.")
            return
        try :
            filename=f"flames_history_{uuid.uuid4()}.txt"
            with open(filename,"w", encoding="utf-8") as f :
                f.write("\n".join(self.history))
            messagebox.showinfo("Success",f"History exported to {filename}.")
        except Exception as e:
            messagebox.showerror("Error",f"Failed to export history : {e}")

    def load_history(self) :
        """load history from a text file."""
        try :
            filename=filedialog.askopenfilename(filetypes=[("Text files" , "*.txt")])
            if not filename :
                return
            with open(filename,"r",encoding="utf-8") as f :
                loaded_history=[line.strip() for line in f if line.strip()]
            self.history.extend(loaded_history)
            for entry in loaded_history :
                tk.Label(self.history_inner_frame,text=entry,font=("Arial",10),
                         bg=self.colors[self.theme]["frame_bg"],fg=self.colors[self.theme]["text"]).pack(
                             anchor="w",padx=10,pady=2)
            messagebox.showinfo("Success","History loaded successfully.")
        except Exception : 
            messagebox.showerror("Error","Failed to load history.")

if __name__=="__main__" : 
        root=tk.Tk()
        app=FlamesGame(root)
        root.mainloop()


# END :)