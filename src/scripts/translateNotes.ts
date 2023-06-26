import { translateNotes } from "../modules/translateNotes";

(async function () {
  const convertedNotesDir: string =
    `${process.env.CONVERTED_NOTES_DIR}/JSON` || ".";
    
  await translateNotes(convertedNotesDir);
})();
