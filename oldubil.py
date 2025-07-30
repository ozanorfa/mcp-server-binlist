from mcp.server.fastmcp import FastMCP
import fitz  # PyMuPDF
import os

mcp = FastMCP("OlduBilServer")

# Get current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text.strip()
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"

def load_oldubil_pdf_files() -> dict:
    """Load all local PDF files with 'oldubil' in their name."""
    summaries = {}
    for filename in os.listdir(BASE_DIR):
        if filename.lower().endswith(".pdf") and "oldubil" in filename.lower():
            path = os.path.join(BASE_DIR, filename)
            summaries[filename] = extract_text_from_pdf(path)
    return summaries

@mcp.tool()
def get_oldubil_info() -> dict:
    """
    Return extracted content from local OlduBil-related PDF files.
    """
    data = load_oldubil_pdf_files()
    if not data:
        return {"error": "No OlduBil-related PDF files found in the server directory."}
    return data

@mcp.prompt("oldubil://info")
def oldubil_prompt() -> str:
    return (
        "You are an expert on OlduBil. When asked about OlduBil, use the 'get_oldubil_info' tool. "
        "This tool reads local PDF documents about OlduBil and provides relevant content. "
        "Do not answer based on assumptions—use the tool output only."
    )

@mcp.resource("oldubil://info")
def oldubil_resource() -> str:
    return (
        "To answer questions about OlduBil, use the 'get_oldubil_info' tool. "
        "It reads from local PDF files located in the same directory as this server. "
        "These documents include internal material, and the assistant must rely on them."
    )

if __name__ == "__main__":
    mcp.run()
