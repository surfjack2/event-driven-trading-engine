import threading
import traceback
from collections import defaultdict
from queue import Queue, Full, Empty

from ltb.system.logger import logger


class QueueBus:

    MAX_QUEUE_SIZE = 10000
    WORKER_COUNT = 4

    def __init__(self):

        self.subscribers = defaultdict(list)

        self.lock = threading.Lock()

        self.queue = Queue(maxsize=self.MAX_QUEUE_SIZE)

        self.workers = []

        logger.info("[EVENT BUS INITIALIZED]")

        # worker thread 시작
        for i in range(self.WORKER_COUNT):

            t = threading.Thread(
                target=self._worker_loop,
                daemon=True,
                name=f"eventbus-worker-{i}",
            )

            t.start()

            self.workers.append(t)

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

            try:

                self.queue.put_nowait((topic, handler, data))

            except Full:

                logger.warning(
                    "[BUS] queue overflow dropping event topic=%s",
                    topic,
                )

    def _worker_loop(self):

        while True:

            try:

                topic, handler, data = self.queue.get(timeout=1)

                self._safe_execute(topic, handler, data)

                self.queue.task_done()

            except Empty:

                continue

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
