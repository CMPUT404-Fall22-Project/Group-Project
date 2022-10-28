import renderer from "react-test-renderer";
import { render } from "@testing-library/react";
import Author from "../author";

it("snapshot test", () => {
  const component = renderer.create(
    <Author
      displayName="testName"
      author_id="testID"
      github="https://github.com/"
      profileImage="https://avatars.githubusercontent.com/u/56713153?v=4"
      id="currentID"
    ></Author>
  );
  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});

it("check that data is correct", () => {
  const { getByLabelText, getByText } = render(
    <Author
      displayName="testName"
      author_id="testID"
      github="https://github.com/"
      profileImage="https://avatars.githubusercontent.com/u/56713153?v=4"
    />
  );
  const displayNameTest = getByText("testName").textContent;
  expect(displayNameTest).toEqual("testName");

  const idTest = getByText("testID").textContent;
  expect(idTest).toEqual("testID");

  expect(getByLabelText("GitHub").hasAttribute("href", "https://github.com"));
});
