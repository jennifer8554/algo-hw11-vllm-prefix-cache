import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt

def load(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main() -> None:
    off_path = Path("result_off.json")
    on_path = Path("result_on.json")
    if not off_path.exists() or not on_path.exists():
        print("找不到 result_off.json 或 result_on.json，請先跑實驗。")
        sys.exit(1)

    off = load(off_path)
    on = load(on_path)

    metrics = [
        ("Throughput (req/s)", off["throughput_req_per_sec"], on["throughput_req_per_sec"], "higher better"),
        ("Throughput (tok/s)", off["throughput_tok_per_sec"], on["throughput_tok_per_sec"], "higher better"),
        ("Total elapsed (sec)", off["elapsed_sec"], on["elapsed_sec"], "lower better"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(11, 4.5))
    for ax, (title, v_off, v_on, hint) in zip(axes, metrics):
        bars = ax.bar(["caching=off", "caching=on"], [v_off, v_on], color=["#888888", "#2a9d8f"])
        ax.set_title(f"{title}\n({hint})")
        ax.bar_label(bars, fmt="%.3g", padding=3)
        ax.margins(y=0.2)

    fig.suptitle(f"vLLM Prefix Caching: off vs. on  (model={off['model']}, n={off['n_prompts']})", fontsize=13)
    fig.tight_layout()
    out_png = "comparison.png"
    fig.savefig(out_png, dpi=130)
    print(f"[saved] {out_png}")

    speedup_req = on["throughput_req_per_sec"] / off["throughput_req_per_sec"]
    speedup_tok = on["throughput_tok_per_sec"] / off["throughput_tok_per_sec"]
    elapsed_red = 1 - on["elapsed_sec"] / off["elapsed_sec"]

    print("\n========== 比較摘要 ==========")
    print(f"  吞吐 (req/s) 加速:  {speedup_req:.2f} 倍")
    print(f"  吞吐 (tok/s) 加速:  {speedup_tok:.2f} 倍")
    print(f"  總耗時下降:         {elapsed_red * 100:5.1f}%")

if __name__ == '__main__':
    main()