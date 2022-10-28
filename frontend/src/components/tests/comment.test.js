import { render, fireEvent, getByText } from "@testing-library/react";
import CommentBox from "../comment";

it("check that data is correct", () => {
  const { getElementById, getByText } = render(<CommentBox />);

  // make sure comment button appears
  const buttonTest = getByText("Comment").textContent;
  expect(buttonTest).toEqual("Comment");

  // make sure comment box is empty
  const textFieldTest = document.getElementById(
    "outlined-multiline-static"
  ).value;
  expect(textFieldTest).toEqual("");
});
