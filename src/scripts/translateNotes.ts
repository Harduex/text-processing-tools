import { translateNotes } from "../modules/translateNotes";

(async function () {
  const convertedNotesDir: string =
    `${process.env.CONVERTED_NOTES_DIR}/JSON` || ".";
  
  const sourceLanguage: string = process.env.SOURCE_LANGUAGE || "bg";
  const targetLanguage: string = process.env.TARGET_LANGUAGE || "en";
    
  await translateNotes(convertedNotesDir, sourceLanguage, targetLanguage);
})();
