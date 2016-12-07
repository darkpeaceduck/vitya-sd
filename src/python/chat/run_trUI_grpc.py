from chat.ConnectionManagers import GrpcConnectionManager
from chat.Views import TkinterUIView
from chat.Bus import StateBus
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    ctrl = GrpcConnectionManager()
    bus = StateBus(ctrl)
    view = TkinterUIView(bus, connect_after_listen=True)
    view.render_loop()