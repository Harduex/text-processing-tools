import dotenv from "dotenv";
dotenv.config();

import { getDocuments } from "../helpers/utilities";
import fs from "fs";
import path from "path";

interface Topic {
  prediction: string;
}

export const extractTopics = async (jsonNotesDir: string) => {
  const outputFilename: string = "translatedNotes";
  const documentsPath = `${jsonNotesDir}/${outputFilename}.json`;
  const documents = getDocuments(documentsPath);

  let documentsWithTopics: Object[] = [];
  for (const doc of documents) {
    const topic: Topic | undefined = await findTopics(
      doc.translation.translated_text
    );
    documentsWithTopics.push({
      text: doc.text,
      extracted: topic?.prediction,
      translation: doc.translation,
    });

    const outputFilePath = path.join(jsonNotesDir, `notesWithTopics.json`);
    fs.writeFile(
      outputFilePath,
      JSON.stringify(documentsWithTopics, null, 2),
      (err) => {
        if (err) {
          console.error(`Error writing file ${outputFilePath}: ${err}`);
          return;
        }
        console.log(`\nMerged notes written to ${outputFilePath}`);
      }
    );
  }
  if (!fs.existsSync(jsonNotesDir)) {
    fs.mkdirSync(jsonNotesDir, { recursive: true });
  }
  return documentsWithTopics;
};

const findTopics = async (text: string): Promise<Topic | undefined> => {
  const topicDetectorApiUrl = `${process.env.TOPIC_DETECTOR_API}/predict` || "";

  // TODO: format the cleanedText to be in valid format for JSON.stringify({ text: cleanedText }), to work every time
  // const cleanedText = text.replace(/(\r\n|\n|\r)/gm, " ");
  const cleanedText = text
    .replace(/(\r\n|\n|\r)/gm, " ")
    .replace(/\\/g, "\\\\")
    .replace(/"/g, '\\"');

  const options = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: cleanedText }),
  };

  try {
    const response = await fetch(topicDetectorApiUrl, options);
    const data = await response?.json();
    return data;
  } catch (error: any) {
    console.log(error);
  }
};
