# LLM-driven FPGA Design

Undergraduate final-year project: **Research on LLM-driven Intelligent FPGA Design Methods** (大模型驱动的 FPGA 智能设计方法研究).

## Research objectives

- Build a tool interaction workflow for FPGA simulation, synthesis, implementation, and selected board tests, with structured feedback and reproducible records.
- Investigate how LLMs can use tool feedback to propose and refine hardware configurations, filter candidates in stages, and reduce unnecessary evaluations.
- Use an existing parameterized NPU for lightweight Transformer inference as the planned case study, comparing functional correctness, latency, throughput, FPGA resources, and exploration cost under consistent constraints.

These are research objectives, not completed capabilities or experimental results.

## Repository structure

```text
.
|-- README.md
|-- .gitignore
|-- 毕设题目.docx                              # Formal project description
|-- 00_毕设完整实施路线图.md                    # Proposed implementation roadmap
|-- LLM、MCP 与 Vivado 智能设计完整学习笔记.md   # Learning notes and workflow examples
`-- Presentation/
    |-- 本科毕业设计 20261021.pptx              # Research presentation
    |-- build_deck.py                          # Presentation generation script
    |-- render_deck.ps1                        # PowerPoint preview export script
    `-- Preview/                              # Slide preview images
```

## Current status

The repository is at the preparation and study stage. It contains the project description, a proposed research roadmap, learning notes, and a presentation with its supporting scripts and previews. NPU source code, an implemented FPGA automation/LLM loop, optimization experiments, and board validation results are not yet included. Hardware, workloads, tool versions, evaluation budgets, and API choices remain to be confirmed.

The notes include illustrative commands, paths, and example data; they should not be interpreted as verified local execution results.

## Presentation tooling

`Presentation/build_deck.py` uses `python-pptx` and also searches the optional local `.pptx_deps/` directory. `Presentation/render_deck.ps1` uses Microsoft PowerPoint COM automation on Windows. Both scripts currently target the generated filename `本科毕设_目标计划进展.pptx`, which differs from the checked-in presentation filename; review the paths before running them.

Third-party VSIX installers, locally installed dependencies, credentials, temporary files, and Vivado build/cache outputs are excluded from version control. Install external tools separately and keep API credentials outside tracked files.
