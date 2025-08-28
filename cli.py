import sys
from lib.db.database import get_db_session
from lib.db.models import Profile, FileLog
from lib.helpers import (
    console,
    display_main_menu,
)

class CLI:
  def __init__(self):
    self.session = get_db_session()

  def run(self):
    """Main application loop."""
    console.print("[bold green]Welcome to Privacy Guard Pro![/bold green]")

    while True:
      display_main_menu()
      choice = input("> ")
      if choice == "1":
        self.handle_scrub_files()
      elif choice == "2":
        self.handle_manage_profiles()
      elif choice == "3":
        self.handle_view_audit_trail()
      elif choice == "4":
        console.print("[bold]Goodbye![/bold]")
        sys.exit()
      else:
        console.print("[bold red]Invalid choice. Please try again.[/bold red]")
