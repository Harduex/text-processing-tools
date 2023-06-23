import { mergeNotesToJson } from "../modules/mergeNotesToJson";

(function () {
  const notesDir: string = process.env.NOTES_DIR || ".";
  const convertedNotesDir: string =
    `${process.env.CONVERTED_NOTES_DIR}/JSON` || ".";
  const outputFilename: string = process.env.OUTPUT_FILENAME || "notes";

  mergeNotesToJson(notesDir, convertedNotesDir, outputFilename);
})();
