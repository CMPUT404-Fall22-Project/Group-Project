export function stringifyComponent(comp) {
	// extracts all text from a component
	if (comp.constructor === String) {
		return comp;
	}
	var s = "";
	if (comp.props?.children) {
		var arr = comp.props.children;
		if (arr.constructor !== Array) {
			arr = [arr];
		}
		for (const c of comp.props.children) {
			s += stringifyComponent(c);
		}
	}
	return s;
}

export function tryStringifyObject(obj) {
	if (obj instanceof String) {
		return obj;
	}
	const keys = Object.keys(obj);
	if (keys.length === 1) {
		return new String(obj[keys[0]]);
	}
	return JSON.stringify(obj);
}
