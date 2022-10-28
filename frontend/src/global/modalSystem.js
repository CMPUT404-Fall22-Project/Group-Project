import React, { Component } from "react";
import GenericModal from "../components/modals/genericModal";
import { ModalActions } from "../components/modals/modalProvider";

export default class ModalSystem extends Component {
	/** @type {ModalSystem} */
	static _instance = null;

	constructor(props) {
		super(props);

		this.state = {
			modals: [],
		};

		ModalSystem._instance = this;
	}

	static getInstance() {
		const inst = ModalSystem._instance;
		if (!inst.state.mounted) {
			throw new Error("ModalSystem not mounted.");
		}
		return inst;
	}

	componentDidMount() {
		this.setState({ mounted: true });
	}

	componentWillUnmount() {
		this.setState({ mounted: false });
	}

	_getModal(id) {
		for (const m of this.state.modals) {
			if (m.id === id) {
				return m;
			}
		}
		return null;
	}

	_dispatchActionToModal(id, action) {
		const m = this._getModal(id);
		if (!m) {
			throw new Error("Cannot dispatch action to modal " + String(id) + ". Cannot find modal.");
		}
		m.provider.dispatchAction(action);
		return m;
	}

	addModal(id, provider, props = {}) {
		if (this._getModal(id)) {
			this._dispatchActionToModal(id, ModalActions.FIND);
			return;
		}
		this.setState((prevState) => {
			const modal = {
				id: id,
				provider: provider,
				open: true,
				_zIndex: 1050,
				props: props,
			};
			const modals = this.resortModals([...prevState.modals, modal], id);
			return { modals: modals };
		});
	}

	closeModal(id) {
		const modal = this._dispatchActionToModal(id, ModalActions.EXECUTE_CLOSE);
		modal.open = false;
	}

	freeModal(id) {
		this.setState((prevState) => {
			var modals = [...prevState.modals].filter((x) => x.id !== id);
			return { modals: modals };
		});
	}

	resortModals(modals, frontId) {
		// in place
		// far too complex, but if i don't do it this way then the animation replays.
		const sortedModals = [...modals].sort((a, b) => a._zIndex - b._zIndex);
		const idx2 = sortedModals.findIndex((x) => x.id === frontId);
		if (idx2 === -1) {
			console.error("Cannot find modal with id " + String(frontId));
			return modals;
		}
		sortedModals.push(...sortedModals.splice(idx2, 1));

		var zIndex = 1050;
		for (const m of sortedModals) {
			m._zIndex = zIndex++;
		}

		return modals;
	}

	bringModalToFront(modalId) {
		this.setState((prevState) => {
			var modals = [...prevState.modals];
			this.resortModals(modals, modalId);

			return { modals: modals };
		});
	}

	render() {
		return (
			<div
				style={{
					top: "0",
					height: "100%",
					width: "100%",
					position: "absolute",
					overflow: "clip",
					pointerEvents: "none",
				}}
			>
				{this.state.modals.map((item) => (
					<GenericModal
						key={item.id}
						modalId={item.id}
						provider={item.provider}
						{...item.props}
						_zIndex={item._zIndex}
					></GenericModal>
				))}
			</div>
		);
	}
}
