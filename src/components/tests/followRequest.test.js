import renderer from "react-test-renderer";
import { render, fireEvent, getByText } from "@testing-library/react";
import FollowRequest from "../followRequest";
import { screen } from "@testing-library/dom";

it("snapshot test", () => {
  const component = renderer.create(<FollowRequest />);
  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});

it("check that text appears", () => {
  const { getByText } = render(<FollowRequest />);

  // make sure comment button appears
  const buttonTest = getByText("Submit Follow Request").textContent;
  expect(buttonTest).toEqual("Submit Follow Request");

  // test selector menu
  const textFieldTest = document.getElementById(
    "demo-simple-select"
  ).value;
  expect(textFieldTest).toEqual(undefined); // not sure how to check contents of selector menu?
});
