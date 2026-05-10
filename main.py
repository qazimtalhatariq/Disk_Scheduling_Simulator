import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

class DiskSimulator:
    # Dark Modern Color Palette
    COLORS = {'bg': '#1e1e2e', 'fg': '#ffffff', 'accent': '#6366f1', 'btn': '#a855f7', 'hover': '#d946ef', 'dark': '#2a2a3e', 'text': '#b0b0b0'}
    ALGOS = {'FCFS': '#6366f1', 'SSTF': '#a855f7', 'SCAN': '#ec4899', 'C-SCAN': '#10b981'}
    
    def __init__(self, root):
        self.root = root
        self.is_fullscreen = False
        self.root.title("Disk Scheduling Simulator")
        self.root.geometry("680x800")
        self.root.minsize(500, 600)
        self.root.configure(bg=self.COLORS['bg'])
        
        # Configure TTK Theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground=self.COLORS['dark'], background=self.COLORS['dark'], foreground=self.COLORS['fg'])
        style.map('TCombobox', fieldbackground=[('readonly', self.COLORS['dark'])], foreground=[('readonly', self.COLORS['fg'])])
        
        # Bind resize event for responsive design
        self.root.bind('<Configure>', self._on_resize)
        
        # Main container
        self.container = tk.Frame(self.root, bg=self.COLORS['bg'])
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Title Section
        title_frame = tk.Frame(self.container, bg=self.COLORS['accent'], height=70)
        title_frame.pack(fill=tk.X)
        
        title_inner = tk.Frame(title_frame, bg=self.COLORS['accent'])
        title_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        
        title_top = tk.Frame(title_inner, bg=self.COLORS['accent'])
        title_top.pack(fill=tk.X)
        
        tk.Label(title_top, text="🚀 Disk Scheduling Simulator", font=("Helvetica", 22, "bold"), bg=self.COLORS['accent'], fg=self.COLORS['fg']).pack(side=tk.LEFT, pady=5)
        
        self.fs_btn = tk.Button(title_top, text="⛶", command=self._toggle_fullscreen, bg=self.COLORS['accent'], fg=self.COLORS['fg'], font=("Helvetica", 16), relief=tk.FLAT, bd=0, cursor="hand2", width=3, height=1)
        self.fs_btn.pack(side=tk.RIGHT, padx=5)
        
        # Main Frame with scrollbar for small screens
        main_frame = tk.Frame(self.container, bg=self.COLORS['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        
        # Input Frame
        inp = tk.LabelFrame(main_frame, text="📊 Configuration", bg=self.COLORS['bg'], fg=self.COLORS['fg'], font=("Helvetica", 12, "bold"), relief=tk.FLAT, borderwidth=1)
        inp.pack(fill=tk.X, pady=8)
        
        self._create_input("Disk Requests:", "98, 183, 37, 122, 14, 124, 65, 67", inp, 'req')
        self._create_input("Head Position:", "53", inp, 'head')
        
        tk.Label(inp, text="Algorithm:", bg=self.COLORS['bg'], fg=self.COLORS['text'], font=("Helvetica", 11)).pack(anchor=tk.W, padx=12, pady=(8, 3))
        self.algo = tk.StringVar(value="FCFS")
        ttk.Combobox(inp, textvariable=self.algo, values=list(self.ALGOS.keys()), state="readonly", font=("Helvetica", 11), width=40).pack(padx=12, pady=5, ipady=4, fill=tk.X)
        
        # Info Frame
        info = tk.LabelFrame(main_frame, text="ℹ️ Algorithms", bg=self.COLORS['bg'], fg=self.COLORS['fg'], font=("Helvetica", 12, "bold"), relief=tk.FLAT, borderwidth=1)
        info.pack(fill=tk.X, pady=8)
        tk.Label(info, text="FCFS: First Come First Served\nSSTF: Shortest Seek Time First\nSCAN: Elevator Algorithm\nC-SCAN: Circular SCAN (jumps to opposite end)", 
                bg=self.COLORS['bg'], fg='#9090a0', font=("Helvetica", 10), justify=tk.LEFT).pack(anchor=tk.W, padx=12, pady=8)
        
        # Button Frame
        btn_frame = tk.Frame(main_frame, bg=self.COLORS['bg'])
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.sim_btn = tk.Button(btn_frame, text="▶ Simulate", command=self.simulate, bg=self.COLORS['btn'], fg=self.COLORS['fg'], font=("Helvetica", 13, "bold"), relief=tk.FLAT, cursor="hand2", pady=10)
        self.sim_btn.pack(fill=tk.X, ipady=3)
        self.sim_btn.bind("<Enter>", lambda e: self.sim_btn.config(bg=self.COLORS['hover']))
        self.sim_btn.bind("<Leave>", lambda e: self.sim_btn.config(bg=self.COLORS['btn']))
        
        # Keyboard shortcuts
        self.root.bind('<F11>', lambda e: self._toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self._exit_fullscreen())
        self.root.bind('<Return>', lambda e: self.simulate())
    
    def _toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        self.fs_btn.config(text="⛶" if not self.is_fullscreen else "⛶ ⌛")
    
    def _exit_fullscreen(self):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes('-fullscreen', False)
            self.fs_btn.config(text="⛶")
    
    def _on_resize(self, event=None):
        """Responsive design based on window size"""
        width = self.root.winfo_width()
        if width < 600:
            title_font = ("Helvetica", 18, "bold")
        else:
            title_font = ("Helvetica", 22, "bold")
    
    def _create_input(self, label, default, parent, attr):
        tk.Label(parent, text=label, bg=self.COLORS['bg'], fg=self.COLORS['text'], font=("Helvetica", 11)).pack(anchor=tk.W, padx=12, pady=(8, 2))
        entry = tk.Entry(parent, font=("Helvetica", 11), bg=self.COLORS['dark'], fg=self.COLORS['fg'], insertbackground=self.COLORS['accent'], relief=tk.FLAT, bd=1)
        entry.insert(0, default)
        entry.pack(padx=12, pady=4, ipady=6, fill=tk.X)
        setattr(self, f'{attr}_entry', entry)

    
    def fcfs(self, reqs, head):
        path = [head] + reqs
        return path, sum(abs(path[i] - path[i+1]) for i in range(len(path)-1))
    
    def sstf(self, reqs, head):
        path, current, dist = [head], head, 0
        temp = reqs.copy()
        while temp:
            closest = min(temp, key=lambda x: abs(x - current))
            dist += abs(closest - current)
            current = closest
            path.append(current)
            temp.remove(current)
        return path, dist
    
    def scan(self, reqs, head):
        reqs.sort()
        left = [x for x in reqs if x < head][::-1]
        right = [x for x in reqs if x >= head]
        path, current, dist = [head], head, 0
        
        for r in left:
            dist += abs(r - current)
            path.append(r)
            current = r
        
        dist += current
        path.append(0)
        current = 0
        
        for r in right:
            dist += abs(r - current)
            path.append(r)
            current = r
        
        return path, dist
    
    def cscan(self, reqs, head):
        reqs.sort()
        right = [x for x in reqs if x >= head]
        left = [x for x in reqs if x < head][::-1]
        path, current, dist = [head], head, 0
        
        # Move right first
        for r in right:
            dist += abs(r - current)
            path.append(r)
            current = r
        
        # Jump to the beginning (assuming disk starts at 0)
        dist += (199 - current)  # Jump to end (assuming 0-199 disk range)
        path.append(199)
        current = 199
        
        # Jump to start and continue with remaining requests from left
        dist += 199  # Jump from 199 to 0
        path.append(0)
        current = 0
        
        for r in left:
            dist += abs(r - current)
            path.append(r)
            current = r
        
        return path, dist

    
    def simulate(self):
        try:
            reqs = [int(x.strip()) for x in self.req_entry.get().split(",")]
            head = int(self.head_entry.get())
            algo = self.algo.get()
            path, dist = getattr(self, algo.lower())(reqs, head)
            self.plot_graph(path, algo, dist)
        except:
            messagebox.showerror("Error", "Invalid input! Check requests and head position.")
    
    def plot_graph(self, path, algo, dist):
        fig, ax = plt.subplots(figsize=(9.5, 6.5))
        fig.patch.set_facecolor(self.COLORS['bg'])
        ax.set_facecolor(self.COLORS['dark'])
        
        y = list(range(len(path), 0, -1))
        color = self.ALGOS[algo]
        
        ax.plot(path, y, marker='o', linestyle='-', color=color, linewidth=2.5, markerfacecolor='#fbbf24', markersize=8, markeredgecolor=color, markeredgewidth=2)
        ax.set_title(f"{algo}: {dist} units", fontsize=18, fontweight='bold', color=self.COLORS['fg'], pad=15)
        ax.set_xlabel("Disk Track", fontsize=13, color=self.COLORS['text'], fontweight='bold')
        ax.set_ylabel("Sequence", fontsize=13, color=self.COLORS['text'], fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.25, color='#4a4a5e')
        
        for i, txt in enumerate(path):
            ax.annotate(txt, (path[i], y[i]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=10, color='#fbbf24', fontweight='bold', bbox=dict(boxstyle='round,pad=0.25', facecolor=color, alpha=0.3, edgecolor='none'))
        
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        for spine in ['left', 'bottom']:
            ax.spines[spine].set_color('#4a4a5e')
        
        ax.tick_params(colors=self.COLORS['text'], labelsize=11)
        fig.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskSimulator(root)
    root.mainloop()