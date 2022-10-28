import React from "react";
import CloseOutlinedIcon from "@mui/icons-material/CloseOutlined";
import { IconButton } from "@mui/material";
import { iconText } from "../../utils/renderHelpers";

export default class AbstractModalProvider {
	// provides a communication layer between a modal and an owner component
	constructor() {
		this._modal = null;
		this._listeners = [];
		this._listenerId = 0;
	}

	_bind(modal) {
		const isNew = this._modal !== modal;
		if (this._modal && isNew) {
			throw new Error("Modal provider cannot be bound to multiple modals.");
		}
		this._modal = modal;
		if (isNew) {
			this.onModalBind();
		}
	}

	_unbind() {
		this._modal = null;
		this.onModalUnbind();
	}

	onModalUnbind() {} // overridable

	onModalBind() {} // overridable

	dispatchAction(action) {
		// relays the action to the modal, which may then ask the provider to act
		this._modal.modalConsumeAction(action);
	}

	emit(action, data = null) {
		for (const listener of this._listeners) {
			if (listener.action === action) {
				listener.func(data);
			}
		}
	}

	addListener(action, callback) {
		const id = this._listenerId++;
		this._listeners.push({
			action: action,
			func: callback,
			id: id,
		});
		return id;
	}

	removeListener(id) {
		this._listeners = this._listeners.filter((x) => x.id !== id);
	}

	consumeAction(action) {
		console.error(
			"Modal Provider failed to acknowledge action with ID " +
				String(action) +
				". This means you need to override consumeAction!"
		);
		// override
	}

	getModalRootElement() {
		return this._modal.getModalElement();
	}

	getTitle() {
		return <span></span>;
	}

	getHeader() {
		return <div>{this.createBasicIconButton("CloseButton", CloseOutlinedIcon, ModalActions.EXECUTE_CLOSE)}</div>;
	}

	getContent() {
		return <div></div>;
	}

	createBasicIconButton(key, icon, dispatch, tooltip = undefined, props = {}) {
		return (
			<span style={{ paddingLeft: "0.5em" }} title={tooltip}>
				{React.createElement(
					IconButton,
					{
						size: "small",
						key: key + "iconButton",
						onClick: this.dispatchAction.bind(this, dispatch),
						...props,
					},
					[React.createElement(icon, { fontSize: "medium", key: key + "icon" })]
				)}
			</span>
		);
	}

	createTitleWithIcon(icon, title) {
		return iconText(title, icon, "0.5em", "medium", { justifyContent: "start" });
	}
}

export class ModalActions {
	constructor() {
		throw new Error("Cannot create static class.");
	}
	static REQUEST_RENDER = "MODAL_REQUEST_RENDER"; // asks the modal to re-render, since modals use providers, they don't know when to re-render themselves
	static REQUEST_CLOSE = "MODAL_REQUEST_CLOSE"; // asks the provider to close the modal
	static EXECUTE_CLOSE = "MODAL_EXECUTE_CLOSE"; // closes the modal
	static FIND = "MODAL_FIND";
}
