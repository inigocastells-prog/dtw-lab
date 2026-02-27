from pathlib import Path
from typing import Callable

try:
    import uvicorn
except ModuleNotFoundError:  # pragma: no cover - fallback for test environments without uvicorn
    uvicorn = None

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import FileResponse
except ModuleNotFoundError:  # pragma: no cover - lightweight fallback for import-only tests
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str):
            self.status_code = status_code
            self.detail = detail
            super().__init__(detail)

    class FileResponse:
        def __init__(self, path: Path, media_type: str = "", filename: str = ""):
            self.path = path
            self.media_type = media_type
            self.filename = filename

    class FastAPI:
        def get(self, *_args, **_kwargs) -> Callable:
            def decorator(func: Callable) -> Callable:
                return func

            return decorator
try:
    from dtw_lab.lab1 import (
        read_csv_from_google_drive,
        visualize_data,
        calculate_statistic,
        clean_data,
        encode_categorical_vars,
    )
except ModuleNotFoundError:  # pragma: no cover - allows running tests via src.* imports
    from .lab1 import (  # type: ignore
        read_csv_from_google_drive,
        visualize_data,
        calculate_statistic,
        clean_data,
        encode_categorical_vars,
    )

# Initialize FastAPI application instance
# This creates our main application object that will handle all routing and middleware
app = FastAPI()
GOOGLE_DRIVE_FILE_ID = "1eKiAZKbWTnrcGs3bqdhINo1E4rBBpglo"

# Server deployment configuration function. We specify on what port we serve, and what IPs we listen to.
def run_server(port: int = 80, reload: bool = False, host: str = "127.0.0.1"):
    if uvicorn is None:
        raise RuntimeError("uvicorn is required to run the server.")
    uvicorn.run("dtw_lab.lab2:app", port=port, reload=reload, host=host)

# Wrapper functions for script entry points
def run_server_dev():
    """Development server with hot reload on port 8000"""
    run_server(port=8000, reload=True)

def run_server_prod():
    """Production server on all interfaces"""
    run_server(reload=False, host='0.0.0.0')

# Define an entry point to our application.
@app.get("/")
def main_route():
    return {"message": "Hello world"}

@app.get("/statistic/{measure}/{column}")
def get_statistic(measure: str, column: str):
    # Read the CSV data, clean the data, and calculate the statistic.
    df = clean_data(read_csv_from_google_drive(GOOGLE_DRIVE_FILE_ID))

    if column not in df.columns:
        raise HTTPException(status_code=404, detail=f"Column '{column}' not found")

    try:
        value = calculate_statistic(measure, df[column])
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    # Keep output JSON-serializable, including mode values when they are pandas scalars.
    if hasattr(value, "item"):
        value = value.item()

    return {"measure": measure, "column": column, "value": value}

@app.get("/visualize/{graph_type}")
def get_visualization(graph_type: str):
    # Read the CSV data, clean the data, and visualize it.
    # This should create 3 files in the graphs folder.
    # Based on the graph_type input, return the corresponding image
    # HINT: Use FileResponse
    graphs_dir = Path("graphs")
    graphs_dir.mkdir(parents=True, exist_ok=True)

    df = clean_data(read_csv_from_google_drive(GOOGLE_DRIVE_FILE_ID))
    visualize_data(df)

    graph_paths = {
        "scatter": graphs_dir / "scatter_plots.png",
        "scatter_plots": graphs_dir / "scatter_plots.png",
        "boxplot": graphs_dir / "boxplots.png",
        "boxplots": graphs_dir / "boxplots.png",
        "histogram": graphs_dir / "histograms.png",
        "histograms": graphs_dir / "histograms.png",
    }

    image_path = graph_paths.get(graph_type.lower())
    if image_path is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid graph_type. Use scatter, boxplot, or histogram.",
        )
    if not image_path.exists():
        raise HTTPException(status_code=404, detail=f"Graph '{graph_type}' not found")

    return FileResponse(path=image_path, media_type="image/png", filename=image_path.name)

@app.get("/version")
def get_visualization_version():
    # Using the toml library, get the version field from the "pyproject.toml" file and return it.
    project_root = Path(__file__).resolve().parents[2]
    pyproject_path = project_root / "pyproject.toml"
    try:
        import toml

        project_data = toml.load(pyproject_path)
    except ModuleNotFoundError:
        version = None
        for line in pyproject_path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("version ="):
                version = line.split("=", maxsplit=1)[1].strip().strip("'\"")
                break
        project_data = {"project": {"version": version}}
    version = project_data.get("project", {}).get("version")

    if version is None:
        raise HTTPException(status_code=500, detail="Version not found in pyproject.toml")

    return {"version": version}
