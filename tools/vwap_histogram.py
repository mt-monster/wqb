#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从 WQ Brain 拉 vwap alpha 的 PnL 序列并画直方图。
alpha_id: zqr0wOEX（raw template: expression=vwap, USA/TOP3000/d1）
"""
import json
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# 中文字体兜底
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 从 stdin 读 json（避免命令行长度问题）
if __name__ == "__main__":
    raw = sys.stdin.read().strip()
    data = json.loads(raw)
    records = data["records"]
    # records: [[date, pnl, risk-neutralized-pnl, investability-constrained-pnl], ...]
    pnl_values = np.array([r[1] for r in records])
    dates = [r[0] for r in records]

    print(f"记录数: {len(pnl_values)}")
    print(f"时间跨度: {dates[0]} → {dates[-1]}")
    print(f"总 PnL 变化: {pnl_values[-1]:,.0f} - {pnl_values[0]:,.0f} = {pnl_values[-1]-pnl_values[0]:,.0f}")
    print(f"\nPnL 描述统计:")
    print(f"  mean   = {pnl_values.mean():>15,.0f}")
    print(f"  median = {np.median(pnl_values):>15,.0f}")
    print(f"  std    = {pnl_values.std():>15,.0f}")
    print(f"  min    = {pnl_values.min():>15,.0f}")
    print(f"  max    = {pnl_values.max():>15,.0f}")
    print(f"  p5     = {np.percentile(pnl_values, 5):>15,.0f}")
    print(f"  p95    = {np.percentile(pnl_values, 95):>15,.0f}")

    # 每周 PnL 增量（相邻两个采样点之差）
    weekly_delta = np.diff(pnl_values)
    print(f"\n周度 PnL 增量 (n={len(weekly_delta)}):")
    print(f"  mean   = {weekly_delta.mean():>12,.0f}")
    print(f"  median = {np.median(weekly_delta):>12,.0f}")
    print(f"  std    = {weekly_delta.std():>12,.0f}")
    print(f"  min    = {weekly_delta.min():>12,.0f}")
    print(f"  max    = {weekly_delta.max():>12,.0f}")
    print(f"  正增周数 = {(weekly_delta > 0).sum()}/{len(weekly_delta)} = {(weekly_delta > 0).mean()*100:.1f}%")

    # ---- 画图 ----
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("VWAP Alpha (zqr0wOEX) — USA/TOP3000/d1", fontsize=14, fontweight="bold")

    # 1) 累计 PnL 时间序列
    ax = axes[0, 0]
    date_dt = np.array(dates)
    ax.plot(range(len(pnl_values)), pnl_values / 1e6, linewidth=1.2, color="#2196F3")
    ax.set_title("1. Cumulative PnL over time (weekly samples)")
    ax.set_xlabel("Week index (150 weeks)")
    ax.set_ylabel("PnL ($M)")
    ax.grid(alpha=0.3)
    ax.axhline(0, color="red", linewidth=0.8, linestyle="--", alpha=0.6)

    # 2) 累计 PnL 直方图
    ax = axes[0, 1]
    ax.hist(pnl_values / 1e6, bins=40, color="#4CAF50", edgecolor="black", alpha=0.8)
    ax.set_title("2. Histogram of cumulative PnL (weekly snapshots)")
    ax.set_xlabel("Cumulative PnL ($M)")
    ax.set_ylabel("Frequency")
    ax.grid(alpha=0.3)
    ax.axvline(pnl_values.mean() / 1e6, color="red", linestyle="--", linewidth=1.5, label=f"mean={pnl_values.mean()/1e6:.2f}M")
    ax.legend()

    # 3) 周度 PnL 增量直方图（真正的"变化分布"）
    ax = axes[1, 0]
    ax.hist(weekly_delta / 1e6, bins=40, color="#FF9800", edgecolor="black", alpha=0.8)
    ax.set_title("3. Histogram of weekly PnL increments (ΔPnL)")
    ax.set_xlabel("Weekly ΔPnL ($M)")
    ax.set_ylabel("Frequency")
    ax.grid(alpha=0.3)
    ax.axvline(0, color="black", linestyle="-", linewidth=0.8)
    ax.axvline(weekly_delta.mean() / 1e6, color="red", linestyle="--", linewidth=1.5, label=f"mean={weekly_delta.mean()/1e6:.3f}M")
    ax.legend()

    # 4) 周度 PnL 增量箱线图（看极端值）
    ax = axes[1, 1]
    ax.boxplot(weekly_delta / 1e6, vert=False, patch_artist=True,
               boxprops=dict(facecolor="#9C27B0", alpha=0.6),
               medianprops=dict(color="black", linewidth=1.5))
    ax.set_title("4. Boxplot of weekly ΔPnL")
    ax.set_ylabel("Weekly ΔPnL ($M)")
    ax.grid(alpha=0.3, axis="x")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    # 仓库根从 __file__ 上溯，不写盘符（硬编码 `D:\coding\...` 会被 S4 拦，且换机器即断）。
    # 想改落点就用环境变量 WQB_OUT_DIR，不必改代码。
    _repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _out_dir = os.environ.get("WQB_OUT_DIR") or os.path.join(_repo_root, "output_report")
    out_path = os.path.join(_out_dir, "vwap_histogram_20261023.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    print(f"\n直方图已保存: {out_path}")
