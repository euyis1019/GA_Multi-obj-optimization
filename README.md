# Optimization of Arch Support Insoles through Genetic Algorithm

### Project Description
This project enhances the functionality and comfort of insoles by optimizing their design parameters using a genetic algorithm. Implemented in Python, the project aims to optimize key parameters such as arch length, width, and height through a parametric design process, addressing the specific needs of students in costume performance disciplines.
```markdown
---------------------------------------------------------------
# Copyright (c) 2024-2025 SCNU, Yifu Guo And GDUT. All rights reserved.
# Licensed under the Apache License, Version 2.0
---------------------------------------------------------------

# The Genetic Algorithm is based on DEAP
https://github.com/DEAP/deap
```

## Project Structure
- **GA_insole/GA/Model_GA.py**: This is the core file of the project where the main genetic algorithm is implemented.
- **GA_insole/data_process**: This directory contains scripts that demonstrate the process of selecting and cleaning raw data. These scripts are essential for preparing the data for use with the genetic algorithm.
- **GA_insole/visualize**: This folder includes scripts for generating visualizations based on the paper's requirements. These visualizations help in understanding the output of the genetic algorithm and the effectiveness of the insole designs.

## Usage
### Data Preparation
Ensure your data is formatted according to the project requirements, which should include parameters such as arch length, width, and height.

### Running the Algorithm
Clone the repository
```bash
git clone https://github.com/euyis1019/GA_Multi-obj-optimization
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the Test program:
```bash
python Model_GA.py
```
You can adjust the settings of the genetic algorithm, such as population size and number of iterations, by modifying the `config.json` file.

## Contribution Guide
Community contributions to this project are welcome. You can participate by:
- Reporting bugs or suggesting features through Issues
- Submitting Pull Requests to improve code or documentation

## License
This project is licensed under the MIT License. For details, see the [LICENSE](LICENSE) file.

## Contact Information
If needed, please contact us via email at: u08yg22@abdn.ac.uk
