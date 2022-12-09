export function extractGithubName(author) {
	const url = author.getGithubUrl();
	if (!url) {
		return null;
	}
	const parsed = new URL(url);
	if (parsed.pathname) {
		return parsed.pathname.split("/")[1];
	}
	return null;
}
