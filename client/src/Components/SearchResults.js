import React from "react";
import tw from "twin.macro";
import { motion } from "framer-motion";
import { TaggedSentence } from "./TaggedSentence";

const Container = tw(motion.div)`sm:m-1 lg:m-2 p-4 flex flex-col`;

export const SearchResults = ({ result, model }) => {
  return (
    <Container
      layout
      animate={{ opacity: [0, 1], y: [100, 0] }}
      transition={{ duration: 0.2 }}
    >
      <TaggedSentence tagged_sent={result.docs} model={model} />
    </Container>
  );
};
