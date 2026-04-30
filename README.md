# Lucianosrp.github.io

Static blog powered by [Zola](https://getzola.org/).

## Adding a new blog post

1. Create a new `.md` file in `content/blog/`

2. Use this format:

```markdown
+++
title = "Your Post Title"
date = 2024-12-01
draft = false
+++

Your content here. Markdown is fully supported.
```

3. Run `zola build` to generate the static site

4. Preview locally with `zola serve`

## Zola commands

```bash
zola build      # Build the site
zola serve     # Build and serve locally (with live reload)
zola check     # Validate links and config
```

## Configuration

- `config.toml` — site settings (title, description, author)
- `templates/` — HTML templates (Tera)
- `static/` — CSS, fonts, and other static assets

## Styling

CSS lives in `static/style.css`. Key colors are CSS variables:

```css
:root {
  --bg: #fefefe;        /* background */
  --text: #1a1a1a;     /* text color */
  --accent: #c05b2c;   /* accent color */
  --border: #e5e5e5;   /* borders */
}
```

Dark mode follows `prefers-color-scheme`.

## Typography

- Body: Geist Mono (monospace)
- Headings: Newsreader (serif)
- Code: Geist Mono

## Deployment

The built site is in `public/`. Push to your GitHub Pages branch or use GitHub Actions.

## Post requirements

- Date format: `YYYY-MM-DD`
- `draft = true` hides the post from production builds
- `reading_time` is auto-calculated from word count