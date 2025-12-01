from time import time

from paho.mqtt.client import Client


class Accumulator:
    def __init__(self, db, models):
        self.phs = []
        self.last_ph = time()
        self.stirrings = []
        self.last_stirring = time()
        self.temps = []
        self.last_temp = time()
        self.db = db
        self.models = models

    def append_ph(self, value):
        self.phs.append(value)
        self._check_and_store_ph()

    def append_stirring(self, value):
        self.stirrings.append(value)
        self._check_and_store_stirring()

    def append_temp(self, value):
        self.temps.append(value)
        self._check_and_store_temp()

    def _check_and_store_ph(self):
        if len(self.phs) > 0 and (time() - self.last_ph) > 1.0:
            average = sum(self.phs) / len(self.phs)
            ph_record = self.models["PH"](int(average), self.models["datetime"].now())
            self.db.session.add(ph_record)
            self.db.session.commit()
            self.phs = []
            self.last_ph = time()

    def _check_and_store_stirring(self):
        if len(self.stirrings) > 0 and (time() - self.last_stirring) > 1.0:
            average = sum(self.stirrings) / len(self.stirrings)
            stirring_record = self.models["Stirring"](
                int(average), self.models["datetime"].now()
            )
            self.db.session.add(stirring_record)
            self.db.session.commit()
            self.stirrings = []
            self.last_stirring = time()

    def _check_and_store_temp(self):
        if len(self.temps) > 0 and (time() - self.last_temp) > 1.0:
            average = sum(self.temps) / len(self.temps)
            temp_record = self.models["Temperature"](
                int(average), self.models["datetime"].now()
            )
            self.db.session.add(temp_record)
            self.db.session.commit()
            self.temps = []
            self.last_temp = time()


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    topic = msg.topic
    if topic == "2025-engf0002/data/ph":
        accumulator.append_ph(float(payload))
    elif topic == "2025-engf0002/data/stirring":
        accumulator.append_stirring(float(payload))
    elif topic == "2025-engf0002/data/temp":
        accumulator.append_temp(float(payload))


def on_set(device_name: str, value: int, mqtt: Client):
    if device_name == "temp":
        mqtt.publish("2025-engf0002/data/temp/action", f"{value}")
    if device_name == "ph":
        mqtt.publish("2025-engf0002/data/ph/action", f"{value}")
    if device_name == "stirring":
        mqtt.publish("2025-engf0002/data/stirring/action", f"{value}")


accumulator = None


def init_accumulator(db, models):
    global accumulator
    accumulator = Accumulator(db, models)
