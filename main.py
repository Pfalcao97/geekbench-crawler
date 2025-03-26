from packages.html_parser import GeekbenchCrawler

def main():

    crawler = GeekbenchCrawler.from_benchmark_id(11217153)
    geekbench_info = crawler.parse()

    print(geekbench_info)

if __name__ == "__main__":
    main()

