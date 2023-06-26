import dotenv from "dotenv";
dotenv.config();

import { getDocuments } from "../helpers/utilities";
import fs from "fs";
import path from "path";

interface Translation {
  translation: Object;
}

export const translateNotes = async (
  jsonNotesDir: string
): Promise<Object[]> => {
  const outputFilename: string = process.env.OUTPUT_FILENAME || "notes";
  const documentsPath = `${jsonNotesDir}/${outputFilename}.json`;
  const documents = getDocuments(documentsPath).data;
  let translatedDocuments: Object[] = [];
  for (const doc of documents) {
    const translation: Translation | undefined = await translateNote(doc);
    console.log(translation);

    translatedDocuments.push({
      text: doc,
      translation: translation?.translation,
    });

    const outputFilePath = path.join(jsonNotesDir, `translatedNotes.json`);
    fs.writeFile(
      outputFilePath,
      JSON.stringify(translatedDocuments, null, 2),
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
  return translatedDocuments;
};

const translateNote = async (
  text: string
): Promise<Translation | undefined> => {
  const textTranslatorApiUrl =
    `${process.env.TOPIC_DETECTOR_API}/translate` || "";
  const cleanedText = text
    .replace(/(\r\n|\n|\r)/gm, " ")
    .replace(/\\/g, "\\\\")
    .replace(/"/g, '\\"');

  const sourceLanguage = "bg";
  const targetLanguage = "en";

  const options = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text: cleanedText,
      source_language: sourceLanguage,
      target_language: targetLanguage,
    }),
  };

  try {
    const response = await fetch(textTranslatorApiUrl, options);
    const data = await response?.json();
    return data;
  } catch (error: any) {
    console.log(error);
  }
};
