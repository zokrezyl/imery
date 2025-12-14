# Imery

**Build interactive GUI applications with YAML instead of code.**

Imery lets you create [Dear ImGui](https://github.com/ocornut/imgui) applications using declarative YAML files, powered by [Dear ImGui Bundle](https://github.com/pthom/imgui_bundle) for Python.

## Why Imery?

Traditional GUI development with ImGui requires writing repetitive boilerplate code. Every button, slider, or layout change means modifying and recompiling your application.

**Imery changes this:**
- **Declarative** - Define your UI in YAML, not code
- **Rapid iteration** - Edit layouts without recompiling
- **No programming required** - Create simple UIs with just YAML
- **Modular** - Reusable widget definitions with imports
- **Data-driven** - Separate UI structure from application logic

## Quick Example

Create a simple GUI in `app.yaml`:

```yaml
app:
  window_title: "Hello Imery"
  widget: builtin.text
  data: greeting

data:
  greeting:
    metadata:
      label: "Welcome to Imery!"
```

Run it:

```bash
imery --main app
```

That's it. No Python code, no compilation - just a YAML file describing what you want.

## Who is Imery for?

- **Python developers** who prefer declarative approaches
- **ImGui users** frustrated with boilerplate code
- **Data scientists** needing quick interactive tools
- **Game developers** prototyping UI and tools
- **Anyone** who wants to experiment with ImGui without writing code

## Project Status

⚠️ **Early Alpha** - Imery is experimental. APIs will change, features are incomplete, and breaking changes should be expected. We welcome feedback and contributions!

## Installation

```bash
pip install imery
```

Requires Python 3.12+

## Examples

Check out the [demo](demo/) directory for examples:
- `demo/classic/` - Classic ImGui demo widgets
- `demo/hello-imgui/` - Basic Hello ImGui examples
- `demo/hello-imgui-full/` - Full-featured application layout

Run any demo:

```bash
imery --layouts-path demo/hello-imgui-full --main app
```

## Documentation

Coming soon. For now, explore the examples and YAML files in the demo directories.

## How It Works

1. **Write YAML** - Define your UI structure, widgets, and data
2. **Import modules** - Compose UIs from reusable components
3. **Run** - Imery renders your YAML as a native ImGui application
4. **Iterate** - Change the YAML and see updates immediately

## Contributing

We're in early development and actively seeking feedback:
- Try Imery with your use cases
- Report issues and suggest features
- Share what works and what doesn't

Your input helps shape Imery's direction.

## License

[Add license information]

## Credits

Built on top of:
- [Dear ImGui](https://github.com/ocornut/imgui) by Omar Cornut
- [Dear ImGui Bundle](https://github.com/pthom/imgui_bundle) by Pascal Thomet
- [HelloImGui](https://github.com/pthom/hello_imgui) by Pascal Thomet
