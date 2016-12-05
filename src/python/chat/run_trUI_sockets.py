from chat.ConnectionManagers import SocketAsyncCoreConnectionManager
from chat.Views import TkinterUIView
from chat.Bus import StateBus
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    ctrl = SocketAsyncCoreConnectionManager()
    bus = StateBus(ctrl)
    view = TkinterUIView(bus)
    view.render_loop()