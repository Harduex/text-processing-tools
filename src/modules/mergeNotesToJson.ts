import fs from "fs";
import path from "path";
import dotenv from "dotenv";
dotenv.config();

import { cleanText, progressBar } from "../helpers/utilities";


interface MergedNotes {
  data: string[];
}

export const mergeNotesToJson = (
  notesDir: string,
  convertedNotesDir: string,
  outputFilename: string
): void => {
  const mergedNotes: MergedNotes = { data: [] };

  const files = fs
    .readdirSync(notesDir)
    .filter((file) => path.extname(file) === ".json");

  let completedCount: number = 0;
  files.forEach((file) => {
    const filePath = path.join(notesDir, file);
    const contents = fs.readFileSync(filePath, "utf8");
    const data = JSON.parse(contents);

    const noteTextFormatted = cleanText(`${data.title ? data.title + ", " : ""}${
      data.textContent
    }`);
    mergedNotes.data.push(noteTextFormatted);

    progressBar(++completedCount, files.length);

    if (completedCount === files.length) {
      const outputFilePath = path.join(
        convertedNotesDir,
        `${outputFilename}.json`
      );
      if (!fs.existsSync(convertedNotesDir)) {
        fs.mkdirSync(convertedNotesDir, { recursive: true });
      }
      fs.writeFile(
        outputFilePath,
        JSON.stringify(mergedNotes, null, 2),
        (err) => {
          if (err) {
            console.error(`Error writing file ${outputFilePath}: ${err}`);
            return;
          }
          console.log(`\nMerged notes written to ${outputFilePath}`);
        }
      );
    }
  });
};
