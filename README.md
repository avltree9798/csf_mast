# CSF Mobile Application Security Testing
CSF MAST is an automated mobile application security testing tool that can help you identify weaknesses in your mobile application. What makes CSF MAST different is that you can write your niche scanner logic effortlessly.

# How to use
- Install dependencies: `pip install -r requirements.txt`.
- `python main.py ~/path/to/application.ipa`.
![Screenshot](https://i.ibb.co/gWcsn93/Screenshot-2022-11-01-at-20-44-09.png)

# How to add a new scanner logic
- Create your scanner script under `modules/scanner/[ios/android]` with a file name that ends with `scanner.py` (e.g. `my_new_scanner.py`).
- Create a new class that extends `Scanner` class from `modules.abstract.scanner`.
- Override `perform_scan` method and write your scanner logic there.
- If you want to add something as a finding, create a `Finding` object from `modules.scanner.finding` and pass that object to `await self.report.add_finding(finding)` method.
- Lastly, you can decide whether to run this scanner if there's a file name that match your criteria by adding decorator `@ScannerManager.add_filename_scanner(FILE_NAME)` before class declaration. Or you can also use `@ScannerManager.add_mimetype_scanner(MIMETYPE)` decorator to register your scanner to a particular mimetype.
