import requests
import xml.etree.ElementTree as ET
import gzip
import io
import pandas as pd
from tqdm import tqdm
from rich import print
from rich.panel import Panel

NAMESPACE = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

def fetch_sitemap_content(sitemap_url):
    try:
        response = requests.get(sitemap_url, timeout=10)
        response.raise_for_status()

        if sitemap_url.endswith('.gz'):
            with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
                content = f.read()
        else:
            content = response.content

        return ET.fromstring(content)
    except Exception as e:
        print(f"[red]Error fetching {sitemap_url}[/red]: {e}")
        return None

def fetch_sitemap_urls(sitemap_url, depth=0):
    urls = []
    indent = "  " * depth
    print(f"{indent}[cyan]Fetching:[/cyan] {sitemap_url}")

    root = fetch_sitemap_content(sitemap_url)
    if root is None:
        print(f"{indent}[red]Failed to parse:[/red] {sitemap_url}")
        return urls

    if root.tag.endswith('sitemapindex'):
        for sitemap in root.findall('ns:sitemap', NAMESPACE):
            loc = sitemap.find('ns:loc', NAMESPACE)
            if loc is not None:
                child_url = loc.text.strip()
                urls.extend(fetch_sitemap_urls(child_url, depth + 1))
    elif root.tag.endswith('urlset'):
        found = 0
        for url in root.findall('ns:url', NAMESPACE):
            loc = url.find('ns:loc', NAMESPACE)
            if loc is not None:
                urls.append(loc.text.strip())
                found += 1
        print(f"{indent}[green]Found {found} URLs in:[/green] {sitemap_url}")

    return urls


def save_to_file(brand_name, urls):
    df = pd.DataFrame({'brand': [brand_name] * len(urls), 'product_url': urls})
    df = df.drop_duplicates(subset='product_url').reset_index(drop=True)
    filename = f"{brand_name.lower().replace(' ', '').replace('.', '')}_urls.csv"
    df.to_csv(filename, index=False)
    print(f"\n[green]Saved {len(df)} filtered URLs to {filename}[/green]")


def main():
    print(Panel.fit("[bold white on red] UNIVERSAL SITEMAP URLs EXTRACTOR [/bold white on red]", border_style="bright_yellow"))
    brand = input("Enter brand name: ").strip()
    sitemap_url = input("Enter sitemap URL: ").strip()
    include_keywords_input = input("Enter keywords to include (comma separated, leave empty to include all): ").strip()
    exclude_keywords_input = input("Enter keywords to exclude (comma separated, optional): ").strip()

    include_keywords = [word.strip().lower() for word in include_keywords_input.split(",") if word.strip()]
    exclude_keywords = [word.strip().lower() for word in exclude_keywords_input.split(",") if word.strip()]

    if not sitemap_url.startswith("http"):
        print("[red]Invalid sitemap URL. Must start with http/https.[/red]")
        return

    print(f"\nFetching URLs from sitemap: [cyan]{sitemap_url}[/cyan]")
    all_urls = fetch_sitemap_urls(sitemap_url)
    print(f"[blue]Found total {len(all_urls)} URLs[/blue]")

    # Filtering logic with tqdm
    filtered_urls = []
    for url in tqdm(all_urls, desc="Filtering URLs"):
        url_lower = url.lower()

        include_check = True if not include_keywords else any(keyword in url_lower for keyword in include_keywords)
        exclude_check = any(bad_keyword in url_lower for bad_keyword in exclude_keywords)

        if include_check and not exclude_check:
            filtered_urls.append(url)

    print(f"[magenta]Filtered {len(filtered_urls)} URLs after applying rules[/magenta]")

    if filtered_urls:
        save_to_file(brand, filtered_urls)
    else:
        print("[yellow]No URLs matched the filters.[/yellow]")

if __name__ == "__main__":
    main()
