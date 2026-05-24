"""Load test with Redis cache."""

import random

from locust import HttpUser, constant, task


class RedisCacheUser(HttpUser):
    wait_time = constant(0.1)
    search_terms = ["the", "war", "ring", "love", "great", "kill", "dark", "lost"]

    @task
    def search_books(self):
        q = random.choice(self.search_terms)
        page = random.randint(1, 3)
        self.client.get(
            f"/books/search/redis?q={q}&page={page}&page_size=5",
            name="/books/search (REDIS)",
        )
