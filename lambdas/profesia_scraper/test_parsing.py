from scraping.company_scraping import get_companies
from scraping.salary_scraping import get_salaries_from_page


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


def test_salary_with_accomodation_scraping():
    sample_html = """
        <ul>
            <li class="list-row">
                <h2>
                    <a id="offer_id" href="offer_href">
                        <span class="title">Listing Title</span>
                    </a>
                </h2>
                <span class="employer">COMPANY NAME</span>
                <span title="city" class="job-location">City</span>
                <span class="label-group">
                    <a href="offer_href">
                        <span class="label label-bordered green half-margin-on-top">
                            <svg class="icon money green">
                                <use xlink:href="/images/svg/money.svg#Layer_1"></use>
                            </svg>
                            260 EUR/month
                        </span>
                    </a>
                </span>
                <a class="half-margin-on-right" data-dimension16="Accommodation label" href="offer_href">
                        <span class="label label-bordered purple half-margin-on-top">
                            <svg class="icon bed purple" viewBox="0 0 20 20">
                                <use xlink:href="/images/svg/bed.svg#Layer_1"></use>
                            </svg> Arranged accommodation
                        </span>
                    </a>
            </li>
        </ul>
    """

    assert get_salaries_from_page(sample_html) == ["260 EUR/month"]


def test_empty_salary():
    sample_html = """
        <ul>
            </li>
            <li class="list-row">
                <h2>
                    <a id="offer_id" href="offer_href">
                        <span class="title">Listing Title</span>
                    </a>
                </h2>
                <span class="employer">COMPANY NAME</span>
                <span title="city" class="job-location">City</span>
            </li>
        </ul>
    """

    assert get_salaries_from_page(sample_html) == []


def test_monthly_salary_scraping():
    sample_html = """
        <ul>
            <li class="list-row">
                <a href="/en/work/company-name/C101" class="offer-company-logo-link"></a>
                <h2>
                    <a id="offer_id" href="offer_href">
                        <span class="title">Listing Title</span>
                    </a>
                </h2>
                <span class="employer">COMPANY NAME</span>
                <span title="city" class="job-location">City</span>
                <span class="label-group">
                    <a href="offer_href">
                        <span class="label label-bordered green half-margin-on-top">
                            <svg class="icon money green">
                                <use xlink:href="/images/svg/money.svg#Layer_1"></use>
                            </svg>
                            1 334 EUR/month
                        </span>
                    </a>
                </span>
            </li>
        </ul>
    """

    assert get_salaries_from_page(sample_html) == ["1 334 EUR/month"]


def test_hourly_salary_scraping():
    sample_html = """
        <ul>
            <li class="list-row">
                <h2>
                    <a id="offer_id" href="offer_href">
                        <span class="title">Listing Title</span>
                    </a>
                </h2>
                <span class="employer">COMPANY NAME</span>
                <span title="city" class="job-location">City</span>
                <span class="label-group">
                    <a href="offer_href">
                        <span class="label label-bordered green half-margin-on-top">
                            <svg class="icon money green">
                                <use xlink:href="/images/svg/money.svg#Layer_1"></use>
                            </svg>
                            16 EUR/hour
                        </span>
                    </a>
                </span>
            </li>
        </ul>
    """

    assert get_salaries_from_page(sample_html) == ["16 EUR/hour"]


def test_salary_range_scraping():
    sample_html = """
        <ul>
            <li class="list-row">
                <h2>
                    <a id="offer_id" href="offer_href">
                        <span class="title">Listing Title</span>
                    </a>
                </h2>
                <span class="employer">COMPANY NAME</span>
                <span title="city" class="job-location">City</span>
                <span class="label-group">
                    <a href="offer_href">
                        <span class="label label-bordered green half-margin-on-top">
                            <svg class="icon money green">
                                <use xlink:href="/images/svg/money.svg#Layer_1"></use>
                            </svg>
                            10 - 16 EUR/hour
                        </span>
                    </a>
                </span>
            </li>
        </ul>
    """

    assert get_salaries_from_page(sample_html) == ["10 - 16 EUR/hour"]