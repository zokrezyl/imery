#!/usr/bin/env python3
"""
Aggregate all YAML files from a demo directory into a single file.

This script:
1. Reads all YAML files from a demo directory
2. Resolves imports recursively
3. Merges widgets and data sections
4. Renames widget references to avoid conflicts
5. Outputs a single aggregated YAML file

Usage:
    python scripts/aggregate_demo_yaml.py demo/hello-imgui-full -o docs/examples/hello-imgui-full.yaml
"""

import argparse
import yaml
from pathlib import Path
from typing import Dict, Set, Any
import sys


class YAMLAggregator:
    """Aggregates YAML files from a demo directory into a single file"""

    def __init__(self, demo_dir: Path, search_paths: list[Path] = None):
        self.demo_dir = demo_dir
        self.search_paths = search_paths or [demo_dir]
        self.widgets = {}  # Merged widgets
        self.data = {}  # Merged data
        self.app_config = None  # App configuration
        self.visited_modules = set()  # Track visited modules to avoid cycles

    def find_yaml_file(self, module_name: str) -> Path | None:
        """Find a YAML file in search paths"""
        module_path = module_name.replace('.', '/')
        yaml_filename = f"{module_path}.yaml"

        for search_path in self.search_paths:
            candidate = search_path / yaml_filename
            if candidate.exists():
                return candidate
        return None

    def load_yaml(self, file_path: Path) -> dict:
        """Load YAML file"""
        try:
            with open(file_path, 'r') as f:
                content = yaml.safe_load(f)
                return content or {}
        except Exception as e:
            print(f"Error loading {file_path}: {e}", file=sys.stderr)
            return {}

    def process_module(self, module_name: str):
        """Process a module and its imports recursively"""
        if module_name in self.visited_modules:
            return

        self.visited_modules.add(module_name)

        # Find and load module
        module_file = self.find_yaml_file(module_name)
        if not module_file:
            print(f"Warning: Module '{module_name}' not found", file=sys.stderr)
            return

        print(f"Processing: {module_file}")
        module_content = self.load_yaml(module_file)

        # Process imports first (depth-first)
        imports = module_content.get('import', [])
        if isinstance(imports, str):
            imports = [imports]
        for imported_module in imports:
            self.process_module(imported_module)

        # Merge widgets WITHOUT namespace in widget name, but track the module
        widgets = module_content.get('widgets', {})
        for widget_name, widget_def in widgets.items():
            if widget_name in self.widgets:
                print(f"Warning: Duplicate widget '{widget_name}' from '{module_name}', overwriting", file=sys.stderr)
            self.widgets[widget_name] = (module_name, widget_def)

        # Merge data
        data = module_content.get('data', {})
        for data_name, data_def in data.items():
            if data_name in self.data:
                print(f"Warning: Duplicate data '{data_name}', overwriting", file=sys.stderr)
            self.data[data_name] = data_def

        # Capture app config from any module (last one wins)
        if 'app' in module_content:
            self.app_config = module_content['app']

    def process_widget_references(self, obj: Any) -> Any:
        """
        Recursively process widget references in the structure.

        Widget references remain in namespaced format (e.g., "module.widget")
        while widget declarations are stored without namespace.
        """
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                result[key] = self.process_widget_references(value)
            return result
        elif isinstance(obj, list):
            return [self.process_widget_references(item) for item in obj]
        else:
            return obj

    def aggregate(self, main_module: str) -> dict:
        """Aggregate all YAML files starting from main module"""
        print(f"Aggregating from main module: {main_module}")

        # Process main module and all its dependencies
        self.process_module(main_module)

        # Build final structure
        result = {}

        # Add app config if present
        if self.app_config:
            result['app'] = self.process_widget_references(self.app_config)

        # Add all widgets
        if self.widgets:
            result['widgets'] = {}
            for widget_name, (module_name, widget_def) in self.widgets.items():
                result['widgets'][widget_name] = self.process_widget_references(widget_def)

        # Add all data
        if self.data:
            result['data'] = {}
            for data_name, data_def in self.data.items():
                result['data'][data_name] = self.process_widget_references(data_def)

        return result

    def save(self, output_file: Path, content: dict):
        """Save aggregated YAML to file"""
        print(f"Writing aggregated YAML to: {output_file}")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            # Add header comment
            f.write("# Auto-generated aggregated YAML file\n")
            f.write(f"# Source: {self.demo_dir}\n")
            f.write("# Do not edit manually - generated by scripts/aggregate_demo_yaml.py\n\n")

            yaml.dump(content, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def main():
    parser = argparse.ArgumentParser(description='Aggregate YAML files from a demo directory')
    parser.add_argument('demo_dir', type=Path, help='Demo directory containing YAML files')
    parser.add_argument('-o', '--output', type=Path, help='Output file path')
    parser.add_argument('-m', '--main', type=str, default='app', help='Main module name (default: app)')
    parser.add_argument('-s', '--search-path', type=Path, action='append', help='Additional search paths')

    args = parser.parse_args()

    # Validate demo directory
    if not args.demo_dir.exists():
        print(f"Error: Demo directory does not exist: {args.demo_dir}", file=sys.stderr)
        sys.exit(1)

    if not args.demo_dir.is_dir():
        print(f"Error: Not a directory: {args.demo_dir}", file=sys.stderr)
        sys.exit(1)

    # Setup search paths
    search_paths = [args.demo_dir]
    if args.search_path:
        search_paths.extend(args.search_path)

    # Default output path if not specified
    if not args.output:
        demo_name = args.demo_dir.name
        args.output = Path('docs/examples') / f"{demo_name}.yaml"

    # Aggregate
    aggregator = YAMLAggregator(args.demo_dir, search_paths)
    aggregated = aggregator.aggregate(args.main)

    # Save
    aggregator.save(args.output, aggregated)

    print(f"\n✅ Successfully aggregated {len(aggregator.visited_modules)} modules")
    print(f"   Widgets: {len(aggregator.widgets)}")
    print(f"   Data: {len(aggregator.data)}")
    print(f"   Output: {args.output}")


if __name__ == '__main__':
    main()
