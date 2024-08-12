
# MMA Fighter Data Analysis and Ranking

## Project Overview

This repository contains the code and resources for a comprehensive analysis of MMA fighters, including data scraping, ranking, and visualization. The project is divided into three major phases:

1. **Data Scraping**: Information about MMA fights is collected from various sources using the Scrapy framework. This data includes details about fighters, events, and fight outcomes.
2. **Fighter Ranking**: Based on the scraped data, a ranking system for fighters is developed using network analysis techniques. The system evaluates factors such as fight outcomes, the strength of opponents, and other relevant metrics.
3. **Visualization and Animation**: The results of the ranking system are visualized through plots, animations, and videos. These visualizations help to illustrate the dynamics and trends in fighter performance over time.

This project aims to provide insights into fighter performance and rankings, serving as a valuable tool for fans, analysts, and MMA enthusiasts.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Project Structure](#project-structure)
4. [Data Collection](#data-collection)
5. [Ranking Methodology](#ranking-methodology)
6. [Visualization and Results](#visualization-and-results)
7. [Future Work](#future-work)
8. [Conclusion](#conclusion)
9. [Contact](#contact)
10. [Current TODOs](#current-todos)

## Installation

To run this project locally, you need Python 3.8 or later and the required libraries. Install the necessary dependencies with:

```bash
pip install -r requirements.txt
```

## Project Structure

The repository is organized into three main phases:

- **Data Scraping**
  - `__init__.py`: Initialization file for the scraping module.
  - `events.py`: Script for scraping MMA event data.
  - `fighter_crawl.py`: Script for scraping individual fighter data.
  - `fighters.py`: Main script orchestrating the fighter data scraping.
  - `scraping_config.py`: Configuration file for the scraping process.
  - `items.py`, `middlewares.py`, `pipelines.py`, `settings.py`: Scrapy framework components.

- **Fighter Ranking**
  - \`__init__.py\`: Initialization file for the ranking module.
  - \`network_ranking.py\`: Script implementing the fighter ranking algorithm.
  - \`preprocess.py\`: Script for preprocessing the scraped data before ranking.
  - \`final_run_notebook.ipynb\`, \`UFC_ranking.ipynb\`, \`UFC_ranking_new.ipynb\`: Jupyter notebooks for running and refining the ranking analysis.

- **Visualization and Animation**
  - \`anime_fighters.ipynb\`: Jupyter notebook for generating visualizations, animations, and videos.

## Data Collection

The data collection phase involves scraping data on MMA fights using the Scrapy framework. The key scripts used for this phase include:

- \`events.py\`: Scrapes data about MMA events.
- \`fighter_crawl.py\`: Scrapes data about individual fighters, including their fight history and stats.

## Ranking Methodology

The ranking of fighters is based on a network analysis approach that evaluates fight outcomes, opponent strength, and other metrics to generate a comprehensive ranking system. This methodology helps to accurately reflect the relative standing of fighters across different weight classes.

### Key Files for Ranking:

- `network_ranking.py`: Implements the ranking algorithm.
- `preprocess.py`: Prepares the data for ranking.

## Visualization and Results

The visualization phase involves creating plots and animations to depict the evolution of fighter rankings over time. These visualizations provide a clear picture of the trends and changes in fighter performance.

### Key Files for Visualization:

- \`anime_fighters.ipynb\`: Generates the visualizations and animations.

## Future Work

The project is still a work in progress with several enhancements planned:

- Refining the ranking method to better align with official rankings.
- Adding photos of fighters to the graphs.
- Improving the ranking method for specific weight classes.
- Ensuring that the ranks do not produce duplicates.
- Transitioning the graph and ranking processes fully into Python scripts.

## Conclusion

This project provides a comprehensive analysis of MMA fighters by combining data scraping, network-based ranking, and advanced visualization techniques. The insights derived from this analysis offer valuable perspectives on fighter rankings and performance trends.

## Contact

For any questions or collaboration inquiries, feel free to reach out:

- **Email:** [Your Email]
- **LinkedIn:** [Your LinkedIn Profile]

## Current TODOs

**TODO:**
- [x] Create a makefile.
- [x] Adjustment of the ranking method is moved to a script.
- [ ] Fix the bantamweight rank, which currently looks incorrect.
- [ ] Correct the ranking issue for Sean Strickland in the light heavyweight division.
- [x] Find the reason for missing ranks (example: lightweight rank 8).
- [x] Resolve the missing rank issue. The reason was that when changing the ranking, fighters below the winner’s rank should not be adjusted.
- [ ] Change the base ranking for each weight class by removing the current ratio; the new one should be \`page_rank * weight_class_p_rank\`.
- [ ] Ensure that ranks do not produce duplicates after changes.
- [ ] Scrape photos of each fighter.
- [ ] Enhance the ranking method to match official rankings.
- [ ] Add photos to the graph.
- [ ] Transfer the graph and ranking processes to Python scripts.
