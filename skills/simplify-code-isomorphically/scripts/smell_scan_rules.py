"""Conservative source-pattern rules for smell_scan.py."""

from __future__ import annotations

import ast
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


WEB_EXTENSIONS = {".astro", ".js", ".jsx", ".svelte", ".ts", ".tsx"}
REACT_EXTENSIONS = {".jsx", ".tsx"}
UI_EXTENSIONS = {".astro", ".jsx", ".svelte", ".tsx"}
TYPED_JS_EXTENSIONS = {".ts", ".tsx"}
CONFIDENCE_ORDER = {"strong": 0, "medium": 1, "weak": 2}


@dataclass(frozen=True)
class Signal:
    path: str
    line: int
    confidence: str
    kind: str
    message: str


@dataclass(frozen=True)
class LineRule:
    pattern: re.Pattern[str]
    extensions: frozenset[str]
    confidence: str
    kind: str
    message: str


def rule(
    pattern: str,
    extensions: set[str],
    confidence: str,
    kind: str,
    message: str,
) -> LineRule:
    return LineRule(re.compile(pattern), frozenset(extensions), confidence, kind, message)


LINE_RULES = (
    rule(
        r"\buseEffect\s*\(",
        WEB_EXTENSIONS,
        "strong",
        "effect-review",
        "Raw useEffect is present; classify it as external synchronization or internal choreography.",
    ),
    rule(
        r"\buseState\s*\(\s*(?:props\.|[A-Za-z_$][\w$]*\.)",
        WEB_EXTENSIONS,
        "medium",
        "possible-mirrored-state",
        "State is initialized from an object field; inspect whether divergence is intentional.",
    ),
    rule(
        r"\buse(?:App)?Selector\s*\([^)]*=>[^\n]*\.(?:map|filter|sort|reduce)\s*\(",
        WEB_EXTENSIONS,
        "strong",
        "inline-selector-derivation",
        "Selector callback performs collection work; inspect canonical selector ownership and memoization.",
    ),
    rule(
        r"\b(?:db\.(?:execute|write|query)|fetch\(|axios\.|supabase\.|PowerSync|SQLite|localStorage\.|sessionStorage\.)",
        UI_EXTENSIONS,
        "strong",
        "ui-infrastructure-access",
        "UI source appears to access persistence, storage, or remote infrastructure directly.",
    ),
    rule(
        r"\b(?:expandRRule|rrulestr)\b",
        WEB_EXTENSIONS,
        "strong",
        "recurrence-expansion",
        "Recurrence expansion is present; verify the calendar/worker ownership boundary.",
    ),
    rule(
        r"(?:\bas\s+any\b|[:<,]\s*any\b)",
        TYPED_JS_EXTENSIONS,
        "medium",
        "loose-any",
        "The line uses any; inspect whether it hides a stable contract or boundary validation.",
    ),
    rule(
        r"\b(?:variant|status|type|kind|intent|size)\??\s*:\s*string\b",
        TYPED_JS_EXTENSIONS,
        "medium",
        "stringly-contract",
        "A finite-looking semantic field is typed as string; check for an existing canonical type.",
    ),
    rule(
        r"\.Provider\b[^\n]*\bvalue=\{\{",
        REACT_EXTENSIONS,
        "strong",
        "inline-provider-value",
        "Context provider creates an inline object; inspect consumer rerender sensitivity.",
    ),
)

TS_LOOKUP_BRANCH = re.compile(
    r"\b(?:if|else\s+if)\s*\(?\s*([A-Za-z_$][\w$.]*)\s*(?:===|==)\s*['\"`][^'\"`]+['\"`]"
)
EFFECT_SETTER = re.compile(
    r"useEffect\s*\(\s*\(\)\s*=>\s*{[^}]*\bset[A-Z][\w$]*\s*\(",
    re.DOTALL,
)
TODO_COMMENT = re.compile(r"(?:^\s*(?://|#|/\*|\*)|<!--)\s*(?:TODO|FIXME)\b")


def make_signal(
    path: str,
    line: int,
    confidence: str,
    kind: str,
    message: str,
) -> Signal:
    return Signal(path, max(1, line), confidence, kind, message)


def signal_sort_key(signal: Signal) -> tuple[int, str, int, str, str]:
    return (
        CONFIDENCE_ORDER.get(signal.confidence, 99),
        signal.path,
        signal.line,
        signal.kind,
        signal.message,
    )


class FunctionBodyVisitor(ast.NodeVisitor):
    def __init__(self, root: ast.AST) -> None:
        self.root = root
        self.decisions = 0
        self.returns: list[ast.Return] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node is self.root:
            self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        if node is self.root:
            self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        self.decisions += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.decisions += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.decisions += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.decisions += 1
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self.decisions += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.decisions += max(0, len(node.values) - 1)
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        self.decisions += len(node.handlers)
        self.generic_visit(node)

    def visit_Match(self, node: ast.Match) -> None:
        self.decisions += len(node.cases)
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        self.returns.append(node)
        self.generic_visit(node)


def scan_python_functions(
    shown_path: str,
    text: str,
    function_threshold: int,
    decision_threshold: int,
) -> tuple[list[Signal], list[str]]:
    try:
        tree = ast.parse(text, filename=shown_path)
    except SyntaxError as error:
        return [], [f"{shown_path}: Python parse failed at line {error.lineno}"]

    signals: list[Signal] = []
    functions = (
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    )
    for function in functions:
        end_line = getattr(function, "end_lineno", function.lineno)
        length = end_line - function.lineno + 1
        visitor = FunctionBodyVisitor(function)
        visitor.visit(function)
        if length > function_threshold:
            signals.append(
                make_signal(
                    shown_path,
                    function.lineno,
                    "strong",
                    "long-function",
                    f"{function.name} spans {length} lines; inspect responsibility cohesion.",
                )
            )
        if visitor.decisions > decision_threshold:
            signals.append(
                make_signal(
                    shown_path,
                    function.lineno,
                    "strong",
                    "decision-density",
                    f"{function.name} has {visitor.decisions} AST decision nodes; inspect branch ownership.",
                )
            )
        rendered_returns = Counter(
            ast.dump(node.value, include_attributes=False)
            for node in visitor.returns
            if node.value is not None
        )
        repeated = max(rendered_returns.values(), default=0)
        if repeated >= 3:
            signals.append(
                make_signal(
                    shown_path,
                    function.lineno,
                    "medium",
                    "repeated-return",
                    f"{function.name} contains an identical return expression {repeated} times.",
                )
            )
    return signals, []


def scan_line_rules(shown_path: str, suffix: str, lines: list[str]) -> list[Signal]:
    signals: list[Signal] = []
    boolean_prefixes = r"(?:is|has|show|hide|allow|enable|disable|use|with)"
    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith(("//", "*")):
            continue
        for line_rule in LINE_RULES:
            if suffix in line_rule.extensions and line_rule.pattern.search(line):
                signals.append(
                    make_signal(
                        shown_path,
                        line_number,
                        line_rule.confidence,
                        line_rule.kind,
                        line_rule.message,
                    )
                )
        if suffix in REACT_EXTENSIONS:
            bare_flags = re.findall(
                rf"\b{boolean_prefixes}[A-Z][A-Za-z0-9_]*(?=(?:\s|/|>))",
                line,
            )
            bare_flags = [flag for flag in bare_flags if f"{flag}=" not in line]
            if len(set(bare_flags)) >= 2:
                signals.append(
                    make_signal(
                        shown_path,
                        line_number,
                        "medium",
                        "boolean-prop-cluster",
                        f"Multiple bare boolean props: {', '.join(sorted(set(bare_flags)))}.",
                    )
                )
            if re.search(r"\b(?:isActive|isSelected|isChecked)\s*=\s*{", line):
                signals.append(
                    make_signal(
                        shown_path,
                        line_number,
                        "weak",
                        "manual-state-prop",
                        "Visual state is passed as a flag; verify whether the caller or component owns the derivation.",
                    )
                )
    return signals


def scan_lookup_chains(shown_path: str, lines: list[str]) -> list[Signal]:
    positions: defaultdict[str, list[int]] = defaultdict(list)
    for line_number, line in enumerate(lines, start=1):
        match = TS_LOOKUP_BRANCH.search(line)
        if match:
            positions[match.group(1)].append(line_number)

    signals: list[Signal] = []
    for variable, line_numbers in positions.items():
        for start in range(len(line_numbers)):
            nearby = [line for line in line_numbers[start:] if line - line_numbers[start] <= 80]
            if len(nearby) < 4:
                continue
            signals.append(
                make_signal(
                    shown_path,
                    nearby[0],
                    "medium",
                    "lookup-chain-candidate",
                    f"{len(nearby)} nearby branches compare {variable}; verify one pure mapping before consolidating.",
                )
            )
            break
    return signals


def scan_source(
    path: Path,
    shown_path: str,
    text: str,
    line_threshold: int,
    function_threshold: int,
    decision_threshold: int,
) -> tuple[list[Signal], list[str]]:
    lines = text.splitlines()
    suffix = path.suffix.lower()
    signals: list[Signal] = []
    warnings: list[str] = []

    if len(lines) > line_threshold:
        signals.append(
            make_signal(
                shown_path,
                1,
                "strong",
                "large-file",
                f"{len(lines)} lines; inspect whether the file owns more than one responsibility.",
            )
        )
    for line_number, line in enumerate(lines, start=1):
        if TODO_COMMENT.search(line):
            signals.append(
                make_signal(
                    shown_path,
                    line_number,
                    "weak",
                    "stale-note-candidate",
                    "TODO/FIXME comment is present; verify that it has a concrete owner or still adds value.",
                )
            )

    if suffix == ".py":
        python_signals, python_warnings = scan_python_functions(
            shown_path,
            text,
            function_threshold,
            decision_threshold,
        )
        signals.extend(python_signals)
        warnings.extend(python_warnings)
    if suffix in WEB_EXTENSIONS:
        signals.extend(scan_line_rules(shown_path, suffix, lines))
        signals.extend(scan_lookup_chains(shown_path, lines))
        for match in EFFECT_SETTER.finditer(text):
            signals.append(
                make_signal(
                    shown_path,
                    text[: match.start()].count("\n") + 1,
                    "strong",
                    "effect-sets-state",
                    "An effect sets component state; verify external synchronization rather than derived state.",
                )
            )
    return signals, warnings
