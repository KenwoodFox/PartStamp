use eframe::egui;

fn main() {
    // Parse command line arguments
    let args: Vec<String> = std::env::args().collect();
    
    // Check if GUI mode is requested
    if args.iter().any(|arg| arg == "--gui" || arg == "-g") {
        run_gui_mode( &args );
    } else {
        run_cli_mode( &args );
    }
}

fn run_cli_mode( args: &Vec<String> ) {
    println!("Running partstamp version 0.1.0");
    println!("you used args: {:?}", args);
}

fn run_gui_mode( args: &Vec<String> ) {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default().with_inner_size([400.0, 300.0]),
        ..Default::default()
    };
    
    eframe::run_native(
        "PartStamp",
        options,
        Box::new(|_cc| Box::new(PartStampApp::default())),
    )
    .unwrap();
}

#[derive(Default)]
struct PartStampApp {}

impl eframe::App for PartStampApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.heading("Hello, world!");
            ui.label("Running in GUI mode");
        });
    }
}

