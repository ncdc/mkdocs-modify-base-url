# mkdocs-modify-base-url

This mkdocs plugin is meant to be used with:

- [mkdocs-material](https://squidfunk.github.io/mkdocs-material/
- [mike](https://github.com/jimporter/mike) for multiple versions of your documentation
- [multi-language documentation](https://github.com/squidfunk/mkdocs-material/discussions/2346)

The code in mkdocs-material that renders the version selection dropdown in the header dynamically requests
`versions.json` relative to the page's `base_url`. This works well normally, but when you try to add multiple
languages, things start to get a bit tricky.

I've set up my project documentation inside my repo like this:

```
.
├─ config/
│    ├─ en/
│    │  └─ mkdocs.yml
│    ├─ nl/
│    │  └─ mkdocs.yml
│    ├─ .../
│
├─ content/
│    ├─ en/
│    │   ├─ index.md 
│    │   └─ ...
│    └─ nl/
│        ├─ index.md 
│        └─ ,,,
│
├─ generated/
│    ├─ branch
│    │  ├─ en/
│    │  └─ nl/
│    └─ index.html
│
└─ ...
```

Each language has its own `mkdocs.yml`. Each is configured like this (only showing relevant parts, using `en` as 
  an example):

```yaml
docs_dir: '../../content/en'
site_dir: '../../generated/branch/en'
theme:
  language: en
extra:
  version:
    provider: mike
  alternate:
  - name: English
    link: en
    lang: en

plugins:
- modify-base-url:
    prefix: '../'
```

All languages are individually generated into `docs/generated/branch/$LANGUAGE`

There is a separate `mkdocs.yml` for `mike` to support versioning. There is really only one key, required setting, that
tells `mike` to use what we previously generated:

```yaml
docs_dir: generated/branch
```

When you run `mike deploy VERSION` from within the `docs` directory, it combines all the generated documentation for 
all the languages into a single version. There is also a static `index.html` file in `docs/generated/branch` that 
redirects initial requests to a default language.

Given a URL such as `docs.kcp.io/kcp/main/en`, when visiting `index.html`, its `base_url` is normally `.` because we 
told `mkdocs` to generate directly into the `en` directory. What's unique about this situation is that `mkdocs` 
thinks that one level up from `en` should be where `versions.json` lives. But it's actually up one more level, at
`docs.kcp.io/kcp/versions.json` because of our configuration.

And this is why this plugin exists. We need to adjust the `base_url` to move it up one more level, so instead of it 
being `.` for `docs.kcp.io/kcp/main/en/index.html`, it's actually `..`. Now, when `mkdocs-material` requests 
`base_url/../versions.json`, that becomes `../../versions.json`, which is really `docs.kcp.io/kcp/versions.json`.
