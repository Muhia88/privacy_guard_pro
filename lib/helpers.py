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


def get_path_input():
  """Gets a valid file or directory path from the user."""
  while True:
    path = input("Enter the full path to a file or directory: ").strip()
    #normalizes common user input artifacts like surrounding quotes, ~, and path separators
    path = _normalize_path(path)
    if os.path.exists(path):
      return path
    console.print(f"[bold red]Error: Path does not exist: {path}. Please try again.[/bold red]")

def _normalize_path(path):
  """Normalize a user-entered path string.
  Returns the normalized path string.
  """
  if not path:
    return path
  p = path.strip()
  #removes surrounding quotes if present
  if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
    p = p[1:-1]
  p = os.path.expanduser(p)

  #converts path like C:\Users\... to the
  #WSL-mounted path (/mnt/c/Users/...) if on WSL
  #making the CLI usable from WSL
  is_wsl = False
  try:
    if os.name == 'posix':
      if 'WSL_DISTRO_NAME' in os.environ:
        is_wsl = True
      else:
        try:
          with open('/proc/version', 'r') as f:
            ver = f.read()
            if 'microsoft' in ver.lower() or 'wsl' in ver.lower():
              is_wsl = True
        except Exception:
          pass
  except Exception:
    is_wsl = False

  m = None
  try:
    #matches drive-letter patterns like C:\... or C:/...
    import re as _re
    m = _re.match(r"^([A-Za-z]):[\\/](.*)$", p)
  except Exception:
    m = None

  if is_wsl and m:
    drive = m.group(1).lower()
    rest = m.group(2).replace('\\', '/')
    p = f"/mnt/{drive}/{rest}"

  #OS-native path representation
  p = os.path.normpath(p)
  return p