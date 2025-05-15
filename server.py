from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP
from mpd import MPDClient

client = MPDClient()

@asynccontextmanager
async def lifespan(app: FastMCP):
    # Startup logic
    print("MCP server is starting...")
    
    # MPDClient config
    client.timeout = 10  # Set timeout
    client.idletimeout = None
    client.connect("localhost", 6600)  # Connect to MPD server
    print(f"Connected to MPD version: {client.mpd_version}")  # Check MPD version
    print(f"Test search for artist: {client.find('artist', 'Komak The Maid')}")  # Search for songs

    yield

    # Shutdown logic
    print("MCP server is shutting down...")
    client.close()  # Close connection
    client.disconnect()  # Disconnect

mcp = FastMCP("MCP for Music Player Daemon", lifespan = lifespan)

@mcp.tool()
def play():
    return client.play()

@mcp.tool()
def pause():
    return client.pause()
