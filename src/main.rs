// use std::path::PathBuf;
use std::fs::File;
use std::io::BufReader;

use log::LevelFilter;

use clap::{Arg, Command};
// use stl_io::{Triangle, Vertex};

// mod gui;


fn main() {
    // First, configure logger
    let mut clog = colog::default_builder(); // Get the default builder
    clog.filter(None, log::LevelFilter::Trace); // Manually set the filter
    clog.init(); // Init

    let matches = Command::new("Partstamp")
        .version("1.0")
        .about("Adds version number to STL files")

        // Arguments
        .arg(Arg::new("path"))

        // Collect matches
        .get_matches();

    // println!(
    //     "path: {:?}",
    //     matches.get_one::<String>("path").expect("required")
    // );


    // Setup the file
    let _file_path = matches.get_one::<String>("path").expect("required");
    log::trace!("Opening file at `{_file_path}`");
    let mut file = File::open(_file_path).expect("Unable to open file");
    log::trace!("Readimng file");
    let mut reader = BufReader::new(file);
    log::trace!("Reader buffered");
    let mut stl = stl_io::read_stl(&mut reader).expect("Failed to read STL");
    log::trace!("Stl loaded");

    // println!("Version: {}", version);
    // println!("Coordinates: ({}, {}, {})", x, y, z);
    // println!("File: {}", file);

    // // Open the STL file
    // let mut file = File::open(file).expect("Unable to open file");
    // let mut reader = BufReader::new(file);
    // let mut stl = stl_io::read_stl(&mut reader).expect("Failed to read STL");

    // // Modify the STL here (add version number at (x, y, z))
    // // This is a placeholder for the actual implementation

    // // Save the modified STL
    // let mut output = File::create("output.stl").expect("Unable to create file");
    // stl_io::write_stl(&mut output, &stl).expect("Failed to write STL");
}
