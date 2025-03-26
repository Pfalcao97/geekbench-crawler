from bs4 import BeautifulSoup, element

def normalize_str(raw_str:str) -> str:
        return raw_str.replace("\n", "").strip()

class GeekbenchCrawler(BeautifulSoup):

    def __init__(self, html_data):
        
        super().__init__(
            html_data,
            "html.parser"
        )

    @classmethod
    def from_benchmark_id(cls, benchmark_id:str|int):
        """
        Create the `GeekbenchCrawler` class from a benchmark id - which is available
        in the benchmark's URL.

        Args:
        - benchmark_id (int or str): the ID of the benchmark, it's a sequence of numbers.

        Returns:
        - GeekbenchCrawler object
        """

        from requests import get
        from requests.exceptions import RequestException

        response = get(
            url = f"https://browser.geekbench.com/v6/cpu/{benchmark_id}"
        )

        if not response.ok:
            RequestException(f"Invalid response ({response.status_code}).\nError Description: {response.text}")

        return cls(response.text)
    
    @staticmethod
    def _get_score(div:element.Tag ,div_class:str, cast_to_int:bool = True) -> str|int:

        _score = normalize_str(div.find(class_ = div_class).find(class_ = "score").string)

        if cast_to_int:
            try:
                return int(_score)
            except ValueError:
                raise ValueError(f"Couldn't convert {_score} to integer - make sure wether `cast_to_int` should, in fact, be True.")
        
        return _score
    
    @staticmethod
    def _table_to_dict(table_element:element.Tag) -> dict:
        """
        Turns a simple table element into a dictionary.

        Args:
        - table_element (element.Tag): table element with class name `table system-table`.

        Returns:
        - a dictonary with the scrapped data.
        """
        _table_dct = dict()

        for row in table_element.find_all("tr"):

            try:
                _table_dct[
                    row.find("td", class_ = "system-name").string.lower()
                ] = row.find("td", class_ = "system-value").string
            except AttributeError:
                # In case there's no `system-name` or `system-value` classes
                # then it probably has another name:

                try:
                    _table_dct[
                        row.find("td", class_ = "name").string.lower()
                    ] = row.find("td", class_ = "value").string
                except AttributeError:
                    # In case there's no `name` or `value` classes either,
                    # then it's probably another type of table.
                    pass        

        return _table_dct
    
    @staticmethod
    def _benchmark_extraction(benchmark_table_raw:element.Tag) -> list:
        """
        Takes benchmark data and transforms it into a list of tuples, in which:

        [
        ...
        (test name, test score, test description)
        ...
        ]

        This method works for a single table, to join both tables (single and multi core),
        you'll need to zip them together before using.

        Args:
        - benchmarck_table_raw (element.Tag): table element with class name `table benchmark-table`.

        Returns:
        - list of tuples with the tests results.
        """

        names = map(
            lambda x: normalize_str(x.contents[0]),
            benchmark_table_raw.find_all("td", class_ = "name")
        )

        values = map(
            lambda x: (normalize_str(x.contents[0]), x.find("span", class_="description").string),
            benchmark_table_raw.find_all("td", class_ = "score")
        )

        return list(zip(names, values))

    def parse(self) -> dict:
        """
        Parse HTML data into a comprehensive dictionary.

        Returns:
        - A dictionary with the parsed data.
        """

        parsed_dct = dict()

        _wrap = self.find(id = "wrap") # All relevant data is in a container called 'wrap'

        parsed_dct["title"] = normalize_str(_wrap.h1.string)

        # Start with the extraction of the top table content
        _abstract = _wrap.find("div", class_ = "table-wrapper cpu")

        parsed_dct["single-core score"] = self._get_score(_abstract, "score-container score-container-1 desktop")
        parsed_dct["multi-core score"] = self._get_score(_abstract, "score-container desktop")
        parsed_dct["plataform"] = normalize_str(_abstract.find(class_ = "platform-info").contents[0])
        parsed_dct["validation status"] = normalize_str(_abstract.find(class_ = "validation-widget validation-success").contents[0])

        # Add all listing tables to dict
        for table in _wrap.find_all("table", class_ = "table system-table"):
            
            parsed_dct.update(
                self._table_to_dict(table)
            )
        
        # Adding discrete results
        single_core, multi_core = _wrap.find_all("table", "table benchmark-table")

        for c in zip(self._benchmark_extraction(single_core), self._benchmark_extraction(multi_core)):

            parsed_dct.update(
                {
                    c[0][0]: {
                        "single-core": {"score": c[0][1][0], "description": c[0][1][1]},
                        "multi-core": {"score": c[1][1][0], "description": c[1][1][1]},
                    }
                }
            )

        return parsed_dct


if __name__ == "__main__":
    print("HTML parser")
