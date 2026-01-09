# 📊 Auto EDA Generator

A modern, web-based Exploratory Data Analysis (EDA) tool built with Streamlit and ydata-profiling. Transform your CSV data into comprehensive insights with just a few clicks!

## ✨ Features

### 🎨 Modern UI/UX Design
- **Neumorphic Design Components**: Clean, modern card-based interface with soft shadows
- **Gradient Color Scheme**: Beautiful purple-to-pink gradient theme (#667eea → #764ba2)
- **Micro-interactions**: Smooth hover effects on buttons, cards, and inputs
- **Fluid Animations**: Fade-in animations with 0.6s ease-out transitions
- **Responsive Layout**: Fully responsive design with breakpoints at 480px, 768px, and 1024px
- **8-point Grid System**: Consistent spacing and alignment (8px, 16px, 24px, 32px, 48px)
- **Accessibility Standards**: WCAG compliant color contrast and visible focus states
- **Visual Depth**: Strategic shadow usage for depth and hierarchy
- **Color Gradients**: Primary gradient for headers and buttons, secondary for dividers
- **Custom Selectors**: Proper Streamlit component styling with data-testid attributes
- **Cross-browser Compatibility**: Tested on Chrome 90+, Firefox 88+, Safari 14+, Edge 90+, Opera 76+

### 🚀 Core Functionality
- **Drag & Drop Upload**: Easily upload CSV files via drag and drop
- **URL Import**: Load data directly from public CSV URLs
- **Dataset Preview**: Quick overview of your data with summary statistics
- **Comprehensive EDA Report**: Generate detailed reports including:
  - Variable types and distributions
  - Missing values analysis
  - Correlation matrices
  - Data quality insights
  - Visualizations and plots
- **HTML Export**: Download complete EDA reports as HTML files

### 📊 Analysis Capabilities
- **Descriptive Statistics**: Mean, median, mode, std deviation, etc.
- **Data Types**: Automatic detection and validation
- **Missing Values**: Analysis of missing data patterns
- **Correlations**: Heatmaps and correlation coefficients
- **Outlier Detection**: Statistical outlier identification
- **Distribution Analysis**: Histograms and density plots
- **Categorical Analysis**: Value counts and frequency distributions

## 🛠️ Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Streamlit** | 1.52.2 | Web framework and UI components |
| **ydata-profiling** | 4.18.0 | Automated EDA report generation |
| **Pandas** | 2.3.3 | Data manipulation and analysis |
| **NumPy** | 2.3.5 | Numerical computations |
| **Matplotlib** | 3.10.0 | Visualization library |
| **Seaborn** | 0.13.2 | Statistical data visualization |
| **Requests** | 2.32.5 | HTTP requests for URL imports |

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/Tanvir-yzu/pandas_profiling.git
cd "Streamlit Auto-EDA app"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv myenv
myenv\Scripts\activate

# On macOS/Linux
python3 -m venv myenv
source myenv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`

## 🚀 Usage

### Method 1: Upload CSV File
1. Click or drag your CSV file into the upload area
2. Wait for the dataset to load
3. Review the dataset preview and statistics
4. Click "🚀 Generate EDA Report" to create the analysis

### Method 2: Load from URL
1. Paste the direct URL to a CSV file
2. Wait for the data to fetch
3. Review the dataset preview and statistics
4. Click "🚀 Generate EDA Report" to create the analysis

### Exporting Reports
After generating an EDA report:
- View the interactive report directly in the browser
- Click "⬇️ Download HTML Report" to save the complete analysis

## 📋 Supported File Formats

| Format | Extension | Support |
|--------|-----------|---------|
| Comma Separated Values | `.csv` | ✅ Full Support |

*Note: Currently, only CSV files are supported. Additional formats may be added in future versions.*

## 🎨 Color Scheme

### Primary Colors
- **Primary Gradient**: `#667eea` → `#764ba2` (Purple)
- **Secondary Gradient**: `#f093fb` → `#f5576c` (Pink)
- **Accent Purple**: `#8b5cf6`
- **Accent Pink**: `#ec4899`

### Neutral Colors
- **Background**: `#f8fafc` (Light Slate)
- **Surface**: `#ffffff` (White)
- **Text Primary**: `#1e293b` (Dark Slate)
- **Text Secondary**: `#64748b` (Medium Slate)
- **Border**: `#e2e8f0` (Light Gray)

### Functional Colors
- **Success**: `#4ade80` (Green)
- **Warning**: `#f59e0b` (Orange)
- **Error**: `#ef4444` (Red)

## 📐 Design System

### Typography
- **Font Family**: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
- **Headings**: 1.6rem - 3rem with 700-800 weight
- **Body**: 1rem with 400 weight
- **Buttons**: 1.1rem with 600 weight

### Spacing (8-point Grid)
- **XS**: 8px (0.5rem)
- **SM**: 16px (1rem)
- **MD**: 24px (1.5rem)
- **LG**: 32px (2rem)
- **XL**: 48px (3rem)

### Border Radius
- **Small**: 12px (Inputs)
- **Medium**: 16px (Buttons)
- **Large**: 20px (File Upload)
- **X-Large**: 24px (Cards, Header)

### Shadows
- **Subtle**: `0 4px 6px rgba(0, 0, 0, 0.04)`
- **Medium**: `0 8px 12px rgba(0, 0, 0, 0.08)`
- **Strong**: `0 10px 40px rgba(102, 126, 234, 0.3)`

## 🌐 Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Full Support |
| Firefox | 88+ | ✅ Full Support |
| Safari | 14+ | ✅ Full Support |
| Edge | 90+ | ✅ Full Support |
| Opera | 76+ | ✅ Full Support |

## 📱 Responsive Breakpoints

| Device | Width | Layout |
|--------|-------|--------|
| Desktop | > 1024px | 3-column layout |
| Laptop | 768px - 1024px | 2-column layout |
| Tablet | 480px - 768px | Single column with adjusted spacing |
| Mobile | < 480px | Single column with optimized touch targets |

## 🔧 Configuration

### Customization Options

The application can be customized by modifying the CSS in `app.py`:

```python
# Change color scheme
st.markdown("""
    <style>
        .gradient-header {
            background: linear-gradient(135deg, #your-color1, #your-color2);
        }
    </style>
""", unsafe_allow_html=True)

# Change button colors
st.markdown("""
    <style>
        div[data-testid="stButton"] > button {
            background: linear-gradient(135deg, #your-color1, #your-color2) !important;
        }
    </style>
""", unsafe_allow_html=True)
```

### Performance Settings

For large datasets, you can adjust the following parameters in `app.py`:

```python
# Adjust preview rows
st.dataframe(df.head(), use_container_width=True, height=300)

# Adjust EDA report detail level
profile = ProfileReport(df, explorative=True)
# Set to False for faster generation with less detail

# Sample data for very large datasets
df_sample = df.sample(n=10000, random_state=42)
profile = ProfileReport(df_sample, explorative=True)
```

### Animation Settings

To disable animations for better performance:

```python
# Comment out or remove animate-fade-in classes
# Example:
# <div class="gradient-header animate-fade-in">
# becomes:
# <div class="gradient-header">
```

### Theme Variations

**Blue Theme:**
```python
background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)
```

**Green Theme:**
```python
background: linear-gradient(135deg, #10b981 0%, #059669 100%)
```

**Orange Theme:**
```python
background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%)
```

## 🐛 Troubleshooting

### Common Issues

**Issue: Application won't start**
```bash
# Solution: Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Streamlit installation
streamlit --version

# If version issues, reinstall streamlit
pip install --upgrade streamlit
```

**Issue: CSV file won't upload**
```bash
# Solution: Check file format
# Ensure file is UTF-8 encoded CSV
# File size should be < 100MB for optimal performance

# Verify CSV structure
# - Should have headers in first row
# - No special characters in column names
# - Consistent delimiters (comma for CSV)
```

**Issue: EDA report generation is slow**
```bash
# Solution: Reduce dataset size or simplify columns
# Or reduce explorative parameter in app.py:
profile = ProfileReport(df, explorative=False)

# For very large datasets (>100MB):
# 1. Sample the data first
df_sample = df.sample(n=10000)
# 2. Exclude columns with too many unique values
# 3. Disable specific analyses if not needed
```

**Issue: URL import fails**
```bash
# Solution: Verify URL points directly to CSV file
# Ensure file is publicly accessible
# Check internet connection

# Test URL in browser first
# Should start with http:// or https://
# Should end with .csv or point to CSV content
# No authentication required
```

**Issue: Colors or styles not displaying correctly**
```bash
# Solution: Clear browser cache
# Try incognito/private mode
# Check browser compatibility (use Chrome, Firefox, Safari, Edge, or Opera 90+)

# If using older browsers:
# - Gradients may not render
# - Animations may be disabled
# - Shadows may appear differently
```

**Issue: Animations not smooth**
```bash
# Solution: Check hardware acceleration
# Reduce dataset size for better performance
# Close other browser tabs
# Update graphics drivers
```

## 📚 Project Structure

```
Streamlit Auto-EDA app/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.MD             # This file
├── .gitignore            # Git ignore rules
└── myenv/                # Virtual environment (not committed)
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test with various CSV file sizes
- Ensure responsive design compatibility
- Maintain color scheme consistency

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgments

- **Streamlit Team** - For the amazing web framework that makes data apps easy
- **ydata-profiling** - For the powerful automated EDA library
- **Design Inspiration** - Modern UI/UX patterns from Dribbble, Behance, and Tailwind CSS
- **Pandas Team** - For the essential data manipulation library
- **Python Community** - For the incredible ecosystem of data science tools

## 💡 Tips & Best Practices

### Data Preparation
1. **Clean column names**: Use clear, descriptive names without special characters
2. **Consistent data types**: Ensure each column has a consistent data type
3. **Handle missing values**: Decide whether to fill or drop missing values before analysis
4. **Remove duplicates**: Consider removing duplicate rows for accurate statistics
5. **Normalize formats**: Use consistent date, number, and text formats

### Getting the Most from EDA Reports
- Review the "Overview" tab first for high-level insights
- Check "Variables" tab for detailed column-by-column analysis
- Use "Correlations" tab to identify relationships between variables
- Examine "Missing values" to understand data completeness
- Look at "Warnings" section for potential data quality issues

### Performance Optimization
- For datasets >50MB, consider sampling first
- Remove unnecessary columns before loading
- Use appropriate data types (e.g., category for low-cardinality strings)
- Close other applications to free up memory
- Use a machine with at least 8GB RAM for large datasets

## 📞 Support

For support, please:
- Open an issue on GitHub with detailed description
- Include: CSV file size, dataset structure, error messages
- Provide: Screenshots of errors, browser version, Python version
- Check the documentation at: [Project Wiki]
- Contact: your.email@example.com

### Quick Tips
- Start with small datasets to test functionality
- Ensure CSV files have headers in the first row
- Use UTF-8 encoding for special characters
- Clear browser cache if styles don't load correctly
- Disable browser extensions if experiencing issues
- Check console (F12) for JavaScript errors

## 🔄 Version History

### Version 1.0.0 (Current)
- ✅ Initial release
- ✅ Drag & drop CSV upload with modern neumorphic UI
- ✅ URL import functionality with error handling
- ✅ Modern UI with gradient purple-to-pink design
- ✅ Responsive layout for all device sizes (mobile, tablet, desktop)
- ✅ Comprehensive EDA reports powered by ydata-profiling
- ✅ HTML export functionality for reports
- ✅ Accessibility compliance (WCAG standards)
- ✅ Micro-interactions and smooth animations
- ✅ 8-point grid system for consistent spacing
- ✅ Dataset preview with summary statistics (rows, columns, total cells)
- ✅ Real-time loading indicators with spinner animations
- ✅ Cross-browser compatibility (Chrome, Firefox, Safari, Edge, Opera)

## 🚀 Future Enhancements

### Planned Features
- [ ] Support for additional file formats (Excel, JSON, Parquet)
- [ ] Interactive data cleaning tools (missing value imputation, outlier removal)
- [ ] Custom report templates and styling options
- [ ] Database connectivity (PostgreSQL, MySQL, SQLite)
- [ ] Data export in multiple formats (Excel, PDF, JSON)
- [ ] Collaborative features (shared workspaces, comments)
- [ ] Cloud deployment options (Streamlit Cloud, Heroku, AWS)
- [ ] Advanced visualizations with Plotly interactivity
- [ ] Machine learning model insights and feature importance
- [ ] Report scheduling and automation (daily, weekly reports)
- [ ] Dark mode theme support
- [ ] Multiple language support
- [ ] Data transformation tools (pivot, merge, aggregate)
- [ ] Advanced filtering and search capabilities
- [ ] Report comparison (compare multiple datasets)
- [ ] Export to PowerPoint presentations

### Known Limitations
- Maximum recommended file size: 100MB (larger files may cause performance issues)
- Only CSV format currently supported
- No database connectivity in current version
- All analysis must be regenerated after data changes (no caching)
- Reports are generated server-side, not real-time updates

## 📈 Performance

| Dataset Size | Load Time | Report Generation |
|--------------|-----------|-------------------|
| < 1MB | < 1s | < 5s |
| 1-10MB | 1-3s | 5-15s |
| 10-50MB | 3-10s | 15-30s |
| > 50MB | 10-30s | 30-60s |

*Performance may vary based on system specifications and data complexity*

## 🔒 Privacy & Security

- All data processing happens locally on your machine
- No data is sent to external servers
- Uploaded files are processed in-memory and not stored
- URL imports only fetch from public sources
- No user data collection or tracking

### Security Best Practices
- Only upload data you have the right to analyze
- Be cautious with sensitive information in CSV files
- URL imports work best with trusted sources
- Generated HTML reports contain your data - share carefully

## 🌟 Star History

If you find this project helpful, please consider giving it a star ⭐️

---

**Built with ❤️ using Streamlit & ydata-profiling**
