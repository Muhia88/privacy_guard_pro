#rich is responsible for styling
import os
from rich.console import Console
from rich.table import Table

console = Console()

def display_main_menu():
  """Prints the main menu of the application using rich for styling."""
  console.print("\n[bold cyan]=== Privacy Guard Pro ===[/bold cyan]")

  #holds menu options
  menu_items = {
    "1": "Scrub Files",
    "2": "Manage Profiles",
    "3": "View Audit Trail",
    "4": "Exit"
  }
  
  for key, value in menu_items.items():
    #Prints each option with the number in green
    console.print(f"[green]{key}[/green]. {value}")
  #separator line
  console.print("-" * 25)
