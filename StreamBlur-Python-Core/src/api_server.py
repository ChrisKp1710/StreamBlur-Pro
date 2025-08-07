# =============================================================================
# StreamBlur Pro - HTTP API Server
# =============================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import json
from typing import Dict, Any, Optional

class StreamBlurAPIServer:
    """Server HTTP per comunicazione con frontend Tauri"""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.app = Flask(__name__)
        CORS(self.app)  # Permetti CORS per Tauri
        
        # Stato interno
        self.streamblur_state = {
            'running': False,
            'blur_intensity': 15,
            'blur_enabled': True,
            'performance_mode': False,
            'edge_smoothing': True,
            'temporal_smoothing': True,
            'fps': 0.0,
            'cpu_usage': 0.0,
            'memory_usage': 0.0
        }
        
        # Riferimenti ai componenti principali
        self.camera_manager = None
        self.ai_processor = None
        self.effects_processor = None
        self.virtual_camera = None
        self.performance_monitor = None
        
        self._setup_routes()
        
    def _setup_routes(self):
        """Configura le route API"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'ok', 'message': 'StreamBlur API is running'})
        
        @self.app.route('/status', methods=['GET'])
        def get_status():
            """Ritorna lo stato attuale del sistema"""
            # Aggiorna metriche performance se disponibili
            if self.performance_monitor:
                self.streamblur_state['fps'] = self.performance_monitor.get_fps()
                self.streamblur_state['cpu_usage'] = self.performance_monitor.get_cpu_usage()
                self.streamblur_state['memory_usage'] = self.performance_monitor.get_memory_usage()
            
            return jsonify(self.streamblur_state)
        
        @self.app.route('/blur/settings', methods=['POST'])
        def update_blur_settings():
            """Aggiorna impostazioni blur"""
            try:
                data = request.get_json()
                intensity = data.get('intensity', 15)
                enabled = data.get('enabled', True)
                
                # Aggiorna stato interno
                self.streamblur_state['blur_intensity'] = intensity
                self.streamblur_state['blur_enabled'] = enabled
                
                # Applica alle effetti se disponibili
                if self.effects_processor:
                    self.effects_processor.set_blur_intensity(intensity)
                    self.effects_processor.set_blur_enabled(enabled)
                
                return jsonify({
                    'success': True,
                    'message': f'Blur aggiornato: {intensity}% ({"ON" if enabled else "OFF"})'
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 400
        
        @self.app.route('/ai/settings', methods=['POST'])
        def update_ai_settings():
            """Aggiorna impostazioni AI"""
            try:
                data = request.get_json()
                performance_mode = data.get('performance_mode', False)
                edge_smoothing = data.get('edge_smoothing', True)
                temporal_smoothing = data.get('temporal_smoothing', True)
                
                # Aggiorna stato interno
                self.streamblur_state['performance_mode'] = performance_mode
                self.streamblur_state['edge_smoothing'] = edge_smoothing
                self.streamblur_state['temporal_smoothing'] = temporal_smoothing
                
                # Applica al processore AI se disponibile
                if self.ai_processor:
                    self.ai_processor.set_performance_mode(performance_mode)
                    self.ai_processor.set_edge_smoothing(edge_smoothing)
                    self.ai_processor.set_temporal_smoothing(temporal_smoothing)
                
                return jsonify({
                    'success': True,
                    'message': 'Impostazioni AI aggiornate'
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 400
        
        @self.app.route('/engine/start', methods=['POST'])
        def start_engine():
            """Avvia il motore StreamBlur"""
            try:
                if not self.streamblur_state['running']:
                    # TODO: Implementa l'avvio dei componenti
                    self.streamblur_state['running'] = True
                    return jsonify({
                        'success': True,
                        'message': 'Motore StreamBlur avviato'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Motore già in esecuzione'
                    })
                    
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 400
        
        @self.app.route('/engine/stop', methods=['POST'])
        def stop_engine():
            """Ferma il motore StreamBlur"""
            try:
                if self.streamblur_state['running']:
                    # TODO: Implementa lo stop dei componenti
                    self.streamblur_state['running'] = False
                    return jsonify({
                        'success': True,
                        'message': 'Motore StreamBlur fermato'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Motore non in esecuzione'
                    })
                    
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 400
    
    def set_components(self, camera_manager, ai_processor, effects_processor, 
                      virtual_camera, performance_monitor):
        """Imposta i riferimenti ai componenti principali"""
        self.camera_manager = camera_manager
        self.ai_processor = ai_processor
        self.effects_processor = effects_processor
        self.virtual_camera = virtual_camera
        self.performance_monitor = performance_monitor
    
    def start_server(self):
        """Avvia il server HTTP in un thread separato"""
        def run_server():
            print(f"🌐 API Server in avvio su porta {self.port}...")
            self.app.run(host='127.0.0.1', port=self.port, debug=False, threaded=True)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        print(f"✅ API Server avviato su http://127.0.0.1:{self.port}")
        return server_thread
    
    def update_running_state(self, running: bool):
        """Aggiorna lo stato di esecuzione"""
        self.streamblur_state['running'] = running

# Singleton per accesso globale
api_server = None

def get_api_server(port: int = 8080) -> StreamBlurAPIServer:
    """Ottieni l'istanza singleton del server API"""
    global api_server
    if api_server is None:
        api_server = StreamBlurAPIServer(port)
    return api_server
