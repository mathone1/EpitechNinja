def safeGet(value: str, key: str):

	value = value.get(key, {})
	return value if value else {}
