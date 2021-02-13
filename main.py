from wgups.ui.cli import GUI
from wgups.controller.delivery_controller import DeliveryController
import threading

if __name__ == '__main__':
    # Initialize GUI and data controller objects
    cli = GUI()
    data_controller = DeliveryController()

    # Load objects before starting cli gui and running data logic loop
    data_controller.start()

    cli_thread = threading.Thread(target=cli.run)
    data_thread = threading.Thread(target=data_controller.run)

    cli_thread.start()
    data_thread.start()
