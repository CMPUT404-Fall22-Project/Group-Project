// https://jacobwicks.github.io/2020/06/19/rendering-markdown-and-resizing-images-with-react-markdown.html#:~:text=Usually%20in%20markdown%20you%20can,Limit%20just%20width%20to%20250%20!
export const MD_COMPONENETS_POST = { img: ({ node, ...props }) => <img style={{ width: "80%" }} {...props} /> };
