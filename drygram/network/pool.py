# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from typing import Dict, List, Optional
from drygram.network.connection import Connection
from drygram.network.proxy import ProxyConnection

class ConnectionPool:
    """
    Socket connections pool manager.

    Parameters
    ----------
    ip : str
        Target server IP address.
    port : int
        Target server port.
    pool_size : int, default=5
        Maximum simultaneous TCP connections allowed.
    use_ipv6 : bool, default=False
        Connect using IPv6.
    proxy_type : Optional[str], default=None
        Proxy type ('socks5', 'http').
    proxy_ip : Optional[str], default=None
        Proxy address.
    proxy_port : Optional[int], default=None
        Proxy port.
    proxy_user : Optional[str], default=None
        Proxy auth username.
    proxy_pass : Optional[str], default=None
        Proxy auth password.
    timeout : float, default=10.0
        Handshake and communication timeout.

    Attributes
    ----------
    ip : str
        Target server IP.
    port : int
        Target server port.
    pool_size : int
        Max connections.
    use_ipv6 : bool
        IPv6 state.
    proxy_type : Optional[str]
        Proxy type.
    proxy_ip : Optional[str]
        Proxy address.
    proxy_port : Optional[int]
        Proxy port.
    proxy_user : Optional[str]
        Proxy username.
    proxy_pass : Optional[str]
        Proxy password.
    timeout : float
        Timeout limit.
    """

    def __init__(
        self,
        ip: str,
        port: int,
        pool_size: int = 5,
        use_ipv6: bool = False,
        proxy_type: Optional[str] = None,
        proxy_ip: Optional[str] = None,
        proxy_port: Optional[int] = None,
        proxy_user: Optional[str] = None,
        proxy_pass: Optional[str] = None,
        timeout: float = 10.0
    ):
        """Initialize the ConnectionPool."""
        self.ip = ip
        self.port = port
        self.pool_size = pool_size
        self.use_ipv6 = use_ipv6
        self.proxy_type = proxy_type
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self.timeout = timeout
        self._pool: List[Connection] = []
        self._acquired: List[Connection] = []
        self._lock = asyncio.Lock()

    async def _create_connection(self) -> Connection:
        """
        Create a connection socket.

        Returns
        -------
        Connection
            Created active connection.
        """
        if self.proxy_type and self.proxy_ip and self.proxy_port:
            conn = ProxyConnection(
                ip=self.ip,
                port=self.port,
                proxy_type=self.proxy_type,
                proxy_ip=self.proxy_ip,
                proxy_port=self.proxy_port,
                username=self.proxy_user,
                password=self.proxy_pass,
                use_ipv6=self.use_ipv6,
                timeout=self.timeout
            )
        else:
            conn = Connection(
                ip=self.ip,
                port=self.port,
                use_ipv6=self.use_ipv6,
                timeout=self.timeout
            )
        await conn.connect()
        return conn

    async def acquire(self) -> Connection:
        """
        Acquire a connection from the pool.

        Returns
        -------
        Connection
            Active connection.

        Raises
        ------
        asyncio.TimeoutError
            If connection limit is reached and timeout expires.
        """
        async with self._lock:
            while self._pool:
                conn = self._pool.pop()
                try:
                    await conn.write(b"")
                    self._acquired.append(conn)
                    return conn
                except Exception:
                    await conn.close()
            
            if len(self._acquired) < self.pool_size:
                conn = await self._create_connection()
                self._acquired.append(conn)
                return conn
            
            raise asyncio.TimeoutError("No connections available in pool")

    async def release(self, conn: Connection) -> None:
        """
        Release a connection back to the pool.

        Parameters
        ----------
        conn : Connection
            Connection to return.
        """
        async with self._lock:
            if conn in self._acquired:
                self._acquired.remove(conn)
                try:
                    await conn.write(b"")
                    self._pool.append(conn)
                except Exception:
                    await conn.close()

    async def close_all(self) -> None:
        """Close all connections inside the pool."""
        async with self._lock:
            for conn in self._pool:
                await conn.close()
            for conn in self._acquired:
                await conn.close()
            self._pool.clear()
            self._acquired.clear()
