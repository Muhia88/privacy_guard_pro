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
      
