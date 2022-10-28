import React, { Component } from "react";
import Draggable from "react-draggable";
import "./genericModal.css";
import { ModalActions } from "./modalProvider";
import ModalSystem from "../../global/modalSystem";

export default class GenericModal extends Component {
	constructor(props) {
		super(props);

		// props:
		// draggable, resizable, noFocus

		const defaultPos = { ...props.defaultPosition };
		if (defaultPos) {
			defaultPos.x = Math.round(defaultPos.x);
			defaultPos.y = Math.round(defaultPos.y);
		}

		this.state = {
			width: props.initialWidth || "300px",
			height: props.initialHeight || "400px",
			isClosing: false,
			open: true,
			defaultPosition: props.defaultPosition
				? defaultPos
				: { x: Math.round(window.innerWidth / 2), y: Math.round(window.innerHeight / 2) },
			mounted: false,
			box: { x: 0, y: 0 },
			constraint: { x: 0, y: 0 },
		};
		this.startInnerWidth = window.innerWidth;
		this.startInnerHeight = window.innerHeight;
	}

	componentDidUpdate() {
		this.props.provider._bind(this);
	}

	constrainModal(xOff = 0, yOff = 0) {
		const element = document.getElementById(this.modalIdentifier());
		const backdrop = document.getElementById(this.modalBackgroundIdentifier());

		const bounds = element.getBoundingClientRect();
		const containerBounds = backdrop.getBoundingClientRect();

		var xCorrection = 0;
		var yCorrection = 0;

		// check top left
		var xt = bounds.left + xOff;
		var yt = bounds.top - containerBounds.top + yOff; // offset for anim
		if (xt < 0) {
			xCorrection = -xt;
		}

		if (yt < 0) {
			yCorrection = -yt;
		}

		// check bottom right
		xt = bounds.right + xOff;
		yt = bounds.bottom - containerBounds.top + yOff; // offset for anim

		if (xt > containerBounds.width) {
			xCorrection = containerBounds.width - xt;
		}

		if (yt > containerBounds.height) {
			yCorrection = containerBounds.height - yt;
		}

		return { x: xCorrection, y: yCorrection };
	}

	convertConstraints() {
		this.setState((prevState) => {
			return {
				box: {
					x: prevState.box.x + prevState.constraint.x,
					y: prevState.box.y + prevState.constraint.y,
				},
				constraint: {
					x: 0,
					y: 0,
				},
			};
		});
	}

	constrainModalState() {
		if (this.props.centered) {
			this.centerModal();
			return;
		}
		this.setState((prevState) => {
			const corr = this.constrainModal(-prevState.constraint.x, -prevState.constraint.y);
			return {
				constraint: {
					x: corr.x,
					y: corr.y,
				},
			};
		});
	}

	centerModal() {
		const xMove = this.startInnerWidth - window.innerWidth;
		const yMove = this.startInnerHeight - window.innerHeight;
		this.setState({
			constraint: { x: -Math.round(xMove / 2), y: -Math.round(yMove / 2) },
		});
	}

	componentDidMount() {
		this.props.provider._bind(this);

		const element = document.getElementById(this.modalIdentifier());

		const xOff = element.clientWidth / -2;
		const yOff = element.clientHeight / -2;
		const corr = this.constrainModal(xOff, yOff);
		this.setState({
			box: {
				x: xOff + corr.x,
				y: yOff + corr.y,
			},
		});

		setTimeout(() => {
			this.setState({ fullyOpen: true });
		}, 250);

		this._listener = this.constrainModalState.bind(this);
		window.addEventListener("resize", this._listener);

		const rootElement = document.getElementById(this.modalContainerIdentifier());
		if (!this.props.noFocus) {
			rootElement.focus();
		}
	}

	componentWillUnmount() {
		this.props.provider._unbind();
		window.removeEventListener("resize", this._listener);
	}

	modalConsumeAction(action) {
		if (action === ModalActions.EXECUTE_CLOSE) {
			this.closeModal();
		} else if (action === ModalActions.FIND) {
			const element = document.getElementById(this.modalContainerIdentifier());
			element.classList.add("modalFind");
			setTimeout(() => {
				element.classList.remove("modalFind");
			}, 250);
		} else if (action === ModalActions.REQUEST_RENDER) {
			this.setState({});
		} else {
			this.props.provider.consumeAction(action);
		}
	}

	getModalElement() {
		return document.getElementById(this.modalContainerIdentifier());
	}

	closeModal() {
		if (this.state.isClosing) {
			return;
		}
		this.setState({ isClosing: true, fullyOpen: false });
		setTimeout(() => {
			this.props.provider._unbind();
			ModalSystem.getInstance().freeModal(this.props.modalId);
		}, 250);
	}

	modalBackgroundIdentifier() {
		return "GenericModalBackground" + String(this.props.modalId);
	}

	modalContainerIdentifier() {
		return "GenericModalContainer" + String(this.props.modalId);
	}

	modalIdentifier() {
		return "GenericModal" + String(this.props.modalId);
	}

	onClickModal() {
		ModalSystem.getInstance().bringModalToFront(this.props.modalId);
	}

	render() {
		// open anim is handled in css file
		return (
			<div
				className="genericModalBackdrop"
				style={{
					transition: "opacity 0.25s ease-in",
					opacity: this.state.isClosing ? 0 : 1,
					pointerEvents: this.props.dialog ? "all" : "none",
					backgroundColor: this.props.dialog ? "#00000080" : "#00000000",
					zIndex: this.props._zIndex /*supplied by modal system*/,
				}}
			>
				<div
					id={this.modalBackgroundIdentifier()}
					className="genericModalBackground"
					style={{
						transition: "transform 1s ease-in-out",
						transform: this.state.isClosing ? "translate(0%, 100%)" : "scale(1)",
						overflow: "clip",
						zIndex: this.props._zIndex,
					}}
				>
					<div style={{ marginLeft: this.state.box.x, marginTop: this.state.box.y }} className="centerHelper">
						<div style={{ marginLeft: this.state.constraint.x, marginTop: this.state.constraint.y }}>
							<div id={this.modalContainerIdentifier()} tabIndex={0}>
								<Draggable
									bounds=".genericModalBackdrop"
									defaultPosition={this.state.defaultPosition}
									handle=".button-groups-container"
									disabled={!this.props.draggable}
									onStop={this.convertConstraints.bind(this)}
								>
									<div
										className="genericModal"
										id={this.modalIdentifier()}
										style={{
											width: this.state.width,
											height: this.state.height,
											resize: this.props.resizable ? "both" : "none",
											overflow: "auto",
											minWidth: "11em",
											minHeight: "5em",
											transition: "filter 0.25s linear",
											filter: this.state.isClosing ? "blur(5px)" : "",
										}}
										onMouseDownCapture={this.onClickModal.bind(this)}
									>
										<div
											className="button-groups-container"
											style={{
												zIndex: 2, // some MUI components have a zIndex of 1 or 2
												width: "100%",
												cursor: this.props.draggable ? "grab" : undefined,
												borderBottom: "1px solid #e6e6e6",
												position: "sticky",
												top: 0,
												backgroundColor: "#ffffff",
											}}
										>
											<span
												className="button-groups"
												style={{
													padding: "0.5em",
												}}
											>
												{this.props.provider.getHeader()}
											</span>
											<span
												className="modal-title-container"
												style={{
													display: "flex",
													padding: "0.75em",
													justifyContent: "left",
													fontWeight: 100,
												}}
											>
												{this.props.provider.getTitle()}
											</span>
										</div>
										{this.props.provider.getContent()}
									</div>
								</Draggable>
							</div>
						</div>
					</div>
				</div>
			</div>
		);
	}
}
