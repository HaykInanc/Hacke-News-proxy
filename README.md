# HTTP Proxy Server with Text Modification

This project is a simple HTTP proxy server that modifies the content of Hacker News pages by appending a trademark symbol (™) after every word containing exactly six characters. The proxy ensures full functionality of the pages while maintaining the original experience as closely as possible.

## Requirements

- Python 3.9 or later
- Libraries: `requests`, `beautifulsoup4`

To install the required libraries, run:

```bash
pip install -r requirements.txt
```

## Usage

1. **Start the Proxy Server**

   Run the server script:

   ```bash
   python app.py
   ```

   This will start the proxy server on `http://127.0.0.1:8232`.

2. **Access Hacker News via Proxy**

   Open your browser and navigate to a Hacker News page through the proxy:

   ```
   http://127.0.0.1:8232/item?id=13713480
   ```

   The content will be modified with ™ symbols after six-character words.

## How It Works

1. The server intercepts requests made to Hacker News and fetches the corresponding page.
2. The HTML content is parsed using `BeautifulSoup`, and all words with six characters in visible text elements are modified to include the ™ symbol.
3. URLs for static assets (e.g., images, styles) are adjusted to ensure proper loading from Hacker News.
4. The modified content is served back to the browser.

## Code Overview

- **`ProxyHandler`**: Custom request handler that processes GET requests, fetches pages, modifies text, and ensures seamless navigation.
- **`safe_request`**: Safely fetches the content from the target URL.
- **`add_mark_symbols`**: Parses and modifies the HTML to add ™ symbols where necessary.
- **`do_GET`**: Handles incoming GET requests, determines content type, and serves modified or original content accordingly.
- **`main`**: Initializes and runs the HTTP server.

## Example

**Original Content:**

```text
The visual description of the colliding files is not very helpful in understanding how they produced the PDFs.
```

**Modified Content (via Proxy):**

```text
The visual™ description of the colliding files is not very helpful in understanding how they produced the PDFs.
```

## Notes

- The server is implemented using Python's `http.server` and `socketserver` modules for simplicity.
- The proxy only modifies text-based content (HTML). Other file types (e.g., images, PDFs) are served without modification.

## License

This project is released under the MIT License. Feel free to use and modify it as needed.

