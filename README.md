# Multi-Provider LLM Gateway & Resilient Routing Architecture

> **Dynamic multi-LLM routing with failover, rate-limit handling and observability**

## Overview

A unified gateway that routes inference requests across multiple foundation models based on task complexity, latency and token cost, with automatic failover and centralized observability for downstream agent workflows.

## Approach

1. **Provider abstraction**: normalize heterogeneous LLM APIs behind one interface.
2. **Routing policy**: score candidate models by cost, latency and task complexity.
3. **Resilience**: exponential-backoff retries, circuit breaking and ordered fallback.
4. **Observability**: structured logs and per-provider metrics (latency, errors, tokens).
5. **Configuration**: declarative provider/model registry in YAML.

## Repository Structure

```
omniroute-llm-gateway/
├── router.py                 # routing + fallback engine
├── providers.py              # provider adapters
├── config/providers.example.yaml
├── requirements.txt
└── README.md
```

## Tech Stack

`Python` · `FastAPI` · `httpx` · `PyYAML` · `pydantic`

## Getting Started

```bash
git clone https://github.com/henryferdianto/omniroute-llm-gateway.git
cd omniroute-llm-gateway
pip install -r requirements.txt
```

```bash
cp config/providers.example.yaml config/providers.yaml  # add your API keys
python -m uvicorn router:app --reload
# POST /route {"prompt": "...", "complexity": "medium"}
```

## Project Status

This repository contains the project documentation and a runnable implementation
skeleton. Scripts are structured so that each pipeline stage can be executed and
extended independently. Update the configuration and data paths to run against
your own datasets.

## License

MIT License — see [LICENSE](LICENSE).


---

**Author:** Rifky Henry Ferdianto — Data Science undergraduate at ITERA  
GitHub: [@henryferdianto](https://github.com/henryferdianto) · Portfolio: [rifky-henry-ferdianto](https://github.com/henryferdianto/rifky-henry-ferdianto)
