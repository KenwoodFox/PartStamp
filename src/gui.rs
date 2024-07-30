use eframe::egui::{self, CentralPanel, Context, FileDialog, Window};
use stl_io::read_stl;
use std::fs::File;
use std::io::BufReader;

pub fn run_gui() {
    let options = eframe::NativeOptions::default();
    eframe::run_native(
        "3DMark",
        options,
        Box::new(|_cc| Box::new(ThreeDMarkApp::default())),
    );
}

#[derive(Default)]
struct ThreeDMarkApp {
    stl_loaded: bool,
    stl_path: Option<String>,
}

impl eframe::App for ThreeDMarkApp {
    fn update(&mut self, ctx: &Context, _frame: &mut eframe::Frame) {
        CentralPanel::default().show(ctx, |ui| {
            ui.label("Welcome to 3DMark!");

            if ui.button("Load STL File").clicked() {
                if let Some(path) = FileDialog::open_file(None).filter(|p| p.extension().map_or(false, |e| e == "stl")).show_open_single_file() {
                    self.stl_path = Some(path.to_string_lossy().to_string());
                    self.stl_loaded = true;
                }
            }

            if self.stl_loaded {
                ui.label(format!("Loaded STL file: {:?}", self.stl_path));
            }
        });
    }
}
