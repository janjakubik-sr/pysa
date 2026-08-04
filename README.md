# PySA

PySA (Pythonic Statistical Analysis) is a desktop application for running common statistical analyses and machine-learning workflows on small, file-based data sets. It provides a wxPython graphical interface around a collection of focused Python scripts, allowing users to select an analysis, choose an input file, enter method-specific parameters, and inspect the generated results without building a Python workflow from scratch.

> **Project status:** PySA is under active development. Check generated results before using them in production or publication workflows.

## Features

- Data editing, sorting, axis swapping, value transformations, and uncertainty propagation
- One-sample, paired, and Welch's t-tests
- Shapiro-Wilk testing, one-way and two-way ANOVA, and Tukey HSD comparisons
- Linear and multiple linear regression
- Pearson and Spearman correlations, including annotated and grouped data
- Correlation-matrix heat maps
- Nested-model F-tests and corrected Akaike information criterion (AICc)
- K-means, spectral, and HDBSCAN clustering
- Decision trees, LightGBM classification, model selection, and principal component analysis (PCA)
- Integration with optional tools such as Grace, IPython, R, pyspread, and a terminal

## How PySA Works

`bin/pysa.py` starts the main wxPython window and exposes the available operations through menus. When an operation is selected, PySA:

1. opens a dialog for the required input file and parameters;
2. runs the corresponding script from `bin/` in the application process;
3. performs the calculation with NumPy, SciPy, pandas, statsmodels, scikit-learn, or another method-specific library;
4. writes result tables, plots, Grace files, or transformed data to the current working directory; and
5. reads the operation's `temp.log` file and displays its summary in the main window.

Use **File > Working Directory** to choose where PySA should read and write data. The **Help > Examples** menu opens the bundled example directories.

## Input and Output

PySA works with plain-text `.dat` files and comma-separated `.csv` files. The required layout depends on the selected analysis:

- Most basic statistics and clustering tools read headerless, whitespace-delimited numeric `.dat` files.
- Two-variable methods generally expect `x` and `y` in the first two columns. Annotated or grouped correlation variants expect their additional fields in subsequent columns.
- One-way ANOVA treats the columns of a numeric `.dat` file as the samples being compared.
- Two-way ANOVA reads a CSV file with column names and asks which columns contain the group, explanatory, and response variables.
- Machine-learning and PCA tools read CSV files with column names. These workflows generally expect identifiers in the first column, predictors in the middle columns, and the target in the final column.

The file-selection dialogs describe the layout required by each operation. Working examples are available under `Examples/Statistics`, `Examples/F-test`, and `Examples/Cluster`.

Result filenames are derived from the input filename and analysis name, commonly using `.res`, `.out`, `.data`, `.draw`, `.agr`, or an image extension. They are saved alongside the working data unless a tool states otherwise.

> **Warning:** sorting, axis-swapping, and value-transformation commands save their output over the selected input file. Keep a backup of source data before using commands from **Data Transformation**.

## Requirements

- Python 3.10
- wxPython 4.2 or a compatible wxPython 4 release
- NumPy, SciPy, matplotlib, pandas, seaborn, Plotly, scikit-learn, statsmodels, and uncertainties
- HDBSCAN, LightGBM, and LazyPredict for their corresponding machine-learning workflows
- Grace or a compatible Grace frontend for `.draw` and `.agr` plotting features (optional)
- IPython, R, pyspread, and a supported terminal emulator for the corresponding auxiliary-app shortcuts (optional)

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/janjakubik-sr/pysa.git
cd pysa
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install wxPython numpy scipy matplotlib pandas seaborn plotly \
  scikit-learn statsmodels uncertainties hdbscan lightgbm lazypredict
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

wxPython may require operating-system packages or a platform-specific wheel. Consult the wxPython installation guidance for your platform if `pip` cannot build it.

## Configuration

Before starting PySA, edit `bin/preferences.py`:

1. Set `install_dir`, `doc_dir`, and `example_dir` to the absolute paths of the repository's `bin`, `Documentation`, and `Examples` directories. Keep the trailing path separator.
2. Adjust `width` and `height` if needed.
3. Set the `cmdIP`, `cmdGG`, `cmdGB`, `cmdR`, `cmdSh`, and `cmdspread` commands to match the auxiliary applications installed on your system.

The Preferences window in PySA edits this same file.

## Running the Application

Start PySA from the repository root while the virtual environment is active:

```bash
python bin/pysa.py
```

Then choose a working directory, select an operation from the menus, and follow the prompts. Messages and result summaries appear in the main window; use **File > Save log** to preserve the session log.

For regular use, create a shell script, desktop entry, or Windows shortcut that launches `bin/pysa.py` with the configured Python environment.

## Project Structure

```text
pysa/
|-- bin/             # GUI launcher and individual analysis scripts
|-- Documentation/   # Installation and help content
|-- Examples/        # Sample inputs and generated outputs
|-- Change.log       # Project change history
|-- requirements.txt # Dependency inventory
`-- README.md
```

## License

PySA is distributed for non-commercial use under the Creative Commons Attribution-NonCommercial (CC BY-NC) license. Copyright and authorship belong to Jan Jakubik. See the source headers and application **About** dialog for the project's licensing notice.

## Author

Jan Jakubik (<jakubik@biomed.cas.cz>)
