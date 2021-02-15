import msvcrt as m
from wgups.objects.package import Package
from wgups.ui.cli import GUI
from wgups.controller.delivery_controller import DeliveryController
import time

def get_any_key_prompt():
    print("\n\nPress any key to continue...", end="\r")
    m.getch()
    print("Loading information hud....")

def main_loop(cli, data_controller, fast_mode = False):
    try:
        while True:
            cli.tick()
            data_controller.tick()
            if fast_mode is False:
                time.sleep(1)

    except KeyboardInterrupt:
        while True:
            package_id = input("\u001b[31m(Type q to exit)\u001b[0m Enter the Package #: ")
            if str.lower(package_id) == "q":
                cli.exit()
                return
            try:
                if 0 < int(package_id) < 41:
                    cli.show_package(Package.package_list[int(package_id) - 1])
                    get_any_key_prompt()
                    break
                else:
                    print("Enter a package number between 1-40 or q to exit.")
            except ValueError:
                print("Enter a package number between 1-40 or q to exit.")

        main_loop(cli, data_controller)


if __name__ == '__main__':
    # Initialize GUI and data controller objects
    cli = GUI()
    data_controller = DeliveryController()

    # Load objects before starting cli gui and running data logic loop
    data_controller.start()

    while True:
        main_loop(cli, data_controller)