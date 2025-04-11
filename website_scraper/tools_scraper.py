import aiohttp
from bs4 import BeautifulSoup


class McpToolsScraper:
    def __init__(self, mcp_tool_url):
        self.url = mcp_tool_url
        self.soup = None

    async def fetch(self, session):
        try:
            async with session.get(self.url, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    self.soup = BeautifulSoup(html, "html.parser")
        except Exception as error:
            print(f"Error fetching URL {self.url}: {error}")

    async def get_all_categories(self):
        try:
            if len([tag.text.strip() for tag in self.soup.select("div.flex.flex-wrap span")]) <= 0:
                return None
            return [tag.text.strip() for tag in self.soup.select("div.flex.flex-wrap span")]
        except Exception as error:
            print(f"When running McpToolScraper.get_all_categories we got this error {error}")
            return []

    async def get_mcp_language(self):
        try:
            find_language = self.soup.find("h3", string="Language:")
            if find_language is None:
                return None
            return find_language.find_next_sibling("p").text.strip()
        except Exception as error:
            print(f"When running McpToolScraper.get_mcp_language we got this error {error}")
            return None

    async def get_mcp_author_github(self):
        try:
            github_link = self.soup.find_all("a")
            for tag in github_link:
                if "View on Github" in tag.get_text(strip=True):
                #     # print("github url", tag['href'])
                    return tag["href"]
            return None
        except Exception as error:
            print(f"When running McpToolScraper.get_mcp_author_github we got this error {error}")
            return None

    async def get_stars(self):
        try:
            divs = self.soup.find_all('div', class_='flex items-center')
            for div in divs:
                label = div.find('h3')
                if label and label.text.strip() == 'Stars:':
                    stars_text = div.find('p').text.strip()
                    return stars_text
                    break

            return 0
        except Exception as error:
            print(f"When running McpToolScraper.get_stars we got this error {error}")
            return None

