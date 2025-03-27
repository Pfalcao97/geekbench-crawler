from packages.html_parser import GeekbenchCrawler
from packages.output_formatter import dict_to_csv

def main():

    # 11195682, 11206607, 11217153

    geekbench_info = GeekbenchCrawler\
                        .from_benchmark_id(11217153)\
                        .parse()

    dict_to_csv(geekbench_info, level = "simple")

if __name__ == "__main__":
    main()

