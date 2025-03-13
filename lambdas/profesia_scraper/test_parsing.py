from scraping.company_scraping import get_companies


def test_companies_scraping():
    sample_html = """
        <ul class="list-reset">
            <h2>Scroll to the letter in the alphabet</h2>
            <a>A</a>
            <h3>@</h3>
            <li>
                <a href="/en/work//C158482">---</a> 
                <span class="text-gray">1</span>
            </li>
            <li>
                <a href="/en/work/company-name-100/C187184">Company Name 100</a> 
                <span class="text-gray">100</span>
            </li>
            <h3 class="margin-on-top" id="0-9">0-9</h3>
        </ul>
    """

    expected = {
        "---": {
            "number_of_listings": "1", 
            "url": "/en/work//C158482"
        },
        "Company Name 100": {
            "number_of_listings": "100", 
            "url": "/en/work/company-name-100/C187184"
        },
    }
    assert get_companies(sample_html) == expected