from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import urlopen
from uuid import uuid4

from langchain_core.documents import Document
from nicegui import events, run, ui

from agents.generator.generator_service import GeneratorService
from cache.cache_keys import generator_cache_key, retrieval_cache_key
from cache.generator_cache import GeneratorCache
from config.model_config import GENERATOR_MODEL, OLLAMA_BASE_URL
from knowledge.knowledge_pipeline import KnowledgePipeline
from knowledge.retrieval.context_builder import build_context


PROJECT_ROOT = Path(__file__).resolve().parents[1]
UPLOAD_ROOT = PROJECT_ROOT / "storage" / "uploads" / "ui"

SUPPORTED_UI_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx",
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".cs",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".html",
    ".css",
    ".json",
    ".xml",
    ".sql",
    ".sh",
    ".ps1",
    ".yaml",
    ".yml",
}


APP_CSS = r"""
:root {
    --bg: #070a12;
    --panel: rgba(14, 18, 31, 0.78);
    --panel-strong: rgba(19, 24, 41, 0.94);
    --border: rgba(159, 175, 255, 0.15);
    --text: #f7f8ff;
    --muted: #9aa4bd;
    --purple: #9b87f5;
    --cyan: #5ee7f7;
    --green: #62e6a7;
    --amber: #ffd479;
    --red: #ff7a9a;
}

html, body, #app {
    background: var(--bg) !important;
    color: var(--text);
    min-height: 100%;
}

body {
    background-image:
        radial-gradient(circle at 12% 8%, rgba(139, 92, 246, 0.22), transparent 28%),
        radial-gradient(circle at 88% 15%, rgba(34, 211, 238, 0.14), transparent 24%),
        radial-gradient(circle at 50% 100%, rgba(59, 130, 246, 0.10), transparent 35%),
        linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.018) 1px, transparent 1px);
    background-size: auto, auto, auto, 38px 38px, 38px 38px;
    background-attachment: fixed;
}

.q-layout, .q-page-container, .q-page {
    background: transparent !important;
}

.shell {
    width: min(1580px, calc(100vw - 34px));
    margin: 0 auto;
    padding: 18px 0 34px;
}

.glass {
    background: linear-gradient(145deg, rgba(19, 24, 41, .88), rgba(10, 14, 26, .72));
    border: 1px solid var(--border);
    box-shadow: 0 24px 80px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.035);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 22px;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 22px 24px;
}

.hero::after {
    content: "";
    position: absolute;
    inset: auto -120px -130px auto;
    width: 320px;
    height: 320px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(94,231,247,.13), transparent 64%);
    pointer-events: none;
}

.brand-kicker {
    letter-spacing: .22em;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: 800;
    color: var(--cyan);
}

.brand-title {
    font-size: clamp(30px, 4vw, 54px);
    line-height: 1;
    letter-spacing: -.045em;
    font-weight: 850;
    margin-top: 6px;
}

.brand-title .ghost {
    color: transparent;
    -webkit-text-stroke: 1px rgba(247,248,255,.42);
}

.muted { color: var(--muted); }
.micro { font-size: 11px; color: var(--muted); letter-spacing: .025em; }

.status-pill {
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 7px 10px;
    background: rgba(255,255,255,.025);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .04em;
}

.status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    margin-right: 7px;
    box-shadow: 0 0 12px currentColor;
}

.panel-title {
    font-size: 13px;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #cdd5eb;
}

.panel-subtitle {
    color: var(--muted);
    font-size: 12px;
    margin-top: 2px;
}

.metric-card {
    padding: 15px;
    min-height: 90px;
}

.metric-value {
    font-size: 24px;
    font-weight: 850;
    letter-spacing: -.035em;
}

.metric-label {
    color: var(--muted);
    font-size: 11px;
    margin-top: 3px;
}

.question-box .q-field__control,
.question-box .q-field__native,
.question-box textarea {
    color: #f7f8ff !important;
}

.question-box .q-field__control {
    background: rgba(255,255,255,.026) !important;
    border-radius: 17px !important;
}

.question-box .q-field__control:before {
    border-color: rgba(159,175,255,.18) !important;
}

.ask-button {
    background: linear-gradient(110deg, #7c3aed, #4f46e5 48%, #0891b2) !important;
    border-radius: 14px !important;
    padding: 9px 20px !important;
    box-shadow: 0 10px 35px rgba(99,102,241,.25);
    font-weight: 800;
    letter-spacing: .02em;
}

.secondary-button {
    border: 1px solid rgba(159,175,255,.18) !important;
    background: rgba(255,255,255,.025) !important;
    border-radius: 12px !important;
}

.answer-card {
    position: relative;
    padding: 19px 20px;
    border: 1px solid rgba(139,92,246,.20);
    background: linear-gradient(135deg, rgba(124,58,237,.08), rgba(15,23,42,.55));
    border-radius: 18px;
}

.answer-card::before {
    content: "GENERATOR";
    position: absolute;
    top: -9px;
    left: 16px;
    background: #0c1020;
    border: 1px solid rgba(139,92,246,.30);
    border-radius: 999px;
    padding: 3px 8px;
    color: #c4b5fd;
    font-size: 9px;
    font-weight: 900;
    letter-spacing: .12em;
}

.source-card {
    padding: 14px;
    border-radius: 15px;
    border: 1px solid rgba(94,231,247,.12);
    background: rgba(7,10,18,.42);
}

.source-chip {
    color: #8be9f5;
    border: 1px solid rgba(94,231,247,.18);
    background: rgba(94,231,247,.05);
    border-radius: 999px;
    padding: 3px 8px;
    font-size: 10px;
    font-weight: 800;
}

.upload-zone .q-uploader {
    width: 100%;
    background: rgba(255,255,255,.018) !important;
    border: 1px dashed rgba(159,175,255,.24);
    border-radius: 16px;
    box-shadow: none;
}

.upload-zone .q-uploader__header {
    background: linear-gradient(110deg, rgba(124,58,237,.22), rgba(8,145,178,.14)) !important;
}

.timeline-node {
    border-left: 2px solid rgba(139,92,246,.22);
    padding: 2px 0 15px 15px;
    margin-left: 6px;
    position: relative;
}

.timeline-node::before {
    content: "";
    position: absolute;
    left: -6px;
    top: 3px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #9b87f5;
    box-shadow: 0 0 16px rgba(155,135,245,.7);
}

.scroll-panel {
    max-height: 520px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(159,175,255,.22) transparent;
}

.code-glow {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    color: #91f2ff;
}

@keyframes pulseGlow {
    0%, 100% { opacity: .7; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.08); }
}

.live-orb {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 16px rgba(98,230,167,.8);
    animation: pulseGlow 1.8s ease-in-out infinite;
}

.q-notification {
    border-radius: 14px !important;
    backdrop-filter: blur(14px);
}
"""


@dataclass
class RuntimeServices:
    knowledge: KnowledgePipeline
    generator: GeneratorService


_runtime_services: RuntimeServices | None = None
_runtime_lock = asyncio.Lock()


async def get_services() -> RuntimeServices:
    """Lazy-load heavy models only when the UI actually needs them."""
    global _runtime_services

    if _runtime_services is not None:
        return _runtime_services

    async with _runtime_lock:
        if _runtime_services is None:
            knowledge = await run.io_bound(KnowledgePipeline.create_default)
            generator = GeneratorService(cache=GeneratorCache())
            _runtime_services = RuntimeServices(
                knowledge=knowledge,
                generator=generator,
            )

    return _runtime_services


def _source_name(document: Document) -> str:
    source = str(document.metadata.get("source", "unknown"))
    if source.startswith(("http://", "https://")):
        return source
    return Path(source).name or source


def _source_location(document: Document) -> str:
    metadata = document.metadata
    parts: list[str] = []
    if "page" in metadata:
        parts.append(f"page {metadata['page']}")
    if "slide" in metadata:
        parts.append(f"slide {metadata['slide']}")
    if "chunk_index" in metadata:
        parts.append(f"chunk {metadata['chunk_index']}")
    return " · ".join(parts) or "retrieved chunk"


def _snippet(text: str, limit: int = 420) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def _ollama_is_online() -> bool:
    try:
        with urlopen(f"{OLLAMA_BASE_URL.rstrip('/')}/api/tags", timeout=1.5) as response:
            return 200 <= response.status < 300
    except (OSError, URLError):
        return False


def _status_html(label: str, state: str, color: str) -> str:
    return (
        '<div class="status-pill">'
        f'<span class="status-dot" style="color:{color};background:{color}"></span>'
        f'{label} · {state}'
        '</div>'
    )


def build_app() -> None:
    ui.add_head_html(f"<style>{APP_CSS}</style>")
    ui.colors(
        primary="#8b5cf6",
        secondary="#22d3ee",
        accent="#62e6a7",
        dark="#070a12",
        positive="#62e6a7",
        negative="#ff7a9a",
        warning="#ffd479",
    )

    conversation_id = f"ui-{uuid4().hex}"
    upload_dir = UPLOAD_ROOT / conversation_id
    upload_dir.mkdir(parents=True, exist_ok=True)

    state: dict[str, Any] = {
        "questions": 0,
        "documents": 0,
        "last_retrieval_hit": None,
        "last_generator_hit": None,
    }

    with ui.column().classes("shell gap-4"):
        with ui.row().classes("w-full items-stretch gap-4 flex-wrap"):
            with ui.column().classes("glass hero grow min-w-[620px]"):
                ui.label("ADVANCED LANGCHAIN · GROUNDED AI LAB").classes("brand-kicker")
                ui.html(
                    '<div class="brand-title">GROUND<span class="ghost">//</span>LOOP</div>',
                    sanitize=False,
                )
                ui.label(
                    "External knowledge in. Generator answer out. Every claim traceable. "
                    "Evaluator loop slots in next."
                ).classes("muted text-sm mt-2 max-w-[820px]")
                with ui.row().classes("items-center gap-2 mt-4 flex-wrap"):
                    ui.html('<div class="live-orb"></div>', sanitize=False)
                    ui.label("Generator workbench live").classes("text-xs font-bold")
                    ui.label("•").classes("muted")
                    ui.label(f"Model: {GENERATOR_MODEL}").classes("micro code-glow")
                    ui.label("•").classes("muted")
                    ui.label("Max loop: 4 iterations").classes("micro")

            with ui.column().classes("glass p-4 min-w-[310px] grow"):
                ui.label("SYSTEM FABRIC").classes("panel-title")
                ui.label("Live dependency health").classes("panel-subtitle")
                status_container = ui.row().classes("gap-2 flex-wrap mt-3")
                with status_container:
                    ui.html(_status_html("Redis", "checking", "#ffd479"), sanitize=False)
                    ui.html(_status_html("Ollama", "checking", "#ffd479"), sanitize=False)
                    ui.html(_status_html("Chroma", "ready", "#62e6a7"), sanitize=False)

                async def refresh_health() -> None:
                    redis_ok = False
                    try:
                        services = await get_services()
                        cache = services.knowledge.retriever.cache
                        redis_ok = bool(
                            cache is not None
                            and await run.io_bound(cache.cache.ping)
                        )
                    except Exception:
                        redis_ok = False

                    ollama_ok = await run.io_bound(_ollama_is_online)

                    status_container.clear()
                    with status_container:
                        ui.html(
                            _status_html(
                                "Redis",
                                "online" if redis_ok else "offline",
                                "#62e6a7" if redis_ok else "#ff7a9a",
                            ),
                            sanitize=False,
                        )
                        ui.html(
                            _status_html(
                                "Ollama",
                                "online" if ollama_ok else "offline",
                                "#62e6a7" if ollama_ok else "#ff7a9a",
                            ),
                            sanitize=False,
                        )
                        ui.html(_status_html("Chroma", "ready", "#62e6a7"), sanitize=False)

                ui.button(
                    "Refresh fabric",
                    icon="sync",
                    on_click=refresh_health,
                ).props("flat dense no-caps").classes("secondary-button mt-3")
                ui.timer(0.25, refresh_health, once=True)

        with ui.row().classes("w-full gap-4 items-start flex-wrap"):
            # LEFT: knowledge ingestion + architecture
            with ui.column().classes("glass p-4 gap-4 w-[330px] max-w-full"):
                with ui.column().classes("gap-0"):
                    ui.label("KNOWLEDGE DOCK").classes("panel-title")
                    ui.label("Feed the vector knowledge base").classes("panel-subtitle")

                upload_status = ui.column().classes("gap-2 w-full")

                async def handle_upload(e: events.UploadEventArguments) -> None:
                    safe_name = Path(e.file.name).name
                    extension = Path(safe_name).suffix.lower()

                    if extension not in SUPPORTED_UI_EXTENSIONS:
                        ui.notify(
                            f"{extension or 'This file type'} is not enabled in your branch yet.",
                            type="warning",
                        )
                        return

                    target = upload_dir / safe_name

                    try:
                        await e.file.save(target)
                        services = await get_services()
                        result = await run.io_bound(
                            lambda: services.knowledge.ingest_file(target)
                        )
                        state["documents"] += 1
                        state["last_retrieval_hit"] = None
                        update_metrics()

                        with upload_status:
                            with ui.row().classes("w-full items-center justify-between source-card"):
                                with ui.column().classes("gap-0 min-w-0"):
                                    ui.label(safe_name).classes("text-xs font-bold truncate max-w-[215px]")
                                    ui.label(
                                        f"{result['chunks_stored']} chunks indexed"
                                    ).classes("micro")
                                ui.icon("check_circle", color="positive").classes("text-lg")

                        ui.notify(
                            f"Indexed {safe_name} · retrieval cache invalidated",
                            type="positive",
                        )
                    except Exception as exc:
                        ui.notify(f"Ingestion failed: {exc}", type="negative", multi_line=True)

                with ui.column().classes("upload-zone w-full"):
                    ui.upload(
                        label="Drop knowledge files here",
                        multiple=True,
                        auto_upload=True,
                        max_file_size=25_000_000,
                        on_upload=handle_upload,
                        on_rejected=lambda: ui.notify(
                            "Upload rejected. Max size is 25 MB per file.",
                            type="warning",
                        ),
                    ).props(
                        'accept=".txt,.pdf,.docx,.py,.js,.ts,.jsx,.tsx,.java,.cs,.cpp,.c,.h,.hpp,.html,.css,.json,.xml,.sql,.sh,.ps1,.yaml,.yml"'
                    ).classes("w-full")

                ui.label(
                    "Active now: TXT · PDF · DOCX · source code. "
                    "PPTX · Web · Wikipedia · WAV will light up when Malak's loaders land."
                ).classes("micro")

                ui.separator().classes("opacity-20")
                ui.label("PIPELINE SIGNAL").classes("panel-title")
                for title, detail in [
                    ("01 · INGEST", "loader → normalize → validate"),
                    ("02 · CHUNK", "recursive splitter · overlap preserved"),
                    ("03 · EMBED", "all-MiniLM-L6-v2"),
                    ("04 · RETRIEVE", "Chroma + Redis retrieval cache"),
                    ("05 · GENERATE", "LCEL + Ollama + isolated memory"),
                ]:
                    with ui.column().classes("timeline-node gap-0"):
                        ui.label(title).classes("text-xs font-extrabold")
                        ui.label(detail).classes("micro")

            # CENTER: generator arena
            with ui.column().classes("glass p-5 gap-4 grow min-w-[520px] max-w-full"):
                with ui.row().classes("w-full items-start justify-between gap-3 flex-wrap"):
                    with ui.column().classes("gap-0"):
                        ui.label("GENERATOR ARENA").classes("panel-title")
                        ui.label("Ask only what your ingested knowledge can support").classes("panel-subtitle")
                    ui.badge("GENERATOR-ONLY PREVIEW", color="primary").props("outline")

                question_input = ui.textarea(
                    placeholder=(
                        "Ask a grounded question…\n"
                        "Example: What can Redis be used for?"
                    )
                ).props("outlined autogrow rows=3").classes("question-box w-full")

                with ui.row().classes("items-center gap-2 w-full"):
                    ask_button = ui.button("Run grounded answer", icon="bolt").props(
                        "no-caps unelevated"
                    ).classes("ask-button")
                    clear_button = ui.button("New conversation", icon="refresh").props(
                        "no-caps flat"
                    ).classes("secondary-button")
                    working = ui.spinner("dots", size="32px").classes("ml-2")
                    working.set_visibility(False)

                answer_container = ui.column().classes("w-full gap-3")
                with answer_container:
                    with ui.column().classes("answer-card w-full"):
                        ui.label(
                            "Your grounded answer will appear here. The model is deliberately blocked "
                            "from filling gaps with its own training knowledge."
                        ).classes("muted text-sm")

                # RIGHT-rail content is declared later but referenced by handlers.
                evidence_container: Any = None
                evidence_meta: Any = None

                async def ask_question() -> None:
                    question = (question_input.value or "").strip()
                    if not question:
                        ui.notify("Enter a question first.", type="warning")
                        return

                    ask_button.disable()
                    working.set_visibility(True)

                    try:
                        services = await get_services()
                        retriever_cache = services.knowledge.retriever.cache

                        retrieval_hit = False
                        if retriever_cache is not None:
                            key = retrieval_cache_key(question, 4)
                            retrieval_hit = await run.io_bound(
                                lambda: retriever_cache.cache.exists(key)
                            )

                        documents = await run.io_bound(
                            lambda: services.knowledge.retrieve(question, k=4)
                        )
                        context = build_context(documents)

                        history = services.generator.memory.get_prompt_history(
                            conversation_id,
                            limit=3,
                        )
                        generator_hit = False
                        if services.generator.cache is not None:
                            key = generator_cache_key(
                                question=question,
                                context=context,
                                history=history,
                                feedback="",
                                model=GENERATOR_MODEL,
                            )
                            generator_hit = await run.io_bound(
                                lambda: services.generator.cache.cache.exists(key)
                            )

                        answer = await run.io_bound(
                            lambda: services.generator.generate(
                                question=question,
                                context=context,
                                conversation_id=conversation_id,
                            )
                        )

                        state["questions"] += 1
                        state["last_retrieval_hit"] = retrieval_hit
                        state["last_generator_hit"] = generator_hit
                        update_metrics()

                        answer_container.clear()
                        with answer_container:
                            with ui.column().classes("answer-card w-full"):
                                ui.markdown(answer).classes("text-[15px] leading-7")
                                with ui.row().classes("gap-2 flex-wrap mt-2"):
                                    ui.badge(
                                        "retrieval cache HIT" if retrieval_hit else "retrieval cache MISS",
                                        color="positive" if retrieval_hit else "secondary",
                                    ).props("outline")
                                    ui.badge(
                                        "generator cache HIT" if generator_hit else "generator cache MISS",
                                        color="positive" if generator_hit else "primary",
                                    ).props("outline")
                                    ui.badge(
                                        f"{len(documents)} evidence chunks",
                                        color="secondary",
                                    ).props("outline")

                        if evidence_container is not None:
                            evidence_container.clear()
                            with evidence_container:
                                if not documents:
                                    ui.label("No chunks retrieved.").classes("muted text-sm")
                                for index, document in enumerate(documents, start=1):
                                    with ui.column().classes("source-card w-full gap-2"):
                                        with ui.row().classes("w-full items-center justify-between gap-2"):
                                            ui.label(f"#{index} · {_source_name(document)}").classes(
                                                "text-xs font-extrabold truncate max-w-[240px]"
                                            )
                                            ui.label(_source_location(document)).classes("source-chip")
                                        ui.label(_snippet(document.page_content)).classes(
                                            "micro leading-5"
                                        )

                        if evidence_meta is not None:
                            evidence_meta.set_text(
                                f"{len(documents)} chunks · k=4 · Chroma semantic retrieval"
                            )

                        question_input.value = ""
                    except Exception as exc:
                        ui.notify(
                            f"Generation failed: {exc}",
                            type="negative",
                            multi_line=True,
                            timeout=8000,
                        )
                    finally:
                        working.set_visibility(False)
                        ask_button.enable()

                async def clear_conversation() -> None:
                    try:
                        services = await get_services()
                        services.generator.memory.clear(conversation_id)
                        answer_container.clear()
                        with answer_container:
                            with ui.column().classes("answer-card w-full"):
                                ui.label("Conversation memory cleared. Start a fresh grounded query.").classes(
                                    "muted text-sm"
                                )
                        ui.notify("Generator memory cleared for this conversation.", type="positive")
                    except Exception as exc:
                        ui.notify(f"Could not clear memory: {exc}", type="negative")

                ask_button.on("click", ask_question)
                clear_button.on("click", clear_conversation)
                question_input.on("keydown.enter", ask_question, args=[])

                ui.separator().classes("opacity-20")
                ui.label("EVALUATOR LOOP · SHARED INTEGRATION SLOT").classes("panel-title")
                with ui.row().classes("gap-2 items-center flex-wrap"):
                    for number in range(1, 5):
                        with ui.row().classes("items-center gap-1"):
                            ui.badge(str(number), color="primary" if number == 1 else "grey-8")
                            ui.label("Generate → Evaluate").classes("micro")
                            if number < 4:
                                ui.icon("arrow_forward", size="14px").classes("muted")
                ui.label(
                    "This UI deliberately does not fake Malak's Evaluator. When her service is merged, "
                    "the shared workflow will drive these four slots and stop early on ACCEPT."
                ).classes("micro")

            # RIGHT: evidence and observability
            with ui.column().classes("glass p-4 gap-4 w-[365px] max-w-full"):
                with ui.column().classes("gap-0"):
                    ui.label("EVIDENCE TRACE").classes("panel-title")
                    evidence_meta = ui.label("Awaiting a question").classes("panel-subtitle")

                evidence_container = ui.column().classes("w-full gap-2 scroll-panel")
                with evidence_container:
                    ui.label(
                        "Retrieved chunks will appear here with source and location metadata."
                    ).classes("muted text-sm")

                ui.separator().classes("opacity-20")
                ui.label("RUN TELEMETRY").classes("panel-title")
                metrics = ui.row().classes("w-full gap-2")

                def update_metrics() -> None:
                    metrics.clear()
                    with metrics:
                        with ui.column().classes("metric-card glass grow gap-0"):
                            ui.label(str(state["documents"])).classes("metric-value")
                            ui.label("files indexed this session").classes("metric-label")
                        with ui.column().classes("metric-card glass grow gap-0"):
                            ui.label(str(state["questions"])).classes("metric-value")
                            ui.label("queries this session").classes("metric-label")

                    cache_summary.clear()
                    with cache_summary:
                        retrieval_state = state["last_retrieval_hit"]
                        generator_state = state["last_generator_hit"]
                        ui.label(
                            "Retrieval cache: —"
                            if retrieval_state is None
                            else f"Retrieval cache: {'HIT' if retrieval_state else 'MISS'}"
                        ).classes("micro code-glow")
                        ui.label(
                            "Generator cache: —"
                            if generator_state is None
                            else f"Generator cache: {'HIT' if generator_state else 'MISS'}"
                        ).classes("micro code-glow")

                cache_summary = ui.column().classes("gap-1")
                update_metrics()

                ui.separator().classes("opacity-20")
                with ui.row().classes("items-center gap-2"):
                    ui.icon("shield", color="secondary")
                    with ui.column().classes("gap-0"):
                        ui.label("Grounding guard active").classes("text-xs font-bold")
                        ui.label(
                            "Unsupported questions must return the configured refusal."
                        ).classes("micro")

    ui.label(
        f"Session {conversation_id[-10:]} · local-first · Redis + Chroma + Ollama"
    ).classes("micro text-center w-full pb-4")