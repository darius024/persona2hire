"""Main entry point for the Persona2Hire application."""

from .gui.main_window import create_main_window


def main():
    """Run the Persona2Hire application."""
    app = create_main_window()
    app.run()


if __name__ == "__main__":
    main()
