# Manim Algorithm Visualizations

Welcome to **Manim Algorithm Visualizations**! This repository contains a collection of algorithm visualizations created using [ManimCE](https://github.com/ManimCommunity/manim), a powerful mathematical animation engine. The goal is to provide clear and visually appealing explanations of various algorithms to enhance understanding and learning.

## Table of Contents

- [Introduction](#introduction)
- [Visualized Algorithms](#visualized-algorithms)
- [Installation](#installation)
- [How to Run](#how-to-run)

## Introduction

Understanding algorithms can be challenging, especially without a good visual representation. This repository offers animated visualizations of popular algorithms that help break down complex concepts into easy-to-follow steps. Each algorithm visualization is implemented in Python using the Manim library.

## Visualized Algorithms

The repository currently includes visualizations of the following algorithms:

- Naive Text Search
- Creation of the LPS table for KMP search

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/DamianKuras/manim-algorithm-visualizations
   cd manim-algorithm-visualizations
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

manim -p -qh path_to_visualization.py SceneName

- '-p' flag previews the rendered video after rendering.
- '-qh' flag specifies high-quality rendering.
- Replace path_to_visualization.py with the relative path to the algorithm file.

For example, to run the Naive Text Search animation:

```bash
manim -p -qh naive_text_search.py
```

For more configuration options and CLI flags, see the [documentation](https://docs.manim.community/en/v0.18.1/guides/configuration.html)
