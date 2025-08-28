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

def display_profiles(profiles):
  """Displays scrubbing profiles in a table."""
  if not profiles:
    console.print("[yellow]No profiles found.[/yellow]")
    return
    
  table = Table(title="Scrubbing Profiles", show_header=True, header_style="bold magenta")
  table.add_column("ID", style="dim", width=5)
  table.add_column("Name")
  table.add_column("Description")
  table.add_column("Tags to Remove")

  for profile in profiles:
    tags = ", ".join([tag.tag_name for tag in profile.tags_to_remove])
    table.add_row(str(profile.id), profile.name, profile.description, tags)
  
  console.print(table)
