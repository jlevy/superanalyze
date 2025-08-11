from __future__ import annotations

import argparse
import logging
import sys
from importlib.metadata import version
from pathlib import Path
from textwrap import dedent

from clideps.utils.readable_argparse import ReadableColorFormatter
from kash.config.settings import DEFAULT_MCP_SERVER_PORT
from prettyfmt import fmt_path
from rich import print as rprint

from superanalyze.analysis_commands import run_analysis

log = logging.getLogger(__name__)

APP_NAME = "superanalyze"

DESCRIPTION = """Analyze claims, rigor, and evidence in a doc."""

DEFAULT_WS = "./superanalyze"


def get_app_version() -> str:
    try:
        return "v" + version(APP_NAME)
    except Exception:
        return "unknown"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=ReadableColorFormatter,
        epilog=dedent((__doc__ or "") + "\n\n" + f"{APP_NAME} {get_app_version()}"),
        description=DESCRIPTION,
    )
    parser.add_argument("--version", action="version", version=f"{APP_NAME} {get_app_version()}")

    # Input argument (required unless --mcp is used)
    parser.add_argument("input", type=str, nargs="?", help="Path or URL to the document to analyze")

    # Analysis options
    parser.add_argument(
        "--no_minify",
        action="store_true",
        help="Skip HTML minification step",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Automatically open the results in a browser after analysis",
    )

    # Common arguments
    parser.add_argument(
        "--workspace",
        type=str,
        default=DEFAULT_WS,
        help="the workspace directory to use for files, metadata, and cache",
    )
    parser.add_argument(
        "--rerun", action="store_true", help="rerun actions even if the outputs already exist"
    )

    # MCP mode
    parser.add_argument(
        "--mcp",
        action="store_true",
        help="Run as an MCP server instead of analyzing",
    )
    parser.add_argument(
        "--sse",
        action="store_true",
        help=f"Run as an SSE MCP server at: http://127.0.0.1:{DEFAULT_MCP_SERVER_PORT} (implies --mcp)",
    )
    parser.add_argument(
        "--logs",
        action="store_true",
        help="Just tail the logs from the MCP server in the terminal (implies --mcp)",
    )

    return parser


def display_results(base_dir: Path, md_path: Path, html_path: Path, show: bool = False) -> None:
    """Display the results of analysis to the user."""

    from kash.commands.base.show_command import show as show_command

    rprint(
        dedent(f"""
            [green]All done![/green]

            All results are stored the workspace:

                [yellow]{fmt_path(base_dir)}[/yellow]

            Cleanly formatted Markdown (with a few HTML tags for citations) is at:

                [yellow]{fmt_path(md_path)}[/yellow]

            Browser-ready HTML is at:

                [yellow]{fmt_path(html_path)}[/yellow]

            You can explore the workspace further using the kash shell if needed.
            """)
    )

    if show:
        show_command(html_path)


def main() -> None:
    # Set up kash logging
    from kash.config.settings import LogLevel
    from kash.config.setup import kash_setup

    kash_setup(rich_logging=True, console_log_level=LogLevel.warning)

    parser = build_parser()
    args = parser.parse_args()

    # Auto-enable MCP mode if --sse or --logs is used
    if args.sse or args.logs:
        args.mcp = True

    # Run as an MCP server
    if args.mcp:
        from kash.mcp.mcp_main import McpMode, run_mcp_server
        from kash.mcp.mcp_server_commands import mcp_logs

        if args.logs:
            mcp_logs(follow=True, all=True)
        else:
            mcp_mode = McpMode.standalone_sse if args.sse else McpMode.standalone_stdio
            # For MCP, expose the analyze_document_claims action
            action_names = ["analyze_document_claims"]
            run_mcp_server(mcp_mode, proxy_to=None, tool_names=action_names)
        sys.exit(0)

    # Validate that input is provided for analysis
    if not args.input:
        parser.error("Input path or URL is required unless --mcp is specified")

    # Handle analysis
    try:
        md_path, html_path = run_analysis(
            Path(args.workspace).resolve(),
            args.input,
            args.no_minify,
        )
        display_results(Path(args.workspace), md_path, html_path, show=args.show)
    except Exception as e:
        log.error("Error running analysis", exc_info=e)
        rprint(f"[red]Error: {e}[/red]")

        from kash.config.logger import get_log_settings

        log_file = get_log_settings().log_file_path
        rprint(f"[bright_black]See logs for more details: {fmt_path(log_file)}[/bright_black]")
        sys.exit(1)


if __name__ == "__main__":
    main()
