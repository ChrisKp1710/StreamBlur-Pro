# =============================================================================
# File 8: src/gui/control_panel.py - MODERN EDITION
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
import time
from typing import Optional

from ..utils.config import StreamBlurConfig
from ..utils.performance import PerformanceMonitor

class StreamBlurControlPanel:
    """Pannello di controllo GUI per StreamBlur Pro - MODERN EDITION"""
    
    # 🎨 Schema colori moderno
    COLORS = {
        'bg_primary': '#1a1a1a',      # Sfondo principale
        'bg_card': '#2d2d2d',         # Sfondo cards
        'bg_hover': '#3d3d3d',        # Hover effect
        'blue': '#0066ff',            # Blu principale
        'green': '#00cc66',           # Verde successo
        'red': '#ff4444',             # Rosso errore
        'orange': '#ff8800',          # Arancione warning
        'text': '#ffffff',            # Testo principale
        'text_dim': '#b3b3b3',        # Testo secondario
        'border': '#404040'           # Bordi
    }
    
    def __init__(self, app_controller):
        self.app = app_controller  # Riferimento al controller principale
        self.config = app_controller.config
        
        # GUI components
        self.root: Optional[tk.Tk] = None
        self.is_running = False
        
        # 🎨 Font moderni
        self.fonts = {}
        
        # Variables per GUI (saranno inizializzate in create_gui)
        self.blur_var: Optional[tk.IntVar] = None
        self.edge_var: Optional[tk.BooleanVar] = None
        self.temporal_var: Optional[tk.BooleanVar] = None
        self.noise_var: Optional[tk.BooleanVar] = None
        self.performance_var: Optional[tk.BooleanVar] = None
        
        # Status labels
        self.status_label = None
        self.fps_label = None
        self.performance_label = None
        self.status_indicator = None  # 🔴🟢 Indicatore colorato
        
    def create_gui(self):
        """Crea interfaccia grafica MODERNA"""
        self.root = tk.Tk()
        self.root.title("🎥 StreamBlur Pro v4.0 - Modern Edition")
        
        # 🎨 Setup moderno
        self.root.configure(bg=self.COLORS['bg_primary'])
        self._setup_modern_fonts()
        
        # Ora che abbiamo root, creiamo le variabili Tkinter
        self.blur_var = tk.IntVar(value=self.config.get('effects.blur_intensity', 15))
        self.edge_var = tk.BooleanVar(value=self.config.get('effects.edge_smoothing', True))
        self.temporal_var = tk.BooleanVar(value=self.config.get('effects.temporal_smoothing', True))
        self.noise_var = tk.BooleanVar(value=self.config.get('effects.noise_reduction', False))
        self.performance_var = tk.BooleanVar(value=self.config.get('ai.performance_mode', False))
        
        width = 580
        height = 650
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(True, True)
        
        # Centra finestra
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main container con padding maggiore
        main_frame = tk.Frame(self.root, bg=self.COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self._create_header(main_frame)
        self._create_status_section(main_frame)
        self._create_control_section(main_frame)
        self._create_settings_section(main_frame)
        self._create_performance_section(main_frame)
        self._create_info_section(main_frame)
        
        # Update loop
        self.is_running = True
        self._start_update_loop()
    
    def _setup_modern_fonts(self):
        """Setup font moderni"""
        try:
            self.fonts = {
                'title': font.Font(family="Segoe UI", size=22, weight="bold"),
                'subtitle': font.Font(family="Segoe UI", size=11),
                'heading': font.Font(family="Segoe UI", size=12, weight="bold"),
                'body': font.Font(family="Segoe UI", size=10),
                'button': font.Font(family="Segoe UI", size=11, weight="bold"),
                'mono': font.Font(family="Consolas", size=9)
            }
        except:
            # Fallback
            self.fonts = {
                'title': ('Arial', 22, 'bold'),
                'subtitle': ('Arial', 11),
                'heading': ('Arial', 12, 'bold'),
                'body': ('Arial', 10),
                'button': ('Arial', 11, 'bold'),
                'mono': ('Courier', 9)
            }
        
    def _create_header(self, parent):
        """Crea header MODERNO"""
        header_frame = tk.Frame(parent, bg=self.COLORS['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Titolo principale GRANDE
        title_label = tk.Label(header_frame, 
                              text="🎥 StreamBlur Pro v4.0",
                              bg=self.COLORS['bg_primary'],
                              fg=self.COLORS['text'],
                              font=self.fonts['title'])
        title_label.pack()
        
        # Sottotitolo colorato
        subtitle_label = tk.Label(header_frame,
                                 text="✨ Modern Edition - Il Tuo NVIDIA Broadcast per AMD ✨",
                                 bg=self.COLORS['bg_primary'],
                                 fg=self.COLORS['blue'],
                                 font=self.fonts['subtitle'])
        subtitle_label.pack(pady=(5, 0))
        
    def _create_modern_card(self, parent, title):
        """Crea una card moderna"""
        # Container con bordo
        card_container = tk.Frame(parent, bg=self.COLORS['border'], padx=1, pady=1)
        card_container.pack(fill=tk.X, pady=(0, 15))
        
        # Card interna
        card_frame = tk.Frame(card_container, bg=self.COLORS['bg_card'])
        card_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(card_frame, bg=self.COLORS['bg_hover'], height=35)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header,
                              text=title,
                              bg=self.COLORS['bg_hover'],
                              fg=self.COLORS['text'],
                              font=self.fonts['heading'])
        title_label.pack(pady=8)
        
        # Content area
        content = tk.Frame(card_frame, bg=self.COLORS['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        
        return content
    
    def _create_status_section(self, parent):
        """Crea sezione status MODERNA"""
        # Card container
        status_card = self._create_modern_card(parent, "📊 Status Sistema")
        
        # Status principale con indicatore colorato
        status_row = tk.Frame(status_card, bg=self.COLORS['bg_card'])
        status_row.pack(fill=tk.X, pady=(0, 10))
        
        # Indicatore colorato (pallino)
        self.status_indicator = tk.Label(status_row,
                                        text="●",
                                        bg=self.COLORS['bg_card'],
                                        fg=self.COLORS['red'],
                                        font=('Arial', 14))
        self.status_indicator.pack(side=tk.LEFT)
        
        # Testo status
        self.status_label = tk.Label(status_row,
                                    text="Inattivo - Virtual Camera OFF",
                                    bg=self.COLORS['bg_card'],
                                    fg=self.COLORS['text'],
                                    font=self.fonts['body'])
        self.status_label.pack(side=tk.LEFT, padx=(8, 0))
        
        # Metriche
        metrics_frame = tk.Frame(status_card, bg=self.COLORS['bg_card'])
        metrics_frame.pack(fill=tk.X)
        
        # FPS
        self.fps_label = tk.Label(metrics_frame,
                                 text="FPS: 0.0",
                                 bg=self.COLORS['bg_card'],
                                 fg=self.COLORS['text_dim'],
                                 font=self.fonts['body'])
        self.fps_label.pack(side=tk.LEFT)
        
        # Separatore
        sep = tk.Label(metrics_frame, text=" • ",
                      bg=self.COLORS['bg_card'],
                      fg=self.COLORS['text_dim'])
        sep.pack(side=tk.LEFT)
        
        # Performance
        self.performance_label = tk.Label(metrics_frame,
                                         text="Performance: N/A",
                                         bg=self.COLORS['bg_card'],
                                         fg=self.COLORS['text_dim'],
                                         font=self.fonts['body'])
        self.performance_label.pack(side=tk.LEFT)
        
    def _create_control_section(self, parent):
        """Crea sezione controlli MODERNA"""
        control_card = self._create_modern_card(parent, "🎮 Controlli")
        
        # Pulsante principale GRANDE
        self.start_button = tk.Button(control_card,
                                     text="🚀 AVVIA STREAMBLUR PRO",
                                     bg=self.COLORS['blue'],
                                     fg='white',
                                     font=self.fonts['button'],
                                     relief='flat',
                                     borderwidth=0,
                                     padx=25,
                                     pady=12,
                                     cursor='hand2',
                                     command=self.start_processing)
        self.start_button.pack(fill=tk.X, pady=(0, 12))
        
        # Hover effect
        self.start_button.bind('<Enter>', lambda e: self.start_button.config(bg='#0052cc'))
        self.start_button.bind('<Leave>', lambda e: self.start_button.config(bg=self.COLORS['blue']))
        
        # Pulsanti secondari
        buttons_frame = tk.Frame(control_card, bg=self.COLORS['bg_card'])
        buttons_frame.pack(fill=tk.X)
        
        # Stop
        self.stop_button = tk.Button(buttons_frame,
                                    text="⏹️ FERMA",
                                    bg=self.COLORS['red'],
                                    fg='white',
                                    font=self.fonts['body'],
                                    relief='flat',
                                    borderwidth=0,
                                    padx=15,
                                    pady=8,
                                    state='disabled',
                                    cursor='hand2',
                                    command=self.stop_processing)
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        # Preview
        self.preview_button = tk.Button(buttons_frame,
                                       text="👁️ PREVIEW",
                                       bg=self.COLORS['bg_hover'],
                                       fg=self.COLORS['text'],
                                       font=self.fonts['body'],
                                       relief='flat',
                                       borderwidth=0,
                                       padx=15,
                                       pady=8,
                                       cursor='hand2',
                                       command=self.toggle_preview)
        self.preview_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 4))
        
        # Reset
        reset_button = tk.Button(buttons_frame,
                                text="🔄 RESET",
                                bg=self.COLORS['bg_hover'],
                                fg=self.COLORS['text'],
                                font=self.fonts['body'],
                                relief='flat',
                                borderwidth=0,
                                padx=15,
                                pady=8,
                                cursor='hand2',
                                command=self.reset_settings)
        reset_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))
        
    def _create_settings_section(self, parent):
        """Crea sezione impostazioni MODERNA"""
        settings_card = self._create_modern_card(parent, "⚙️ Impostazioni Effetti")
        
        # Blur intensity
        blur_frame = tk.Frame(settings_card, bg=self.COLORS['bg_card'])
        blur_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Header blur
        blur_header = tk.Frame(blur_frame, bg=self.COLORS['bg_card'])
        blur_header.pack(fill=tk.X, pady=(0, 8))
        
        blur_label = tk.Label(blur_header,
                             text="🌪️ Intensità Blur",
                             bg=self.COLORS['bg_card'],
                             fg=self.COLORS['text'],
                             font=self.fonts['body'])
        blur_label.pack(side=tk.LEFT)
        
        # Valore con badge colorato
        self.blur_value_label = tk.Label(blur_header,
                                        text="15",
                                        bg=self.COLORS['blue'],
                                        fg='white',
                                        font=self.fonts['button'],
                                        padx=8,
                                        pady=3)
        self.blur_value_label.pack(side=tk.RIGHT)
        
        # Scale moderno
        if self.blur_var is not None:  # ✅ Controllo sicurezza
            self.blur_scale = tk.Scale(blur_frame,
                                      from_=1, to=25,
                                      variable=self.blur_var,
                                      orient=tk.HORIZONTAL,
                                      command=self.on_blur_change,
                                      bg=self.COLORS['bg_card'],
                                      fg=self.COLORS['text'],
                                      highlightthickness=0,
                                      troughcolor=self.COLORS['bg_hover'],
                                      activebackground=self.COLORS['blue'],
                                      showvalue=False,
                                      relief='flat',
                                      borderwidth=0,
                                      length=400)
            self.blur_scale.pack(fill=tk.X)
        
        # Checkboxes moderne
        checkboxes = [
            ("🎯 Edge Smoothing (Bordi morbidi)", self.edge_var, self.on_edge_toggle),
            ("⏱️ Temporal Smoothing (Stabilità movimento)", self.temporal_var, self.on_temporal_toggle),
            ("🔧 Noise Reduction (Rallenta performance)", self.noise_var, self.on_noise_toggle),
            ("⚡ Performance Mode (Veloce ma meno preciso)", self.performance_var, self.on_performance_toggle)
        ]
        
        for text, var, callback in checkboxes:
            if var is not None:  # ✅ Controllo sicurezza per le variabili
                cb_frame = tk.Frame(settings_card, bg=self.COLORS['bg_card'])
                cb_frame.pack(fill=tk.X, pady=(0, 6))
                
                checkbox = tk.Checkbutton(cb_frame,
                                         text=text,
                                         variable=var,
                                         command=callback,
                                         bg=self.COLORS['bg_card'],
                                         fg=self.COLORS['text'],
                                         font=self.fonts['body'],
                                         selectcolor=self.COLORS['blue'],
                                         activebackground=self.COLORS['bg_card'],
                                         activeforeground=self.COLORS['text'],
                                         borderwidth=0,
                                         highlightthickness=0,
                                         cursor='hand2')
                checkbox.pack(side=tk.LEFT)
        
    def _create_performance_section(self, parent):
        """Crea sezione performance MODERNA"""
        perf_card = self._create_modern_card(parent, "📈 Performance Monitor")
        
        self.perf_info = tk.Label(perf_card,
                                 text="Avvia StreamBlur per vedere le statistiche in tempo reale",
                                 bg=self.COLORS['bg_card'],
                                 fg=self.COLORS['text_dim'],
                                 font=self.fonts['mono'],
                                 justify=tk.LEFT)
        self.perf_info.pack(fill=tk.X)
    
    def _create_info_section(self, parent):
        """Crea sezione info MODERNA"""
        info_card = self._create_modern_card(parent, "📖 Quick Start Guide")
        
        instructions = """🚀 Come iniziare:

1. Clicca 'AVVIA STREAMBLUR PRO'
2. Apri la tua app preferita (Discord, Teams, OBS, Zoom...)
3. Seleziona 'OBS Virtual Camera' come sorgente webcam
4. Regola l'intensità del blur e gli effetti in tempo reale
5. Goditi il tuo background blur professionale!

💡 La Virtual Camera apparirà come 'OBS Virtual Camera' ma è StreamBlur Pro che lavora dietro le quinte per darti il miglior effetto blur possibile con la tua AMD RX 7900 XTX!

⚡ Performance Mode: Massime prestazioni (30+ FPS)
🎯 Edge Smoothing: Bordi più morbidi e naturali
⏱️ Temporal Smoothing: Riduce il flickering"""
        
        info_label = tk.Label(info_card,
                             text=instructions,
                             bg=self.COLORS['bg_card'],
                             fg=self.COLORS['text'],
                             font=self.fonts['body'],
                             justify=tk.LEFT,
                             wraplength=500)
        info_label.pack(fill=tk.BOTH, expand=True)
    
    # Event handlers MODERNI
    def start_processing(self):
        """Avvia processing con feedback visivo"""
        if self.app.start_processing():
            self.start_button.config(state='disabled', text="🔄 AVVIANDO...", bg=self.COLORS['bg_hover'])
            self.stop_button.config(state='normal')
            self.preview_button.config(state='normal')
            
            # Aggiorna indicatore visivo
            if self.status_indicator:
                self.status_indicator.config(fg=self.COLORS['green'])
            if self.status_label:
                self.status_label.config(text="Attivo - Virtual Camera ON")
    
    def stop_processing(self):
        """Ferma processing"""
        self.app.stop_processing()
        self.start_button.config(state='normal', text="🚀 AVVIA STREAMBLUR PRO", bg=self.COLORS['blue'])
        self.stop_button.config(state='disabled')
        self.preview_button.config(state='disabled')
        
        # Reset indicatore visivo
        if self.status_indicator:
            self.status_indicator.config(fg=self.COLORS['red'])
        if self.status_label:
            self.status_label.config(text="Inattivo - Virtual Camera OFF")
    
    def toggle_preview(self):
        """Toggle preview window"""
        self.app.toggle_preview()
    
    def reset_settings(self):
        """Reset impostazioni a default"""
        if messagebox.askyesno("Reset Impostazioni", 
                              "Vuoi ripristinare tutte le impostazioni ai valori predefiniti?"):
            self.config.reset_to_defaults()
            self._load_settings_from_config()
            messagebox.showinfo("Reset Completato", "Impostazioni ripristinate ai valori predefiniti!")
    
    def on_blur_change(self, value):
        """Callback cambio blur"""
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
        """Callback toggle performance mode"""
        if self.performance_var:
            performance_mode = self.performance_var.get()
            self.config.set('ai.performance_mode', performance_mode)
            
            # Cambio dinamico del modello AI senza riavvio
            if hasattr(self.app, 'ai_processor') and self.app.ai_processor:
                try:
                    # Cambia modello immediatamente
                    self.app.ai_processor.switch_model(performance_mode)
                    
                    # Mostra feedback all'utente
                    mode_text = "Performance (Veloce)" if performance_mode else "Accurato (Preciso)"
                    if hasattr(self, 'status_label') and self.status_label:
                        current_status = self.status_label.cget('text')
                        if "🟢" in current_status:
                            self.status_label.config(text=f"🟢 Attivo - Modello: {mode_text}")
                    
                    print(f"🔄 Modello AI cambiato: {mode_text}")
                    
                except Exception as e:
                    print(f"⚠️ Errore cambio modello: {e}")
                    messagebox.showwarning("Cambio Modello", 
                                         "Errore durante il cambio modello. Riavvia StreamBlur se necessario.")
            else:
                # Se l'app non è ancora avviata, il cambio sarà applicato al prossimo avvio
                mode_text = "Performance (Veloce)" if performance_mode else "Accurato (Preciso)"
                print(f"⚙️ Modello impostato per il prossimo avvio: {mode_text}")
    
    def _load_settings_from_config(self):
        """Carica impostazioni dalla configurazione"""
        if self.blur_var:
            self.blur_var.set(self.config.get('effects.blur_intensity', 15))
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
        """Aggiorna status con indicatori visivi MODERNI"""
        if not self.is_running:
            return
        
        try:
            # Ottieni stats dall'app
            if hasattr(self.app, 'get_stats'):
                stats = self.app.get_stats()
                
                # Aggiorna indicatore colorato
                if stats['is_processing']:
                    if self.status_indicator:
                        self.status_indicator.config(fg=self.COLORS['green'])
                    if self.status_label:
                        self.status_label.config(text="Attivo - Virtual Camera ON")
                else:
                    if self.status_indicator:
                        self.status_indicator.config(fg=self.COLORS['red'])
                    if self.status_label:
                        self.status_label.config(text="Inattivo - Virtual Camera OFF")
                
                # Aggiorna FPS con colori
                fps = stats.get('fps', 0.0)
                if fps >= 25:
                    fps_color = self.COLORS['green']
                elif fps >= 20:
                    fps_color = self.COLORS['orange']
                else:
                    fps_color = self.COLORS['red']
                    
                if self.fps_label:
                    self.fps_label.config(text=f"FPS: {fps:.1f}", fg=fps_color)
                
                # Aggiorna performance grade
                grade = stats.get('performance_grade', 'N/A')
                if self.performance_label:
                    self.performance_label.config(text=f"Performance: {grade}")
                
                # Aggiorna performance monitor
                perf_text = self._format_performance_info(stats)
                if self.perf_info:
                    self.perf_info.config(text=perf_text)
            
        except Exception as e:
            print(f"⚠️ Errore update GUI: {e}")
        
        # Schedule prossimo update
        if self.root:
            self.root.after(1000, self._update_status)
    
    def _format_performance_info(self, stats):
        """Formatta informazioni performance in stile MODERNO"""
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
        """Avvia GUI"""
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
