import sys
import argparse
from PyQt5.QtWidgets import QApplication
from .stl_tool import STLViewer, engrave_text_on_stl, load_stl


def main():
    # Set up argument parsing for CLI
    parser = argparse.ArgumentParser(description="Partstamp - STL Engraving Tool")
    parser.add_argument(
        "input", help="Input STL file path"
    )  # Changed to positional argument for easier GUI mode triggering
    parser.add_argument("--text", help="Text to engrave")
    parser.add_argument(
        "--position", type=float, nargs=3, help="Position (x, y, z) to engrave the text"
    )
    parser.add_argument("--size", type=float, default=5, help="Size of the text")
    parser.add_argument("--output", help="Output STL file path")

    args = parser.parse_args()

    # If only STL file is passed (no text and no position), launch GUI mode
    if not args.text and not args.position:
        run_gui(args.input)
    else:
        # CLI mode
        if not args.output:
            print("Error: Output file must be specified when engraving text.")
            sys.exit(1)

        stl_mesh = load_stl(args.input)
        engrave_text_on_stl(stl_mesh, args.text, args.position, args.size, args.output)
        print(f"Engraved '{args.text}' onto {args.input} and saved as {args.output}")


def run_gui(stl_file):
    # Initialize the Qt application
    app = QApplication(sys.argv)

    # Load the STL file
    stl_mesh = load_stl(stl_file)

    # Create and show the viewer
    viewer = STLViewer(stl_mesh)
    viewer.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
