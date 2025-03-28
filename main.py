from packages.html_parser import GeekbenchCrawler
from packages.output_formatter import dict_to_csv

from argparse import ArgumentParser

GeekbenchCrawlerCLI = ArgumentParser(
    prog = "GeekbenchCrawlerCLI",
    description = "Program used to extract data from the Geekbench plataform."
)


GeekbenchCrawlerCLI.add_argument("geekbench_id")
GeekbenchCrawlerCLI.add_argument("-l", "--level", default = "simple")
def main():

    # 11195682, 11206607, 11217153, 11236233

    args = GeekbenchCrawlerCLI.parse_args()


    geekbench_info = GeekbenchCrawler\
                        .from_benchmark_id(args.geekbench_id)\
                        .parse()

    dict_to_csv(geekbench_info, level = args.level)

if __name__ == "__main__":
    main()

