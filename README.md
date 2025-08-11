# superanalyze

Analyze claims, rigor, and evidence in a doc.

## Motivation

We are now inundated with more content than ever in text form.
And it is even harder to tell what to trust.

Say you have a document that makes an argument or claim.
It might be a deep research report.
Or it might be a transcript of a talk, or anything else where someone makes claims or
takes a stance on a topic.

## Approach

This tool is an experiment in using more structured analysis of a document:

- What are the key claims

- What parts of the document relate to those claims (this is done by paragraph)

- Researching related content using a thinking LLM with web search, and inserting
  annotations on each

- Evaluating the rigor of the claims and if the evidence supports it

- Visualizing these in some way.

Our belief is that

1. **Automatic, easier deep analysis:** While establishing absolute truth of statements
   is very hard, there *are *many statements are arguments that are easy to evaluate for
   rigor or evidence or counter-arguments, and this is the kind of thing that should be
   done automatically and easily within tools.

2. **Using a consistent structure and clear rubrics:** Just asking an AI tool to
   evaluate the strength or rigor of arguments can help, but it’s not consistent and
   it’s different for every person and every prompt.
   We need systematic analyses that break down the process of analyzing a document into
   key steps that can be verified and each run fairly reliably.
   Rubrics (like 1-to-4 scores on clarity or depth, for example) can help with this.

3. **Exposing full details to the reader:** The only way to share this is to give the
   reader both an overview of the assessment and an ability to drill down into the
   document and its sources.

## How It Works

This is built on [kash](https://www.github.com/jlevy/kash) and its
[kash-docs](https://www.github.com/jlevy/kash-docs) kit of tools for docs and analysis.

It’s a good use case for this framework as it has lots of actions that do individual
portions like summarizing, chunking, handling footnotes, etc, but none had been stitched
together properly for a deeper analysis of document claims.

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
