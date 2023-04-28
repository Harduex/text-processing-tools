import { convertNotesToTxt } from "../modules/convertNotesToTxt";

(function () {
  const notesDir: string = process.env.NOTES_DIR || ".";
  const convertedNotesDir: string =
    `${process.env.CONVERTED_NOTES_DIR}/TXT` || ".";

  convertNotesToTxt(notesDir, convertedNotesDir);
})();
