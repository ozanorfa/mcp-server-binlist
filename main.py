from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("BinLookupServer")

BINLIST_API = "https://lookup.binlist.net"

@mcp.tool()
def lookup_card(bin: str) -> dict:
    """Lookup metadata for a credit/debit card BIN (6-digit Bank Identification Number)."""
    if not (bin.isdigit() and len(bin) == 6):
        return {"error": "Input must be exactly 6 digits. Please enter only the BIN, not the full card number."}

    url = f"{BINLIST_API}/{bin}"
    headers = {"Accept-Version": "3"}

    try:
        response = httpx.get(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"No card found for BIN: {bin}"}
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        return {"error": str(e)}

@mcp.tool()
def validate_bin(bin: str) -> bool:
    """Validate that the input is a 6-digit BIN."""
    return len(bin) >= 6

@mcp.prompt("card://bin-lookup")
def bin_lookup_prompt() -> str:
    """
    A secure system prompt to guide AI behavior during card lookups.
    """
    return (
        "You are a secure card lookup assistant. Ask the user to enter only the first 6 digits of a card (BIN/IIN). "
        "Do not ask for or accept full card numbers. When using the 'lookup_card' tool, only pass 6-digit BINs."
    )

@mcp.resource("card://bin-lookup")
def get_bin_lookup_instruction() -> str:
    """
    A resource that tells the LLM what to ask the user when looking up card information.
    This instructs the model to request only the first 6 digits of a card number (BIN).
    """
    return (
        "To look up card details, ask the user to provide only the first 6 digits of their card number. "
        "These 6 digits are known as the Bank Identification Number (BIN). "
        "Do not ask for or use the full card number. "
        "Once you have a 6-digit BIN, use the 'lookup_card' tool to retrieve card metadata."
    )


if __name__ == "__main__":
    mcp.run_stdio()
