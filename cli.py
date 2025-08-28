import sys
from lib.db.database import get_db_session
from lib.db.models import Profile, FileLog
from lib.helpers import (
    console,
    display_main_menu,
    display_profiles,
    get_path_input,
)

from lib.scrubber import get_metadata, scrub_file

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

  def handle_manage_profiles(self):
    """Displays the sub-menu for managing profiles and handles user choices."""
    while True:
      console.print("\n[bold cyan]--- Manage Profiles ---[/bold cyan]")
      console.print("1. Create New Profile")
      console.print("2. View All Profiles")
      console.print("3. Delete Profile")
      console.print("4. Back to Main Menu")
      choice = input("> ")

      if choice == "1":
        self.create_profile()
      elif choice == "2":
        profiles = Profile.get_all(self.session)
        display_profiles(profiles)
      elif choice == "3":
        self.delete_profile()
      elif choice == "4":
        break #returns to main menu.
      else:
        console.print("[bold red]Invalid choice.[/bold red]")
  
  def create_profile(self):
    """Handles creation of a new profile."""
    try:
      name = input("Enter profile name: ")
      description = input("Enter a short description: ")
      console.print("Enter tag names to remove, comma-separated (e.g., GPSInfo, Make, Model):")
      tags_input = input("> ")
      tags_list = [tag.strip() for tag in tags_input.split(',')]
      
      profile = Profile.create(self.session, name, description, tags_list)
      console.print(f"[green]Profile '{profile.name}' created successfully![/green]")
    except ValueError as e:
      console.print(f"[bold red]Error: {e}[/bold red]")
    except Exception as e:
      console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
      self.session.rollback()

  def delete_profile(self):
    """Handles deletion of a profile."""
    try:
      profile_id = int(input("Enter the ID of the profile to delete: "))
      profile = Profile.find_by_id(self.session, profile_id)
      if profile:
        profile_name = profile.name
        profile.delete(self.session)
        console.print(f"[green]Profile '{profile_name}' deleted successfully.[/green]")
      else:
        console.print("[bold red]Profile not found.[/bold red]")
    except ValueError:
      console.print("[bold red]Invalid ID format.[/bold red]")
    except Exception as e:
      console.print(f"[bold red]An error occurred: {e}[/bold red]")
      self.session.rollback()

  def handle_scrub_files(self):
    """Handles the file scrubbing workflow."""
    path = get_path_input()
    
    #determines if path is a file or directory
    if os.path.isfile(path):
      files_to_process = [path]
    else:
      files_to_process = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    if not files_to_process:
      console.print("[yellow]No files found to process.[/yellow]")
      return

    console.print(f"Found {len(files_to_process)} file(s) to process.")
    
    #previews metadata of the first file if several
    metadata, error = get_metadata(files_to_process[0])
    if error and "No EXIF" not in error:
      console.print(f"[bold red]{error}[/bold red]")
      return
    display_metadata(metadata)

    #Choose scrubbing method
    console.print("\n[bold]How would you like to scrub?[/bold]")
    console.print("1. Use a Profile")
    console.print("2. Remove All Metadata")
    console.print("3. Select Tags Manually")
    scrub_choice = input("> ")

    profile_id = None
    tags_to_remove = []
    remove_all = False

    if scrub_choice == "1":
      profile = self.select_profile()
      if not profile: return
      tags_to_remove = [tag.tag_name for tag in profile.tags_to_remove]
      profile_id = profile.id
    elif scrub_choice == "2":
      remove_all = True
    elif scrub_choice == "3":
      console.print("Enter tag names to remove, comma-separated (e.g., GPSInfo, Make, Model):")
      tags_input = input("> ")
      tags_to_remove = [tag.strip() for tag in tags_input.split(',')]
    else:
      console.print("[bold red]Invalid choice.[/bold red]")
      return
      
    #asks user to modify original files or create copies
    in_place_choice = input("Overwrite original files? (This is permanent!) [y/n]: ").lower().strip()
    in_place = in_place_choice == 'y'
    if in_place:
      console.print("[bold yellow]Warning: Original files will be overwritten.[/bold yellow]")
    else:
      console.print("[green]A scrubbed copy of the files will be created.[/green]")

    #process each file
    for file_path in files_to_process:
      self.process_single_file(file_path, tags_to_remove, remove_all, profile_id, in_place)

if __name__ == "__main__":
  app = Cli()
  app.run()