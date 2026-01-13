#!/usr/bin/env python3
"""
Simple script to plot 5-day temperatures and save the figure.

Usage:
  - Interactive: run without arguments and follow prompts
    python3 temps_plot.py
  - Non-interactive: pass 5 temperature values as args
    python3 temps_plot.py 20 22 19 21 23
"""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def parse_args():
    args = sys.argv[1:]
    temps = []
    for a in args:
        try:
            temps.append(float(a))
        except ValueError:
            pass
    return temps

def prompt_for_temps(count=5):
    temps = []
    for i in range(1, count+1):
        while True:
            try:
                val = input(f"Temperature for day {i}: ").strip()
                if val == "":
                    print("Empty input, please enter a number.")
                    continue
                temps.append(float(val))
                break
            except ValueError:
                print("Invalid number, try again.")
    return temps

def plot_temps(temps, out_path='temperatures.png'):
    days = [f"Day {i+1}" for i in range(len(temps))]
    plt.figure(figsize=(8,4.5))
    plt.plot(days, temps, marker='o', linestyle='-', color='tab:blue')
    plt.title('5-Day Temperatures')
    plt.xlabel('Day')
    plt.ylabel('Temperature')
    plt.grid(True, linestyle='--', alpha=0.5)
    for i, t in enumerate(temps):
        plt.text(i, t, f"{t:.1f}", ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    print(f"Saved plot to {out_path}")

def main():
    temps = parse_args()
    if len(temps) < 5:
        print("Need 5 temperatures. Prompting for missing values.")
        needed = 5 - len(temps)
        temps += prompt_for_temps(needed) if len(temps) == 0 else prompt_for_temps(needed)
    temps = temps[:5]
    plot_temps(temps)

if __name__ == '__main__':
    main()
