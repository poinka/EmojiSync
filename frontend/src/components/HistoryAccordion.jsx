import React from "react";
import { Accordion, AccordionItem } from "@heroui/react";
import "./HistoryAccordion.css";

const trimTextPreview = (text, maxWords = 5) => {
  if (!text || typeof text !== "string") return "...";
  const words = text.split(" ");
  return words.length <= maxWords
    ? text
    : words.slice(0, maxWords).join(" ") + " ...";
};

const HistoryAccordion = ({ history }) => {
  return (
    <Accordion variant="splitted" className="custom-accordion">
      {history.map((item, idx) => (
        <AccordionItem
          key={idx}
          aria-label={`Preview: ${item.input}`}
          className="accordion-item"
          title={
            <div className="accordion-title">
              <span className="accordion-text">{trimTextPreview(item.input)}</span>
              <span className="accordion-icon" />
            </div>
          }
        >

          <div className="accordion-divider" />

          <div className="accordion-content">
            <div className="content-block">
              <strong>Original:</strong>
              <p>{item.input}</p>
            </div>
            <div className="content-block">
              <strong>Translation:</strong>
              <p>{item.output}</p>
            </div>
          </div>
        </AccordionItem>
      ))}
    </Accordion>
  );
};

export default HistoryAccordion;
