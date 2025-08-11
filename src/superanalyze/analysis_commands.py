from __future__ import annotations

import logging
from pathlib import Path

# Keep kash imports minimal initially.
from kash.model import Item

from superanalyze.actions.analyze_document_claims import analyze_document_claims

log = logging.getLogger(__name__)


def run_analysis(
    ws_root: Path, url: str, no_minify: bool = False, include_debug: bool = True
) -> tuple[Path, Path]:
    # Import dynamically for faster startup.
    from kash.config.setup import kash_setup
    from kash.config.unified_live import get_unified_live
    from kash.exec import kash_runtime, prepare_action_input

    # Set up kash workspace.
    kash_setup(kash_ws_root=ws_root, rich_logging=True)
    ws_path = ws_root / "workspace"

    # Run all actions in the context of this workspace.
    with kash_runtime(ws_path) as runtime:
        # Show the user the workspace info.
        runtime.workspace.log_workspace_info()

        with get_unified_live().status("Processing…"):
            # Prepare the input and run analysis.
            input = prepare_action_input(url)
            result_item = analyze_document_claims(input.items[0], include_debug=include_debug)

            return format_results(result_item, runtime.workspace.base_dir, no_minify=no_minify)


def format_results(result_item: Item, base_dir: Path, no_minify: bool = False) -> tuple[Path, Path]:
    """
    Format the results of analysis into HTML and ensure proper file paths.

    Args:
        result_item: The analysis result item
        base_dir: Base directory for output files
        no_minify: If True, skip HTML minification

    Returns:
        Tuple of (markdown_path, html_path) for the generated files
    """
    # Import dynamically for faster startup.
    from kash.actions.core.minify_html import minify_html
    from kash.model import Format, ItemType
    from kash.web_gen.template_render import render_web_template
    from kash.workspaces.workspaces import current_ws

    # Generate HTML using simple webpage template
    html_content = render_web_template(
        "youtube_webpage.html.jinja",
        data={
            "title": result_item.title,
            "add_title_h1": True,
            "content_html": result_item.body_as_html(),
            "thumbnail_url": result_item.thumbnail_url,
            "enable_themes": True,
            "show_theme_toggle": False,
        },
    )

    # Create initial HTML item from template
    raw_html_item = result_item.derived_copy(
        type=ItemType.export,
        format=Format.html,
        body=html_content,
    )
    current_ws().save(raw_html_item)

    # Minify HTML if requested
    if not no_minify:
        minified_item = minify_html(raw_html_item)
        html_content = minified_item.body
    else:
        html_content = raw_html_item.body

    # Create final HTML item with the processed content
    html_item = raw_html_item.derived_copy(
        type=ItemType.export,
        format=Format.html,
        body=html_content,
    )
    current_ws().save(html_item)

    # Get file paths from the items
    assert result_item.store_path
    assert html_item.store_path
    assert html_content

    md_path = base_dir / Path(result_item.store_path)
    html_path = base_dir / Path(html_item.store_path)
    html_path.write_text(html_content)

    return md_path, html_path
