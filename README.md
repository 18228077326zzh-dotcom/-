# Commerce Automation Portfolio / 电商与研究自动化作品集

Two production-minded, runnable portfolio projects for small businesses and operations teams. Both demos work without paid API keys, use synthetic data by default, include automated tests, and document what they do **not** promise.

两个面向小微企业与运营团队的可运行项目。默认无需付费 API Key，演示数据均为合成数据，并包含自动化测试、安全边界和交付限制。

## Projects / 项目

### 1. E-commerce Lead Automation / 电商线索与客服表格自动化

Turn a sanitized Excel/CSV customer-message sheet into an auditable lead queue: intent classification, reply drafts, follow-up actions, session-only funnel stages, human confirmation, and safe workbook export.

把脱敏客户留言表转换成可审核的线索队列：意向分类、回复草稿、跟进动作、会话内漏斗阶段、人工确认和安全 Excel 导出。

- Offline demo; optional OpenAI-compatible provider behind an explicit feature flag
- XLSX/CSV import, common Chinese encodings, formula-injection protection
- Human review separates AI drafts from confirmed, sendable exports
- Funnel stages: new, contacted, awaiting information, handed off
- 117 automated tests at publication time

[Open project README](projects/ecommerce-lead-automation/README.md)

![E-commerce Lead Automation](projects/ecommerce-lead-automation/screenshots/result.png)

### 2. Market Research Brief / 竞品研究与行业周报助手

Convert a small set of public URLs or pasted source texts into an evidence-linked competitor brief, industry weekly, or content-idea report.

把少量公开网页或粘贴资料整理成带原文证据的竞品简报、行业周报或内容选题报告。

- Synthetic templates work without an API key
- Source-by-source evidence, visible failures, Markdown/JSON/project ZIP export
- DNS and redirect SSRF protection plus response-size and timeout limits
- Real AI is disabled by default and requires an explicit deployment flag
- 47 automated tests at publication time

[Open project README](projects/market-research-brief/README.md)

![Market Research Brief](projects/market-research-brief/screenshots/overview.png)

## Run locally / 本地运行

Each project is independent:

```bash
cd projects/ecommerce-lead-automation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PORT=8501 bash start.sh
```

For the research brief, replace the directory with `projects/market-research-brief`. Both `start.sh` files read `PORT` and bind to `0.0.0.0` for managed deployment.

## Quality and scope / 质量与边界

- Each project includes independent automated tests and Python compilation checks.
- No customer data, live store credentials, API keys, internal logs, or private repository history are included.
- These are portfolio-grade, single-session tools—not claims of production multi-tenant SaaS, guaranteed model accuracy, or guaranteed business outcomes.
- Read [market fit notes](docs/market-fit.md), [delivery boundaries](docs/delivery-boundaries.md), and each project's `SECURITY.md` before adapting them for a client.

## License

Portfolio code is available under the MIT License. Runtime dependencies remain under their own licenses; see the project-level third-party notices.
