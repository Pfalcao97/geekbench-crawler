# Geekbench Crawler
### A tool made to scrape Geekbench's results into a more automation friendly format.

Take the HTML page with the results from a benchmark and transform's them into a simple CSV file - useful for automations and batch benchmarking.

![image](https://github.com/user-attachments/assets/7c4ee406-6ced-4601-8cac-c9bd3b3f6985)

## How to use?

This tool was made using Astral's `uv` tool, so you'll need [to have it installed](https://docs.astral.sh/uv/getting-started/installation/):

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Once you've cloned this repository into your local machine, you can `cd` into it's path and run it:

```
uv run main.py {{geekbench id}}
```

You can add flags such as `--verbose` to show more info. 

![image](https://github.com/user-attachments/assets/7107e628-c933-4086-96a5-baae9e9a7b75)


## To Do

- [x] Code for "simple" leve of extraction.
- [ ] Code for "discrete" level of extraction.
- [x] Output a CSV file.
- [ ] Output a human friendly XLSX file.
