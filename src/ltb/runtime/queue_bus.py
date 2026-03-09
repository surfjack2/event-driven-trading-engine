import threading
import traceback
from collections import defaultdict

from ltb.system.logger import logger


class QueueBus:

    def __init__(self):

        self.subscribers = defaultdict(list)

        self.lock = threading.Lock()

        logger.info("[EVENT BUS INITIALIZED]")


    def subscribe(self, topic, handler):

        with self.lock:

            self.subscribers[topic].append(handler)

            logger.debug(
                "[BUS] handler subscribed topic=%s handler=%s",
                topic,
                handler.__name__
            )


    def publish(self, topic, data):

        handlers = []

        with self.lock:

            handlers = list(self.subscribers.get(topic, []))

        if not handlers:

            logger.debug("[BUS] no subscribers topic=%s", topic)

            return

        for handler in handlers:

            try:

                handler(data)

            except Exception as e:

                logger.error("[BUS ERROR] topic=%s error=%s", topic, e)

                # 어떤 handler에서 터졌는지 출력
                logger.error("[BUS ERROR] handler=%s", handler.__name__)

                # stack trace 출력
                traceback.print_exc()
