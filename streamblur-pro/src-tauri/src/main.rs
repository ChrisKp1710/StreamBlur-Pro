// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Command, Stdio};
use std::sync::{Arc, Mutex};
use tauri::State;
use serde::{Deserialize, Serialize};

// Strutture dati per comunicazione con Python
#[derive(Debug, Serialize, Deserialize)]
struct StreamBlurStatus {
    running: bool,
    fps: f32,
    cpu_usage: f32,
    memory_usage: f32,
}

#[derive(Debug, Serialize, Deserialize)]
struct BlurSettings {
    intensity: u8,
    enabled: bool,
}

#[derive(Debug, Serialize, Deserialize)]
struct AISettings {
    performance_mode: bool,
    edge_smoothing: bool,
    temporal_smoothing: bool,
}

// Stato globale dell'applicazione
struct AppState {
    python_process: Arc<Mutex<Option<std::process::Child>>>,
    status: Arc<Mutex<StreamBlurStatus>>,
}

// Comandi Tauri
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! StreamBlur Pro is working with Tauri v1! 🎉", name)
}

#[tauri::command]
async fn start_streamblur_engine(state: State<'_, AppState>) -> Result<String, String> {
    // Configura path per StreamBlur Pro Advanced
    let python_path = r"c:\Users\chris\Documents\StreamBlur-Pro\StreamBlur-Python-Core\streamblur_env\Scripts\python.exe";
    let script_path = r"c:\Users\chris\Documents\StreamBlur-Pro\StreamBlur-Python-Core\streamblur_pro_advanced.py";
    
    println!("🚀 Avviando StreamBlur Pro Advanced...");
    
    match Command::new(python_path)
        .arg(script_path)
        .current_dir(r"c:\Users\chris\Documents\StreamBlur-Pro\StreamBlur-Python-Core")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
    {
        Ok(child) => {
            // Aggiorna stato in blocco separato per rilasciare i lock
            {
                let mut process_guard = state.python_process.lock().unwrap();
                *process_guard = Some(child);
                
                let mut status_guard = state.status.lock().unwrap();
                status_guard.running = true;
            } // I lock vengono rilasciati qui
            
            // Aspetta un po' per permettere al server di avviarsi
            tokio::time::sleep(tokio::time::Duration::from_millis(3000)).await;
            
            // Invia comando di start al backend
            let client = reqwest::Client::new();
            match client
                .post("http://127.0.0.1:8080/api/start")
                .json(&serde_json::json!({}))
                .send()
                .await
            {
                Ok(response) => {
                    if response.status().is_success() {
                        Ok("StreamBlur Engine avviato con successo!".to_string())
                    } else {
                        Ok("Server avviato ma motore non si è avviato".to_string())
                    }
                }
                Err(_) => {
                    Ok("Server avviato (controllo connessione in corso...)".to_string())
                }
            }
        }
        Err(e) => {
            println!("❌ Errore avvio engine: {}", e);
            Err(format!("Errore avvio StreamBlur Engine: {}", e))
        }
    }
}

#[tauri::command]
async fn stop_streamblur_engine(state: State<'_, AppState>) -> Result<String, String> {
    println!("🛑 Fermando StreamBlur Engine...");
    
    // Prima invia comando di stop al backend
    let client = reqwest::Client::new();
    let _ = client
        .post("http://127.0.0.1:8080/api/stop")
        .json(&serde_json::json!({}))
        .send()
        .await;
    
    // Poi termina il processo Python
    let mut process_guard = state.python_process.lock().unwrap();
    if let Some(mut child) = process_guard.take() {
        match child.kill() {
            Ok(_) => {
                // Aggiorna stato
                let mut status_guard = state.status.lock().unwrap();
                status_guard.running = false;
                
                Ok("StreamBlur Engine fermato con successo!".to_string())
            }
            Err(e) => Err(format!("Errore fermata engine: {}", e))
        }
    } else {
        Err("Engine non in esecuzione".to_string())
    }
}

#[tauri::command]
async fn get_streamblur_status(state: State<'_, AppState>) -> Result<StreamBlurStatus, String> {
    // Prova a ottenere lo stato dal backend Python
    let client = reqwest::Client::new();
    
    match client
        .get("http://127.0.0.1:8080/api/status")
        .send()
        .await
    {
        Ok(response) => {
            if response.status().is_success() {
                match response.json::<StreamBlurStatus>().await {
                    Ok(status) => {
                        // Aggiorna stato locale
                        let mut local_status = state.status.lock().unwrap();
                        *local_status = StreamBlurStatus {
                            running: status.running,
                            fps: status.fps,
                            cpu_usage: status.cpu_usage,
                            memory_usage: status.memory_usage,
                        };
                        Ok(status)
                    }
                    Err(_) => {
                        // Fallback allo stato locale
                        let status_guard = state.status.lock().unwrap();
                        Ok(StreamBlurStatus {
                            running: status_guard.running,
                            fps: status_guard.fps,
                            cpu_usage: status_guard.cpu_usage,
                            memory_usage: status_guard.memory_usage,
                        })
                    }
                }
            } else {
                // Fallback allo stato locale
                let status_guard = state.status.lock().unwrap();
                Ok(StreamBlurStatus {
                    running: status_guard.running,
                    fps: status_guard.fps,
                    cpu_usage: status_guard.cpu_usage,
                    memory_usage: status_guard.memory_usage,
                })
            }
        }
        Err(_) => {
            // Backend Python non disponibile - usa stato locale
            let status_guard = state.status.lock().unwrap();
            Ok(StreamBlurStatus {
                running: status_guard.running,
                fps: status_guard.fps,
                cpu_usage: status_guard.cpu_usage,
                memory_usage: status_guard.memory_usage,
            })
        }
    }
}

#[tauri::command]
async fn update_blur_settings(intensity: u8, enabled: bool) -> Result<String, String> {
    println!("🎛️ Aggiornando blur: intensity={}, enabled={}", intensity, enabled);
    
    // Chiamata HTTP al backend Python
    let client = reqwest::Client::new();
    let payload = serde_json::json!({
        "strength": intensity as f64,
        "mode": if enabled { "gaussian" } else { "none" }
    });
    
    match client
        .post("http://127.0.0.1:8080/api/blur")
        .json(&payload)
        .send()
        .await
    {
        Ok(response) => {
            if response.status().is_success() {
                Ok(format!("Blur aggiornato: {}% ({})", intensity, if enabled { "ON" } else { "OFF" }))
            } else {
                Err(format!("Errore HTTP: {}", response.status()))
            }
        }
        Err(e) => Err(format!("Errore connessione: {}", e))
    }
}

#[tauri::command]
async fn update_ai_settings(performance_mode: bool, edge_smoothing: bool, temporal_smoothing: bool) -> Result<String, String> {
    println!("🤖 Aggiornando AI: perf={}, edge={}, temporal={}", performance_mode, edge_smoothing, temporal_smoothing);
    
    // Chiamata HTTP al backend Python
    let client = reqwest::Client::new();
    let payload = serde_json::json!({
        "quality": if performance_mode { "high" } else { "medium" },
        "smoothing": if edge_smoothing { 0.8 } else { 0.3 }
    });
    
    match client
        .post("http://127.0.0.1:8080/api/ai")
        .json(&payload)
        .send()
        .await
    {
        Ok(response) => {
            if response.status().is_success() {
                Ok("Impostazioni AI aggiornate".to_string())
            } else {
                Err(format!("Errore HTTP: {}", response.status()))
            }
        }
        Err(e) => Err(format!("Errore connessione: {}", e))
    }
}

fn main() {
    // Inizializza stato globale
    let app_state = AppState {
        python_process: Arc::new(Mutex::new(None)),
        status: Arc::new(Mutex::new(StreamBlurStatus {
            running: false,
            fps: 0.0,
            cpu_usage: 0.0,
            memory_usage: 0.0,
        })),
    };

    tauri::Builder::default()
        .manage(app_state)
        .invoke_handler(tauri::generate_handler![
            greet,
            start_streamblur_engine,
            stop_streamblur_engine,
            get_streamblur_status,
            update_blur_settings,
            update_ai_settings
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}