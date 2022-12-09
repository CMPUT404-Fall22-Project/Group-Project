import { isUrlLocal } from "./local";
import axios from "axios";

export function proxy(axiosParams) {
	if (!isUrlLocal(axiosParams.url)) {
		axiosParams.params = { ...(axiosParams.params || {}), PROXY_TARGET: axiosParams.url };
		axiosParams.url = process.env.REACT_APP_HOST + "proxy/";
	}
	return axiosParams;
}

export function proxiedAxios(config) {
	return axios(proxy(config));
}
