
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

# 1. 뉴스 검색 조건 설정
keyword = "반도체"

query = urllib.parse.quote(keyword)
rss_url = (
    f"https://news.google.com/rss/search?q={query}"
    "&hl=ko&gl=KR&ceid=KR:ko"
)

# 2. Google 뉴스 RSS 데이터 요청
request = urllib.request.Request(
    rss_url,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=20) as response:
    xml_data = response.read()

# 3. XML 데이터 분석
root = ET.fromstring(xml_data)

news_list = []

for item in root.findall("./channel/item")[:20]:
    title = item.findtext("title", default="")
    link = item.findtext("link", default="")
    pub_date = item.findtext("pubDate", default="")

    article = {
        "title": title,
        "link": link,
        "published": pub_date
    }

    news_list.append(article)

# 4. JSON 파일로 저장
with open("news.json", "w", encoding="utf-8") as file:
    json.dump(
        news_list,
        file,
        ensure_ascii=False,
        indent=4
    )

print(f"총 {len(news_list)}개의 기사를 저장했습니다.")
