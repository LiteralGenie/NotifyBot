def list_to_string(lst):
	if not isinstance(lst, list):
		return str(lst)
	return ", ".join(str(x) for x in lst)

def dump_json(dct, escape='\''):
	import json, re

	ret= json.dumps(dct)
	ret= re.sub(rf"([{escape}\\])", r"\\\1", ret)

	return ret