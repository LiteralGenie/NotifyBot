import re


def extract_num(el) -> float:
	text = el.text
	ret = re.search(r'(\d+(?:\.\d+)?)', text)
	ret = float(ret.group(0))
	return ret