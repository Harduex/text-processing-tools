import { mergeNotesToJson } from "../modules/mergeNotesToJson";

(function () {
  const NOTES_DIR: string = process.env.NOTES_DIR || ".";
  const CONVERTED_NOTES_DIR: string =
    `${process.env.CONVERTED_NOTES_DIR}/JSON` || ".";
  const OUTPUT_FILENAME: string = process.env.OUTPUT_FILENAME || "notes";

  mergeNotesToJson(NOTES_DIR, CONVERTED_NOTES_DIR, OUTPUT_FILENAME);
})();
