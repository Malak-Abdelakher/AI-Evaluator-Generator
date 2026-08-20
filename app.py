from nicegui import ui

from ui.modern_app import build_app


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        root=build_app,
        host="127.0.0.1",
        port=8080,
        title="GROUND//LOOP · AI Evaluator–Generator",
        favicon="🧠",
        dark=True,
        reload=False,
        show=True,
    )