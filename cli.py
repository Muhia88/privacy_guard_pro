import sys
from lib.db.database import get_db_session
from lib.db.models import Profile, FileLog
from lib.helpers import (
    console,
    display_main_menu,
    display_profiles,
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