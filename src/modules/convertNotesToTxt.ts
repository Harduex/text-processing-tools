import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import { progressBar } from "../helpers/utilities";

dotenv.config();

export const convertNotesToTxt = (
  notesDir: string,
  convertedNotesDir: string
): void => {
  const files: string[] = fs
    .readdirSync(notesDir)
    .filter((file: string) => path.extname(file) === ".json");
  const notesCount: number = files.length;

  if (!fs.existsSync(convertedNotesDir)) {
    fs.mkdirSync(convertedNotesDir, { recursive: true });
  }

  files.forEach((file: string, index: number) => {
    let notesProcessed: number = index + 1;

    let filename: string = file
      .replace(".json", ".txt")
      .replace(/[\\/:*?"<>|]/g, "")
      .replace(/\s/g, "_");
    let noteData: any = JSON.parse(
      fs.readFileSync(path.join(notesDir, file), "utf8")
    );
    let date: string = new Date(noteData.createdTimestampUsec / 1000)
      .toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
      })
      .replace(/\//g, "_");
    filename = `${date}_${filename}`;
    let convertedNote: string = path.join(convertedNotesDir, filename);
    if (!fs.existsSync(convertedNote)) {
      let noteText: string = `${noteData.title}\n${noteData.textContent}`
        .replace(/^\s+|\s+$/g, "")
        .replace(/\n\s*\n/g, "\n");
      fs.writeFileSync(convertedNote, noteText);
      fs.writeFileSync(convertedNote, noteText);
    }

    progressBar(notesProcessed, notesCount);
  });

  console.log(
    `\nDone! You can find your converted notes in ${convertedNotesDir}`
  );
};
