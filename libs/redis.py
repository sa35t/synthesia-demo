import redis


class Redis:
    """
    Connection class for redis
    """

    def __init__(self, app):
        if app:
            self.config = app.config["REDIS"]
        self.redis_conn = None
        self.get_connection()

    def get_connection(self):
        if not self.redis_conn or not self.redis_conn.ping():
            self.redis_conn = redis.Redis(
                host=self.config["host"],
                port=self.config["port"],
                db=self.config["db"],
            )

    def get_key(self, key):
        """
        GET key from redis

        Args:
            key (string): Key to get

        Returns:
            string: Value corresponding to the Key
        """
        self.get_connection()
        return self.redis_conn.get(key)

    def set_key(self, key, value, expiry=None):
        """Set key in redis

        Args:
            key (string): Key
            value (string): Value
            expiry (seconds, optional): Key expiry time. Defaults to None.

        Returns:
            bool: Status if key set or not
        """
        self.get_connection()
        if expiry:
            response = self.redis_conn.setex(key, expiry, value)
        else:
            response = self.redis_conn.set(key, value)
        return response

    def incr_key(self, key):
        """
        Increment key in redis by 1

        Args:
            key (string): Key to increment

        Returns:
            integer: Value corresponding to the Key
        """
        self.get_connection()
        return self.redis_conn.incr(key)

    def exists_key(self, key):
        """
        Increment key in redis by 1

        Args:
            key (string): Key to increment

        Returns:
            integer: Value corresponding to the Key
        """
        self.get_connection()
        return self.redis_conn.exists(key)
