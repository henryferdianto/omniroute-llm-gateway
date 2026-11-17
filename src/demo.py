from src.router_core import AllProvidersFailed, ModelSpec, route


def flaky(model: ModelSpec, prompt: str) -> str:
    if model.name == "frontier":
        raise TimeoutError("provider timed out")
    return f"answered by {model.name}"


def main():
    for complexity in ("low", "medium", "high"):
        result = route("Summarise the quarterly report", complexity)
        print(complexity, "->", result["model"])
    print("fallback ->", route("hard task", "high", flaky)["model"])
    try:
        route("x", "high", lambda m, p: (_ for _ in ()).throw(RuntimeError("down")))
    except AllProvidersFailed as exc:
        print("all providers failed as expected:", len(exc.args[0]), "errors")


if __name__ == "__main__":
    main()
