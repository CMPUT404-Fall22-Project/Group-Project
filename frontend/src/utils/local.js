export function isUrlLocal(url) {
	return String(url).startsWith(process.env.REACT_APP_HOST);
}
