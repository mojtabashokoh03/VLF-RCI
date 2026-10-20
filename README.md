# VLF-RCI
# Phishing Website Dataset and VLF–RCI Feature Extraction

## 1. Data Collection

Use **Critical_Moment**, a software tool developed using **.NET Framework 4**, to collect information about phishing websites.

Configure the database connection settings in the `app.config` file before running the software.

## 2. Database Setup

To create the database tables, use the SQL queries provided in the `database` file located in the project directory. Execute the queries to create the required database structure before collecting data.

## 3. Feature Extraction

After collecting the website information, use the following Python script to extract features related to **VLF** and **RCI**:

```bash
python ExtractVLFRCIfeature.py
```

## 4. Final Dataset

The final dataset, collected and curated by our team after removing invalid entries, is provided in the `Dataset` directory as two compressed RAR archives.

Extract the archives using [WinRAR](https://www.win-rar.com/) to access and use the dataset.

## 5. Experimental Evaluation

The experiments reported in our research were conducted using the following scripts:

- **`Maincode.py`** — Main experimental implementation.
- **`Allkfold.py`** — Experiments using multiple K-fold cross-validation configurations.
- **`Ablationvisual.py`** — Ablation study comparisons and visualization.

Please ensure that the required Python libraries and dependencies are installed before running the scripts.

## 6. Additional Data Availability

The original website source data comprises approximately **240 GB**, and the website screenshots account for approximately **12 GB**.

Due to GitHub's file size and storage limitations, these large-scale data sources could not be uploaded to this repository.

Researchers who require access to the original source data and website screenshots may contact us by email. We will discuss feasible methods for transferring the data.

## 7. Contact Information

For questions, research collaboration, or requests for access to the additional datasets, please contact:

- **Mojtaba Shokoh:** [Mojtaba.shokoh03@gmail.com](mailto:Mojtaba.shokoh03@gmail.com)
- **Institutional email:** [shokoh@pgs.usb.ac.ir](mailto:shokoh@pgs.usb.ac.ir)

We welcome inquiries from researchers interested in reproducing our experiments or conducting further research using this dataset and codebase.
