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
