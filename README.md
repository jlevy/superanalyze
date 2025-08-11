# superanalyze

Analyze claims, rigor, and evidence in a doc.

This is built on [kash](https://www.github.com/jlevy/kash) and its
[kash-docs](https://www.github.com/jlevy/kash-docs) kit of tools for docs and analysis.

## Usage

### Key Setup

See the `env.template` to set up keys (default model is OpenAI).

### Basic Usage

It should work on most file types, including text, HTML, and PDF.

```bash
uv run superanalyze somefile.pdf
```

## MCP Server

Run as an MCP server for integration with other tools.
Once it is in your path:

```bash
# Run as stdio MCP server
superanalyze --mcp

# Run as SSE MCP server at 127.0.0.1:4440
superanalyze --sse

# View MCP server logs
superanalyze --logs
```

Note: Both `--sse` and `--logs` automatically enable MCP mode, so you don’t need to
specify `--mcp` explicitly.

### Claude Desktop Configuration

For Claude Desktop, a config like this should work (adjusted to use your appropriate
home folder):

```json
{
  "mcpServers": {
    "superanalyze": {
      "command": "/Users/levy/.local/bin/superanalyze",
      "args": ["--mcp"]
    }
  }
}
```

## Project Docs

For how to install uv and Python, see [installation.md](installation.md).

For development workflows, see [development.md](development.md).

For instructions on publishing to PyPI, see [publishing.md](publishing.md).

* * *

*This project was built from
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*
