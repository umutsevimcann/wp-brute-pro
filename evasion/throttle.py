"""Smart throttle — ban detection, auto slowdown, proxy rotation"""
import time


class Throttle:
    def __init__(self, initial_delay=2.0, batch_size=50):
        self.delay = initial_delay
        self.batch_size = batch_size
        self.initial_batch_size = batch_size
        self.min_delay = 0.5
        self.max_delay = 60.0
        self.consecutive_ok = 0
        self.consecutive_fail = 0
        self.total_requests = 0
        self.total_blocks = 0
        self.ban_count = 0

    def success(self):
        self.consecutive_ok += 1
        self.consecutive_fail = 0
        self.total_requests += 1
        # 5 successful batches → speed up
        if self.consecutive_ok >= 5 and self.delay > self.min_delay:
            self.delay = max(self.min_delay, self.delay - 0.3)
            self.consecutive_ok = 0
        # Restore batch size
        if self.consecutive_ok >= 10 and self.batch_size < self.initial_batch_size:
            self.batch_size = min(self.initial_batch_size, self.batch_size + 10)

    def blocked(self, status_code):
        self.consecutive_fail += 1
        self.consecutive_ok = 0
        self.total_blocks += 1

        if status_code == 429:
            self.delay = min(self.max_delay, self.delay * 2)
            return 60
        elif status_code == 403:
            self.delay = min(self.max_delay, self.delay * 2)
            return 60
        elif status_code == 503:
            self.delay = min(self.max_delay, self.delay * 3)
            self.batch_size = max(10, self.batch_size // 2)
            return 120
        else:
            self.delay = min(self.max_delay, self.delay * 1.5)
            return 30

    def timeout(self):
        self.consecutive_fail += 1
        self.delay = min(self.max_delay, self.delay * 3)
        return 60

    def is_banned(self):
        return self.consecutive_fail >= 3

    def mark_ban(self):
        self.ban_count += 1
        self.consecutive_fail = 0
        self.delay = max(2.0, self.delay)  # reset delay after ban
        self.batch_size = max(20, self.batch_size - 10)  # reduce batch

    def wait(self):
        time.sleep(self.delay)

    def wait_penalty(self, seconds):
        time.sleep(seconds)

    def stats(self):
        return {
            "delay": round(self.delay, 1),
            "batch_size": self.batch_size,
            "total_requests": self.total_requests,
            "total_blocks": self.total_blocks,
            "ban_count": self.ban_count,
        }
