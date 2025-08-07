# =============================================================================
# File: src/gui/modern_control_panel.py
# StreamBlur Pro - Modern UI with Dark Theme
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
import time
from typing import Optional

from ..utils.config import StreamBlurConfig
from ..utils.performance import PerformanceMonitor

class ModernStreamBlurPanel:
    """Pannello di controllo moderno per StreamBlur Pro con dark theme"""
    
    # Color scheme moderno
    COLORS = {
        'bg_primary': '#1a1a1a',      # Nero principale
        'bg_secondary': '#2d2d2d',    # Grigio scuro per cards
        'bg_accent': '#3d3d3d',       # Grigio medio per hover
        'accent_blue': '#0066ff',     # Blu accento principale
        'accent_green': '#00cc66',    # Verde per status attivo
        'accent_red': '#ff4444',      # Rosso per errori
        'accent_orange': '#ff8800',   # Arancione per warning
        'text_primary': '#ffffff',    # Testo principale
        'text_secondary': '#b3b3b3',  # Testo secondario
        'border': '#404040',          # Bordi
        'gradient_start': '#0066ff',  # Gradiente inizio
        'gradient_end': '#00cc66'     # Gradiente fine
    }
    
    def __init__(self, app_controller):
        self.app = app_controller
        self.config = app_controller.config
        
        # GUI components
        self.root: Optional[tk.Tk] = None
        self.is_running = False
        
        # Variables per GUI
        self.blur_var: Optional[tk.IntVar] = None
        self.edge_var: Optional[tk.BooleanVar] = None
        self.temporal_var: Optional[tk.BooleanVar] = None
        self.noise_var: Optional[tk.BooleanVar] = None
        self.performance_var: Optional[tk.BooleanVar] = None
        
        # Status components
        self.status_label = None
        self.fps_label = None
        self.performance_label = None
        self.status_indicator = None
        
        # Custom fonts
        self.fonts = {}
        
    def create_gui(self):
        """Crea interfaccia grafica moderna"""
        self.root = tk.Tk()
        self.root.title("StreamBlur Pro v4.0 - Modern Edition")
        
        # Configurazione finestra
        self.root.configure(bg=self.COLORS['bg_primary'])
        width = 600
        height = 700
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(True, True)
        
        # Centra la finestra
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Setup custom fonts
        self._setup_fonts()
        
        # Setup modern style
        self._setup_modern_style()
        
        # Inizializza variabili
        self._init_variables()
        
        # Crea layout moderno
        self._create_modern_layout()
        
        # Avvia update loop
        self.is_running = True
        self._start_update_loop()
        
    def _setup_fonts(self):
        """Setup font personalizzati"""
        try:
            self.fonts = {
                'title': font.Font(family="Segoe UI", size=24, weight="bold"),
                'subtitle': font.Font(family="Segoe UI", size=12, weight="normal"),
                'heading': font.Font(family="Segoe UI", size=14, weight="bold"),
                'body': font.Font(family="Segoe UI", size=10, weight="normal"),
                'button': font.Font(family="Segoe UI", size=11, weight="bold"),
                'monospace': font.Font(family="Consolas", size=9, weight="normal")
            }
        except:
            # Fallback a font standard
            self.fonts = {
                'title': ('Arial', 24, 'bold'),
                'subtitle': ('Arial', 12),
                'heading': ('Arial', 14, 'bold'),
                'body': ('Arial', 10),
                'button': ('Arial', 11, 'bold'),
                'monospace': ('Courier', 9)
            }
    
    def _setup_modern_style(self):
        """Configura stile moderno per ttk"""
        style = ttk.Style()
        
        # Configura tema base
        style.theme_use('clam')
        
        # Style per Frame moderni
        style.configure('Modern.TFrame',
                       background=self.COLORS['bg_secondary'],
                       relief='flat',
                       borderwidth=1)
        
        # Style per Label moderni
        style.configure('ModernTitle.TLabel',
                       background=self.COLORS['bg_primary'],
                       foreground=self.COLORS['text_primary'],
                       font=self.fonts['title'])
        
        style.configure('ModernSubtitle.TLabel',
                       background=self.COLORS['bg_primary'],
                       foreground=self.COLORS['text_secondary'],
                       font=self.fonts['subtitle'])
        
        style.configure('ModernHeading.TLabel',
                       background=self.COLORS['bg_secondary'],
                       foreground=self.COLORS['text_primary'],
                       font=self.fonts['heading'])
        
        style.configure('ModernBody.TLabel',
                       background=self.COLORS['bg_secondary'],
                       foreground=self.COLORS['text_primary'],
                       font=self.fonts['body'])
        
        # Style per Button moderni
        style.configure('Modern.TButton',
                       background=self.COLORS['accent_blue'],
                       foreground='white',
                       font=self.fonts['button'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 10))
        
        style.map('Modern.TButton',
                 background=[('active', '#0052cc'),
                           ('pressed', '#004499')])
        
        # Style per Button di successo
        style.configure('Success.TButton',
                       background=self.COLORS['accent_green'],
                       foreground='white',
                       font=self.fonts['button'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 10))
        
        # Style per Button di stop
        style.configure('Danger.TButton',
                       background=self.COLORS['accent_red'],
                       foreground='white',
                       font=self.fonts['button'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(15, 8))
        
        # Style per Scale moderni
        style.configure('Modern.Horizontal.TScale',
                       background=self.COLORS['bg_secondary'],
                       troughcolor=self.COLORS['bg_accent'],
                       borderwidth=0,
                       lightcolor=self.COLORS['accent_blue'],
                       darkcolor=self.COLORS['accent_blue'])
        
        # Style per Checkbutton moderni
        style.configure('Modern.TCheckbutton',
                       background=self.COLORS['bg_secondary'],
                       foreground=self.COLORS['text_primary'],
                       font=self.fonts['body'],
                       focuscolor='none',
                       borderwidth=0)
        
        # Style per LabelFrame moderni
        style.configure('Modern.TLabelframe',
                       background=self.COLORS['bg_secondary'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.COLORS['border'])
        
        style.configure('Modern.TLabelframe.Label',
                       background=self.COLORS['bg_secondary'],
                       foreground=self.COLORS['text_primary'],
                       font=self.fonts['heading'])
    
    def _init_variables(self):
        """Inizializza variabili Tkinter"""
        self.blur_var = tk.IntVar(value=self.config.get('effects.blur_intensity', 15))
        self.edge_var = tk.BooleanVar(value=self.config.get('effects.edge_smoothing', True))
        self.temporal_var = tk.BooleanVar(value=self.config.get('effects.temporal_smoothing', True))
        self.noise_var = tk.BooleanVar(value=self.config.get('effects.noise_reduction', False))
        self.performance_var = tk.BooleanVar(value=self.config.get('ai.performance_mode', False))
    
    def _create_modern_layout(self):
        """Crea layout moderno con card design"""
        # Main container con padding
        main_frame = tk.Frame(self.root, bg=self.COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configura grid
        main_frame.grid_rowconfigure(0, weight=0)  # Header
        main_frame.grid_rowconfigure(1, weight=0)  # Status
        main_frame.grid_rowconfigure(2, weight=0)  # Controls  
        main_frame.grid_rowconfigure(3, weight=0)  # Settings
        main_frame.grid_rowconfigure(4, weight=0)  # Performance
        main_frame.grid_rowconfigure(5, weight=1)  # Info (expand)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Crea sezioni
        self._create_modern_header(main_frame)
        self._create_modern_status(main_frame)
        self._create_modern_controls(main_frame)
        self._create_modern_settings(main_frame)
        self._create_modern_performance(main_frame)
        self._create_modern_info(main_frame)
    
    def _create_modern_header(self, parent):
        """Crea header moderno con gradiente"""
        header_frame = tk.Frame(parent, bg=self.COLORS['bg_primary'])
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))
        
        # Titolo principale con emoji e stile
        title_label = tk.Label(header_frame, 
                              text="🎥 StreamBlur Pro v4.0",
                              bg=self.COLORS['bg_primary'],
                              fg=self.COLORS['text_primary'],
                              font=self.fonts['title'])
        title_label.pack()
        
        # Sottotitolo con colore accento
        subtitle_label = tk.Label(header_frame,
                                 text="✨ Modern Edition - Il Tuo NVIDIA Broadcast per AMD ✨",
                                 bg=self.COLORS['bg_primary'],
                                 fg=self.COLORS['accent_blue'],
                                 font=self.fonts['subtitle'])
        subtitle_label.pack(pady=(5, 0))
    
    def _create_modern_status(self, parent):
        """Crea card di status moderna"""
        status_frame = self._create_card(parent, "📊 Status Sistema")
        status_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Container interno
        inner_frame = tk.Frame(status_frame, bg=self.COLORS['bg_secondary'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Status principale con indicatore colorato
        status_container = tk.Frame(inner_frame, bg=self.COLORS['bg_secondary'])
        status_container.pack(fill=tk.X, pady=(0, 10))
        
        # Indicatore status (cerchio colorato)
        self.status_indicator = tk.Label(status_container, 
                                        text="●", 
                                        bg=self.COLORS['bg_secondary'],
                                        fg=self.COLORS['accent_red'],
                                        font=('Arial', 16))
        self.status_indicator.pack(side=tk.LEFT)
        
        # Testo status
        self.status_label = tk.Label(status_container,
                                    text="Inattivo - Virtual Camera OFF",
                                    bg=self.COLORS['bg_secondary'],
                                    fg=self.COLORS['text_primary'],
                                    font=self.fonts['body'])
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Metriche in formato moderno
        metrics_frame = tk.Frame(inner_frame, bg=self.COLORS['bg_secondary'])
        metrics_frame.pack(fill=tk.X)
        
        # FPS
        self.fps_label = tk.Label(metrics_frame,
                                 text="FPS: 0.0",
                                 bg=self.COLORS['bg_secondary'],
                                 fg=self.COLORS['text_secondary'],
                                 font=self.fonts['body'])
        self.fps_label.pack(side=tk.LEFT)
        
        # Separatore
        sep1 = tk.Label(metrics_frame, text=" • ",
                       bg=self.COLORS['bg_secondary'],
                       fg=self.COLORS['text_secondary'])
        sep1.pack(side=tk.LEFT)
        
        # Performance
        self.performance_label = tk.Label(metrics_frame,
                                         text="Performance: N/A",
                                         bg=self.COLORS['bg_secondary'],
                                         fg=self.COLORS['text_secondary'],
                                         font=self.fonts['body'])
        self.performance_label.pack(side=tk.LEFT)
    
    def _create_modern_controls(self, parent):
        """Crea controlli principali moderni"""
        control_frame = self._create_card(parent, "🎮 Controlli")
        control_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        
        inner_frame = tk.Frame(control_frame, bg=self.COLORS['bg_secondary'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Pulsante principale grande
        self.start_button = tk.Button(inner_frame,
                                     text="🚀 AVVIA STREAMBLUR PRO",
                                     bg=self.COLORS['accent_blue'],
                                     fg='white',
                                     font=self.fonts['button'],
                                     relief='flat',
                                     borderwidth=0,
                                     padx=30,
                                     pady=15,
                                     cursor='hand2',
                                     command=self.start_processing)
        self.start_button.pack(fill=tk.X, pady=(0, 15))
        
        # Hover effects per il pulsante principale
        self.start_button.bind('<Enter>', lambda e: self.start_button.config(bg='#0052cc'))
        self.start_button.bind('<Leave>', lambda e: self.start_button.config(bg=self.COLORS['accent_blue']))
        
        # Pulsanti secondari
        secondary_frame = tk.Frame(inner_frame, bg=self.COLORS['bg_secondary'])
        secondary_frame.pack(fill=tk.X)
        
        # Stop button
        self.stop_button = tk.Button(secondary_frame,
                                    text="⏹️ FERMA",
                                    bg=self.COLORS['accent_red'],
                                    fg='white',
                                    font=self.fonts['body'],
                                    relief='flat',
                                    borderwidth=0,
                                    padx=20,
                                    pady=10,
                                    state='disabled',
                                    cursor='hand2',
                                    command=self.stop_processing)
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Preview button
        self.preview_button = tk.Button(secondary_frame,
                                       text="👁️ PREVIEW",
                                       bg=self.COLORS['bg_accent'],
                                       fg=self.COLORS['text_primary'],
                                       font=self.fonts['body'],
                                       relief='flat',
                                       borderwidth=0,
                                       padx=20,
                                       pady=10,
                                       cursor='hand2',
                                       command=self.toggle_preview)
        self.preview_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        # Reset button
        reset_button = tk.Button(secondary_frame,
                                text="🔄 RESET",
                                bg=self.COLORS['bg_accent'],
                                fg=self.COLORS['text_primary'],
                                font=self.fonts['body'],
                                relief='flat',
                                borderwidth=0,
                                padx=20,
                                pady=10,
                                cursor='hand2',
                                command=self.reset_settings)
        reset_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
    
    def _create_modern_settings(self, parent):
        """Crea sezione impostazioni moderna"""
        settings_frame = self._create_card(parent, "⚙️ Impostazioni Effetti")
        settings_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        
        inner_frame = tk.Frame(settings_frame, bg=self.COLORS['bg_secondary'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Blur intensity con design moderno
        blur_container = tk.Frame(inner_frame, bg=self.COLORS['bg_secondary'])
        blur_container.pack(fill=tk.X, pady=(0, 20))
        
        # Label e valore blur
        blur_header = tk.Frame(blur_container, bg=self.COLORS['bg_secondary'])
        blur_header.pack(fill=tk.X, pady=(0, 10))
        
        blur_label = tk.Label(blur_header,
                             text="🌪️ Intensità Blur",
                             bg=self.COLORS['bg_secondary'],
                             fg=self.COLORS['text_primary'],
                             font=self.fonts['body'])
        blur_label.pack(side=tk.LEFT)
        
        self.blur_value_label = tk.Label(blur_header,
                                        text="15",
                                        bg=self.COLORS['accent_blue'],
                                        fg='white',
                                        font=self.fonts['button'],
                                        padx=10,
                                        pady=5)
        self.blur_value_label.pack(side=tk.RIGHT)
        
        # Scale personalizzato
        self.blur_scale = tk.Scale(blur_container,
                                  from_=1, to=25,
                                  variable=self.blur_var,
                                  orient=tk.HORIZONTAL,
                                  command=self.on_blur_change,
                                  bg=self.COLORS['bg_secondary'],
                                  fg=self.COLORS['text_primary'],
                                  highlightthickness=0,
                                  troughcolor=self.COLORS['bg_accent'],
                                  activebackground=self.COLORS['accent_blue'],
                                  showvalue=False,
                                  relief='flat',
                                  borderwidth=0,
                                  length=400)
        self.blur_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Checkboxes con stile moderno
        checkboxes = [
            ("🎯 Edge Smoothing (Bordi morbidi)", self.edge_var, self.on_edge_toggle),
            ("⏱️ Temporal Smoothing (Stabilità movimento)", self.temporal_var, self.on_temporal_toggle),
            ("🔧 Noise Reduction (Rallenta performance)", self.noise_var, self.on_noise_toggle),
            ("⚡ Performance Mode (Veloce ma meno preciso)", self.performance_var, self.on_performance_toggle)
        ]
        
        for text, var, callback in checkboxes:
            self._create_modern_checkbox(inner_frame, text, var, callback)
    
    def _create_modern_checkbox(self, parent, text, variable, callback):
        """Crea checkbox con stile moderno"""
        cb_frame = tk.Frame(parent, bg=self.COLORS['bg_secondary'])
        cb_frame.pack(fill=tk.X, pady=(0, 8))
        
        checkbox = tk.Checkbutton(cb_frame,
                                 text=text,
                                 variable=variable,
                                 command=callback,
                                 bg=self.COLORS['bg_secondary'],
                                 fg=self.COLORS['text_primary'],
                                 font=self.fonts['body'],
                                 selectcolor=self.COLORS['accent_blue'],
                                 activebackground=self.COLORS['bg_secondary'],
                                 activeforeground=self.COLORS['text_primary'],
                                 borderwidth=0,
                                 highlightthickness=0,
                                 cursor='hand2')
        checkbox.pack(side=tk.LEFT)
    
    def _create_modern_performance(self, parent):
        """Crea monitor performance moderno"""
        perf_frame = self._create_card(parent, "📈 Performance Monitor")
        perf_frame.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        
        inner_frame = tk.Frame(perf_frame, bg=self.COLORS['bg_secondary'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        self.perf_info = tk.Label(inner_frame,
                                 text="Avvia StreamBlur per vedere le statistiche in tempo reale",
                                 bg=self.COLORS['bg_secondary'],
                                 fg=self.COLORS['text_secondary'],
                                 font=self.fonts['monospace'],
                                 justify=tk.LEFT)
        self.perf_info.pack(fill=tk.X)
    
    def _create_modern_info(self, parent):
        """Crea sezione info moderna"""
        info_frame = self._create_card(parent, "📖 Quick Start Guide")
        info_frame.grid(row=5, column=0, sticky="nsew", pady=(0, 0))
        
        inner_frame = tk.Frame(info_frame, bg=self.COLORS['bg_secondary'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        instructions = """🚀 Come iniziare:

1. Clicca 'AVVIA STREAMBLUR PRO'
2. Apri la tua app preferita (Discord, Teams, OBS, Zoom...)
3. Seleziona 'OBS Virtual Camera' come sorgente webcam
4. Regola l'intensità del blur e gli effetti in tempo reale
5. Goditi il tuo background blur professionale!

💡 La Virtual Camera apparirà come 'OBS Virtual Camera' ma è StreamBlur Pro che lavora dietro le quinte per darti il miglior effetto blur possibile con la tua AMD RX 7900 XTX!

⚡ Performance Mode: Attiva per massime prestazioni (30+ FPS)
🎯 Edge Smoothing: Bordi più morbidi e naturali
⏱️ Temporal Smoothing: Riduce il flickering tra i frame"""
        
        info_label = tk.Label(inner_frame,
                             text=instructions,
                             bg=self.COLORS['bg_secondary'],
                             fg=self.COLORS['text_primary'],
                             font=self.fonts['body'],
                             justify=tk.LEFT,
                             wraplength=520)
        info_label.pack(fill=tk.BOTH, expand=True)
    
    def _create_card(self, parent, title):
        """Crea una card moderna con titolo"""
        # Container con bordo arrotondato simulato
        card_frame = tk.Frame(parent, bg=self.COLORS['border'], padx=1, pady=1)
        
        # Frame interno
        inner_card = tk.Frame(card_frame, bg=self.COLORS['bg_secondary'])
        inner_card.pack(fill=tk.BOTH, expand=True)
        
        # Header della card
        header_frame = tk.Frame(inner_card, bg=self.COLORS['bg_accent'], height=40)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Titolo
        title_label = tk.Label(header_frame,
                              text=title,
                              bg=self.COLORS['bg_accent'],
                              fg=self.COLORS['text_primary'],
                              font=self.fonts['heading'])
        title_label.pack(pady=10)
        
        return inner_card
    
    # Event handlers (stessi della versione originale ma con aggiornamenti visuali)
    def start_processing(self):
        """Avvia processing con feedback visivo"""
        if self.app.start_processing():
            self.start_button.config(state='disabled', text="🔄 AVVIANDO...", bg=self.COLORS['bg_accent'])
            self.stop_button.config(state='normal')
            self.preview_button.config(state='normal')
            
            # Aggiorna indicatore visivo
            self.status_indicator.config(fg=self.COLORS['accent_green'])
            self.status_label.config(text="Attivo - Virtual Camera ON")
    
    def stop_processing(self):
        """Ferma processing"""
        self.app.stop_processing()
        self.start_button.config(state='normal', text="🚀 AVVIA STREAMBLUR PRO", bg=self.COLORS['accent_blue'])
        self.stop_button.config(state='disabled')
        self.preview_button.config(state='disabled')
        
        # Reset indicatore visivo
        self.status_indicator.config(fg=self.COLORS['accent_red'])
        self.status_label.config(text="Inattivo - Virtual Camera OFF")
    
    def toggle_preview(self):
        """Toggle preview window"""
        self.app.toggle_preview()
    
    def reset_settings(self):
        """Reset impostazioni"""
        if messagebox.askyesno("Reset Impostazioni", 
                              "Vuoi ripristinare tutte le impostazioni ai valori predefiniti?",
                              parent=self.root):
            self.config.reset_to_defaults()
            self._load_settings_from_config()
            messagebox.showinfo("Reset Completato", 
                              "Impostazioni ripristinate ai valori predefiniti!",
                              parent=self.root)
    
    def on_blur_change(self, value):
        """Callback cambio blur con aggiornamento visivo"""
        intensity = int(float(value))
        self.blur_value_label.config(text=str(intensity))
        self.app.set_blur_intensity(intensity)
    
    def on_edge_toggle(self):
        """Callback toggle edge smoothing"""
        if self.edge_var:
            self.app.set_edge_smoothing(self.edge_var.get())
    
    def on_temporal_toggle(self):
        """Callback toggle temporal smoothing"""
        if self.temporal_var:
            self.app.set_temporal_smoothing(self.temporal_var.get())
    
    def on_noise_toggle(self):
        """Callback toggle noise reduction"""
        if self.noise_var:
            self.app.set_noise_reduction(self.noise_var.get())
    
    def on_performance_toggle(self):
        """Callback toggle performance mode con feedback visivo"""
        if self.performance_var:
            performance_mode = self.performance_var.get()
            self.config.set('ai.performance_mode', performance_mode)
            
            if hasattr(self.app, 'ai_processor') and self.app.ai_processor:
                try:
                    self.app.ai_processor.switch_model(performance_mode)
                    mode_text = "Performance (Veloce)" if performance_mode else "Accurato (Preciso)"
                    print(f"🔄 Modello AI cambiato: {mode_text}")
                except Exception as e:
                    print(f"⚠️ Errore cambio modello: {e}")
                    messagebox.showwarning("Cambio Modello", 
                                         "Errore durante il cambio modello. Riavvia StreamBlur se necessario.",
                                         parent=self.root)
    
    def _load_settings_from_config(self):
        """Carica impostazioni dalla configurazione"""
        if self.blur_var:
            self.blur_var.set(self.config.get('effects.blur_intensity', 15))
            self.blur_value_label.config(text=str(self.blur_var.get()))
        if self.edge_var:
            self.edge_var.set(self.config.get('effects.edge_smoothing', True))
        if self.temporal_var:
            self.temporal_var.set(self.config.get('effects.temporal_smoothing', True))
        if self.noise_var:
            self.noise_var.set(self.config.get('effects.noise_reduction', False))
        if self.performance_var:
            self.performance_var.set(self.config.get('ai.performance_mode', False))
    
    def _start_update_loop(self):
        """Avvia loop aggiornamento GUI"""
        self._update_status()
    
    def _update_status(self):
        """Aggiorna status con indicatori visivi moderni"""
        if not self.is_running:
            return
        
        try:
            if hasattr(self.app, 'get_stats'):
                stats = self.app.get_stats()
                
                # Aggiorna indicatore status
                if stats['is_processing']:
                    self.status_indicator.config(fg=self.COLORS['accent_green'])
                    self.status_label.config(text="Attivo - Virtual Camera ON")
                else:
                    self.status_indicator.config(fg=self.COLORS['accent_red'])
                    self.status_label.config(text="Inattivo - Virtual Camera OFF")
                
                # Aggiorna FPS con colori
                fps = stats.get('fps', 0.0)
                if fps >= 25:
                    fps_color = self.COLORS['accent_green']
                elif fps >= 20:
                    fps_color = self.COLORS['accent_orange']
                else:
                    fps_color = self.COLORS['accent_red']
                
                self.fps_label.config(text=f"FPS: {fps:.1f}", fg=fps_color)
                
                # Aggiorna performance
                grade = stats.get('performance_grade', 'N/A')
                self.performance_label.config(text=f"Performance: {grade}")
                
                # Aggiorna monitor performance
                perf_text = self._format_performance_info(stats)
                self.perf_info.config(text=perf_text)
            
        except Exception as e:
            print(f"⚠️ Errore update GUI: {e}")
        
        # Schedule prossimo update
        if self.root:
            self.root.after(1000, self._update_status)
    
    def _format_performance_info(self, stats):
        """Formatta informazioni performance in stile moderno"""
        try:
            fps = stats.get('fps', 0.0)
            processing_ms = stats.get('processing_time_ms', 0.0)
            cpu = stats.get('cpu_usage', 0.0)
            memory = stats.get('memory_usage', 0.0)
            frames_sent = stats.get('frames_sent', 0)
            frames_dropped = stats.get('frames_dropped', 0)
            
            return f"""📊 Statistiche in Tempo Reale:

🎯 FPS: {fps:.1f} | ⚡ Processing: {processing_ms:.1f}ms | 🖥️ CPU: {cpu:.1f}% | 💾 RAM: {memory:.1f}%

📈 Frames Inviati: {frames_sent:,} | 📉 Frames Persi: {frames_dropped}

🚀 StreamBlur Pro sta utilizzando la tua AMD RX 7900 XTX per il massimo delle performance!"""
        except:
            return "📊 Avvia StreamBlur per vedere le statistiche in tempo reale"
    
    def run(self):
        """Avvia GUI moderna"""
        self.create_gui()
        if self.root:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
    
    def on_closing(self):
        """Callback chiusura finestra"""
        self.is_running = False
        self.app.cleanup()
        if self.root:
            self.root.destroy()
