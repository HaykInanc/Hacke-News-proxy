import http.server
import socketserver

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

PORT = 8232
HACKER_NEWS_URL = "https://news.ycombinator.com/"
NOT_TEXT_TAGS = ["style", "script", "head", "meta", "[document]"]
MARK_SYMBOL = "™"


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    """
    Request handler for proxying and modifying content.
    """

    def safe_request(self, url):
        """
        Performs a safe HTTP request and returns the response.
        If an error occurs, returns a 500 error.
        """
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Error fetching the requested page.")

    def add_mark_symbols(self, response):
        """
        Modifies the HTML page by adding mark symbols to words of length 6 characters.
        """
        soup = BeautifulSoup(response.content, "html.parser")

        for tag in soup.find_all(string=True):
            if tag.parent.name not in NOT_TEXT_TAGS:
                words = tag.string.split()
                if len(words) == 0:
                    continue
                processed_text = " ".join(
                    [word + MARK_SYMBOL if len(word) == 6 else word for word in words]
                )
                tag.replace_with(processed_text)

        for tag in soup.find_all(["img", "script", "link"]):
            attr = "href" if tag.name in ["link"] else "src"
            if tag.has_attr(attr):
                tag[attr] = urljoin(HACKER_NEWS_URL, tag[attr])

        return soup.prettify().encode("utf-8")

    def do_GET(self):
        """
        Handles the GET request, modifying the HTML content if it is text-based.
        """
        target_url = urljoin(HACKER_NEWS_URL, self.path)
        response = self.safe_request(target_url)
        content_type = response.headers.get("Content-Type", "")

        if "text/html" in content_type:
            modified_content = self.add_mark_symbols(response)
        else:
            modified_content = response.content

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(modified_content)


def main():
    """
    Starts the HTTP server, serving requests on the specified port.
    """
    with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
        print(f"Serving at port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server.")
            httpd.server_close()


if __name__ == "__main__":
    main()