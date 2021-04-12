def list_to_string(lst):
	if not isinstance(lst, list):
		return str(lst)
	return ", ".join(str(x) for x in lst)