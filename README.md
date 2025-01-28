# Resume-to-Portfolio Architect AI 🤖

**Transform your resume into a professional developer portfolio in 3 steps**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![React 18+](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)

## Project Overview 🚀

This AI-powered pipeline converts resume documents (PDF/DOC) into fully functional portfolio websites through:

1. **Smart Resume Analysis** - Extract structured data from resumes
2. **Design Customization** - Interactive preference questionnaire
3. **Code Generation** - Production-ready React website output

## Key Features ✨

- 📄 Automatic extraction of skills, experience, and education data
- 🎨 Customizable design system with theme options
- ⚡ Generated React components with Framer Motion animations
- 📱 Mobile-first responsive layouts
- 🛠️ Complete developer workflow integration

## Installation 💻

```bash
# Clone repository
git clone https://github.com/yourusername/resume-portfolio-architect.git
cd resume-portfolio-architect

# Install Python dependencies
pip install python-docx pdfplumber deepseek-api

# Install React dependencies (for generated website)
cd generated-portfolio
npm install
```
## Configuration ⚙️

1. Get Deepseek API key from [https://platform.deepseek.com](https://platform.deepseek.com)
2. Create `.env` file:
```python
DEEPSEEK_API_KEY="your_api_key_here"
```

## Usage 🛠️

```python
# Process resume and generate questionnaire
python main.py --resume path/to/resume.pdf

# Generate portfolio website after answering questions
python build_portfolio.py --answers answers.json
```

## Project Structure 📂

```bash
generated-portfolio/
├── public/
└── src/
    ├── components/      # All React components
    ├── styles/          # CSS Modules and theme
    ├── data/            # Processed resume data
    └── App.jsx          # Root component
```

## Customization 🎨

Modify `theme.css` to customize colors and styling:
```css
:root {
  --primary-color: #3D9970;  /* Tech Green */
  --secondary-color: #FF851B; /* Orange accent */
  --spacing-unit: 12px;      /* Base spacing */
}
```

## Contributing 🤝

Contributions welcome! Please follow:
1. Fork the repository
2. Create your feature branch
3. Commit changes with descriptive messages
4. Push to the branch
5. Open a pull request

## License 📄

MIT License - see [LICENSE](LICENSE) for details

---

**Disclaimer**: This project requires your own Deepseek API key. API usage costs may apply.
