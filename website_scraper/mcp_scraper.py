import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
from website_scraper.tools_scraper import McpToolsScraper

from utils.enhance_mcp import enhance_mcp_description


async def validate_link(session, url):
    try:
        async with session.get(url) as response:
            return response.status == 200
    except:
        return False




async def process_card(session, card):
    try:
        title_tag = card.find("a", class_="text-xl")
        title = title_tag.text.strip()
        link = "https://www.mcpserverfinder.com" + title_tag['href']

        if not await validate_link(session, link):
            return None

        created_by = card.find("p", class_="text-sm text-muted-foreground truncate").text.strip()
        description = card.find("p", class_="text-muted-foreground mb-4 line-clamp-2").text.strip()

        stats = card.find_all("span", class_="flex items-center mr-3")
        baseline_stars = stats[0].text.strip() if len(stats) > 0 else "0"

        details_scraper = McpToolsScraper(link)
        await details_scraper.fetch(session)

        categories = await details_scraper.get_all_categories()
        language = await details_scraper.get_mcp_language()
        github_link = await details_scraper.get_mcp_author_github()
        stars = await details_scraper.get_stars()
        stars = stars if stars else baseline_stars
        markdown = "More description about MCP server" + await details_scraper.get_markdown()

        # print({
        #     "link":link,
        #     "categories":categories,
        #     "language":language,
        #     "github link":github_link,
        #     "stars":stars
        # })

        content =  {
            "title": title,
            "link": link,
            "created_by": created_by,
            "description": description + markdown,
            "stars": stars,
            "categories": categories,
            "language": language,
            "github_link": github_link
        }
        return content
    except Exception as e:
        print("Error parsing card:", e)
        return None


async def main():
    mcp_registry_url = "https://www.mcpserverfinder.com/servers"

    async with aiohttp.ClientSession() as session:
        page = await session.get(mcp_registry_url)
        content = await page.text()
        soup = BeautifulSoup(content, "html.parser")
        cards = soup.find_all("div", class_="p-6")

        tasks = [process_card(session, card) for card in cards]
        results_raw = await asyncio.gather(*tasks)
        results = [res for res in results_raw if res]

        with open('all_mcp_server.json', 'w', encoding='utf-16') as file:
            json_instance = json.dumps(results, ensure_ascii=False)
            file.write(json_instance)


if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(enhance_mcp_description())
