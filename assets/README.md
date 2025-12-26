# Assets Directory

This directory is for storing static assets like images, logos, and icons.

## Suggested Structure

```
assets/
├── images/
│   ├── logo.png
│   ├── banner.png
│   └── screenshots/
├── icons/
│   └── favicon.ico
└── docs/
    └── user_guide.pdf
```

## Usage

Place any static files here that you want to reference in the application.

To use images in Streamlit:
```python
st.image("assets/images/logo.png")
```

## Notes

- Keep file sizes reasonable for web performance
- Use compressed/optimized images where possible
- Follow consistent naming conventions
