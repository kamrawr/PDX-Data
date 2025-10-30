# Repository Guide

Welcome to the PDX-Data repository! This guide will help you navigate the project structure and find what you need.

## 📁 Directory Structure

```
PDX-Data/
│
├── 🌐 index.html                    # Project website (GitHub Pages)
├── 📄 README.md                     # Main project documentation
├── ⚖️ LICENSE                        # MIT License
├── 📚 CITATION.cff                  # Citation metadata
├── 📦 requirements.txt              # Python dependencies
│
├── 📊 data/                         # Dataset information
│   ├── README.md                   # Data access guide
│   ├── data_summary.txt           # Collection statistics
│   ├── advanced_analysis_results.txt
│   └── deep_analysis_summary.txt
│
├── 📖 docs/                         # Documentation
│   ├── DATA_DICTIONARY.md         # Complete field reference
│   ├── METHODOLOGY.md             # Collection process
│   └── REPOSITORY_GUIDE.md        # This file
│
├── 💻 examples/                     # Analysis examples
│   ├── README.md                   # Usage guide
│   ├── basic_analysis.py          # Starter analysis script
│   ├── advanced_analysis.py       # Advanced analysis
│   └── deep_analysis.py           # Deep dive analysis
│
├── 🛠️ tools/                        # Data collection tools
│   ├── README.md                   # Tools documentation
│   ├── portlandmaps_scrape.py     # Main scraper
│   ├── portlandmaps_scrape_reverse.py
│   ├── cleanup_and_merge.py       # Data consolidation
│   ├── create_quality_subsets.py  # Quality filtering
│   ├── test_alameda.py           # Test/development
│   └── alameda_page_source.html   # Reference HTML
│
├── 📥 raw_downloads/                # Individual CSVs (gitignored)
├── 🗂️ subsets/                      # Filtered datasets (gitignored)
└── 📊 Portland_Assessor_AllNeighborhoods.csv  # Main dataset (gitignored)
```

## 🎯 Quick Navigation

### For Data Users

**Want to analyze the data?**
1. Start with [`README.md`](../README.md) for overview
2. Read [`data/README.md`](../data/README.md) for data access
3. Check [`docs/DATA_DICTIONARY.md`](DATA_DICTIONARY.md) for field definitions
4. Browse [`examples/`](../examples/) for code samples

**Need help with specific fields?**
- Go to [`docs/DATA_DICTIONARY.md`](DATA_DICTIONARY.md)
- Search for the field name
- Find type, description, examples, and completeness info

**Want to understand data quality?**
- Read [`docs/METHODOLOGY.md`](METHODOLOGY.md)
- See "Data Validation" and "Limitations" sections

### For Researchers

**Planning to cite this work?**
1. Check [`CITATION.cff`](../CITATION.cff) for formatted citation
2. See [`README.md`](../README.md) citation section for BibTeX
3. Review [`LICENSE`](../LICENSE) for usage terms

**Understanding the methodology?**
- Read [`docs/METHODOLOGY.md`](METHODOLOGY.md) thoroughly
- Review collection timeline and process
- Note limitations and considerations

### For Developers

**Want to collect fresh data?**
1. Review [`tools/README.md`](../tools/README.md)
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python tools/portlandmaps_scrape.py`
4. Process: `python tools/create_quality_subsets.py`

**Contributing code?**
1. Fork the repository
2. Make changes in appropriate directory
3. Update relevant README files
4. Submit pull request

**Modifying the website?**
- Edit [`index.html`](../index.html)
- Test locally before committing
- GitHub Pages will auto-deploy

## 📚 Documentation Files

### Main Documentation

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Project overview, quick start | Everyone |
| `data/README.md` | Dataset descriptions, access | Data users |
| `docs/DATA_DICTIONARY.md` | Field definitions | Analysts, researchers |
| `docs/METHODOLOGY.md` | Collection process | Researchers, validators |
| `docs/REPOSITORY_GUIDE.md` | Navigation help | New users |
| `examples/README.md` | Analysis examples | Data scientists |
| `tools/README.md` | Scraping tools | Developers |

### Supporting Files

| File | Purpose |
|------|---------|
| `CITATION.cff` | Structured citation metadata |
| `LICENSE` | MIT License + data notice |
| `requirements.txt` | Python dependencies |
| `data/data_summary.txt` | Collection statistics |

## 🔍 Common Tasks

### Exploring the Data

**Q: Where do I find the actual data files?**
- A: Due to size, data files are gitignored. See [`data/README.md`](../data/README.md) for access options.

**Q: What's the difference between the datasets?**
- A: See "Available Datasets" in [`README.md`](../README.md) or [`data/README.md`](../data/README.md)

**Q: How do I know which fields are available?**
- A: Check [`docs/DATA_DICTIONARY.md`](DATA_DICTIONARY.md) for complete schema

### Running Analysis

**Q: How do I get started with Python analysis?**
- A: Run `python examples/basic_analysis.py` after obtaining data

**Q: What libraries do I need?**
- A: `pip install pandas matplotlib seaborn` (see [`examples/README.md`](../examples/README.md))

**Q: Can I see example code?**
- A: Yes! Browse [`examples/`](../examples/) directory

### Collecting Data

**Q: How long does data collection take?**
- A: ~12 hours for complete collection (see [`docs/METHODOLOGY.md`](METHODOLOGY.md))

**Q: Can I collect only specific neighborhoods?**
- A: Yes, modify the scraper in `tools/portlandmaps_scrape.py`

**Q: How do I update the data?**
- A: Re-run the scraper tools (see [`tools/README.md`](../tools/README.md))

## 🚀 Getting Started Paths

### Path 1: Quick Analysis (30 minutes)
1. Read [`README.md`](../README.md) (5 min)
2. Obtain data from [`data/README.md`](../data/README.md) (10 min)
3. Run `examples/basic_analysis.py` (5 min)
4. Review output and explore (10 min)

### Path 2: Deep Research (2-3 hours)
1. Read all main documentation (30 min)
2. Study [`docs/DATA_DICTIONARY.md`](DATA_DICTIONARY.md) (30 min)
3. Review [`docs/METHODOLOGY.md`](METHODOLOGY.md) (30 min)
4. Explore data with custom analysis (1 hour)

### Path 3: Data Collection (1-2 days)
1. Review [`tools/README.md`](../tools/README.md) (15 min)
2. Understand [`docs/METHODOLOGY.md`](METHODOLOGY.md) (30 min)
3. Set up environment and dependencies (30 min)
4. Run data collection (12 hours automated)
5. Process and validate (1 hour)

## 📝 File Formats

### Markdown (.md)
All documentation uses Markdown for readability and GitHub compatibility.

### Python (.py)
Analysis examples and scraping tools are in Python 3.x.

### CSV (.csv)
All data outputs are in CSV format for broad compatibility.

### HTML (.html)
Project website and reference pages.

### CFF (.cff)
Citation File Format for academic citations.

## 🔗 External Resources

- **Project Website**: https://communityconsultingpartners.github.io/PDX-Data
- **GitHub Repository**: https://github.com/CommunityConsultingPartners/PDX-Data
- **Data Source**: https://www.portlandmaps.com/advanced/?action=assessor
- **Issues/Support**: https://github.com/CommunityConsultingPartners/PDX-Data/issues

## 💡 Tips

1. **Start Small**: Use the Portland-focused subset for initial exploration
2. **Read the Docs**: Most questions are answered in documentation
3. **Check Examples**: See working code before writing your own
4. **Cite Properly**: Use provided citation formats
5. **Report Issues**: Help improve the project by reporting bugs

## 📧 Need Help?

1. Check this guide first
2. Browse relevant documentation
3. Look at example code
4. Search GitHub issues
5. Open a new issue if needed

---

**Last Updated**: October 30, 2024  
**Guide Version**: 1.0
