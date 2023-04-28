import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import { progressBar } from "../helpers/utilities";

dotenv.config();

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

    mergedNotes.data.push(
      `${data.title ? data.title + ", " : ""}${data.textContent}`
    );

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
