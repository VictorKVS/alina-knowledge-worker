from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageStat


def _rgb(path: str | Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def _mean_rgb(image: Image.Image) -> list[float]:
    mean = ImageStat.Stat(image).mean[:3]
    return [round(v, 3) for v in mean]


def _mean_luminance(image: Image.Image) -> float:
    r, g, b = ImageStat.Stat(image).mean[:3]
    # Relative luminance approximation in sRGB display space.
    return round((0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0, 6)


def _normalized_mae(reference: Image.Image, implementation: Image.Image) -> float:
    diff = ImageChops.difference(reference, implementation)
    stat = ImageStat.Stat(diff)
    return round(sum(stat.mean[:3]) / (3.0 * 255.0), 6)


def _difference_ratio(
    reference: Image.Image,
    implementation: Image.Image,
    *,
    threshold: int = 24,
) -> float:
    diff = ImageChops.difference(reference, implementation)
    # One scalar difference value per pixel: max channel delta.
    pixels = diff.getdata()
    changed = 0
    total = reference.width * reference.height
    for px in pixels:
        if max(px) >= threshold:
            changed += 1
    return round(changed / total, 6) if total else 0.0


def compare_images(
    reference_path: str | Path,
    implementation_path: str | Path,
    *,
    project_id: str = "book-craft",
    theme_id: str = "default",
    breakpoint: str = "desktop",
    commit_ref: str | None = None,
    threshold: int = 24,
) -> dict[str, Any]:
    """Return measurable visual evidence.

    This function intentionally does not claim semantic/pixel identity and does
    not choose frontend corrections. It produces evidence for ALINA Analyst.
    """

    reference_path = Path(reference_path)
    implementation_path = Path(implementation_path)

    reference = _rgb(reference_path)
    implementation = _rgb(implementation_path)

    same_size = reference.size == implementation.size
    implementation_for_compare = implementation
    resampled = False

    if not same_size:
        implementation_for_compare = implementation.resize(reference.size, Image.Resampling.LANCZOS)
        resampled = True

    diff = ImageChops.difference(reference, implementation_for_compare)
    bbox = diff.getbbox()

    reference_mean = _mean_rgb(reference)
    implementation_mean = _mean_rgb(implementation_for_compare)

    observations: list[dict[str, Any]] = []

    if not same_size:
        observations.append(
            {
                "category": "viewport_geometry",
                "severity": "high",
                "observation": (
                    f"Reference size {reference.width}x{reference.height}; "
                    f"implementation size {implementation.width}x{implementation.height}."
                ),
                "evidence_type": "measured",
            }
        )

    mae = _normalized_mae(reference, implementation_for_compare)
    ratio = _difference_ratio(
        reference, implementation_for_compare, threshold=threshold
    )

    observations.append(
        {
            "category": "pixel_difference",
            "severity": (
                "low" if mae < 0.05 else
                "medium" if mae < 0.12 else
                "high"
            ),
            "observation": (
                f"Normalized mean absolute pixel error = {mae:.6f}; "
                f"changed-pixel ratio at threshold {threshold} = {ratio:.6f}."
            ),
            "evidence_type": "measured",
        }
    )

    luminance_ref = _mean_luminance(reference)
    luminance_impl = _mean_luminance(implementation_for_compare)
    observations.append(
        {
            "category": "global_luminance",
            "severity": (
                "low" if abs(luminance_ref - luminance_impl) < 0.05 else
                "medium" if abs(luminance_ref - luminance_impl) < 0.12 else
                "high"
            ),
            "observation": (
                f"Reference luminance = {luminance_ref:.6f}; "
                f"implementation luminance = {luminance_impl:.6f}."
            ),
            "evidence_type": "measured",
        }
    )

    return {
        "schema_version": "1.0",
        "role": "ALINA Analyst",
        "project_id": project_id,
        "theme_id": theme_id,
        "breakpoint": breakpoint,
        "commit_ref": commit_ref,
        "reference": {
            "path": str(reference_path),
            "width": reference.width,
            "height": reference.height,
            "mean_rgb": reference_mean,
            "mean_luminance": luminance_ref,
        },
        "implementation": {
            "path": str(implementation_path),
            "width": implementation.width,
            "height": implementation.height,
            "mean_rgb": implementation_mean,
            "mean_luminance": luminance_impl,
        },
        "comparison": {
            "same_size": same_size,
            "resampled_for_metrics": resampled,
            "normalized_mae": mae,
            "changed_pixel_ratio": ratio,
            "difference_bbox": list(bbox) if bbox else None,
            "threshold": threshold,
        },
        "observations": observations,
        "semantic_review_status": "required",
        "semantic_review_note": (
            "Pixel metrics are evidence only. Composition, hero placement, "
            "typography, lighting intent and correction advice require a "
            "separate visual/semantic review."
        ),
    }


def _main() -> int:
    parser = argparse.ArgumentParser(description="ALINA visual evidence comparator")
    parser.add_argument("reference")
    parser.add_argument("implementation")
    parser.add_argument("--project", default="book-craft")
    parser.add_argument("--theme", default="default")
    parser.add_argument("--breakpoint", default="desktop")
    parser.add_argument("--commit")
    parser.add_argument("--threshold", type=int, default=24)
    parser.add_argument("--output")
    args = parser.parse_args()

    report = compare_images(
        args.reference,
        args.implementation,
        project_id=args.project,
        theme_id=args.theme,
        breakpoint=args.breakpoint,
        commit_ref=args.commit,
        threshold=args.threshold,
    )
    encoded = json.dumps(report, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
