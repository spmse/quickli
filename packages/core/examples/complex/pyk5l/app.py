from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from sys import argv

from quickli import Application, Argument, CommandExecutionError, Option, file_path
from quickli import positive_number


@dataclass(frozen=True, slots=True)
class Pod:
    name: str
    namespace: str
    status: str
    ready: str
    restarts: int
    age: str
    node: str
    ip: str
    labels: dict[str, str]


@dataclass(frozen=True, slots=True)
class Service:
    name: str
    namespace: str
    service_type: str
    cluster_ip: str
    external_ip: str
    port: str
    age: str
    selector: dict[str, str]


def one_of(*choices: str):
    allowed = tuple(choices)
    description = "one of: " + ", ".join(allowed)

    def validate(value: object) -> object:
        if value not in allowed:
            raise ValueError(f"Expected one of: {', '.join(allowed)}")
        return value

    validate.description = description
    return validate


def label_selector():
    description = "label selector in key=value form"

    def validate(value: object) -> object:
        if not isinstance(value, str) or "=" not in value:
            raise ValueError("Expected a selector in key=value form")
        key, selected_value = value.split("=", 1)
        if not key or not selected_value:
            raise ValueError("Expected a selector in key=value form")
        return value

    validate.description = description
    return validate


PODS = (
    Pod(
        name="api-7d4f5f6b89-l2xq9",
        namespace="default",
        status="Running",
        ready="1/1",
        restarts=0,
        age="2d",
        node="worker-a",
        ip="10.42.0.12",
        labels={"app": "api", "tier": "backend"},
    ),
    Pod(
        name="web-6b5dd6cb6f-ptm8k",
        namespace="default",
        status="Running",
        ready="1/1",
        restarts=1,
        age="2d",
        node="worker-b",
        ip="10.42.0.21",
        labels={"app": "web", "tier": "frontend"},
    ),
    Pod(
        name="jobs-8b4f68c79-rh2vs",
        namespace="ops",
        status="Pending",
        ready="0/1",
        restarts=0,
        age="14m",
        node="worker-c",
        ip="10.42.1.7",
        labels={"app": "jobs", "tier": "batch"},
    ),
)

SERVICES = (
    Service(
        name="api",
        namespace="default",
        service_type="ClusterIP",
        cluster_ip="10.96.0.10",
        external_ip="<none>",
        port="8080/TCP",
        age="10d",
        selector={"app": "api"},
    ),
    Service(
        name="web",
        namespace="default",
        service_type="NodePort",
        cluster_ip="10.96.0.20",
        external_ip="127.0.0.1",
        port="80:30080/TCP",
        age="10d",
        selector={"app": "web"},
    ),
    Service(
        name="jobs-metrics",
        namespace="ops",
        service_type="ClusterIP",
        cluster_ip="10.96.1.15",
        external_ip="<none>",
        port="9090/TCP",
        age="3d",
        selector={"app": "jobs"},
    ),
)

POD_LOGS = {
    "api-7d4f5f6b89-l2xq9": [
        "2026-05-03T08:40:12Z boot complete",
        "2026-05-03T08:40:15Z listening on :8080",
        "2026-05-03T09:01:02Z handled GET /healthz",
        "2026-05-03T09:10:41Z handled GET /v1/orders",
    ],
    "web-6b5dd6cb6f-ptm8k": [
        "2026-05-03T08:41:00Z assets warmed",
        "2026-05-03T08:41:04Z serving on :80",
        "2026-05-03T09:02:12Z rendered home page",
        "2026-05-03T09:11:08Z rendered status page",
    ],
    "jobs-8b4f68c79-rh2vs": [
        "2026-05-03T09:12:44Z waiting for image pull",
        "2026-05-03T09:13:12Z scheduling retry",
    ],
}

app = Application(
    name="pyk5l",
    description="A minimal kubectl-like CLI built with quickli.",
    global_options=[
        Option("context", short_name="c", default="dev-cluster", help_text="Cluster context."),
        Option("namespace", short_name="n", default="default", help_text="Namespace to target."),
        Option(
            "output",
            short_name="o",
            default="table",
            validators=[one_of("table", "json", "wide")],
            help_text="Output mode for list commands.",
        ),
        Option("verbose", short_name="v", is_flag=True, help_text="Print execution context."),
    ],
)

GET_RESOURCE_VALIDATOR = one_of("pods", "services")
DESCRIBE_RESOURCE_VALIDATOR = one_of("pod")


@app.command(
    name="get",
    help_text="List resources in the selected namespace.",
    arguments=[
        Argument(
            "resource",
            help_text="Resource kind to list, for example pods or services.",
            validators=[GET_RESOURCE_VALIDATOR],
        )
    ],
    options=[
        Option(
            "selector",
            short_name="l",
            multiple=True,
            validators=[label_selector()],
            help_text="Filter pods with one or more label selectors.",
        ),
        Option(
            "status",
            short_name="s",
            validators=[one_of("Running", "Pending", "CrashLoopBackOff")],
            help_text="Filter pods by status.",
        ),
        Option(
            "service-type",
            short_name="t",
            validators=[one_of("ClusterIP", "NodePort", "LoadBalancer")],
            help_text="Filter services by type.",
        ),
    ],
)
def get(
    resource: str,
    selector: list[str] | None = None,
    status: str | None = None,
    service_type: str | None = None,
    context: str = "dev-cluster",
    namespace: str = "default",
    output: str = "table",
    verbose: bool = False,
) -> str:
    if resource == "pods":
        pods = [pod for pod in PODS if pod.namespace == namespace]
        if status is not None:
            pods = [pod for pod in pods if pod.status == status]
        if selector:
            pods = [pod for pod in pods if _matches_selectors(pod.labels, selector)]
        rendered = _render_pod_list(pods, output)
        return _with_context(rendered, context, namespace, verbose)

    services = [service for service in SERVICES if service.namespace == namespace]
    if service_type is not None:
        services = [service for service in services if service.service_type == service_type]

    if selector:
        services = [
            service for service in services if _matches_selectors(service.selector, selector)
        ]

    rendered = _render_service_list(services, output)
    return _with_context(rendered, context, namespace, verbose)


@app.command(
    name="describe",
    help_text="Show detailed information for one resource.",
    arguments=[
        Argument(
            "resource",
            help_text="Resource kind to describe.",
            validators=[DESCRIBE_RESOURCE_VALIDATOR],
        ),
        Argument("name", help_text="Resource name to describe."),
    ],
)
def describe(
    resource: str,
    name: str,
    context: str = "dev-cluster",
    namespace: str = "default",
    verbose: bool = False,
    output: str = "table",
) -> str:
    del output
    del resource
    pod = _find_pod(name, namespace)
    lines = [
        f"Name:        {pod.name}",
        f"Namespace:   {pod.namespace}",
        f"Status:      {pod.status}",
        f"Ready:       {pod.ready}",
        f"Restarts:    {pod.restarts}",
        f"Node:        {pod.node}",
        f"IP:          {pod.ip}",
        "Labels:",
    ]
    for key, value in sorted(pod.labels.items()):
        lines.append(f"  {key}={value}")
    return _with_context("\n".join(lines), context, namespace, verbose)


@app.command(
    help_text="Print recent log lines for one pod.",
    arguments=[Argument("name", help_text="Pod name to read logs from.")],
    options=[
        Option(
            "tail",
            default=10,
            converter=int,
            validators=[positive_number()],
            help_text="Number of log lines to display.",
        ),
        Option(
            "timestamps",
            short_name="t",
            is_flag=True,
            help_text="Keep RFC3339 timestamps in the output.",
        ),
    ],
)
def logs(
    name: str,
    tail: int = 10,
    timestamps: bool = False,
    context: str = "dev-cluster",
    namespace: str = "default",
    verbose: bool = False,
    output: str = "table",
) -> str:
    del output
    pod = _find_pod(name, namespace)
    lines = list(POD_LOGS.get(pod.name, []))[-tail:]
    if not timestamps:
        lines = [line.split(" ", 1)[1] for line in lines]
    rendered = "\n".join(lines) if lines else "No log lines available."
    return _with_context(rendered, context, namespace, verbose)


@app.command(
    help_text="Preview a manifest file before a simulated apply.",
    arguments=[Argument("manifest", validators=[file_path()])],
    options=[
        Option(
            "dry-run",
            short_name="d",
            is_flag=True,
            help_text="Print the simulated action without changing state.",
        )
    ],
)
def apply(
    manifest: Path,
    dry_run: bool = False,
    context: str = "dev-cluster",
    namespace: str = "default",
    verbose: bool = False,
    output: str = "table",
) -> str:
    del output
    summary = _manifest_summary(manifest)
    mode = "dry-run" if dry_run else "simulated apply"
    lines = [
        f"Mode:        {mode}",
        f"Manifest:    {manifest}",
        f"Resource:    {summary['kind']}/{summary['name']}",
        f"Namespace:   {summary['namespace'] or namespace}",
    ]
    return _with_context("\n".join(lines), context, namespace, verbose)


def _with_context(text: str, context: str, namespace: str, verbose: bool) -> str:
    if not verbose:
        return text
    header = f"context={context} namespace={namespace}"
    return f"{header}\n{text}" if text else header


def _matches_selectors(labels: dict[str, str], selectors: list[str]) -> bool:
    for selector in selectors:
        key, value = selector.split("=", 1)
        if labels.get(key) != value:
            return False
    return True


def _find_pod(name: str, namespace: str) -> Pod:
    for pod in PODS:
        if pod.namespace == namespace and pod.name == name:
            return pod
    raise CommandExecutionError(f"Pod '{name}' was not found in namespace '{namespace}'.")


def _render_pod_list(pods: list[Pod], output: str) -> str:
    if output == "json":
        return json.dumps([asdict(pod) for pod in pods], indent=2, sort_keys=True)

    headers = ["NAME", "READY", "STATUS", "RESTARTS", "AGE"]
    rows = [[pod.name, pod.ready, pod.status, str(pod.restarts), pod.age] for pod in pods]
    if output == "wide":
        headers.extend(["IP", "NODE"])
        rows = [
            [pod.name, pod.ready, pod.status, str(pod.restarts), pod.age, pod.ip, pod.node]
            for pod in pods
        ]
    return _render_table(headers, rows)


def _render_service_list(services: list[Service], output: str) -> str:
    if output == "json":
        return json.dumps([asdict(service) for service in services], indent=2, sort_keys=True)

    headers = ["NAME", "TYPE", "CLUSTER-IP", "EXTERNAL-IP", "PORT", "AGE"]
    rows = [
        [
            service.name,
            service.service_type,
            service.cluster_ip,
            service.external_ip,
            service.port,
            service.age,
        ]
        for service in services
    ]
    if output == "wide":
        headers.append("SELECTOR")
        rows = [
            [
                service.name,
                service.service_type,
                service.cluster_ip,
                service.external_ip,
                service.port,
                service.age,
                _format_labels(service.selector),
            ]
            for service in services
        ]
    return _render_table(headers, rows)


def _render_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "No resources found."

    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    rendered_rows = ["  ".join(value.ljust(widths[index]) for index, value in enumerate(headers))]
    for row in rows:
        rendered_rows.append(
            "  ".join(value.ljust(widths[index]) for index, value in enumerate(row))
        )
    return "\n".join(rendered_rows)


def _format_labels(labels: dict[str, str]) -> str:
    return ",".join(f"{key}={value}" for key, value in sorted(labels.items()))


def _manifest_summary(manifest: Path) -> dict[str, str | None]:
    kind: str | None = None
    name: str | None = None
    namespace: str | None = None
    in_metadata = False

    for raw_line in manifest.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line == "metadata:":
            in_metadata = True
            continue
        if not raw_line.startswith(" "):
            in_metadata = False
        if line.startswith("kind:"):
            kind = line.split(":", 1)[1].strip()
            continue
        if in_metadata and line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
            continue
        if in_metadata and line.startswith("namespace:"):
            namespace = line.split(":", 1)[1].strip()

    return {
        "kind": kind or "Unknown",
        "name": name or manifest.stem,
        "namespace": namespace,
    }


if __name__ == "__main__":
    print(app.run(argv[1:]))
