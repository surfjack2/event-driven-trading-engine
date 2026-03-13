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
                "[BUS] subscribed topic=%s handler=%s",
                topic,
                handler.__qualname__,
            )

    def publish(self, topic, data):

        with self.lock:

            handlers = list(self.subscribers.get(topic, []))

        if not handlers:

            logger.debug("[BUS] no subscribers topic=%s", topic)

            return

        for handler in handlers:

            # handler 실행을 별도 thread에서 처리
            t = threading.Thread(
                target=self._safe_execute,
                args=(topic, handler, data),
                daemon=True,
            )

            t.start()

    def _safe_execute(self, topic, handler, data):

        try:

            handler(data)

        except Exception as e:

            logger.error(
                "[BUS ERROR] topic=%s handler=%s error=%s",
                topic,
                handler.__qualname__,
                e,
            )

            traceback.print_exc()
