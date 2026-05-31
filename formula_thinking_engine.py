import json
import math
import random
from dataclasses import dataclass, field, asdict
from typing import Optional

DIMENSIONS = {
    "K": "Knowledge",
    "R": "Reasoning",
    "C": "Creativity",
    "M": "Memory",
    "S": "SelfHealing",
    "G": "Guardrails",
    "A": "Automation",
    "P": "Prediction",
    "F": "Formula",
    "H": "Hardware",
}

OPERATORS = {
    "+": "combine",
    "-": "remove",
    "*": "cross",
    "/": "specialize",
    "sq": "self-improve",
    "sqrt": "decompose",
    "^": "amplify",
    "log": "abstract",
}

DIMENSION_KEYS = list(DIMENSIONS.keys())
OPERATOR_KEYS = list(OPERATORS.keys())

BINARY_OPS = ["+", "-", "*", "/", "^"]
UNARY_OPS = ["sq", "sqrt", "log"]


@dataclass
class FormulaResult:
    formula_id: str
    expression: str
    operators_used: list = field(default_factory=list)
    dimensions_used: list = field(default_factory=list)
    l1_accuracy: float = 0.0
    l2_accuracy: float = 0.0
    l3_accuracy: float = 0.0
    l1_passed: bool = False
    l2_passed: bool = False
    l3_passed: bool = False
    best_accuracy: float = 0.0


def _apply_op(op: str, a: float, b: Optional[float] = None) -> float:
    if op == "+":
        return a + b
    if op == "-":
        return max(0.0, a - b)
    if op == "*":
        return a * b
    if op == "/":
        return a / b if b != 0 else 1.0
    if op == "^":
        return min(1.0, a ** b) if b is not None else min(1.0, a * a)
    if op == "sq":
        return min(1.0, a * a)
    if op == "sqrt":
        return math.sqrt(max(0.0, a))
    if op == "log":
        return math.log(1.0 + a)
    return a


class _FormulaNode:
    __slots__ = ("op", "left", "right", "dim")

    def __init__(self, op=None, left=None, right=None, dim=None):
        self.op = op
        self.left = left
        self.right = right
        self.dim = dim

    def evaluate(self, dim_values: dict) -> float:
        if self.dim is not None:
            return dim_values.get(self.dim, 0.5)
        left_val = self.left.evaluate(dim_values) if self.left else 0.0
        if self.op in UNARY_OPS:
            return _apply_op(self.op, left_val)
        right_val = self.right.evaluate(dim_values) if self.right else 0.0
        return _apply_op(self.op, left_val, right_val)

    def to_string(self) -> str:
        if self.dim is not None:
            return self.dim
        if self.op in UNARY_OPS:
            inner = self.left.to_string() if self.left else ""
            return f"{self.op}({inner})"
        left_s = self.left.to_string() if self.left else ""
        right_s = self.right.to_string() if self.right else ""
        return f"({left_s}{self.op}{right_s})"

    def collect_ops(self) -> list:
        ops = []
        if self.op:
            ops.append(self.op)
        if self.left:
            ops.extend(self.left.collect_ops())
        if self.right:
            ops.extend(self.right.collect_ops())
        return ops

    def collect_dims(self) -> list:
        dims = []
        if self.dim:
            dims.append(self.dim)
        if self.left:
            dims.extend(self.left.collect_dims())
        if self.right:
            dims.extend(self.right.collect_dims())
        return dims


def _make_dim_node(dim: str) -> _FormulaNode:
    return _FormulaNode(dim=dim)


def _make_unary_node(op: str, child: _FormulaNode) -> _FormulaNode:
    return _FormulaNode(op=op, left=child)


def _make_binary_node(op: str, left: _FormulaNode, right: _FormulaNode) -> _FormulaNode:
    return _FormulaNode(op=op, left=left, right=right)


def _generate_single_op_formulas() -> list:
    formulas = []
    for op in BINARY_OPS:
        for i, d1 in enumerate(DIMENSION_KEYS):
            for d2 in DIMENSION_KEYS[i + 1:]:
                node = _make_binary_node(op, _make_dim_node(d1), _make_dim_node(d2))
                formulas.append(node)
    for op in UNARY_OPS:
        for d in DIMENSION_KEYS:
            node = _make_unary_node(op, _make_dim_node(d))
            formulas.append(node)
    return formulas


def _generate_two_op_formulas() -> list:
    formulas = []
    single_binaries = []
    for op in BINARY_OPS:
        for d1 in DIMENSION_KEYS:
            for d2 in DIMENSION_KEYS:
                if d1 != d2:
                    single_binaries.append((op, d1, d2))

    for op_outer in BINARY_OPS:
        for op_inner, d1, d2 in single_binaries:
            inner = _make_binary_node(op_inner, _make_dim_node(d1), _make_dim_node(d2))
            for d3 in DIMENSION_KEYS:
                if d3 not in (d1, d2):
                    node = _make_binary_node(op_outer, inner, _make_dim_node(d3))
                    formulas.append(node)

    for op_outer in UNARY_OPS:
        for op_inner, d1, d2 in single_binaries:
            inner = _make_binary_node(op_inner, _make_dim_node(d1), _make_dim_node(d2))
            node = _make_unary_node(op_outer, inner)
            formulas.append(node)

    for op_outer in BINARY_OPS:
        for op_inner in UNARY_OPS:
            for d1 in DIMENSION_KEYS:
                inner = _make_unary_node(op_inner, _make_dim_node(d1))
                for d2 in DIMENSION_KEYS:
                    if d2 != d1:
                        node = _make_binary_node(op_outer, inner, _make_dim_node(d2))
                        formulas.append(node)

    return formulas


def _generate_three_op_formulas() -> list:
    formulas = []
    two_op_cache = _generate_two_op_formulas()
    sample_size = min(200, len(two_op_cache))
    sampled = random.sample(two_op_cache, sample_size) if len(two_op_cache) > sample_size else two_op_cache

    for op_outer in BINARY_OPS:
        for inner in sampled:
            for d in DIMENSION_KEYS:
                node = _make_binary_node(op_outer, inner, _make_dim_node(d))
                formulas.append(node)

    for op_outer in UNARY_OPS:
        for inner in sampled:
            node = _make_unary_node(op_outer, inner)
            formulas.append(node)

    return formulas


def _generate_scenario(rng: random.Random) -> dict:
    home_strength = rng.random()
    away_strength = rng.random()
    draw_tendency = rng.random()
    home_advantage = rng.uniform(0.4, 0.7)
    form_factor = rng.random()
    xfactor_factor = rng.random()
    fatigue_factor = rng.random()
    tactical_factor = rng.random()
    market_consensus = rng.random()
    noise = rng.random() * 0.1
    return {
        "home_strength": home_strength,
        "away_strength": away_strength,
        "draw_tendency": draw_tendency,
        "home_advantage": home_advantage,
        "form_factor": form_factor,
        "xfactor_factor": xfactor_factor,
        "fatigue_factor": fatigue_factor,
        "tactical_factor": tactical_factor,
        "market_consensus": market_consensus,
        "noise": noise,
    }


def _ground_truth_home(scenario: dict) -> float:
    return (
        0.4 * scenario["home_strength"]
        + 0.2 * (1.0 - scenario["away_strength"])
        + 0.1 * scenario["home_advantage"]
        + 0.05 * scenario["form_factor"]
        + 0.05 * scenario["xfactor_factor"]
        + 0.05 * scenario["fatigue_factor"]
        + 0.05 * scenario["tactical_factor"]
        + 0.05 * scenario["market_consensus"]
        + 0.05 * scenario["noise"]
    )


def _ground_truth_draw(scenario: dict) -> float:
    return max(0.05, min(0.45, 0.25 - 0.1 * abs(scenario["home_strength"] - scenario["away_strength"])))


def _scenario_to_dim_values(scenario: dict) -> dict:
    return {
        "K": scenario["home_strength"] * 0.5 + scenario["market_consensus"] * 0.5,
        "R": scenario["form_factor"] * 0.4 + scenario["tactical_factor"] * 0.6,
        "C": scenario["xfactor_factor"] * 0.7 + scenario["noise"] * 3.0 * 0.3,
        "M": scenario["home_strength"] * 0.3 + scenario["away_strength"] * 0.3 + scenario["draw_tendency"] * 0.4,
        "S": scenario["fatigue_factor"] * 0.5 + scenario["form_factor"] * 0.5,
        "G": scenario["tactical_factor"] * 0.6 + scenario["market_consensus"] * 0.4,
        "A": scenario["home_advantage"] * 0.5 + scenario["fatigue_factor"] * 0.5,
        "P": scenario["home_strength"] * 0.6 + scenario["form_factor"] * 0.4,
        "F": scenario["home_strength"] * 0.4 + scenario["away_strength"] * 0.2 + scenario["form_factor"] * 0.4,
        "H": scenario["home_advantage"] * 0.7 + scenario["fatigue_factor"] * 0.3,
    }


class FormulaThinkingEngine:
    def __init__(self):
        self._registry: list[FormulaResult] = []
        self._formula_nodes: dict[str, _FormulaNode] = {}

    def generate_formulas(self, count: int = 50) -> list[FormulaResult]:
        rng = random.Random(42)
        all_nodes = []

        single = _generate_single_op_formulas()
        rng.shuffle(single)
        all_nodes.extend(single)

        two = _generate_two_op_formulas()
        rng.shuffle(two)
        all_nodes.extend(two)

        three = _generate_three_op_formulas()
        rng.shuffle(three)
        all_nodes.extend(three)

        selected = all_nodes[:count]

        start_id = len(self._registry) + 1
        for i, node in enumerate(selected):
            fid = f"FT-{start_id + i:03d}"
            expr = node.to_string()
            ops = list(dict.fromkeys(node.collect_ops()))
            dims = list(dict.fromkeys(node.collect_dims()))
            result = FormulaResult(
                formula_id=fid,
                expression=expr,
                operators_used=ops,
                dimensions_used=dims,
            )
            self._registry.append(result)
            self._formula_nodes[fid] = node

        return self._registry[-len(selected):]

    def _evaluate_formula(self, formula: FormulaResult, scenario: dict) -> float:
        node = self._formula_nodes.get(formula.formula_id)
        if node is None:
            return 0.5
        dim_values = _scenario_to_dim_values(scenario)
        result = node.evaluate(dim_values)
        return max(0.0, min(1.0, result))

    def run_l1_test(self, formulas: list[FormulaResult], num_scenarios: int = 10_000_000) -> list[FormulaResult]:
        rng = random.Random(2026)
        chunk_size = 1_000_000
        num_chunks = num_scenarios // chunk_size

        correct_counts = {f.formula_id: 0 for f in formulas}
        total = 0

        for chunk_idx in range(num_chunks):
            for _ in range(chunk_size):
                scenario = _generate_scenario(rng)
                gt_home = _ground_truth_home(scenario)
                gt_draw = _ground_truth_draw(scenario)
                gt_away = max(0.05, 1.0 - gt_home - gt_draw)

                gt_outcome = 0
                r = rng.random()
                if r < gt_home:
                    gt_outcome = 1
                elif r < gt_home + gt_draw:
                    gt_outcome = 0
                else:
                    gt_outcome = -1

                for f in formulas:
                    pred_home = self._evaluate_formula(f, scenario)
                    pred_draw = gt_draw
                    pred_away = max(0.05, 1.0 - pred_home - pred_draw)

                    if pred_home >= pred_draw and pred_home >= pred_away:
                        pred_outcome = 1
                    elif pred_draw >= pred_home and pred_draw >= pred_away:
                        pred_outcome = 0
                    else:
                        pred_outcome = -1

                    if pred_outcome == gt_outcome:
                        correct_counts[f.formula_id] += 1

                total += 1

            if (chunk_idx + 1) % 5 == 0:
                print(f"  L1 progress: {(chunk_idx + 1) * chunk_size:,} / {num_scenarios:,} scenarios")

        for f in formulas:
            f.l1_accuracy = correct_counts[f.formula_id] / total if total > 0 else 0.0
            f.l1_passed = f.l1_accuracy >= 0.65
            f.best_accuracy = max(f.best_accuracy, f.l1_accuracy)

        return formulas

    def run_l2_test(self, formulas: list[FormulaResult], num_scenarios: int = 100_000_000) -> list[FormulaResult]:
        passed = [f for f in formulas if f.l1_passed]
        if not passed:
            return formulas

        rng = random.Random(20260206)
        chunk_size = 10_000_000
        num_chunks = num_scenarios // chunk_size

        correct_counts = {f.formula_id: 0 for f in passed}
        total = 0

        for chunk_idx in range(num_chunks):
            for _ in range(chunk_size):
                scenario = _generate_scenario(rng)
                gt_home = _ground_truth_home(scenario)
                gt_draw = _ground_truth_draw(scenario)
                gt_away = max(0.05, 1.0 - gt_home - gt_draw)

                gt_outcome = 0
                r = rng.random()
                if r < gt_home:
                    gt_outcome = 1
                elif r < gt_home + gt_draw:
                    gt_outcome = 0
                else:
                    gt_outcome = -1

                for f in passed:
                    pred_home = self._evaluate_formula(f, scenario)
                    pred_draw = gt_draw
                    pred_away = max(0.05, 1.0 - pred_home - pred_draw)

                    if pred_home >= pred_draw and pred_home >= pred_away:
                        pred_outcome = 1
                    elif pred_draw >= pred_home and pred_draw >= pred_away:
                        pred_outcome = 0
                    else:
                        pred_outcome = -1

                    if pred_outcome == gt_outcome:
                        correct_counts[f.formula_id] += 1

                total += 1

            print(f"  L2 progress: {(chunk_idx + 1) * chunk_size:,} / {num_scenarios:,} scenarios")

        for f in passed:
            f.l2_accuracy = correct_counts[f.formula_id] / total if total > 0 else 0.0
            f.l2_passed = f.l2_accuracy >= 0.70
            f.best_accuracy = max(f.best_accuracy, f.l2_accuracy)

        return formulas

    def run_l3_test(self, formulas: list[FormulaResult], num_scenarios: int = 1_000_000_000) -> list[FormulaResult]:
        passed = [f for f in formulas if f.l2_passed]
        if not passed:
            return formulas

        rng = random.Random(2026020600)
        chunk_size = 10_000_000
        num_chunks = num_scenarios // chunk_size

        correct_counts = {f.formula_id: 0 for f in passed}
        total = 0

        for chunk_idx in range(num_chunks):
            for _ in range(chunk_size):
                scenario = _generate_scenario(rng)
                gt_home = _ground_truth_home(scenario)
                gt_draw = _ground_truth_draw(scenario)
                gt_away = max(0.05, 1.0 - gt_home - gt_draw)

                gt_outcome = 0
                r = rng.random()
                if r < gt_home:
                    gt_outcome = 1
                elif r < gt_home + gt_draw:
                    gt_outcome = 0
                else:
                    gt_outcome = -1

                for f in passed:
                    pred_home = self._evaluate_formula(f, scenario)
                    pred_draw = gt_draw
                    pred_away = max(0.05, 1.0 - pred_home - pred_draw)

                    if pred_home >= pred_draw and pred_home >= pred_away:
                        pred_outcome = 1
                    elif pred_draw >= pred_home and pred_draw >= pred_away:
                        pred_outcome = 0
                    else:
                        pred_outcome = -1

                    if pred_outcome == gt_outcome:
                        correct_counts[f.formula_id] += 1

                total += 1

            if (chunk_idx + 1) % 10 == 0:
                print(f"  L3 progress: {(chunk_idx + 1) * chunk_size:,} / {num_scenarios:,} scenarios")

        for f in passed:
            f.l3_accuracy = correct_counts[f.formula_id] / total if total > 0 else 0.0
            l2_l3_diff = abs(f.l3_accuracy - f.l2_accuracy)
            f.l3_passed = f.l3_accuracy >= 0.70 and l2_l3_diff < 0.01
            f.best_accuracy = max(f.best_accuracy, f.l3_accuracy)

        return formulas

    def get_best_formula(self, formulas: list[FormulaResult]) -> FormulaResult:
        return max(formulas, key=lambda f: f.best_accuracy)

    def get_all_formulas(self) -> list[FormulaResult]:
        return list(self._registry)

    def save_results(self, filepath: str):
        data = [asdict(f) for f in self._registry]
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)

    def load_results(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self._registry = []
        self._formula_nodes = {}
        for item in data:
            result = FormulaResult(**item)
            self._registry.append(result)


def run_full_testing_pipeline():
    engine = FormulaThinkingEngine()

    print("Generating 50 formulas...")
    formulas = engine.generate_formulas(count=50)
    print(f"Generated {len(formulas)} formulas")
    for f in formulas[:5]:
        print(f"  {f.formula_id}: {f.expression}")

    print("\nRunning L1 test (10M scenarios)...")
    formulas = engine.run_l1_test(formulas, num_scenarios=10_000_000)
    l1_passed = [f for f in formulas if f.l1_passed]
    print(f"L1 complete: {len(l1_passed)}/{len(formulas)} passed")
    for f in l1_passed[:5]:
        print(f"  {f.formula_id}: accuracy={f.l1_accuracy:.4f}")

    if not l1_passed:
        print("No formulas passed L1. Best formula:")
        best = engine.get_best_formula(formulas)
        print(f"  {best.formula_id}: {best.expression} (accuracy={best.best_accuracy:.4f})")
        return best

    print("\nRunning L2 test (100M scenarios)...")
    formulas = engine.run_l2_test(formulas, num_scenarios=100_000_000)
    l2_passed = [f for f in formulas if f.l2_passed]
    print(f"L2 complete: {len(l2_passed)}/{len(l1_passed)} passed")
    for f in l2_passed[:5]:
        print(f"  {f.formula_id}: accuracy={f.l2_accuracy:.4f}")

    if not l2_passed:
        print("No formulas passed L2. Best formula:")
        best = engine.get_best_formula(formulas)
        print(f"  {best.formula_id}: {best.expression} (accuracy={best.best_accuracy:.4f})")
        return best

    print("\nRunning L3 test (1B scenarios)...")
    formulas = engine.run_l3_test(formulas, num_scenarios=1_000_000_000)
    l3_passed = [f for f in formulas if f.l3_passed]
    print(f"L3 complete: {len(l3_passed)}/{len(l2_passed)} passed (convergence confirmed)")
    for f in l3_passed[:5]:
        print(f"  {f.formula_id}: accuracy={f.l3_accuracy:.4f} (L2->L3 delta={abs(f.l3_accuracy - f.l2_accuracy):.4f})")

    best = engine.get_best_formula(formulas)
    print(f"\nBest formula: {best.formula_id}: {best.expression}")
    print(f"  L1 accuracy: {best.l1_accuracy:.4f}")
    print(f"  L2 accuracy: {best.l2_accuracy:.4f}")
    print(f"  L3 accuracy: {best.l3_accuracy:.4f}")
    print(f"  Best accuracy: {best.best_accuracy:.4f}")
    print(f"  Operators: {best.operators_used}")
    print(f"  Dimensions: {best.dimensions_used}")

    return best


if __name__ == "__main__":
    run_full_testing_pipeline()
