import React, { useState } from "react";
import tw, { styled } from "twin.macro";
import TextareaAutosize from "react-autosize-textarea";
import { motion, AnimateSharedLayout } from "framer-motion";

import { SearchResults } from "./Components/SearchResults";

import { ImSpinner9 } from "react-icons/im";
import { IoBarcodeOutline, IoSearchSharp } from "react-icons/io5";

let API =
  process.env.NODE_ENV === "production"
    ? process.env.REACT_APP_PROD_API
    : process.env.REACT_APP_DEV_API;

const Container = tw.div`flex min-h-screen p-2 lg:p-4  bg-gradient-to-tr from-indigo-200 via-pink-100 to-yellow-50`;
const MainContent = tw(motion.div)`w-full flex flex-col`;
const TextInput = tw(TextareaAutosize)`border p-3 rounded-3xl border-gray-200
ring-2 ring-pink-700 text-gray-500 resize-none text-center
 hover:shadow-xl mx-auto w-full lg:w-2/4 outline-none`;
const Button = tw(
  motion.div
)`cursor-pointer flex align-middle rounded-3xl px-6 font-bold h-10 m-3 mx-auto bg-gradient-to-br from-indigo-600 via-pink-600 to-yellow-500 text-white shadow focus:ring-2 focus:ring-yellow-400`;

export const SelectableHalf = styled.div(({ selected, direction }) => [
  tw`w-1/2 h-full bg-gradient-to-br from-indigo-200 via-pink-200 to-yellow-100 hover:bg-gradient-to-tr hover:from-yellow-200 hover:via-pink-300 hover:to-indigo-300 flex text-pink-600 cursor-pointer`,
  selected &&
    tw`bg-gradient-to-br from-indigo-500 via-pink-500 to-yellow-400 hover:bg-gradient-to-tr hover:from-yellow-500 hover:via-pink-600 hover:to-indigo-600  text-yellow-50`,
  direction === "right" ? tw`rounded-r-3xl` : tw`rounded-l-3xl`,
]);

function App() {
  const [sent, setSent] = useState("(preliminary or (report and time))");
  const [selectedModel, setSelectedModel] = useState(1);
  const [selectedVectType, setSelectedVectType] = useState(0);
  const [result, setResult] = useState(undefined);
  const [loading, setLoading] = useState(false);

  const handleBooleanSearch = () => {
    setLoading(true);
    setResult(undefined);

    fetch(`${API}/booleansearch?sent=${sent}`)
      .then((response) => response.json())
      .then((data) => {
        setResult(data);
        setLoading(false);
      })
      .catch((e) => {
        alert("Error from server !");
        setLoading(false);
      });
  };

  const handleVectorialSearch = () => {
    setLoading(true);
    setResult(undefined);

    fetch(`${API}/vectsearch?sent=${sent}&type=${selectedVectType}`)
      .then((response) => response.json())
      .then((data) => {
        setResult(data);
        setLoading(false);
      })
      .catch((e) => {
        alert("Error from server !");
        setLoading(false);
      });
  };

  return (
    <AnimateSharedLayout>
      <Container>
        <MainContent>
          <motion.div layout tw="flex flex-col my-auto w-full">
            <IoBarcodeOutline tw="mx-auto text-7xl text-pink-600" />
            <h1 tw="mx-auto text-4xl font-bold mb-2 text-center text-transparent  bg-clip-text bg-gradient-to-br from-yellow-300 via-pink-500 to-indigo-600 ">
              Information Retrival Project
            </h1>
            <div tw="h-10 w-full lg:w-1/4 mx-auto my-4 font-bold text-center uppercase flex rounded-3xl border border-pink-300 shadow">
              <div tw="flex w-full">
                <SelectableHalf
                  selected={selectedModel === 1}
                  direction="left"
                  onClick={() =>
                    setSelectedModel(1) ||
                    setSent("(preliminary or (report and time))") ||
                    setResult(undefined)
                  }
                >
                  <motion.div
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    tw="m-auto"
                  >
                    Boolean Model
                  </motion.div>
                </SelectableHalf>
                <SelectableHalf
                  selected={selectedModel === 2}
                  direction="right"
                  onClick={() =>
                    setSelectedModel(2) ||
                    setSent(
                      "Dictionary construction and accessing methods for fast retrieval of words or lexical items or morphologically related information. Hashing or indexing methods are usually applied to English spelling or natural language problems."
                    ) ||
                    setResult(undefined)
                  }
                >
                  <motion.div
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    tw="m-auto"
                  >
                    Victorien Model{" "}
                  </motion.div>
                </SelectableHalf>
              </div>
            </div>

            {selectedModel === 2 && (
              <select
                tw="w-full mb-4 mx-auto lg:w-1/4  text-lg font-bold uppercase text-pink-600 border-2 border-pink-600 rounded-3xl bg-gradient-to-br from-indigo-100 via-pink-200 to-yellow-100 outline-none p-1"
                style={{ textAlignLast: "center" }}
                value={selectedVectType}
                onChange={(e) => setSelectedVectType(e.target.value)}
              >
                <option value={0}>Sørensen–Dice coefficient</option>
                <option value={1}>Cosine similarity</option>
                <option value={2}>Jaccard index</option>
                <option value={3}>Inner product</option>
              </select>
            )}

            <TextInput
              placeholder="Enter a sentence to scan here"
              value={sent}
              onChange={(e) => setSent(e.target.value)}
            />

            {loading ? (
              <Loading />
            ) : (
              <Button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                style={{ outline: "none" }}
                onClick={
                  selectedModel === 1
                    ? handleBooleanSearch
                    : handleVectorialSearch
                }
              >
                <IoSearchSharp tw="my-auto mr-2 text-lg " />
                <span tw="my-auto">{result && "new"} Search</span>
              </Button>
            )}
          </motion.div>
          {result && <SearchResults result={result} model={selectedModel} />}
        </MainContent>
      </Container>
    </AnimateSharedLayout>
  );
}

export default App;

const Loading = () => (
  <div tw="flex flex-col h-10 m-3 mx-auto text-pink-600 ">
    <div tw="my-2">
      <ImSpinner9 tw="animate-spin text-7xl text-center mx-auto" />
    </div>
    <div tw="mx-auto font-bold">Searching</div>
  </div>
);
